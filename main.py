def openbytes(myfile):
	f = open(myfile, 'rb')
	return f.read()

def compress(myfile):
	hex = openbytes(myfile)
	print(f"{hex} compressed")

def decompress(myfile):
	hex = openbytes(myfile)
	print(f"{hex} decompressed")
