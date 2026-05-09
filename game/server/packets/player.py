from dataclasses import dataclass
#================================#
@dataclass
class Player:
    #-------------------------------#
    id: int
    #-------------------------------#
    x: float = 100
    y: float = 100
    #-------------------------------#
    dir_x: float = 0
    dir_y: float = 0
    #-------------------------------#
    color: str = "standard"
    #================================#
    def update(self, data: dict):
        #-------------------------------#
        self.x = data["pos"][0]
        self.y = data["pos"][1]
        #-------------------------------#
        self.dir_x = data["dir"][0]
        self.dir_y = data["dir"][1]
        #-------------------------------#
        self.inputs = data.get("inputs", {})
        #-------------------------------#
    #================================#
    def serialize(self):
        return {
            "inputs": self.inputs,
            "id": self.id,
            "pos": [self.x, self.y],
            "dir": [self.dir_x, self.dir_y],
            "color": self.color
        }
    
