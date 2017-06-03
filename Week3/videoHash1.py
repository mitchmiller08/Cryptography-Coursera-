from Crypto.Hash import SHA256
import os

blockSize = 1024
path = r'C:\Users\mitch\Dropbox\Code\Other\Coursera\Cryptography\Week3\6.2.birthday.mp4'

file = open(path,'rb')
fileSize = os.path.getsize(path)
numBlocks = fileSize / blockSize
lastBlock = fileSize % blockSize

blockList = range(0,fileSize,blockSize)
blockList.reverse()

lastHash = ""

for blockPos in blockList:
	
	file.seek(blockPos)
	block = file.read(blockSize)
	h = SHA256.new()
	h.update(block)
	h.update(lastHash)
	lastHash = h.digest()
	
print lastHash.encode('hex')