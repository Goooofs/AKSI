import heapq
from heapq import heappop, heappush

class Node:
	def __init__(self, ch, dict, left=None, right=None):
		self.ch = ch
		self.dict = dict
		self.left = left
		self.right = right
 
	def __lt__(self, other):
		return self.dict < other.dict

def input_text(filename):
	f = open(filename, 'rb')
	input = f.read()
	f.close()
	return input

def isLeaf(root):
	return root.left is None and root.right is None
 
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

def compress(filename):

	text = input_text(filename)
	
	if len(text) == 0:
		print("file is empty")
		exit(1)

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

	bits = 8 
	chunks = [s[i : i + bits] for i in range(0, len(s), bits)] 
	k = 0
	l = chunks[0]

	for i in range(len(l)):
		if int(l[i]) == 0:
			k += 1	#кол-во 0 для добавления в начало
		if int(l[i]) == 1:
			break

	#запись
	with open(f'{filename}.huf','wb') as out:		
		out.write(int(amount).to_bytes(1, 'little')) #запись длины словаря
		for key,val in dict.items(): #запись словаря
			out.write(key.to_bytes(3, 'little'))
			out.write(val.to_bytes(3, 'little'))

		out.write(k.to_bytes(1, 'little'))	#кол-во 0 в начале
		for index, elem in enumerate(chunks):
			elem = chunks[index]
			b = int(elem, 2).to_bytes((len(elem) + 7) // 8, 'little')
			out.write(b)

def decompress(filename):

	text = input_text(filename)
	if len(text) == 0:
		print("file is empty")
		exit(1)
	
	with open(filename,'rb') as out:	
		f = open(f'dec.{filename}', 'wb')
		b = out.read(1)
		mybyte = bytes.fromhex(b.hex()) 	#считываем кол-во уникальных символов
		amount_symb = int("{:08b}".format(int(mybyte.hex(),16)), 2)
		
		dict = {}
		for x in range(amount_symb): #чтение словаря
			c = out.read(6)
			key = int.from_bytes(c[:len(c)//2], 'little')
			val = int.from_bytes(c[len(c)//2:], 'little')
			dict[key] = dict.setdefault(key, val)

		a = out.read(1)
		mybyte = bytes.fromhex(a.hex()) 
		adder = int("{:08b}".format(int(mybyte.hex(),16)), 2)
		bintext = ''
		for i in range(adder):	#добавляем нули
			bintext += '0'

		bits = 8
		y = out.read()
		bintext += "{:08b}".format(int(y.hex(),16))
		piece = [bintext[i : i + bits] for i in range(0, len(bintext), bits)]
		bintxt = ''
		for index, elem in enumerate(piece):	#считываем текст
			elem = piece[index]
			bintxt += elem

		pq = [Node(k, v) for k, v in dict.items()]
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
			for i in range(len(huffmanCode)):	#декодируем текст
				if g == v[i]:
					f.write(k[i].to_bytes(1, 'little'))
					g = ''
		
	if isLeaf(root):
		while root.dict > 0:
			root.dict = root.dict - 1
	else:
		index = -1
		while index < len(bintxt) - 1:
			index = decode(root, index, bintxt)


if __name__ == '__main__':

	print("[c]ompress or [d]ecompress file?")
	type = input()

	print("Enter filename: ")
	file = input()

	if (type == "c"):
		compress(file)
		print("successfully!")
	elif (type == "d"):
		decompress(file)
		print("successfully!")
	else:
		print("Wrong action, pls, try again")
		exit(1)