lista = [["a", "b", "c", "d"], [1, 2, 3, 4]]
for i in range(len(lista[0])):
    lista[1][i] = i+10
    print(lista[1][i])