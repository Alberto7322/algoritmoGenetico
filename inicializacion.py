import random
import requests

m = 100
n = 32


def iniciar(m, n):

    palabra = ""
    poblacion = []
    for i in range(m):
        for j in range(n):
            palabra += (str(random.randint(0,1)))
        poblacion.append(palabra)
        palabra = ""
    return poblacion

def evaluar(poblacion):
    resultados = []
    for i in poblacion:
            cromosoma = i
            web = "http://163.117.164.219/age/test?c="
            r = requests.get(web + cromosoma)
            resultados.append(r.text)
    return resultados

def seleccionar(resultados, m, poblacion):
    pos_elegido = []
    for k in range(m):
        mejor = 10000000000
        pos = None
        for i in range(4):
            x = random.randint(0, len(resultados)-1)
            elegido = float(resultados[x])
            if elegido < mejor:
                mejor = elegido
                pos = x
        pos_elegido.append(poblacion[pos])

    return pos_elegido

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

def mutacion (poblacion):
    poblacion2 = []
    for i in range(len(poblacion)):
        aux = ""
        for j in range(len(poblacion[i])):
            aleatorio = random.randint(0, 100)
            if aleatorio <= 5:
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

for k in range(250):
    resultados = evaluar(poblacion)
    mejores = seleccionar(resultados, m, poblacion)
    cruzados = cruce(mejores)
    poblacion = mutacion(cruzados)
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
        iteracion= k
    print(k)
   # print("El mejor resultado es:", mejor, "del cromosoma", poblacion[pos], "en la iteracion", k)
print("El mejor resultado es:", mejor_absoluto, "del cromosoma", cromosoma_absolto, "en la iteracion", iteracion)