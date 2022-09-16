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
    mejor = 10000000000
    pos_elegido = None
    for i in poblacion:
            cromosoma = i
            web = "http://memento.evannai.inf.uc3m.es/age/test?c="
            r = requests.get(web + cromosoma)
            resultados.append(r.text)
    for i in range(10):
        x = random.randint(0, len(resultados))
        elegido = float(resultados[x])
        if elegido < mejor:
            mejor = elegido
            pos_elegido = x
    print(mejor)
    return pos_elegido

poblacion = iniciar(m, n)
print(poblacion)
mejor = evaluar(poblacion)
print(poblacion[mejor])