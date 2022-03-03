// generated by cultio/switch/generate.py
// Architecture: AMD64
// Platform: Windows

#pragma section(".text")

__declspec(allocate(".text")) static unsigned char sswitch_code[] = {
    0x48, 0x81, 0xEC, 0xA8, 0x00, 0x00, 0x00,        // sub rsp,0xa8
    0x0F, 0x29, 0x34, 0x24,                          // movaps oword [rsp],xmm6
    0x0F, 0x29, 0x7C, 0x24, 0x10,                    // movaps oword [rsp+0x10],xmm7
    0x44, 0x0F, 0x29, 0x44, 0x24, 0x20,              // movaps oword [rsp+0x20],xmm8
    0x44, 0x0F, 0x29, 0x4C, 0x24, 0x30,              // movaps oword [rsp+0x30],xmm9
    0x44, 0x0F, 0x29, 0x54, 0x24, 0x40,              // movaps oword [rsp+0x40],xmm10
    0x44, 0x0F, 0x29, 0x5C, 0x24, 0x50,              // movaps oword [rsp+0x50],xmm11
    0x44, 0x0F, 0x29, 0x64, 0x24, 0x60,              // movaps oword [rsp+0x60],xmm12
    0x44, 0x0F, 0x29, 0x6C, 0x24, 0x70,              // movaps oword [rsp+0x70],xmm13
    0x44, 0x0F, 0x29, 0xB4, 0x24, 0x80, 0x00, 0x00,  // movaps oword [rsp+0x80],xmm14
    0x00,
    0x44, 0x0F, 0x29, 0xBC, 0x24, 0x90, 0x00, 0x00,  // movaps oword [rsp+0x90],xmm15
    0x00,
    0x56,                                            // push rsi
    0x57,                                            // push rdi
    0x55,                                            // push rbp
    0x53,                                            // push rbx
    0x41, 0x54,                                      // push r12
    0x41, 0x55,                                      // push r13
    0x41, 0x56,                                      // push r14
    0x41, 0x57,                                      // push r15
    0x65, 0xFF, 0x34, 0x25, 0x00, 0x00, 0x00, 0x00,  // push qword [gs:0x0]
    0x65, 0xFF, 0x34, 0x25, 0x08, 0x00, 0x00, 0x00,  // push qword [gs:0x8]
    0x65, 0xFF, 0x34, 0x25, 0x10, 0x00, 0x00, 0x00,  // push qword [gs:0x10]
    0x48, 0x89, 0x21,                                // mov [rcx],rsp
    0x48, 0x8B, 0x22,                                // mov rsp,[rdx]
    0x5E,                                            // pop rsi
    0x5F,                                            // pop rdi
    0x5D,                                            // pop rbp
    0x5B,                                            // pop rbx
    0x41, 0x5C,                                      // pop r12
    0x41, 0x5D,                                      // pop r13
    0x41, 0x5E,                                      // pop r14
    0x41, 0x5F,                                      // pop r15
    0x65, 0x8F, 0x04, 0x25, 0x00, 0x00, 0x00, 0x00,  // pop qword [gs:0x0]
    0x65, 0x8F, 0x04, 0x25, 0x08, 0x00, 0x00, 0x00,  // pop qword [gs:0x8]
    0x65, 0x8F, 0x04, 0x25, 0x10, 0x00, 0x00, 0x00,  // pop qword [gs:0x10]
    0x0F, 0x28, 0x34, 0x24,                          // movaps xmm6,oword [rsp]
    0x0F, 0x28, 0x7C, 0x24, 0x10,                    // movaps xmm7,oword [rsp+0x10]
    0x44, 0x0F, 0x28, 0x44, 0x24, 0x20,              // movaps xmm8,oword [rsp+0x20]
    0x44, 0x0F, 0x28, 0x4C, 0x24, 0x30,              // movaps xmm9,oword [rsp+0x30]
    0x44, 0x0F, 0x28, 0x54, 0x24, 0x40,              // movaps xmm10,oword [rsp+0x40]
    0x44, 0x0F, 0x28, 0x5C, 0x24, 0x50,              // movaps xmm11,oword [rsp+0x50]
    0x44, 0x0F, 0x28, 0x64, 0x24, 0x60,              // movaps xmm12,oword [rsp+0x60]
    0x44, 0x0F, 0x28, 0x6C, 0x24, 0x70,              // movaps xmm13,oword [rsp+0x70]
    0x44, 0x0F, 0x28, 0xB4, 0x24, 0x80, 0x00, 0x00,  // movaps xmm14,oword [rsp+0x80]
    0x00,
    0x44, 0x0F, 0x28, 0xBC, 0x24, 0x90, 0x00, 0x00,  // movaps xmm15,oword [rsp+0x90]
    0x00,
    0x48, 0x8B, 0x8C, 0x24, 0xA8, 0x00, 0x00, 0x00,  // mov rcx,[rsp+0xa8]
    0x48, 0x81, 0xC4, 0xA8, 0x00, 0x00, 0x00,        // add rsp,0xa8
    0xFF, 0xE1,                                      // jmp rcx
};

void (*sswitch)(void **, void **) = (void (*)(void **, void **))sswitch_code;
