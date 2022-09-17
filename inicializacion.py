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
            web = "http://memento.evannai.inf.uc3m.es/age/test?c="
            r = requests.get(web + cromosoma)
            resultados.append(r.text)
    return resultados

def seleccionar(resultados):
    pos_elegido = []
    for k in range(6):
        mejor = 10000000000
        for i in range(10):
            x = random.randint(0, len(resultados))
            elegido = float(resultados[x])
            if elegido < mejor:
                mejor = elegido
        print(mejor)
        pos_elegido.append(x)

    return pos_elegido

poblacion = iniciar(m, n)
resultados = evaluar(poblacion)
mejor = seleccionar(resultados)
print(mejor)
"""for i in range(6):
    print(poblacion[mejor[i]])
"""
def cruce(cromosoma1,cromosoma2):
    hijo1 = ""
    hijo2 = ""
    for i in range(len(cromosoma1)):
        a = cromosoma1[i]
        b = cromosoma2[i]
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
    return hijo1 + "\n" + hijo2

def mutacion (hijos):
    for i in range(len(hijos)):
        for j in range(len(hijos[i])):
            aleatorio = random.randint(0, 100)
            if aleatorio <= 5:
                if hijos[i][j] == 0:
                    hijos[i][j] = 1
                else:
                    hijos[i][j] = 0
    return hijos
