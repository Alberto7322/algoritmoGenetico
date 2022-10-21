import requests

cromosoma = '000000000000000100000000000000000000000000001000000000001100'

web = "http://memento.evannai.inf.uc3m.es/age/test?c="

r = requests.get(web + cromosoma)
print(r.text)
