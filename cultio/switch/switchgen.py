import re
import io
import subprocess

UNIX_AMD64_REGS = (
    'r12',
    'r13',
    'r14',
    'r15',
    'rbx',
    'rbp',
)
# Unix Exclusions:
# rdi, rsi, rdx, rcx, r8, r9 because they are used for arguments
# rax, r10, r11 because they are considered volatile

WIN_AMD64_REGS = (
    'xmm6',
    'xmm7',
    'xmm8',
    'xmm9',
    'xmm10',
    'xmm11',
    'xmm12',
    'xmm13',
    'xmm14',
    'xmm15',
    'rsi',
    'rdi',
    'rbp',
    'rbx',
    'r12',
    'r13',
    'r14',
    'r15',
    'gs:0x00',
    'gs:0x08',
    'gs:0x10'
)
# Windows Exclusions:
# rcx, rdx, r8, r9, xmm0L, xmm1L, xmm2L, xmm3L because they are used for arguments
# rax, r10, r11, xmm4, xmm5 because they are considered volatile

DISASM_RE = re.compile(r'^([\dA-F]+)\s+([\dA-F]+)\s+(.*)$')


def parse_disasm_instructions(lines: list[str]) -> list[tuple[str, str]]:
    instructions: list[tuple[str, str]] = []

    for line in lines:
        match = DISASM_RE.match(line.strip())

        if match is not None:
            instructions.append((match.group(2), match.group(3)))
        elif line.strip() == '-00':
            instructions.append(('-00', ''))

    return instructions


def generate_win_amd64_asm(fp: io.TextIOBase) -> None:
    fp_regs: list[str] = []
    seh_regs: list[str] = []
    regs: list[str] = []

    for reg in WIN_AMD64_REGS:
        if reg.startswith('xmm'):
            fp_regs.append(reg)
        elif reg.startswith('gs'):
            seh_regs.append(reg)
        else:
            regs.append(reg)

    fp.write('; generated by cultio/switch/generate.py\n')
    fp.write('; Architecture: AMD64\n')
    fp.write('; Platform: Windows\n\n')

    fp.write('BITS 64\n\n')

    fp.write('global switch\n')
    fp.write('section .text\n\n')

    fp.write('sswitch:\n')

    reserve = (16 * len(fp_regs)) + 8
    fp.write(f'    sub rsp, {hex(reserve)}\n')

    stack_offset = 0

    for reg in fp_regs:
        fp.write(f'    movaps [rsp+{hex(stack_offset)}], {reg}\n')
        stack_offset += 16

    for reg in regs:
        fp.write(f'    push {reg}\n')

    for reg in seh_regs:
        fp.write(f'    push QWORD [{reg}]\n')

    fp.write('\n')
    fp.write('    mov [rcx], rsp\n')
    fp.write('    mov rsp, [rdx]\n\n')

    for reg in regs:
        fp.write(f'    pop {reg}\n')

    for reg in seh_regs:
        fp.write(f'    pop QWORD [{reg}]\n')

    stack_offset = 0

    for reg in fp_regs:
        fp.write(f'    movaps {reg}, [rsp+{hex(stack_offset)}]\n')
        stack_offset += 16

    fp.write('\n')
    fp.write(f'    mov rcx, [rsp+{hex(reserve)}]\n')
    fp.write(f'    add rsp, {hex(reserve)}\n')
    fp.write('    jmp rcx\n')


def generate_win_amd64_c(fp: io.TextIOBase, output: str) -> None:
    proc = subprocess.Popen(['ndisasm', '-b', '64', output], stdout=subprocess.PIPE)
    assert proc.stdout is not None

    lines = [line.decode('utf-8') for line in proc.stdout.readlines()]
    instructions = parse_disasm_instructions(lines)

    fp.write('// generated by cultio/switch/generate.py\n')
    fp.write('// Architecture: AMD64\n')
    fp.write('// Platform: Windows\n\n')

    fp.write('#pragma section(".text")\n\n')
    fp.write('__declspec(allocate(".text")) static unsigned char sswitch_code[] = {\n')

    largest = max(len(instruction[0]) for instruction in instructions)
    asm_start = (largest // 2) * 6

    for instruction, asm in instructions:
        if instruction == '-00':
            fp.write('    0x00,\n')
        else:
            chars = ', '.join(
                f'0x{instruction[i:i+2]}' for i in range(0, len(instruction), 2)
            )

            padding = ' ' * (asm_start - len(chars))
            fp.write(f'    {chars},{padding}// {asm}\n')

    fp.write('};\n\n')

    fp.write(
        'void (*sswitch)(void **, void **) = (void (*)(void **, void **))sswitch_code;\n'
    )


def generate_unix_amd64_c(fp: io.TextIOBase) -> None:
    fp.write('// generated by cultio/switch/generate.py\n')
    fp.write('// Architecture: AMD64\n')
    fp.write('// Platform: Unix\n\n')

    fp.write('void sswitch(void **ostack, void **dstack) {\n')

    fp.write('    __asm__ __volatile__ (\n')

    reserve = 8 * len(UNIX_AMD64_REGS)
    fp.write(f'        "subq ${hex(reserve)}, %rsp\\n"\n')

    stack_offset = 0

    for reg in UNIX_AMD64_REGS:
        fp.write(f'        "movq %{reg}, {hex(stack_offset)}(%rsp)\\n"\n')
        stack_offset += 8

    fp.write('\n')
    fp.write('        "movq %rsp, (%rdi)\\n"\n')
    fp.write('        "movq (%rsi), %rsp\\n"\n\n')

    stack_offset = 0

    for reg in UNIX_AMD64_REGS:
        fp.write(f'        "movq {hex(stack_offset)}(%rsp), %{reg}\\n"\n')
        stack_offset += 8

    fp.write(f'        "addq ${hex(reserve)}, %rsp\\n"\n\n')

    fp.write('        "popq %rcx\\n"\n')
    fp.write('        "jmpq %rcx\\n"\n')

    fp.write('    );\n')
    fp.write('}\n')


if __name__ == '__main__':
    import os
    import io

    dirname = os.path.dirname(__file__)

    source = os.path.join(dirname, 'win_amd64_switch.asm')
    output = os.path.join(dirname, 'win_amd64_switch.out')

    with open(source, 'w') as fp:
        generate_win_amd64_asm(fp)

    subprocess.run(f'nasm -f bin {source} -o {output}', check=True)

    with open(os.path.join(dirname, 'win_amd64_switch.c'), 'w') as fp:
        generate_win_amd64_c(fp, output)

    os.remove(output)

    with open(os.path.join(dirname, 'unix_amd64_switch.c'), 'w') as fp:
        generate_unix_amd64_c(fp)
