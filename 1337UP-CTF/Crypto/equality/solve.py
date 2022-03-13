import gmpy2
from Crypto.Util.number import *

def egcd(a, b):
  if (a == 0):
    return (b, 0, 1)
  else:
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def neg_pow(a, b, n):
	assert b < 0
	assert GCD(a, n) == 1
	res = int(gmpy2.invert(a, n))
	res = pow(res, b*(-1), n)
	return res

def common_modulus(e1, e2, n, c1, c2):
	g, a, b = egcd(e1, e2)
	if a < 0:
		c1 = neg_pow(c1, a, n)
	else:
		c1 = pow(c1, a, n)
	if b < 0:
		c2 = neg_pow(c2, b, n)
	else:
		c2 = pow(c2, b, n)
	ct = c1*c2 % n
	m = int(gmpy2.iroot(ct, g)[0])
	return long_to_bytes(m)
	
n = 0xa6241c28743fbbe4f2f67cee7121497f622fd81947af30f327fb028445b39c2d517ba7fdcb5f6ac9e6217205f8ec9576bdec7a0faef221c29291c784eed393cd95eb0d358d2a1a35dbff05d6fa0cc597f672dcfbeecbb14bd1462cb6ba4f465f30f22e595c36e6282c3e426831d30f0479ee18b870ab658a54571774d25d6875
e1 = 0x3045
e2 = 0xff4d

c1 = 0x5d1e39bc751108ec0a1397d79e63c013d238915d13380ae649e84d7d85ebcffbbc35ebb18d2218ccbc5409290dfa8a4847e5923c3420e83b1a9d7aa67190dc0d34711cce261665c64c28ed2834394d4b181926febf7eb685f9ce81f36c7fb72798da3a14a123287171d26e084948aab0fba81c53f10b5696fc291006254ee690
c2 = 0x3d90f2bec4fe02d8ce4cece3ddb6baed99337f7e6856eef255445741b5cfe378390f058679d70236e51be4746db4c207f274c40b092e24f8c155a0957867e84dca48e27980af488d2615a280c6eadec2f1d30b95653b1ee3135e2edff100dd2c529994f846722f811348b082d0bec7cfab579a4bd0ab789928b1bebed68d628f

print(common_modulus(e1, e2, n, c1, c2))
