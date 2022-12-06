#функция сортирует колличество каждого символа по столбикам
def sort(x):
  for i in range(128):
    for j in range(127):
      if x[1][j] > x[1][j + 1] :  
        tmp = x[1][j]
        x[1][j] = x[1][j + 1]
        x[1][j + 1] = tmp

        tmp = x[0][j]
        x[0][j] = x[0][j + 1]
        x[0][j + 1] = tmp
  return x

#функция удаляет символы, которые не используются 
def removal(x):
  while x[1][0] == 0:
      del x[1][0]
      del x[0][0]
  return x


file = open("text.txt", "r")
text = file.read()
file.close()
symbols = [[0] * 128,[0] * 128]

for i in range(128):
  symbols[0][i] = chr(i)
  
for i in range(len(text)):
  symbols[1][ord(text[i])] += 1

sort(symbols)
removal(symbols)
print(symbols)