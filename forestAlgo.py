import numpy as np 
import math as mt

# use psuedo algorithm 
# 1) intaitate data p_0 and h and read omega from a file. Print data and plot to make sure it works 
# 2) make function to take in omega and p_o that returns the slops of the line 
# put inside while loop and compute p_{n+1} = p_n + m_n * h 

# make checking method to make sure h is small compared to lambda or the first radius.
# while |p_n-\omega(t)|>\epsilon for all t in domain then keep going. 
# this ensures p_n is close to boundary before ending loop

#need to make sure p_0 is in domain before we start 
index = 0 
alpha = 0 
p_0 = [mt.pi, mt.pi]
h = 0.1
epsilon = 0.1
counter = False
large_value = 10000000000
escape_path = []
length_of_line = epsilon + large_value # intiate loop to run for large value
escape_x_cordinate = []
escape_y_cordinate = []

domain = open("domain.txt", "r")
converted_domain = []
points = domain.readlines()



def find_intersection(omega, start):
	# returns point q_n in paper 
	minimum = (omega[0][0]-start[0])**2+(omega[0][1]-start[1])**2
	i = 0
	for point in omega:
		radial = (point[0]-start[0])**2+(point[1]-start[1])**2
		if (radial <= minimum) : 
			minimum = radial
			i = i+1 
		else:
			pass
	return omega[i]


for i in range(0,len(points)): 
	xcordinate = ''
	ycordinate = ''
	counter = False
	for j in range(0, len(points[i])):
		if (points[i][j] == '['):
			pass
		elif (points[i][j] == ','):
			counter = True 
			#print("we found a comma")
			for l in range(j+1,len(points[i])):
				if(points[i][l] == ']'):
					pass
				else:
					ycordinate = ycordinate + points[i][l]
		else:
			if(counter == True):
				pass
			else: 
				xcordinate = xcordinate + points[i][j]
	converted_x_cordinate = float(xcordinate)
	converted_y_cordinate = float(ycordinate)
	converted_domain.append([converted_x_cordinate,converted_y_cordinate])
domain.close()



while(length_of_line > epsilon): 
	intersection = find_intersection(converted_domain, p_0)
	slope = (intersection[1]- p_0[1])/(intersection[0]- p_0[0])
	#print slope
	p_0[0] = p_0[0] + slope * h 
	p_0[1] = p_0[1] + slope * h 
	escape_path.append([p_0[0],p_0[1]])
	escape_x_cordinate.append(p_0[0])
	escape_y_cordinate.append(p_0[1])

	#reset length of line from intesection to (p_0[0],p_0[1])  
	old_line_length  = length_of_line
	length_of_line = mt.sqrt((intersection[0] - p_0[0])**2 + (intersection[1] - p_0[1])**2)

	if(old_line_length < length_of_line): #check if length of line p_0 increases stop and print values
		break

		#check if point is still inside region and if so keep going

with open("escape_path.txt", "w") as file:
    for line in escape_path:
    	file.write(str(line[0])+ ' ' + str(line[1])+ '\n')
file.close()


with open("boundaryplot.txt", "w") as textfile:
    for line in converted_domain:
    	textfile.write(str(line[0])+ ' ' + str(line[1])+ '\n')
textfile.close()

#write to file and use mathlab 
