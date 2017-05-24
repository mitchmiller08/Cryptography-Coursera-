from Crypto.Cipher import AES
from Crypto.Util import Counter


#XOR two strings together
def strxor(a,b):
	if len(a) > len(b):
		return "".join([chr(ord(x) ^ ord(y)) for (x,y) in zip(a[:len(b)], b )])
	else:
		return "".join([chr(ord(x) ^ ord(y)) for (x,y) in zip(a,b[:len(a)])])


		
#AES decryption in CBC mode using pre-built routine
def decryptCBC1(key,ct):

	keydec = key.decode('hex')
	ctdec = ct.decode('hex')
	
	iv = ctdec[:16]
	message = ctdec[16:]
	
	decryptor = AES.new(keydec,AES.MODE_CBC,iv)
	
	ptpadded = decryptor.decrypt(message)
	
	pt = ptpadded[:-ord(ptpadded[-1])]
	return pt


	
#AES decryption in CBC mode using from-scratch routine
def decryptCBC2(key,ct):
	ptpadded = ''
	keydec = key.decode('hex')
	ctdec = ct.decode('hex')
	
	numblocks = len(ctdec)/16
	
	decryptor = AES.new(keydec,AES.MODE_ECB)
	
	for i in range(1,numblocks+1):
		block = decryptor.decrypt(ctdec[16*i:16*i+16])
		ptpadded = ptpadded + strxor(block, ctdec[16*(i-1):16*(i-1)+16])
		 
	pt = ptpadded[:-ord(ptpadded[-1])]
	return pt

	
#AES decryption in CTR mode using pre-built routine
def decryptCTR1(key,ct):

	keydec = key.decode('hex')
	ctdec = ct.decode('hex')
	
	iv = ctdec[:16]
	message = ctdec[16:]
	ctr = Counter.new(16*8,initial_value=long(iv.encode('hex'),16))
	
	decryptor = AES.new(keydec,AES.MODE_CTR,counter=ctr)
	
	pt = decryptor.decrypt(message)
	
	return pt

	
	
key = raw_input("Enter key: ")	
ct = raw_input("Enter Ciphertext: ")
mode = raw_input("Choose mode (CBC or CTR): ")

if(mode.lower() == "cbc"):
	print(decryptCBC1(key,ct))
	print(decryptCBC2(key,ct))
	
elif(mode.lower() == "ctr"):
	print(decryptCTR1(key,ct))

else:
	print("That mode is not supported.")
