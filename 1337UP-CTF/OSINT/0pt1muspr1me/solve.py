import random
import string
import zipfile
import time
from tqdm import tqdm 

with zipfile.ZipFile('flag.zip') as zip_file:
	for i in tqdm(range(int(time.time()), 1645608370, -1)): #to save time you can use (1645696380 + 100) instead of time.time() as epoch time 

		  random.seed(i)
		  length, letters = 32, string.ascii_letters
		  result_str = ''.join(random.choice(letters) for i in range(length))

		  try:
		      zip_file.extractall(pwd=result_str.encode())
		  except:
					pass
		  else:
		      print("[+] Password found:", result_str)
		      exit(0)
