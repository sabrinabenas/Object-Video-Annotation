## falta gui de esto!

import numpy as np
import matplotlib.pyplot as plt

def specific_differences(lst,fps):
    #falta chequear que sean pares las listas
    return np.sum([(lst[i+1] - lst[i])/fps for i in range(0, len(lst)-1, 2)])

path = 'logfile'
f = open('logfile','r')

lines = [i for i in f.read().splitlines()]

fps = int(float(lines[7]))
nof = int(float(lines[10]))
datos = eval(lines[-1])

differences_dict_seg = {key: specific_differences(value,fps) for key, value in datos.items()}

keys = list(differences_dict_seg.keys())
values = list(differences_dict_seg.values())

plt.figure(figsize=(8, 4))
plt.bar(keys, values)#, color=['blue', 'green', 'red', 'purple'])
plt.title('Distribución de Distancias y Cercanías')
plt.xlabel('Objeto')
plt.ylabel('Tiempo Exploracion [s]')
plt.show()

for i in keys:
    print('el tiempo explorado en minutos es ')
    print(differences_dict_seg[i]/60 )
    print('para el objeto ', i)
    print('  ')