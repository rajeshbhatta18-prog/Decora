class Chair():
    def __init__(self, chair):
        self.height = chair["height"]
        self.width = chair["width"]
        self.gap = chair["gap"]

    def get_position(self, room, bookshelf, table):
            height = room.height
            width = room.width
            return {
                "bottom_left": {
                    "x": table["gap"] + table["width"] + self.gap,
                    "y": bookshelf["wallgap"] + bookshelf["width"] + bookshelf["gap"] + table["height"]/2 - self.height/2,
                    "h": self.height,
                    "w": self.width,
                    "color": "lightgreen",
                    "label": "chair" 
                },
                "top_left": {
                    "x": table["gap"] + table["width"] + self.gap,
                    "y": height - bookshelf["wallgap"] - bookshelf["width"] -  bookshelf["gap"] - table["height"]/2 - self.height/2,
                    "h": self.height,
                    "w": self.width,
                    "color": "lightgreen",
                    "label": "chair" 
                },
                "top_right": {
                    "x": width - table["gap"] - table["width"] - self.gap - self.width,
                    "y": height - bookshelf["wallgap"] - bookshelf["width"] -  bookshelf["gap"] - table["height"]/2 - self.height/2,
                    "h": self.height,
                    "w": self.width,
                    "color": "lightgreen",
                    "label": "chair"  
                },
                "bottom_right": {
                    "x": width - table["gap"] - table["width"] - self.gap - self.width,
                    "y": bookshelf["wallgap"] + bookshelf["width"] + bookshelf["gap"] + table["height"]/2 - self.height/2,
                    "h": self.height,
                    "w": self.width,
                    "color": "lightgreen",
                    "label": "chair" 
                },
    
                "t_bottom_left": {
                    "x": bookshelf["width"] + bookshelf["wallgap"] + bookshelf['gap'] + table["height"]/2 - self.height/2,
                    "y": table["gap"] + table["width"] + self.gap,
                    "h": self.width,
                    "w": self.height,
                    "color": "lightgreen",
                    "label": "chair" 
                },
                "t_top_left": {
                    "x": bookshelf["wallgap"] + bookshelf["width"] + bookshelf["gap"] + table["height"]/2 - self.height/2,
                    "y": height - table["gap"] - table["width"] - self.gap - self.width,
                    "h": self.width,
                    "w": self.height,
                    "color": "lightgreen",
                    "label": "chair"  
                },
                "t_top_right": {
                    "x": width - bookshelf["width"] - bookshelf["wallgap"] -bookshelf['gap'] - table["height"]/2 - self.height/2,
                    "y": height - table["gap"] - table["width"] - self.gap - self.width,
                    "h": self.width,
                    "w": self.height,
                    "color": "lightgreen",
                    "label": "chair"
                },
                "t_bottom_right": {
                    "x": width - bookshelf["width"] - bookshelf["wallgap"] - bookshelf['gap'] - table["height"]/2 - self.height/2,
                    "y": table["gap"] + table["width"] + self.gap,
                    "h": self.width,
                    "w": self.height,
                    "color": "lightgreen",
                    "label": "chair"
                },
            }

    def place_chair(self, room, wind_wall, door_wall, door_side, table, bookshelf):
        if wind_wall == "east":
            if door_wall == "north" and door_side == "left":
                room.add_rectangle(**(self.get_position(room, bookshelf, table)["bottom_left"]))
    
            else:
                room.add_rectangle(**(self.get_position(room, bookshelf, table)["top_left"]))    

        elif wind_wall== "west":
            if door_wall == "north" and door_side == "right":
               room.add_rectangle(**(self.get_position(room, bookshelf, table)["bottom_right"])) 

            else:
                room.add_rectangle(**(self.get_position(room, bookshelf, table)["top_right"]))

        elif wind_wall == "north":
            if door_wall == "east" and door_side == "top":
                room.add_rectangle(**(self.get_position(room, bookshelf, table)["t_top_right"]))

            else:
                room.add_rectangle(**(self.get_position(room, bookshelf, table)["t_top_left"]))

        elif wind_wall == "south":
            if door_wall == "west" and door_side == "bottom":
                room.add_rectangle(**(self.get_position(room, bookshelf, table)["t_bottom_left"]))
            else:
                room.add_rectangle(**(self.get_position(room, bookshelf, table)["t_bottom_right"]))

        else:
            print("Error While plotting the chair.")