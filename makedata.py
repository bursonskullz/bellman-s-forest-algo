import numpy as np 
import math as mt 
# test on first ellipse in paper
data = []
def makedomain():
	domain = np.linspace(0, 2*mt.pi, 200)
	A = mt.pow(2, 0.25)/mt.sqrt(mt.pi)
	B =  mt.pow(2, 0.25)/mt.sqrt(3* mt.pi)
	for t in domain:
		x = A* mt.cos(t)
		y = B* mt.sin(t)
		point = [x,y]
		data.append(point)
makedomain()

with open("domain.txt", "w") as txt_file:
    for line in data:
        txt_file.write('['+ str(line[0]) + "," + str(line[1]) +']' + '\n')
txt_file.close()
