import sys
import struct

class Leaf:
    def __init__(self, amount, symbol):			#__init__ вызовится при скобках
        self.amount = amount					#кол-во какого-либо символа
        self.symbol = symbol
    
    def __lt__(self, other):					#__lt__ вызовится при сравнении
        return self.amount <= other.amount

class Node:
    def __init__(self, sym1, sym2):				#__init__ вызовится при скобках
        self.amount = sym1.amount + sym2.amount	#при создании узла мы складываем кол-во		
        self.right = sym1						#вхождений двух символов
        self.left = sym2

    def __lt__(self, other):					#__lt__ вызовится при сравнении
        return self.amount <= other.amount

def symbols_counter(input):
    dict_sym = {}								#создаем словарь и заполняем его символами из
    for i in range(len(input)):					#тескта, подсчитывая кол-во их вхождений
        dict_sym[chr(input[i])] = dict_sym.get(chr(input[i]), 0) + 1
    return dict(sorted(dict_sym.items(), key=lambda item: item[1]))

def sorted_leafs(dict_symb):			#создаем массив листьев по составленному словарю
	arr = []
	for i in dict_symb:
		arr.append(Node(dict_symb[i], i))
	arr.sort()
	return arr

def generate_tree(sorted_leafs):			#генерируем дерево по нашемму сортированному массиву листьев
    while (len(sorted_leafs) >= 2):			#пока не останется 1 элемент массива
        first = sorted_leafs.pop(0)			#мы записываем первые два минимальных элемента
        second = sorted_leafs.pop(0)		#в один узел, при этом мы удаляем эти два символа
        new_node = Node(first, second)		#а новый узел записываем в конец, после чего опять сортируем
        sorted_leafs.append(new_node)
        sorted_leafs.sort()
    root_node = sorted_leafs[0]				#после окончания while получем дерево
    return root_node

def huffman_codes_gen(root, code = '', code_huf = dict()):				#при первом вызове передаём наше дерево, создаем пустую строку и словарь
	if type(root.right) is Leaf :				#проверка на ветвь дерева
		code_huf[root.right.sym] = code + '1'	#записываем наш код
	else:
		code_huf = huffman_codes_gen(root.right, code + '1', code_huf)
	if type(root.left) is Leaf :				#проверка на ветвь дерева
		code_huf[root.left.sym] = code + '0'	#записываем наш код
	else:
		code_huf = huffman_codes_gen(root.left, code + '0', code_huf)
	return code_huf

def huffman_compress(input, code_huf):	#передаём наш файл и кодируем по коду Хаффмана
    enc_text = ''
    for i in input:
        ch = chr(i)
        enc_text += code_huf[ch]
    return enc_text

def raw_bytes(letter):
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

def write_header(file, dict_sym):
	col_letters = (len(dict_sym.keys())-1).to_bytes(1, byteorder='little')
	file.write(col_letters)
	for letter, code in dict_sym.items():
		file.write(raw_bytes(letter))
		file.write(code.to_bytes(4, byteorder = 'little'))

def input_file(filename_in):
	f = open(filename_in, 'rb')
	input = f.read()
	f.close
	return input

def output_file_compr(filename_out, dict_sym, enc_text):
	f = open(filename_out, 'wb')
	f.write(b"HUF")
	write_header(f, dict_sym)
	extra_pad = 8 - len(enc_text) % 8
	pad_enc_text = ''
	for _ in range(extra_pad):
		pad_enc_text += "0"
	if (len(pad_enc_text) % 8 != 0):
		print("Encoded text not padded")
		exit(0)
	b = bytearray()
	for i in range(0, len(pad_enc_text), 8):
		byte = pad_enc_text[i:i+8]
		b.append(int(byte, 2))
	out = b
	f.write(bytes(out))
	
	f.close
	
def prompt():
	text = print("[c]ompress or [d]ecompress? Enter name input file = <inpit_file> , Enter name output file = <output_file>")
	return text

def compress(myfile_in, myfile_out):
	filename_in = myfile_in #sys.argv[1]
	filename_out = myfile_out #sys.argv[2]
	
	input = input_file(filename_in)
	dict_sym = symbols_counter(input)
	leafs = sorted_leafs(dict_sym)
	root_node = generate_tree(leafs)
	code_huf = huffman_codes_gen(root_node)
	enc_text = huffman_compress(input, code_huf)
	
	output_file_compr(filename_out, dict_sym, enc_text)

def decompress(myfile):
	filename_in = sys.argv[1]
	filename_out = sys.argv[2]
	
	input = input_file(filename_in)

if __name__ == '__main__':
	#if(len(sys.argv) != 3):
	#	prompt()
	#	exit(0)
	#if(sys.argv[0] == 'c'):
	#	compress(sys.argv[1])
	#elif(sys.argv[0] == 'd'):
	#	decompress()
	#else: prompt()
	print("[c]ompress/[d]ecompress?")
	arg1 = "c" #input()
	print("input file")
	arg2 = "text.txt" #input()
	arg3 = "text.txt.enc"
	if (arg1 == "c"):
		compress(arg2, arg3)
	elif (arg1 == "d"):
		decompress(arg2, arg3)
	else:
		print("error!")
	
	


	