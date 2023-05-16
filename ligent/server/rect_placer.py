
from pyqtree import Index
from typing import Tuple

class RectPlacer:
    def __init__(self, bbox:Tuple[float, float, float, float]) -> None:
        """
        Args:
            bbox (Tuple[float, float, float, float]): (xmin, ymin, xmax, ymax)
        """
        self.spindex = Index(bbox=bbox)

    def place_rectangle(self, name:str, bbox:Tuple[float, float, float, float])->bool:
        """place a rectangle into the 2d space without overlapping

        Args:
            name (str): rectangle name
            bbox (Tuple[float, float, float, float]): (xmin, ymin, xmax, ymax)

        Returns:
            bool: whether successfully placed without overlapping
        """
        matches = self.spindex.intersect(bbox)
        if matches:
            return False
        else:
            self.spindex.insert(name, bbox)
            return True

    def insert(self, name:str, bbox:Tuple[float, float, float, float]):
        """force place a rectangle into the 2d space"""
        self.spindex.insert(name, bbox)