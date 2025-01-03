import numpy as np 
import math as mt 

data = []
def makedomain():
	domain = np.linspace(-4, 4, 200)
	for t in domain:
		x = mt.pi+ mt.cos(t)
		y = mt.pi * mt.tan(t)+mt.sin(t)
		point = [x,y]
		data.append(point)
makedomain()

with open("domain.txt", "w") as txt_file:
    for line in data:
        txt_file.write('['+ str(line[0]) + "," + str(line[1]) +']' + '\n')
txt_file.close()
