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

def generate_sort_leafs(dict_symb):			#создаем массив листьев по составленному словарю
    return [Leaf(dict_symb[i], i) for i in dict_symb]

def generate_tree(sorted_leafs):			#генерируем дерево по нашемму сортированному массиву листьев
    while (len(sorted_leafs) >= 2):			#пока не останется 1 элемент массива
        first = sorted_leafs.pop(0)			#мы записываем первые два минимальных элемента
        second = sorted_leafs.pop(0)		#в один узел, при этом мы удаляем эти два символа
        new_node = Node(first, second)		#а новый узел записываем в конец, после чего опять сортируем
        sorted_leafs.append(new_node)
        sorted_leafs.sort()
    root_node = sorted_leafs[0]				#после окончания while получем дерево
    return root_node
	
def openbytes(myfile):
	f = open(myfile, 'rb')
	return f.read()

def compress(myfile):
	dict_sym = symbols_counter(hex)
	print(dict_sym)

def decompress(myfile):
	hex = openbytes(myfile)
	print(f"{hex} decompressed")

if __name__ == '__main__':
	


	