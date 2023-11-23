import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

class GridDrawer:
    
    def __init__(self, rows, cols, point_size=0.1):
        self.rows = cols
        self.cols = rows
        self.point_size = point_size
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-1, rows + 1)
        self.ax.set_ylim(-1, cols + 1) 

    # Drawing a grid 
    def draw_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                point = Circle((j, i), self.point_size, facecolor='none', edgecolor='b')
                self.ax.add_patch(point)
    
    # Drawing a tower and coverage
    def draw_a_square(self, middle, coords, color = 'green'):
        x1 = coords[0][0]
        x2 = coords[1][0]
        y1 = coords[0][1]
        y2 = coords[1][1]
        x_left_top = x1
        y_left_top = y2
        width = (x2 - x1)
        height = -(y2 - y1)
        wh = 0.5
        
        little =  Rectangle((middle[0] - wh/2, middle[1]+ wh/2), wh, -wh, edgecolor='black', color=color)
        self.ax.add_patch(little)
       
        square = Rectangle((x_left_top, y_left_top), width, height, edgecolor='black', facecolor=color, alpha = 0.3)
        self.ax.add_patch(square)
    #drawing a obstructed block
    def draw_black(self, coords):
        for i in coords:
            point = Circle((i[0], i[1]), self.point_size, color='black')
            self.ax.add_patch(point)
            
    def draw_a_line(self, p1, p2):
        self.ax.plot([p1[0], p2[0]], [p1[1], p2[1]],color='b',marker= 'o',linewidth=2.5)
        
