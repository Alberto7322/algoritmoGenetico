import requests
import random
from random import uniform, gauss
import time
print(random.randrange(0,1,1))


extension = 4

def incializar():
    padre = []
    varianzas = []
    for _ in range(extension):
        padre.append(random.uniform(-180, 180))
        varianzas.append(random.uniform(100, 300))
    return padre, varianzas

def mutar(padre, varianzas):
    hijo = []
    for i in range(len(padre)):
        var = padre[i] + random.gauss(0, varianzas[i])
        hijo.append(var)

    return hijo


def evaluar(padre):
    web = "http://memento.evannai.inf.uc3m.es/age/robot4?"
    for i in range(len(padre)):
        if i != extension -1:
            c = "c"+str(i+1)+"="+str(padre[i])+"&"
        else:
            c = "c"+str(i+1)+"=" + str(padre[i])
        web = web + c
    r = requests.get(web)
    return r.text

def seleccion(ev_padre, ev_hijo, list_ev):
    if ev_padre < ev_hijo:
        list_ev.append(0)
    else:
        list_ev.append(1)
    return list_ev


def modi_varianzas():
    pass



