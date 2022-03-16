# HTML2PDF

### 1. Initial reconnaissance:

This is the first appearance of this challenge. There are only 2 functions in the given web app: the homepage and the login page for admin.

![image](https://user-images.githubusercontent.com/61876488/158508140-a8e24f19-72d1-48da-9c4d-23be486d1d0a.png)

![image](https://user-images.githubusercontent.com/61876488/158508262-86369b95-5af5-414e-93db-219c7ac35224.png)

The login page said `Login to view super secret admin stuff.`, so maybe the flag will be given after we login successfully. Come back to the homepage and check whether wwe can steal the credential of "secret" admin.

### 2. Analysis:

The homepage have a text box, and what we need to fill in it are HTML elements as their example. After submit the author sample HTML elements, it convert the whole HTML document to PDF, such as the image converted from `img` tag like following:

![image](https://user-images.githubusercontent.com/61876488/158509192-a0fbf254-37be-4e1d-a81e-5df2159503eb.png)

As everyone knows, Cross-site scripting (XSS) is a client-side vulnerability allow executing javascript through HTML tags (there are some other ways too) in victim's client, and it likely happens in this `HTML2PDF Rendering Tool`. But this tool convert every HTML tags to PDF components, so never try to `alert(1)` as a script kiddie like this, because it is useless =)))

![image](https://user-images.githubusercontent.com/61876488/158510606-51513eaa-af12-45c6-92b0-976479ed0c5c.png)

### 3. Exploit:

Luckily, this challenge share the same idea with a challenge I used to make for [FPT Night Wolf CTF](https://doantung99.medium.com/fpt-night-wolf-ctf-writeup-de43925ed84b), so immediately I realize this "HTML2PDF Rendering Tool" is vulnerable to [Server Side XSS (Dynamic PDF)](https://book.hacktricks.xyz/pentesting-web/xss-cross-site-scripting/server-side-xss-dynamic-pdf). Try some "read local file" payloads the cheatsheet I have found to read `/etc/shadow`:

```javascript
// Payload
<script>
    xhzeem = new XMLHttpRequest();
    xhzeem.open("GET","file:///etc/shadow");
    xhzeem.send();
    xhzeem.onload = function(){document.write(this.responseText);}
    xhzeem.onerror = function(){document.write('failed!')}
</script>
```

Result:

![image](https://user-images.githubusercontent.com/61876488/158511713-59d6b9d7-4380-48b0-a8f1-66d6ee81bc11.png)

The last user `WeakPasswordAdmin` made me so triggered, so I decided to crack his password hash. The prefix `$1$` indicates that this is a MD5 hash (chek from this [hash category](https://hashcat.net/wiki/doku.php?id=example_hashes)), so we can easily crack it by [hashcat](https://samsclass.info/123/proj10/hashcat-2.00.7z):

- Create a hash file and save the hash of `WeakPasswordAdmin`:

![image](https://user-images.githubusercontent.com/61876488/158513908-1e74e4c9-ad49-4306-85e3-4b5c408d9c3f.png)

- Then run the command `./hashcat-cli32.bin -m 500 -a 0 -o found3.txt --remove crack3.hash 500_passwords.txt`, see the command's output in `found3.txt`:

![image](https://user-images.githubusercontent.com/61876488/158514161-b8453ef0-4ef0-42d8-8162-bf7429b2aa48.png)

The password of `WeakPasswordAdmin` is `WeakPasswordAdmin`. Just login and get the flag :D

![image](https://user-images.githubusercontent.com/61876488/158514302-de907ce2-596e-48da-ba3c-883516ed5478.png)

Flag: `utflag{b1g_r3d_t3am_m0v35_0ut_h3r3}`.
