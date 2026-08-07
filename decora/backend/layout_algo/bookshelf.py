class Bookshelf:
    def __init__(self, bookshelf):
        self.height = bookshelf["height"]
        self.width = bookshelf["width"]
        self.gap = bookshelf["gap"]
        self.wallgap = bookshelf["wallgap"]

    def get_position(self, room):
        height = room.height
        width = room.width
        return {
            "bottom_left": {
                "x": self.wallgap,
                "y": self.wallgap,
                "h": self.height,
                "w": self.width,
                "color": "yellow",
                "label": "bookshelf" 
            },
            "top_left": {
                "x": self.wallgap,
                "y": height - self.height - self.wallgap,
                "h": self.height,
                "w": self.width,
                "color": "yellow",
                "label": "bookshelf" 
            },
            "top_right": {
                "x": width - self.width - self.wallgap,
                "y": height - self.height - self.wallgap,
                "h": self.height,
                "w": self.width,
                "color": "yellow",
                "label": "bookshelf"  
            },
            "bottom_right": {
                "x": width - self.width - self.wallgap,
                "y": self.wallgap,
                "h": self.height,
                "w": self.width,
                "color": "yellow",
                "label": "bookshelf" 
            },

            "t_bottom_left": {
                "x": self.wallgap,
                "y": self.wallgap,
                "h": self.width,
                "w": self.height,
                "color": "yellow",
                "label": "bookshelf" 
            },
            "t_top_left": {
                "x": self.wallgap,
                "y": height - self.width - self.wallgap,
                "h": self.width,
                "w": self.height,
                "color": "yellow",
                "label": "bookshelf"  
            },
            "t_top_right": {
                "x": width - self.height - self.wallgap,
                "y": height - self.width - self.wallgap,
                "h": self.width,
                "w": self.height,
                "color": "yellow",
                "label": "bookshelf"
            },
            "t_bottom_right": {
                "x": width - self.height - self.wallgap,
                "y":self.wallgap,
                "h": self.width,
                "w": self.height,
                "color": "yellow",
                "label": "bookshelf"
            },
        }

    def place_bookshelf(self, room, wind_wall, door_wall, door_side):
        if wind_wall == "east":
            if door_wall == "south" and door_side == "left":
                room.add_rectangle(**(self.get_position(room)["t_top_left"]))

            elif door_wall == "north" and door_side == "left":
                room.add_rectangle(**(self.get_position(room)["t_bottom_left"]))

            else: 
                room.add_rectangle(**(self.get_position(room)["t_top_left"]))

        elif wind_wall == "west":
            if door_wall == "south" and door_side == "right":
                room.add_rectangle(**(self.get_position(room)["t_top_right"]))

            elif door_wall == "north" and door_side == "right":
                room.add_rectangle(**(self.get_position(room)["t_bottom_right"]))

            else: 
                room.add_rectangle(**(self.get_position(room)["t_top_right"]))

        elif wind_wall == "north":
            if door_wall == "east" and door_side == "top":
                room.add_rectangle(**(self.get_position(room)["top_right"]))

            else: 
                room.add_rectangle(**(self.get_position(room)["top_left"]))

        elif wind_wall == "south":
            if door_wall == "west" and door_side == "bottom":
                room.add_rectangle(**(self.get_position(room)["bottom_left"]))
            else:
                room.add_rectangle(**(self.get_position(room)["bottom_right"]))

        else:
            print("Error While plotting the bookshelf.")




