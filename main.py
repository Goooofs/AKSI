import struct  
import os

class Leaf:
	def __init__(self, amount, symbol):			#__init__ вызовится при скобках
		self.amount = amount					#кол-во какого-либо символа
		self.symbol = symbol

	def __lt__(self, other):					#__lt__ вызовится при сравнении
		b = (self.amount <= other.amount)
		return b

class Node:
	def __init__(self, right, left):
		self.amount = right.amount + left.amount#при создании узла мы складываем кол-во
		self.right = right
		self.left = left

	def __lt__(self, other):
		b = (self.amount <= other.amount)
		return b

def input_file(file):
	f = open(file, 'rb')
	input = f.read()
	f.close()
	return input

def symbols_counter(input):
	dict_sym = {}						#создаем словарь и заполняем его символами из
	for i in range(len(input)):			#тескта, подсчитывая кол-во их вхождений
		dict_sym[chr(input[i])] = dict_sym.get(chr(input[i]), 0) + 1
	return dict_sym

def sorted_leafs(dict_symb):			#создаем массив листьев по составленному словарю
	arr = []
	for i in dict_symb:
		arr.append(Leaf(dict_symb[i], i))
	arr.sort()
	return arr

def generate_tree(leafs):				#генерируем дерево по нашемму сортированному массиву листьев
	while (len(leafs) >= 2):			#пока не останется 1 элемент массива
		left = leafs.pop(0)				#мы записываем первые два минимальных элемента
		right = leafs.pop(0)			#в один узел, при этом мы удаляем эти два символа
		node = Node(left, right)		#а новый узел записываем в конец, после чего опять сортируем
		leafs.append(node)
		leafs.sort()
	root_node = leafs[0]				#после окончания while получем дерево
	return root_node

def huffman_codes_gen(root, code='', code_huf=dict()):	#при первом вызове передаём наше дерево, создаем пустую строку и словарь
	if type(root.right) is Leaf:						#проверка на ветвь дерева
		code_huf[root.right.symbol] = code + '1'		#записываем наш код
	else:
		code_huf = huffman_codes_gen(root.right, code + '1', code_huf)
	if type(root.left) is Leaf:							#проверка на ветвь дерева
		code_huf[root.left.symbol] = code + '0'			#записываем наш код
	else:
		code_huf = huffman_codes_gen(root.left, code + '0', code_huf)
	return code_huf

def huffman_compress(input, code_huf):					#передаём наш файл и кодируем по коду Хаффмана
	enc_text = ''
	for i in input:
		ch = chr(i)
		enc_text += code_huf[ch]
	return enc_text

def huffman_decompress(b_enc_text, code_huf_inv):	#расшифровываем текст
    text = ''
    next_code = ''
    for bit in b_enc_text:
        next_code += bit
        if (next_code in code_huf_inv.keys()):
            text += code_huf_inv[next_code]
            next_code = ''
    return text


def rawbytes(letter):				#взял из интернета
	list_out = []
	for c in letter:
		n = ord(c)
		if n < 256:
			list_out.append(struct.pack('B', n))
		elif n < 65535:
			list_out.append(struct.pack('>H', n))
		else:
			b = (n & 0xFF0000) >> 16
			H = n & 0xFFFF
			list_out.append(struct.pack('>bH', b, H))
	return b''.join(list_out)

def write_header(file, dict_sym):	#пишем хейдер
	col_letters = (len(dict_sym.keys()) - 1).to_bytes(1, byteorder='little')
	file.write(col_letters)
	for letter, code in dict_sym.items():
		file.write(rawbytes(letter))
		file.write(code.to_bytes(4, byteorder='little'))

def get_byte_array(enc_text_pad):	#взял из интернета
	if (len(enc_text_pad) % 8 != 0):
		print("Encoded text not padded")
		exit(0)

	b = bytearray()
	for i in range(0, len(enc_text_pad), 8):
		byte = enc_text_pad[i:i + 8]
		b.append(int(byte, 2))
	return b

def enc_text_padding(enc_text):		#паддим текст
	pad = 8 - len(enc_text) % 8
	for _ in range(pad):
		enc_text += "0"

	pad_info = "{0:08b}".format(pad)
	enc_text = pad_info + enc_text
	return enc_text

def write_text(file, enc_text):		#обработка двоичных последовательнсотей в байты
	enc_text_pad = enc_text_padding(enc_text)
	out = get_byte_array(enc_text_pad)
	file.write(bytes(out))

def analysis_header(input):			#составляем словарь для функции decompress
    letters = input[0]+1
    header = input[1:5*letters + 1]
    dict_sym = dict()
    for i in range(letters):
        dict_sym[chr(header[i*5])] = int.from_bytes(header[i*5+1:i*5+5], byteorder='little')
    return dict_sym

def analysis_text(input):			#для считывания файла(закодированного)
    letters = input[0]+1
    pad_enc_text = input[5*letters + 1:]
    return pad_enc_text

def binary_code(pad_enc_text):		#для обработки в бинарный код
    result = ''
    for i in pad_enc_text:
        binary_byte = bin(i)[2:].rjust(8, '0')
        result += binary_byte
    return result

def pad_cleaner(b_enc_text_pad):	#для очищения от паддинга
    pad_info = b_enc_text_pad[:8]
    extra_pad = int(pad_info, 2)

    b_enc_text_pad = b_enc_text_pad[8:]
    b_enc_text = b_enc_text_pad[:-1*extra_pad]

    return b_enc_text


def compress(file):
	
	input = input_file(file)			#открываем файл
	
	dict_sym = symbols_counter(input)	#создаем словарь
	leafs = sorted_leafs(dict_sym)		#создаем листья
	root_node = generate_tree(leafs)	#создаем дерево
	
	code_huf = huffman_codes_gen(root_node)		#генерируем код хаффмана
	enc_text = huffman_compress(input, code_huf)#кодируем наш текст

	f = open(f"{file}.huf", 'wb')		#записываем в файл всю информацию
	write_header(f, dict_sym)
	write_text(f, enc_text)
	f.close()

def decompress(file):
	
	input = input_file("text.txt.huf")	#считываем байты
	
	dict_sym = analysis_header(input)	#словарь
	pad_enc_text = analysis_text(input)	#читаем закодированный файл
	
	leafs = sorted_leafs(dict_sym)		#создаем листья
	root_node = generate_tree(leafs)	#создаем дерево
	code_huf = huffman_codes_gen(root_node)	#генерируем код хаффмана
	code_huf_inv = {v: k for k, v in code_huf.items()}	

	b_enc_text_pad = binary_code(pad_enc_text)	#обрабатываем в бинарный код
	b_enc_text = pad_cleaner(b_enc_text_pad)	#очищаем от паддинга
	text = huffman_decompress(b_enc_text, code_huf_inv)	#расшифровываем текст
	
	f = open(f"{file}"[:-4], 'wb')	#записываем в файл
	f.write(rawbytes(text))
	f.close()

def file_presence(file):	#проверяем файл на наличие
	filepath = os.path.join(file)
	return os.path.isfile(filepath)
	
if __name__ == '__main__':

	print("[c]ompress or [d]ecompress file? ◕‿◕")
	arg1 = input()
	
	if not(arg1 == "c" or arg1 == "d"):	#проверяем параметр на comress или decompress
		print("The parameter is set incorrectly! ¯\_(ツ)_/¯")
		exit(1)
		
	print("Enter file. For compress or decompress, the filename is the same.")
	print("For example: text.txt")
	arg2 = input()

	if not(file_presence(arg2)):	#проверяем файл на наличие
		print("File was not found! ¯\_(ツ)_/¯")
		exit(1)

	if (arg1 == "c"):
		compress(arg2)
		print("File was successfully compressed!  \ (•◡•) /")
	elif (arg1 == "d"):
		decompress(arg2)
		print("File was successfully decompressed!  \ (•◡•) /")
			