import heapq
from heapq import heappop, heappush

def input_text(filename):
	f = open(filename, 'rb')
	input = f.read()
	f.close()
	return input

def isLeaf(root):
	return root.left is None and root.right is None
 
class Node:
	def __init__(self, ch, dict, left=None, right=None):
		self.ch = ch
		self.dict = dict
		self.left = left
		self.right = right
 
	def __lt__(self, other):
		return self.dict < other.dict
 
def encode(root, s, huffman_code):
 
	if root is None:
		return
 
	if isLeaf(root):
		huffman_code[root.ch] = s if len(s) > 0 else '1'
 
	encode(root.left, s + '0', huffman_code)
	encode(root.right, s + '1', huffman_code)
 
def decode(root, index, s):
 
	if root is None:
		return index
 
	if isLeaf(root):
		return index
 
	index = index + 1
	root = root.left if s[index] == '0' else root.right
	return decode(root, index, s)
 
def buildHuffmanTree(text):
 	#если текст пустой
	if len(text) == 0:
		return

	dict = {} #заполнение словаря
	for x in text:
		dict[x] = dict.setdefault(x, 0) + 1
	
	pq = [Node(k, v) for k, v in dict.items()]
	heapq.heapify(pq)
	
	while len(pq) != 1:
 
		left = heappop(pq)
		right = heappop(pq)

		total = left.dict + right.dict
		heappush(pq, Node(None, total, left, right))

	root = pq[0]

	huffmanCode = {}
	encode(root, '', huffmanCode) #создание кодов хаффмана

	s = '' #переписывание текста в хаф
	for c in text:
		s += huffmanCode.get(c)

	amount = str(len(dict)).encode() #кол-во уникальных символов

	n = 8 
	chunks = [s[i:i+n] for i in range(0, len(s), n)] 
	m = 8 - len(chunks[-1])
	k = 0
	l = chunks[0]

	for i in range(len(l)):
		if int(l[i]) == 0:
			k += 1
		if int(l[i]) == 1:
			break

	#запись
	with open('enctext.txt','wb') as out:		
		out.write(int(amount).to_bytes(1, 'little')) #запись длины словаря
		for key,val in dict.items(): #запись словаря
			out.write(key.to_bytes(3, 'little'))
			out.write(val.to_bytes(3, 'little'))

		out.write(k.to_bytes(1, 'little'))	#кол-во 0 в начале
		out.write(m.to_bytes(1, 'little'))	#кол-во 0 в конце
		for index, elem in enumerate(chunks):
			elem = chunks[index]
			b = int(elem, 2).to_bytes((len(elem) + 7) // 8, 'little')
			out.write(b)

	#чтение
	with open('enctext.txt','rb') as out:
		f = open('dectext.txt', 'wb')
		b = out.read(1)
		mybyte = bytes.fromhex(b.hex()) 
		amount_symb = int("{:08b}".format(int(mybyte.hex(),16)), 2)
		
		dict1 = {}
		for x in range(amount_symb): #чтение словаря
			c = out.read(6)
			key = int.from_bytes(c[:len(c)//2], 'little')
			val = int.from_bytes(c[len(c)//2:], 'little')
			dict1[key] = dict1.setdefault(key, val)

		a = out.read(1)
		mybyte = bytes.fromhex(a.hex()) 
		adder = int("{:08b}".format(int(mybyte.hex(),16)), 2)
		bintext = ''
		for i in range(adder):
			bintext += '0'

		n = 8
		y = out.read()
		bintext += "{:08b}".format(int(y.hex(),16))
		piece = [s[i:i+n] for i in range(0, len(bintext), n)]
		bintxt = ''
		for index, elem in enumerate(piece):
			elem = piece[index]
			bintxt += elem

		pq = [Node(k, v) for k, v in dict1.items()]
		heapq.heapify(pq)
	
		while len(pq) != 1:
 
			left = heappop(pq)
			right = heappop(pq)

			total = left.dict + right.dict
			heappush(pq, Node(None, total, left, right))

		root = pq[0]

		huffmanCode = {}
		encode(root, '', huffmanCode)

		k = []
		v = []
		for key,val in huffmanCode.items():
			k.append(key) 
			v.append(val)

		g = ''
		for x in bintxt:
			g += x
			for i in range(len(huffmanCode)):
				if g == v[i]:
					f.write(k[i].to_bytes(1, 'little'))
					g = ''
		
	if isLeaf(root):
		while root.dict > 0:
			root.dict = root.dict - 1
	else:
		index = -1
		while index < len(s) - 1:
			index = decode(root, index, s)

if __name__ == '__main__':

	text = input_text('text.txt')
	buildHuffmanTree(text)