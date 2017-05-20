def strxor(a,b):
	if len(a) > len(b):
		return "".join([chr(ord(x) ^ ord(y)) for (x,y) in zip(a[:len(b)], b )])
	else:
		return "".join([chr(ord(x) ^ ord(y)) for (x,y) in zip(a,b[:len(a)])])
		
def importStrings():
	with open('multipad.txt') as f:
		lines = f.read().splitlines()	
	return lines

def cribDrag(a,s):
	for i in range(0,len(a)-len(s)):
		print strxor(a[i:i+len(s)],s)

		
		
ciphers = importStrings()
input = ''
x = raw_input("Choose first cipher: ")
cipher1 = ciphers[int(x)]
y = raw_input("Choose second cipher: ")
cipher2 = ciphers[int(y)]
xt = cipher1.decode('hex')
yt = cipher2.decode('hex')
mt = strxor(xt,yt)
print("\nBegin crib dragging (Type 'quit()' to end)")
while input != "quit()":
	input = raw_input("\nEnter test string: ")
	cribDrag(mt,input)