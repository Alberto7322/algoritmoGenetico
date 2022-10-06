import random
import requests
import time

m = 100
n = 80


def iniciar(m, n):
    return [''.join([str(random.randint(0,1)) for j in range(n)]) for i in range(m)]

def evaluar(poblacion):
    resultados = []
    for i in poblacion:
            cromosoma = i
            web = "http://163.117.164.219/age/alfa?c="
            r = requests.get(web + cromosoma)
            resultados.append(r.text)
    return resultados

def seleccionar(resultados, m, poblacion, torneo):
    mejores = []
    for k in range(m):
        mejor = 10000000000
        pos = None
        for i in range(torneo):
            x = random.randint(0, len(resultados)-1)
            elegido = float(resultados[x])
            if elegido < mejor:
                mejor = elegido
                pos = x
        mejores.append(poblacion[pos])

    return mejores

def cruce(mejores):

    poblacion = []

    for i in range(0, len(mejores), 2):
        hijo1 = ""
        hijo2 = ""
        padre = mejores[i-1]
        madre = mejores[i]

        for j in range(len(padre)):
            a = padre[j]
            b = madre[j]
            r = random.randint(0, 1)
            if r == 0:
                hijo1 += a
            else:
                hijo1 += b
            s = random.randint(0, 1)
            if s == 0:
                hijo2 += a
            else:
                hijo2 += b
        poblacion.append(hijo1)
        poblacion.append(hijo2)
    return poblacion

def mutacion (poblacion, factor):
    poblacion2 = []
    for i in range(len(poblacion)):
        aux = ""
        for j in range(len(poblacion[i])):
            aleatorio = random.uniform(0, 100)
            if aleatorio <= factor:
                if poblacion[i][j] == "0":
                    aux += "1"
                else:
                    aux += "0"
            else:
                aux +=poblacion[i][j]
        poblacion2.append(aux)
    return poblacion2

mejor_absoluto = 100000000000000000
poblacion = iniciar(m, n)

#for k in range(100):
cont = 0
k = 0
inicio = time.time()
factor = 2
torneo = 10

while cont == 0 and k < 100:
    if k > 50:
        factor = 1
    resultados = evaluar(poblacion)
    mejores = seleccionar(resultados, m, poblacion, torneo)
    cruzados = cruce(mejores)
    poblacion = mutacion(cruzados, factor)
    resultados_f = evaluar(poblacion)
    mejor = 1000000000000
    for i in range(len(resultados_f)):
        comparado = float(resultados_f[i])
        if comparado < mejor:
            mejor = comparado
            pos = i

    if mejor < mejor_absoluto:
        mejor_absoluto = mejor
        cromosoma_absolto = poblacion[pos]
        iteracion = k
        no_mej = 0
        print(mejor)
    else:
        no_mej += 1

    if no_mej == 50:
        cont = 500
    print(k, no_mej)
    k += 1

   # print("El mejor resultado es:", mejor, "del cromosoma", poblacion[pos], "en la iteracion", k)
fin = time.time()
print("El mejor resultado es:", mejor_absoluto, "del cromosoma", cromosoma_absolto, "en la iteracion", iteracion, "con numero de evuluacion", iteracion*m)
print("Tiempo ejecucion:", (fin - inicio))