from typing import Tuple 
class Tower:
    """
    Class represent G7-network tower
    """
    
    def __init__(self, range: int, coords_plased: Tuple[int]) -> None:
        self.range = range
        self.coords = coords_plased
        self.neighbors = []
        
    def set_neighbor(self, neighbor_coords: Tuple[int]) -> None:
        if  not neighbor_coords in self.neighbors:
            self.neighbors.append(neighbor_coords)
            print(f'{self.coords} is neighbor to {neighbor_coords}')
        
    def set_coverage(self,leftPoint: Tuple[int], rightPoint: Tuple[int]) -> None:
        self.coverage = (leftPoint, rightPoint)
            
    def __str__(self) -> str:
        return f'{self.coords}'