def symbols_counter(input):
    dict_sym = {}
    for i in range(len(input)):
        dict_sym[chr(input[i])] = dict_sym.get(chr(input[i]), 0) + 1
    return dict(sorted(dict_sym.items(), key=lambda item: item[1]))
	
def openbytes(myfile):
	f = open(myfile, 'rb')
	return f.read()

def compress(myfile):
	dict_sym = symbols_counter(hex)
	print(dict_sym)

def decompress(myfile):
	hex = openbytes(myfile)
	print(f"{hex} decompressed")
