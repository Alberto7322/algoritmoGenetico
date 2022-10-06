import requests
import random

cromosoma = ""
for i in range(100):
    cromosoma += str(random.randint(0,1))


while r != 0:
    aux = ""
    for i in cromosoma:
        cambio = random.randint(0, 50)
        if cambio <= 5:
            if i == "1":
                aux += 0
            else:
                aux += "1"
        else:
            aux += i

    web = "http://memento.evannai.inf.uc3m.es/age/test?c="
    ra = requests.get(web + aux)
    r = requests.get(web + cromosoma)
    if ra < r:
        r = ra
        cromosoma = aux
    print(r.text)
