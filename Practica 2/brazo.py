import requests
import random
import math
from random import uniform, gauss
import time


extension = 4
c = 0.82
s = 30
b = 1

def inicializar():
    padre = []
    varianzas = []
    for _ in range(extension):
        padre.append(random.uniform(-180, 180))
        varianzas.append(random.uniform(300, 1000))
    return padre, varianzas


def mutar(padre, varianzas):
    hijo = []
    for i in range(len(padre)):
        var = padre[i] + random.gauss(0, varianzas[i])
        hijo.append(var)

    return hijo

def sobrecruzamiento(individuos, varianzas):
    cruzado = individuos[0]
    varianza_cruzada = varianzas[0]
    funcion_ind=0
    funcion_var=0
    for i in range(len(individuos)):
        for j in range(len(individuos)):
            funcion_ind += individuos[j][i]
            funcion_var += varianzas[j][i]
        cruzado[i]= funcion_ind / poblacion
        varianza_cruzada[i] = funcion_var/ poblacion
    return cruzado, varianza_cruzada


def evaluar(padre):
    web = "http://memento.evannai.inf.uc3m.es/age/robot4?"
    for i in range(len(padre)):
        if i != extension - 1:
            c = "c" + str(i + 1) + "=" + str(padre[i]) + "&"
        else:
            c = "c" + str(i + 1) + "=" + str(padre[i])
        web = web + c
    r = requests.get(web)
    return r.text


def seleccion_11(ev_padre, ev_hijo, list_ev, padre, hijo):
    if float(ev_padre) < float(ev_hijo):
        list_ev.append(0)
    else:
        list_ev.append(1)
    if list_ev[-1] == 1:
        return list_ev, hijo.copy(), ev_hijo
    else:
        return list_ev, padre.copy(), ev_padre


def modi_varianzas_11(lis_ev, c, varianzas, s):
    if len(lis_ev) >= s:
        v = lis_ev[-s:].count(1) / s
        if v > 1 / 5:
            for i in range(len(varianzas)):
                varianzas[i] = varianzas[i] / c
        elif v < 1 / 5:
            for i in range(len(varianzas)):
                varianzas[i] = varianzas[i] * c

    return varianzas

def seleccion_mult(individuo, hijo, varianzas, var_hijo):
    peor = 0
    for i in range(len(individuo)):
        evaluacion = float(evaluar(individuo[i]))
        if evaluacion > peor:
            peor = evaluacion
            pos = i
    eval_hijo = float(evaluar(hijo))
    if peor > eval_hijo:
        individuo.pop(pos)
        individuo.append(hijo)
        varianzas.pop(pos)
        varianzas.append(var_hijo)
        mejor = eval_hijo
    else:
        mejor = peor
    return individuo, varianzas, mejor

def modi_varianzas_mult(varianza, b, individuos):
    t = b/((2*(len(individuos)**0.5))**0.5)
    t0 = b/((2*len(individuos))**0.5)
    opcion = 1
    if opcion == 1:
        for i in range(len(varianza)):
            varianza[i] = varianza[i] * (math.e)**random.gauss(0, t)
    else:
        for i in range(len(varianza)):
            varianza[i] = (math.e)**random.gauss(0, t0) * varianza[i] * math.e(random.gauss(0, t))
    return varianza

if __name__ == '__main__':
    modo = "1+1"  # 1+1 o multiple
    #modo = "multiple"

    if modo == "1+1":
        media_var = 1
        list_ev = []
        padre, varianzas = inicializar()

        while media_var > 1e-5:
            for i in range(s):
                hijo = mutar(padre, varianzas)
                ev_padre = evaluar(padre)
                ev_hijo = evaluar(hijo)
                list_ev, padre, ev = seleccion_11(ev_padre, ev_hijo, list_ev, padre, hijo)
            varianzas = modi_varianzas_11(list_ev, c, varianzas, s)
            aux = 0
            for i in range(len(varianzas)):
                aux += varianzas[i]
            media_var = aux/4
            print(ev)

        print(varianzas, "\n", padre, "\n", ev)
    elif modo == "multiple":
        poblacion = 3
        individuos = []
        varianzas = []
        mejor_abs = 100000
        for i in range(poblacion):  # inciamos poblacion
            aux_ind, aux_var = inicializar()
            individuos.append(aux_ind)
            varianzas.append(aux_var)
        for _ in range(1000):
            cruzado, var_cruzada = sobrecruzamiento(individuos, varianzas)
            hijo = mutar(cruzado, var_cruzada)
            var_hijo = modi_varianzas_mult(var_cruzada, b, individuos)
            individuos, varianzas, mejor = seleccion_mult(individuos, hijo, varianzas, var_hijo)

            if float(mejor) < float(mejor_abs):
                mejor_abs = mejor
            print(mejor)
        print(mejor_abs)