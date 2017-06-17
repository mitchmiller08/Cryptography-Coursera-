import urllib2
import sys

TARGET = 'http://crypto-class.appspot.com/po?er='

#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------

def strxor(a,b):
	    return "".join(["%x" % (int(x,16) ^ int(y,16)) for (x, y) in zip(a, b)])


def guessByte(bytePos,currentBlock,lastBlock,knownPT):
	pad = chr(0).encode('hex') * bytePos + chr(16-bytePos).encode('hex') * (17-bytePos)
	print "Pad = " + pad
	for i in [x for x in range(256) if x not in range(1,17-bytePos)]:
		guess = chr(0).encode('hex') * bytePos + chr(i).encode('hex') + knownPT
		sys.stdout.write("\rGuess = " +bcolors.RED+"%s" % guess[:2*bytePos] + bcolors.YELLOW + "%s" % guess[2*bytePos:(2*bytePos)+2] + bcolors.GREEN + "%s" % guess[(2*bytePos)+2:] + bcolors.ENDC)
		sys.stdout.flush()
		
		testBlock = strxor(lastBlock,strxor(guess,pad))

		if po.query(testBlock+currentBlock):
			print '\n*****************Good guess: ' + chr(i) + knownPT.decode('hex') + "*******************"
			print testBlock
			return chr(i).encode('hex') + knownPT
	for i in reversed(range(1,17-bytePos)):
		guess = chr(0).encode('hex') * bytePos + chr(i).encode('hex') + knownPT
		sys.stdout.write("\rGuess = " +bcolors.RED+"%s" % guess[:2*bytePos] + bcolors.YELLOW + "%s" % guess[2*bytePos:(2*bytePos)+2] + bcolors.GREEN + "%s" % guess[(2*bytePos)+2:] + bcolors.ENDC)
		sys.stdout.flush()
		
		testBlock = strxor(lastBlock,strxor(guess,pad))

		if po.query(testBlock+currentBlock):
			print '\n*****************Good guess: ' + chr(i) + knownPT.decode('hex') + "*******************"
			print testBlock
			return chr(i).encode('hex') + knownPT

	print '\n GUESSING FAILED! TERMINATE PROGRAM NOW!'
	return '00' + knownPT


class bcolors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'


class PaddingOracle(object):
	def query(self, q):
	        target = TARGET + urllib2.quote(q)    # Create query URL
	        req = urllib2.Request(target)         # Send HTTP request to server
	        try:
			f = urllib2.urlopen(req)          # Wait for response
	        except urllib2.HTTPError, e:          
			#print "We got: %d" % e.code       # Print response code
			if e.code != 404:
				return False # bad padding
			return True # good padding


if __name__ == "__main__":
	po = PaddingOracle()
	arg = r'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'
	blockLength = 32
	numBlocks = len(arg)/blockLength
	blockList = []
	plainTextList = []
	for i in range(0,numBlocks):
		blockList.append(arg[i*blockLength:(i+1)*blockLength])
		plainTextList.append('')

	for i in range(1,len(blockList)):
		lastBlock = blockList[i-1]
		currentBlock = blockList[i]
		print "Begin block #" + str(i) + " = " + currentBlock
		
		for bytePos in range(15,-1,-1):
			plainTextList[i] = guessByte(bytePos,currentBlock,lastBlock,plainTextList[i])


	output = ''
	for pt in plainTextList:
		output = output + pt.decode('hex')
	print output


