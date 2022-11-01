import random
import requests
import math

extension = 4
b = random.uniform(0.95,1.05)


def inicializar(tamanio_poblacion):
    poblacion = []
    poblacion_varianzas = []
    tipo_poblacion = int(input("Tipo de poblacion 0=ángulos 1=varianza: "))
    for i in range(tamanio_poblacion):  # inciamos poblacion
        auxpadre = []
        auxvar = []
        if tipo_poblacion == 0:
            for _ in range(extension):
                auxpadre.append(random.uniform(-180, 180))
                auxvar.append(random.uniform(300, 1000))
            poblacion.append(auxpadre)
            poblacion_varianzas.append(auxvar)

        elif tipo_poblacion == 1:
            for _ in range(extension):
                auxvar.append(random.uniform(300, 1000))
                auxpadre.append(random.gauss(0, auxvar))
            poblacion.append(auxpadre)
            poblacion_varianzas.append(auxvar)

    return poblacion, poblacion_varianzas


def selec_padres(individuos, evaluacion, varianzas):
    torneo = 4
    padres = 2

    padres_elegidos = []
    varianzas_padres = []
    for k in range(padres):
        elegido = []
        for i in range(torneo):
            x = random.randint(0, len(individuos) - 1)
            elegido.append(float(evaluacion[x]))
        mejor = min(elegido)
        pos = evaluacion.index(mejor)

        padres_elegidos.append(individuos[pos])
        varianzas_padres.append(varianzas[pos])

    return padres_elegidos, varianzas_padres


def sobrecruzamiento(individuos, varianzas, evaluacion, landa):
    cruzados = []
    varianzas_cruzadas = []
    for _ in range(landa):
        individuos_elegidos, varianzas_elegidas = selec_padres(individuos, evaluacion, varianzas)
        cruzado = individuos[0]
        varianza_cruzada = varianzas[0]
        funcion_ind = 0

        for i in range(len(individuos_elegidos[0])):
            for j in range(len(individuos_elegidos)):
                var_padr = random.randint(0, len(individuos_elegidos)-1)
                funcion_ind += individuos_elegidos[j][i]
                varianza_cruzada[i] = varianzas_elegidas[var_padr][i]
            cruzado[i] = funcion_ind / len(individuos_elegidos)
            #varianza_cruzada[i] = funcion_var / len(individuos_elegidos)
        cruzados.append(cruzado.copy())
        varianzas_cruzadas.append(varianza_cruzada.copy())
    return cruzados.copy(), varianzas_cruzadas.copy()


def evaluar(poblacion):
    evaluacion = []
    for j in range(len(poblacion)):
        web = "http://163.117.164.219/age/robot4?"

        for i in range(len(poblacion[j])):
            if i != extension - 1:
                c = "c" + str(i + 1) + "=" + str(poblacion[j][i]) + "&"
            else:
                c = "c" + str(i + 1) + "=" + str(poblacion[j][i])
            web = web + c

        r = requests.get(web)
        evaluacion.append(float(r.text))
    return evaluacion.copy()


def mutar(padre, varianzas):
    hijos = []
    for i in range(len(padre)):
        hijo = []
        for j in range(len(padre[i])):
            var = padre[i][j] + random.gauss(0, varianzas[i][j])
            hijo.append(var)
        hijos.append(hijo)
    return hijos


def seleccion_mult(individuo, varianzas, landa, evaluacion):

    for j in range(landa):
        peor = max(evaluacion)
        peor_pos = evaluacion.index(peor)

        individuos.pop(peor_pos)
        varianzas.pop(peor_pos)
        evaluacion.pop(peor_pos)

    return individuos, varianzas.copy(), evaluacion.copy()

def modi_varianzas_mult(varianza, b, landa):
    t = b / ((2 * (landa ** 0.5)) ** 0.5)
    t0 = b / ((2 * landa) ** 0.5)
    opcion = 1
    if opcion == 1:
        for i in range(len(varianza)):
            for j in range(len(varianza[i])):
                varianza[i][j] = varianza[i][j] * (math.e ** random.gauss(0, t))
    else:
        for i in range(len(varianza)):
            for j in range(len(varianza[i])):
                varianza[i][j] = (math.e ** random.gauss(0, t0)) * varianza[i][j] * (math.e ** random.gauss(0, t))
    return varianza


if __name__ == '__main__':
    tamanio_poblacion = 100
    landa = 20
    individuos = []
    varianzas = []
    seleccionados = []
    mejor_abs = 100000
    individuos , varianzas = inicializar(tamanio_poblacion)
    evaluacion = evaluar(individuos)

    for k in range(100):
        print("Iteracion:", k)

        cruzados, var_cruzadas = sobrecruzamiento(individuos, varianzas, evaluacion, landa)
        hijos = mutar(cruzados, var_cruzadas)
        var_cruzadas = modi_varianzas_mult(var_cruzadas, b, landa)

        individuos = individuos + hijos
        varianzas = varianzas + var_cruzadas

        eval_hijos = evaluar(hijos)
        evaluacion = evaluacion + eval_hijos

        individuos, varianzas, evaluacion = seleccion_mult(individuos, varianzas, landa,
                                                           evaluacion)
        mejor = min(evaluacion)
        pos_mejor = evaluacion.index(mejor)

        print(mejor, "\t", pos_mejor)
        #print(individuos[pos_mejor])
        if float(mejor) < float(mejor_abs):
            mejor_abs = mejor
            mejor_ang = individuos[pos_mejor]
            print("Nuevo mejor", mejor, "angulos:", mejor_ang)

    print(mejor_abs, "||", mejor_ang)
