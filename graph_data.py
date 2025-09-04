import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Set Seaborn style for better aesthetics
sns.set(style="whitegrid")

# Read and parse domain.txt (boundary points in [x,y] format)
boundary_points = []
try:
    with open("domain.txt", "r") as domain_file:
        for line in domain_file:
            # Remove [ and ] and split by comma
            line = line.strip().strip('[]')
            if line:
                x, y = map(float, line.split(','))
                boundary_points.append([x, y])
    boundary_points = np.array(boundary_points)
except FileNotFoundError:
    print("Error: domain.txt not found")
    exit()
except ValueError as e:
    print(f"Error parsing domain.txt: {e}")
    exit()

# Read escape_path.txt (space-separated x y coordinates)
try:
    escape_points = np.loadtxt("escape_path.txt")
except FileNotFoundError:
    print("Error: escape_path.txt not found")
    exit()
except ValueError as e:
    print(f"Error parsing escape_path.txt: {e}")
    exit()

# Create the plot
plt.figure(figsize=(8, 8))  # Square figure for equal aspect ratio

# Plot boundary using Seaborn's lineplot
sns.lineplot(x=boundary_points[:, 0], y=boundary_points[:, 1], 
             color='blue', label='Boundary', linewidth=2)

# Plot escape path with line and markers
sns.lineplot(x=escape_points[:, 0], y=escape_points[:, 1], 
             color='red', label='Escape Path', marker='o', markersize=5, linewidth=1)

# Customize the plot
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Ellipse Boundary and Escape Path')
plt.axis('equal')  # Ensure ellipse isn't distorted
plt.legend()

# Show the plot
plt.show()
