import random
m=100
n=32
poblacion=[]
for i in range(m):
    for j in range(n):
        poblacion[i][j]=random.randint(0,1)
print(poblacion)