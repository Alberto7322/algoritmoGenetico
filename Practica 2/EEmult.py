import random
import requests
import math

extension = 4
b = 1


def inicializar():
    padre = []
    varianzas = []
    for _ in range(extension):
        padre.append(random.uniform(-180, 180))
        varianzas.append(random.uniform(300, 1000))
    return padre, varianzas



def selec_padres(individuos, evaluacion, varianzas):
    torneo = 20
    padres = 2

    padres_elegidos = []
    varianzas_padres = []
    for k in range(padres):
        mejor = 10000000000
        pos = None
        for i in range(torneo):
            x = random.randint(0, len(individuos) - 1)
            elegido = float(evaluacion[x])
            if elegido < mejor:
                mejor = elegido
                pos = x
        padres_elegidos.append(individuos[pos])
        varianzas_padres.append(varianzas[pos])

    return padres_elegidos, varianzas_padres

def sobrecruzamiento(individuos, varianzas, evaluacion, hijos):
    cruzados = []
    varianzas_cruzadas = []
    for _ in range(hijos):
        individuos_elegidos, varianzas_elegidas = selec_padres(individuos, evaluacion, varianzas)
        cruzado = individuos[0]
        varianza_cruzada = varianzas[0]
        funcion_ind = 0
        funcion_var = 0

        for i in range(len(individuos_elegidos[0])):
            for j in range(len(individuos_elegidos)):
                var_padr = random.randint(0, len(individuos_elegidos))
                funcion_ind += individuos_elegidos[j][i]
                funcion_var = varianzas[var_padr][i]
            cruzado[i] = funcion_ind / len(individuos_elegidos)
            varianza_cruzada[i] = funcion_var / len(individuos_elegidos)
        cruzados.append(cruzado.copy())
        varianzas_cruzadas.append(varianza_cruzada.copy())
    return cruzados, varianzas_cruzadas


def evaluar(poblacion):
    evaluacion = []
    for j in range(len(poblacion)):
        web = "http://memento.evannai.inf.uc3m.es/age/robot4?"

        for i in range(len(poblacion[j])):
            if i != extension - 1:
                c = "c" + str(i + 1) + "=" + str(poblacion[j][i]) + "&"
            else:
                c = "c" + str(i + 1) + "=" + str(poblacion[j][i])
            web = web + c

        r = requests.get(web)
        evaluacion.append(float(r.text))
    return evaluacion

def mutar(padre, varianzas):
    hijos = []
    for i in range(len(padre)):
        hijo = []
        for j in range(len(padre[i])):
            var = padre[i][j] + random.gauss(0, varianzas[i][j])
            hijo.append(var)
        hijos.append(hijo)
    return hijos

def seleccion_mult(individuo, hijo, varianzas, var_hijo, num_hijos, eval_padre):
    pos_mejor = 0
    eval_hijos = evaluar(hijo)
    eval_tot = eval_padre + eval_hijos
    individuos = individuo + hijo
    varianzas = varianzas + var_hijo
    mejor = 10000000000000000
    for j in range(num_hijos):
       peor = 0
       for i in range(len(individuos)):
           if float(eval_tot[i]) > peor:
               peor = float(eval_tot[i])
               peor_pos = i
       individuos.pop(peor_pos)
       varianzas.pop(peor_pos)
       eval_tot.pop(peor_pos)

    for i in range(len(individuos)):
       if float(eval_tot[i]) <= mejor:
        mejor = float(eval_tot[i])
        pos_mejor = i
    return individuos.copy(), varianzas.copy(), mejor, pos_mejor



def modi_varianzas_mult(varianza, b, individuos):
    t = b/((2*(len(individuos)**0.5))**0.5)
    t0 = b/((2*len(individuos))**0.5)
    opcion = 1
    if opcion == 1:
        for i in range(len(varianza)):
            for j in range(len(varianza[i])):
                varianza[i][j] = varianza[i][j] * (math.e)**random.gauss(0, t)
    else:
        for i in range(len(varianza)):
            for j in range(len(varianza[i])):
                varianza[i][j] =(math.e)**random.gauss(0, t0) * varianza[i][j] * (math.e)**random.gauss(0, t)
    return varianza



if __name__ == '__main__':
    poblacion = 100
    num_hijos = 20
    individuos = []
    varianzas = []
    seleccionados = []
    mejor_abs = 100000
    for i in range(poblacion):  # inciamos poblacion
        aux_ind, aux_var = inicializar()
        individuos.append(aux_ind)
        varianzas.append(aux_var)

    for k in range(100):
        evaluacion = evaluar(individuos)
        cruzados, var_cruzadas = sobrecruzamiento(individuos, varianzas, evaluacion, num_hijos)
        hijos = mutar(cruzados, var_cruzadas)
        var_cruzadas = modi_varianzas_mult(var_cruzadas, b, individuos)
        individuos, varianzas, mejor, pos_mejor = seleccion_mult(individuos, hijos, varianzas, var_cruzadas, num_hijos, evaluacion)

        print(mejor)
        if float(mejor) < float(mejor_abs):
            mejor_abs = mejor
            mejor_ang = individuos[pos_mejor]
            print("Nuevo mejor", mejor, "angulos:", mejor_ang)
        print("Iteracion:", k)

    print(mejor_abs, "||", mejor_ang)
