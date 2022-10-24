import requests
import random
from random import uniform, gauss
import time
print(random.randrange(0,1,1))


extension = 4
c = 0.82
s = 10

def inicializar():
    padre = []
    varianzas = []
    for _ in range(extension):
        padre.append(random.uniform(-180, 180))
        varianzas.append(random.uniform(0, 1000))
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

def seleccion(ev_padre, ev_hijo, list_ev, padre, hijo):
    if ev_padre < ev_hijo:
        list_ev.append(0)
    else:
        list_ev.append(1)
    if list_ev[-1] == 1:
        return list_ev, hijo, ev_hijo
    else:
        return list_ev, padre, ev_padre


def modi_varianzas(lis_ev, c, varianzas, s):
    if len(lis_ev) >= 10:
        v = lis_ev[-s:].count(1)/s
        if v > 1/5:
            for i in range(len(varianzas)):
                varianzas[i] = varianzas[i] / c
        elif v < 1/5:
            for i in range(len(varianzas)):
                varianzas[i] = varianzas[i] * c
        else:
            pass
    return varianzas

list_ev = []

padre, varianzas = inicializar()

for _ in range(300):
    hijo = mutar(padre, varianzas)
    ev_padre = evaluar(padre)
    ev_hijo = evaluar(hijo)
    list_ev, padre , ev= seleccion(ev_padre, ev_hijo, list_ev, padre, hijo)
    varianzas = modi_varianzas(list_ev, c, varianzas, s)
    print(ev)

print(varianzas,"\n", padre, "\n", ev)


