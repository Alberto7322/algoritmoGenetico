import random
import requests
import math


class Multiple():
    def __init__(self, size_poblacion, tipo_poblacion, numero_articulaciones, size_torneo, numero_padres,
                 tipo_sobrecruzamiento, tipo_mutacion_varianza, landa):
        self.poblacion = []
        self.varianzas = []
        self.fitness = []
        self.size_poblacion = size_poblacion
        self.tipo_poblacion = tipo_poblacion
        self.numero_articulaciones = numero_articulaciones
        self.size_torneo = size_torneo
        self.numero_padres = numero_padres
        self.tipo_sobrecruzamiento = tipo_sobrecruzamiento
        self.tipo_mutacion_varianza = tipo_mutacion_varianza
        self.landa = landa
        self.web4 = "http://163.117.164.219/age/robot4?"
        self.web6 = "http://163.117.164.219/age/robot6?"
        self.web10 = "http://163.117.164.219/age/robot10?"

    def __str__(self):
        return ("La poblacion es {}\n de tipo {}\n con las varianzas {}".format(self.poblacion, self.tipo_poblacion,
                                                                                self.varianzas))

    # Se inicializa la poblacion
    def inicializar(self):
        for _ in range(self.size_poblacion):
            auxpadre = []
            auxvar = []
            if self.tipo_poblacion == 0:
                for _ in range(self.numero_articulaciones):
                    auxpadre.append(random.uniform(-180, 180))
                    auxvar.append(random.uniform(300, 1000))
                self.poblacion.append(auxpadre)
                self.varianzas.append(auxvar)

            elif self.tipo_poblacion == 1:
                for _ in range(self.numero_articulaciones):
                    auxvar.append(random.uniform(300, 1000))
                    auxpadre.append(random.gauss(0, auxvar))
                self.poblacion.append(auxpadre)
                self.varianzas.append(auxvar)

        return self.poblacion, self.varianzas

    # Se llama al servidor con el objeto de obtener la evaluación
    def evaluar(self, lista, evaluacion):
        fitness_lista = []
        for i in range(len(lista)):
            contador = 1
            url = ""
            for articulacion in range(self.numero_articulaciones):
                if evaluacion != 1:
                    if contador == 1:
                        url += "c1=" + str(lista[i][articulacion])
                    else:
                        url += "&c" + str(contador) + "=" + str(lista[i][articulacion])
                else:
                    if contador == 1:
                        url += "c1=" + str(self.poblacion[i][articulacion])
                    else:
                        url += "&c" + str(contador) + "=" + str(self.poblacion[i][articulacion])
                contador += 1

            if evaluacion != 1:
                if self.numero_articulaciones == 4:
                    r = requests.get(self.web4 + url)
                    fitness_lista.append(float(r.text))

                elif self.numero_articulaciones == 6:
                    r = requests.get(self.web6 + url)
                    fitness_lista.append(float(r.text))

                elif self.numero_articulaciones == 10:
                    r = requests.get(self.web10 + url)
                    fitness_lista.append(float(r.text))

            else:
                if self.numero_articulaciones == 4:
                    r = requests.get(self.web4 + url)
                    self.fitness.append(float(r.text))

                elif self.numero_articulaciones == 6:
                    r = requests.get(self.web6 + url)
                    self.fitness.append(float(r.text))

                elif self.numero_articulaciones == 10:
                    r = requests.get(self.web10 + url)
                    self.fitness.append(float(r.text))
                print(i)
        if evaluacion != 1:
            return fitness_lista
        else:
            return self.fitness

    # Se lleva a cabo el torneo
    def sobrecruzamiento(self):
        padres = []
        varianzas_padres = []

        ganadores = []
        varianzas_ganadores = []

        # Se lleva a cabo la selección de los padres a cruzar
        for _ in range(self.numero_padres):
            elegidos = []
            for _ in range(self.size_torneo):
                indice = random.randint(0, len(self.poblacion) - 1)
                elegidos.append(self.fitness[indice])
            mejor = min(elegidos)
            pos = self.fitness.index(mejor)
            padres.append(self.poblacion[pos])
            varianzas_padres.append(self.varianzas[pos])

        # Se realiza el cruzamiento
        # A la hora de realizar pruebas, cambiamos la declaración del número de padres a cruzar
        self.size_progenitores = random.randint(2, 4)
        for _ in range(self.landa):
            padres_seleccionados = []
            varianzas_seleccionadas = []
            indices = []
            while len(padres_seleccionados) < self.size_progenitores:
                indice = random.randint(0, len(padres) - 1)
                if indice not in indices:
                    padres_seleccionados.append(padres[indice])
                    varianzas_seleccionadas.append(varianzas_padres[indice])
                    indices.append(indice)

            hijo = []
            varianza_hijo = []
            longitud_seleccionados = len(padres_seleccionados)

            # Media de cada articulación de los padres
            for articulacion in range(self.numero_articulaciones):
                hijo.append(0)
                for padre in range(longitud_seleccionados):
                    hijo[articulacion] += (padres_seleccionados[padre][articulacion]) / longitud_seleccionados

            if self.tipo_sobrecruzamiento == 0:
                for articulacion in range(self.numero_articulaciones):
                    varianza_hijo.append(0)
                    for padre in range(longitud_seleccionados):
                        varianza_hijo[articulacion] += (varianzas_seleccionadas[padre][articulacion])
                    varianza_hijo[articulacion] = (varianza_hijo[articulacion]) ** 0.5

            elif self.tipo_sobrecruzamiento == 1:
                for varianza in range(self.numero_articulaciones):
                    varianza_hijo.append(0)
                    padre_indice = random.randint(0, longitud_seleccionados - 1)
                    varianza_hijo[varianza] = varianzas_seleccionadas[padre_indice][varianza]

            ganadores.append(hijo.copy())
            varianzas_ganadores.append(varianza_hijo.copy())

        return ganadores, varianzas_ganadores

    def mutar(self, ganadores, varianzas_ganadores):
        hijos = []
        b = random.uniform(0.95, 1.05)
        t = b / ((2 * (self.landa ** 0.5)) ** 0.5)
        t0 = b / ((2 * self.landa) ** 0.5)

        for i in range(len(ganadores)):
            hijo = []
            for j in range(len(ganadores[i])):
                var = ganadores[i][j] + random.gauss(0, varianzas_ganadores[i][j])
                hijo.append(var)
            hijos.append(hijo)
        if self.tipo_mutacion_varianza == 1:
            for i in range(len(varianzas_ganadores)):
                for j in range(len(varianzas_ganadores[i])):
                    varianzas_ganadores[i][j] = varianzas_ganadores[i][j] * (math.e ** random.gauss(0, t))
        else:
            for i in range(len(varianzas_ganadores)):
                for j in range(len(varianzas_ganadores[i])):
                    varianzas_ganadores[i][j] = (math.e ** random.gauss(0, t0)) * varianzas_ganadores[i][j] * (
                                math.e ** random.gauss(0, t))

        return hijos, varianzas_ganadores

    def seleccion_mult(self, hijos, varianzas_ganadores):
        fitness_hijos = self.evaluar(hijos, 2)
        self.poblacion = self.poblacion + hijos
        self.varianzas = self.varianzas + varianzas_ganadores
        self.fitness = self.fitness + fitness_hijos

        for _ in range(self.landa):
            peor = max(self.fitness)
            peor_pos = self.fitness.index(peor)

            self.poblacion.pop(peor_pos)
            self.varianzas.pop(peor_pos)
            self.fitness.pop(peor_pos)

        return self.poblacion, self.varianzas, self.fitness

if __name__ == '__main__':
    # Valores a modificar
    size_poblacion = 100
    tipo_poblacion = 0
    numero_articulaciones = 4
    tamanio_torneo = 10
    numero_de_padres = 30
    tipo_sobrecruzamiento = 1
    tipo_mutacion_varianza = 1
    landa = 20
    # Fin

    poblacion1 = Multiple(size_poblacion, tipo_poblacion, numero_articulaciones,
                          tamanio_torneo, numero_de_padres, tipo_sobrecruzamiento, tipo_mutacion_varianza, landa)
    # size_poblacion,tipo_poblacion,numero_articulaciones,size_torneo,numero_padres, tipo_sobrecruzamiento, tipo_mutacion_varianza, landa
    poblacion1.inicializar()
    print("evaluacion tocha")
    fitness = poblacion1.evaluar(poblacion1.poblacion, 1)
    print("\033[1m \033[96m El mejor individuo es {} \033[0m".format(min(poblacion1.fitness)))
    iteracion = 0
    while min(poblacion1.fitness) > 1e-2:
        print("\033[1m \033[92m Iteracion:{}\033[0m\n".format(iteracion))
        ganadores, varianzas = poblacion1.sobrecruzamiento()
        mutados, varianzas_mutados = poblacion1.mutar(ganadores, varianzas)
        poblacion1.seleccion_mult(mutados, varianzas_mutados)
        print("\033[1m \033[96m El mejor individuo es {} cuyos angulos son {} \033[0m".format(min(poblacion1.fitness),
                                                                                              poblacion1.poblacion[
                                                                                                  poblacion1.fitness.index(
                                                                                                      min(poblacion1.fitness))]))
        iteracion += 1
