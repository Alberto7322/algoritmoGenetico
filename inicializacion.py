import random
m = 100
n = 32
poblacion = []
for i in range(m):
    poblacion.append([])
    for j in range(n):
        poblacion[i].append(random.randint(0,1))

for i in poblacion:
    print(i,"\n")

print(len(poblacion))
