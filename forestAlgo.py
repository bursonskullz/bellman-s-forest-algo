import numpy as np 
import math as mt

# Initialize data
index = 0 
alpha = 0 
p_0 = [0.01, 0.01]  # Changed to be inside; revert to [0.01, 0.25] if needed
h = 0.1  # Will be overwritten
d_counter = 0
counter = False
escape_path = []
escape_x_cordinate = []
escape_y_cordinate = []

# Read domain from file
try:
    domain = open("domain.txt", "r")
    converted_domain = []
    points = domain.readlines()
except FileNotFoundError:
    print("Error: domain.txt not found")
    exit()

# Parse domain points
for i in range(len(points)): 
    xcordinate = ''
    ycordinate = ''
    counter = False
    for j in range(len(points[i])):
        if points[i][j] == '[':
            pass
        elif points[i][j] == ',':
            counter = True 
        elif points[i][j] == ']':
            pass
        else:
            if counter:
                ycordinate += points[i][j]
            else: 
                xcordinate += points[i][j]
    try:
        converted_x_cordinate = float(xcordinate)
        converted_y_cordinate = float(ycordinate)
        converted_domain.append([converted_x_cordinate, converted_y_cordinate])
    except ValueError:
        print(f"Skipping invalid line: {points[i].strip()}")
domain.close()

def isPointInBoundary(omega, p):
    """
    Check if point p is inside the closed curve defined by omega using ray-casting.
    """
    x, y = p
    n = len(omega)
    inside = False
    
    for i in range(n):
        j = (i + 1) % n
        px_i, py_i = omega[i]
        px_j, py_j = omega[j]
        
        if ((py_i > y) != (py_j > y)) and \
           (x < (px_j - px_i) * (y - py_i) / (py_j - py_i + 1e-10) + px_i):
            inside = not inside
    
    return inside

def find_intersection(omega, start):
    """
    Find the closest point in omega to start.
    """
    minimum = (omega[0][0] - start[0])**2 + (omega[0][1] - start[1])**2
    min_idx = 0
    for i in range(len(omega)):
        radial = mt.sqrt((omega[i][0] - start[0])**2 + (omega[i][1] - start[1])**2)
        if radial < minimum:
            minimum = radial
            min_idx = i
    return omega[min_idx]

def determineMeshSize(omega):
    """
    Determine mesh size as smallest distance between opposite points divided by 1000.
    """
    omega = np.array(omega)
    n = len(omega)
    if n < 2:
        raise ValueError("omega must contain at least two points")
   
    distances = np.zeros(n)
    for i in range(n):
        p1 = omega[i]
        opp_idx = (i + n // 2) % n
        p2 = omega[opp_idx]
        dist = np.sqrt(np.sum((p1 - p2) ** 2))
        distances[i] = dist
    min_distance = np.min(distances)
    return min_distance / 1000  # Changed to 1000 for smaller steps

# Compute mesh size
h = determineMeshSize(converted_domain)
print('the mesh size', h)

# Check if starting point is inside
if not isPointInBoundary(converted_domain, p_0):
    print("Error: Starting point is not inside the domain")
    exit()

# Main loop
distance_tracker = 0
escape_path.append([p_0[0], p_0[1]])
escape_x_cordinate.append(p_0[0])
escape_y_cordinate.append(p_0[1])
last_intersection = None
direction_change_threshold = h * 10  # Persist direction unless significantly closer

while isPointInBoundary(converted_domain, p_0):
    # Only update intersection if significantly closer
    if last_intersection is None:
        intersection = find_intersection(converted_domain, p_0)
    else:
        new_intersection = find_intersection(converted_domain, p_0)
        new_distance = mt.sqrt((new_intersection[0] - p_0[0])**2 + (new_intersection[1] - p_0[1])**2)
        if new_distance < distance_tracker - direction_change_threshold:
            intersection = new_intersection
        else:
            intersection = last_intersection
    
    # Compute slope with division-by-zero check
    if abs(intersection[0] - p_0[0]) < 1e-10:
        slope = 0 if intersection[1] == p_0[1] else float('inf')
    else:
        slope = (intersection[1] - p_0[1]) / (intersection[0] - p_0[0])
    
    # Compute distance to intersection
    new_distance = mt.sqrt((intersection[0] - p_0[0])**2 + (intersection[1] - p_0[1])**2)
    
    if d_counter == 0:
        distance_tracker = new_distance
    else:
        d_counter += 1
        if distance_tracker <= new_distance:
            distance_tracker = new_distance
        else:
            print('Error: the distance to boundary is getting larger')
            break
    
    print(distance_tracker)

    # Euler method: move p_n+1 = p_n + h * direction
    if slope == float('inf') or slope == -float('inf'):
        p_0[0] = p_0[0]
        p_0[1] = p_0[1] + h * (1 if intersection[1] > p_0[1] else -1)
    else:
        dx = h / mt.sqrt(1 + slope**2)  # Normalize to step size h
        dy = slope * dx
        p_0[0] += dx
        p_0[1] += dy

    escape_path.append([p_0[0], p_0[1]])
    escape_x_cordinate.append(p_0[0])
    escape_y_cordinate.append(p_0[1])
    last_intersection = intersection  # Persist the intersection point

# Write escape path and boundary to files
with open("escape_path.txt", "w") as file:
    for line in escape_path:
        file.write(f"{line[0]} {line[1]}\n")
file.close()

with open("boundaryplot.txt", "w") as textfile:
    for line in converted_domain:
        textfile.write(f"{line[0]} {line[1]}\n")
textfile.close()
