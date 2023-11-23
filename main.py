from tower import Tower
from typing import Tuple, List
from draw import GridDrawer
import matplotlib.pyplot as plt
from numpy import Inf
from random import random, seed, choice
from math import sqrt, ceil

seed(42)
class CityGrid:
    
    towerPlased = []
    obstructedBlocks = []
    
    
    def __init__(self, m:int, n:int, obstructedBlocksRatio:float = 0.3, towerRange:int = 1) -> None:
        self.columnNumber = m
        self.rowNumber = n
        self.towerRange = towerRange
        
        # pl_points it is an area to plase tower around expected placment point
        playsment_range = 2*towerRange 
        self.pl_points = [(i, j) for i in range(-playsment_range, playsment_range+1) for j in range(-playsment_range, playsment_range+1)]
        self.pl_points = sorted(self.pl_points, key=lambda x: (abs(x[0]), abs(x[1])))
        
        self.ratio = obstructedBlocksRatio
        self.grid = [[0]*m for _ in range(n)]
        self.fill_grid()
        
    def fill_grid(self):
        for i in range(self.rowNumber):
            for j in range(self.columnNumber):
                if random() >= self.ratio:
                    self.grid[i][j] = 1     # 1 mean we can place tower
                else:
                    self.obstructedBlocks.append((i, j))
    
    #Method to place a tower, return True if tower placed 
    def place_tower(self, coords: Tuple[int]) -> bool:
        
        if 0 <= coords[0] < self.rowNumber and 0 <= coords[1] < self.columnNumber and self.grid[coords[0]][coords[1]] == 1:
            self.grid[coords[0]][coords[1]] = Tower(self.towerRange,(coords[0], coords[1]))
            self.towerPlased.append(coords)
            self.set_tower_coverage(self.grid[coords[0]][coords[1]])
            return True
        else:
            return False
    
    def set_tower_coverage(self, tower:Tower) -> None:
        
        if tower.coords[0] - tower.range < 0:
            leftUpi = 0
        else:
            leftUpi = tower.coords[0] - tower.range
            
        if tower.coords[1] - tower.range < 0:
            leftUpj = 0
        else:
            leftUpj = tower.coords[1] - tower.range
            
        if tower.coords[0] + tower.range >= self.rowNumber:
            RightDowni = self.rowNumber - 1
        else:
            RightDowni = tower.coords[0] + tower.range
            
        if tower.coords[1] + tower.range >= self.columnNumber:
            RightDownj = self.columnNumber - 1 
        else:
            RightDownj = tower.coords[1] + tower.range
        tower.set_coverage((leftUpi, leftUpj), (RightDowni,RightDownj))
    
    #check if tower covers ob remove it from list
    def remove_covered(self, tow:Tower) -> None:
        not_rem_ob = []
        for ob in self.obstructedBlocks:
            if not ((tow.coverage[0][0] <= ob[0] <= tow.coverage[1][0]) and (tow.coverage[0][1] <= ob[1] <= tow.coverage[1][1])):
                not_rem_ob.append(ob)
            else:
                self.grid[ob[0]][ob[1]] = 2 #place 2 if obstructedBlocks covered 
        self.obstructedBlocks = not_rem_ob
            
    
    def tower_placement(self) -> None:
        count = 0
        while self.obstructedBlocks:
            if (l := len(self.obstructedBlocks)) > 1:
                
                cur_ob1 = choice(self.obstructedBlocks)
                cur_ob2 = choice(self.obstructedBlocks)
            
                distance = sqrt((cur_ob2[0]- cur_ob1[0])**2 +(cur_ob2[0] - cur_ob1[1])**2) #Compute the distance between points to place tower
                distToPlace = ceil(distance/2)
                
                # create a placment point clouser to middle
                if  cur_ob1[0] + distToPlace > self.rowNumber - (cur_ob1[0] + distToPlace):
                    p1 =  cur_ob1[0] - 1
                else: 
                    p1 =  cur_ob1[0] + 1
                
                if cur_ob1[1] + distToPlace > self.columnNumber - (cur_ob1[1] + distToPlace):
                    p2 =  cur_ob1[1] - 1
                else: 
                    p2 =  cur_ob1[1] + 1
                
                placement_point =  (p1 + 1, p2 + 1)
                
            else:
                
                placement_point = (self.obstructedBlocks[0][0] + 1 , self.obstructedBlocks[0][1] + 1)
                
            for point in self.pl_points:
                if self.place_tower((placement_point[0]+point[0], placement_point[1] + point[1])):
                    self.remove_covered(self.grid[placement_point[0]+point[0]][placement_point[1] + point[1]])
                    break  
            else:
                if count > 3:
                    break
                if l < 2:
                    break
                count += 1
    
    def set_tower_neighbor(self):
        l = len(self.towerPlased)
        
        for t in range(l): # for each tower
            
            curTowerCoords = self.towerPlased[t]
            curTower = self.grid[curTowerCoords[0]][curTowerCoords[1]] # get Tower object via coords in towerPlased
            
            for nt in range(t+1, l): # check other towers on neighbors
                
                nTowerCoords = self.towerPlased[nt]
                nTower = self.grid[nTowerCoords[0]][nTowerCoords[1]]
                
                if (curTower.coverage[0][0] <= nTower.coords[0] <= curTower.coverage[1][0]) and (curTower.coverage[0][1] <= nTower.coords[1] <= curTower.coverage[1][1]):
                    # Write neighbors to both towers 
                    curTower.set_neighbor(nTower.coords)
                    nTower.set_neighbor(curTower.coords)
                
            
    def connect_two(self, tow1:Tower, tow2:Tower, prew_n = []):
        
        neighbors = tow1.neighbors.copy()
        #sorting by distance between neighbors and final tower
        neighbors = sorted(neighbors, key = lambda x: sqrt((tow2.coords[0] - x[0])**2 + (tow2.coords[1] - x[1])**2))
        for ne in neighbors:
            
            if not ne in prew_n:
                if ne == tow2.coords:
                    return [(tow1.coords, tow2.coords)]
                prew_n.append(tow1.coords)
                next = self.connect_two(self.grid[ne[0]][ne[1]], tow2, prew_n)
                
                if next is not None:
                    return [(tow1.coords, ne)] + next
        return None
        
                
            
        
    
if __name__=='__main__':
    grid = CityGrid(15, 15, 0.3, towerRange = 1)
    
    gd = GridDrawer(grid.rowNumber, grid.columnNumber)
    gd.draw_grid()
    gd.draw_black(grid.obstructedBlocks)
    
    grid.tower_placement()
    
    for i, towerC in enumerate(grid.towerPlased):
        cur_tower = grid.grid[towerC[0]][towerC[1]]
        gd.draw_a_square(towerC, cur_tower.coverage, plt.cm.viridis(i*20))   
    grid.set_tower_neighbor()
    t1 = grid.grid[1][9]
    t2 = grid.grid[2][5]
    points = grid.connect_two(t1, t2)
    for p in points:
        gd.draw_a_line(p[0],p[1])
    
    
    plt.show()
        