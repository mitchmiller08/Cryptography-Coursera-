from Crypto.Hash import SHA256
import os

blockSize = 1024
path = r'C:\Users\mitch\Dropbox\Code\Other\Coursera\Cryptography\Week3\6.1.intro.mp4'

file = open(path,'rb')
fileSize = os.path.getsize(path)
numBlocks = fileSize / blockSize
lastBlock = fileSize % blockSize

h = SHA256.new()

#Do last block separately
file.seek(fileSize-lastBlock)
currentBlock = file.read(lastBlock)

h.update(currentBlock)
currentHash = h.digest()

#Do remainder of file
for i in range(numBlocks):
	
	file.seek(fileSize-((i+1)*blockSize+lastBlock))
	currentBlock = file.read(blockSize)
	currentBlock = currentBlock + currentHash
	
	h = SHA256.new()
	h.update(currentBlock)
	currentHash = h.digest()
	
print h.hexdigest()