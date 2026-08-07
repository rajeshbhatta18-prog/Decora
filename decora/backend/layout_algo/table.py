class Table:
    def __init__(self, table):
        self.height = table["height"]
        self.width = table["width"]
        self.gap = table["gap"]

    def get_position(self, room, bookshelf):
        height = room.height
        width = room.width
        return {
            "bottom_left": {
                "x": self.gap,
                "y": bookshelf["wallgap"] + bookshelf["width"] + bookshelf["gap"],
                "h": self.height,
                "w": self.width,
                "color": "lightgreen",
                "label": "table" 
            },
            "top_left": {
                "x": self.gap,
                "y": height - bookshelf["wallgap"] - bookshelf["width"] - bookshelf["gap"] - self.height,
                "h": self.height,
                "w": self.width,
                "color": "lightgreen",
                "label": "table" 
            },
            "top_right": {
                "x": width - self.gap - self.width,
                "y": height - self.height - bookshelf["wallgap"] - bookshelf["width"] - bookshelf["gap"],
                "h": self.height,
                "w": self.width,
                "color": "lightgreen",
                "label": "table"  
            },
            "bottom_right": {
                "x": width - self.gap - self.width,
                "y": bookshelf["wallgap"] + bookshelf["width"] + bookshelf["gap"],
                "h": self.height,
                "w": self.width,
                "color": "lightgreen",
                "label": "table" 
            },

            "t_bottom_left": {
                "x": bookshelf["width"] + bookshelf["wallgap"] + bookshelf['gap'],
                "y": self.gap,
                "h": self.width,
                "w": self.height,
                "color": "lightgreen",
                "label": "table" 
            },
            "t_top_left": {
                "x": bookshelf["wallgap"] + bookshelf["width"] + bookshelf["gap"],
                "y": height - self.gap - self.width,
                "h": self.width,
                "w": self.height,
                "color": "lightgreen",
                "label": "table"  
            },
            "t_top_right": {
                "x": width - bookshelf["width"] - bookshelf["wallgap"] -bookshelf['gap'] - self.height,
                "y": height - self.gap -self.width,
                "h": self.width,
                "w": self.height,
                "color": "lightgreen",
                "label": "table"
            },
            "t_bottom_right": {
                "x": width - bookshelf["width"] - bookshelf["wallgap"] -bookshelf['gap'] - self.height,
                "y": self.gap,
                "h": self.width,
                "w": self.height,
                "color": "lightgreen",
                "label": "table"
            },
        }

    def place_table(self, room, wind_wall, door_wall, door_side, bookshelf):

        if wind_wall == "east":
            if door_wall == "north" and door_side == "left":
                room.add_rectangle(**(self.get_position(room,bookshelf)["bottom_left"]))
    
            else:
                room.add_rectangle(**(self.get_position(room,bookshelf)["top_left"]))    

        elif wind_wall== "west":
            if door_wall == "north" and door_side == "right":
               room.add_rectangle(**(self.get_position(room,bookshelf)["bottom_right"])) 

            else:
                room.add_rectangle(**(self.get_position(room,bookshelf)["top_right"]))

        elif wind_wall == "north":
            if door_wall == "east" and door_side == "top":
                room.add_rectangle(**(self.get_position(room,bookshelf)["t_top_right"]))

            else:
                room.add_rectangle(**(self.get_position(room,bookshelf)["t_top_left"]))

        elif wind_wall == "south":
            if door_wall == "west" and door_side == "bottom":
                room.add_rectangle(**(self.get_position(room,bookshelf)["t_bottom_left"]))
            else:
                room.add_rectangle(**(self.get_position(room,bookshelf)["t_bottom_right"]))

        else:
            print("Error While plotting the table.")
