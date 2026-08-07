class Wardrobe:
    def __init__(self, wardrobe):
        self.height = wardrobe["height"]
        self.width = wardrobe["width"]
        self.gap = wardrobe["gap"]

    def get_position(self, room):
        height = room.height
        width = room.width
        return {
            "bottom_left": {
                "x": self.gap,
                "y": self.gap,
                "h": self.height,
                "w": self.width,
                "color": "green",
                "label": "wardrobe" 
            },
            "top_left": {
                "x": self.gap,
                "y": height - self.height - self.gap,
                "h": self.height,
                "w": self.width,
                "color": "green",
                "label": "wardrobe" 
            },
            "top_right": {
                "x": width - self.width - self.gap,
                "y": height - self.height - self.gap,
                "h": self.height,
                "w": self.width,
                "color": "green",
                "label": "wardrobe"  
            },
            "bottom_right": {
                "x": width - self.width - self.gap,
                "y":self.gap,
                "h": self.height,
                "w": self.width,
                "color": "green",
                "label": "wardrobe" 
            },

            "t_bottom_left": {
                "x": self.gap,
                "y": self.gap,
                "h": self.width,
                "w": self.height,
                "color": "green",
                "label": "wardrobe" 
            },
            "t_top_left": {
                "x": self.gap,
                "y": height - self.width - self.gap,
                "h": self.width,
                "w": self.height,
                "color": "green",
                "label": "wardrobe"  
            },
            "t_top_right": {
                "x": width - self.height - self.gap,
                "y": height - self.width - self.gap,
                "h": self.width,
                "w": self.height,
                "color": "green",
                "label": "wardrobe"
            },
            "t_bottom_right": {
                "x": width - self.height - self.gap,
                "y":self.gap,
                "h": self.width,
                "w": self.height,
                "color": "green",
                "label": "wardrobe"
            },
        }

    def place_wardrobe(self, room, wind_wall, door_wall, door_side ):
        if wind_wall == "east":
            if door_wall == "south" and door_side == "left":
                room.add_rectangle( **(self.get_position(room) ["t_bottom_right"]))

            elif (door_wall, door_side) in [("south","right"),("west","bottom")]:
                room.add_rectangle( **(self.get_position(room) ["top_right"]))

            elif door_wall == "north" and door_side == "left":
                room.add_rectangle( **(self.get_position(room) ["t_top_right"]))

            elif (door_wall, door_side) in [("north","right"),("west","top")]:
                room.add_rectangle( **(self.get_position(room) ["bottom_right"]))                   

        elif wind_wall == "west":
            if (door_wall,door_side) in [("south","left"),("east","bottom")]:
                room.add_rectangle( **(self.get_position(room) ["top_left"]))

            elif door_wall == "south" and door_side == "right":
                room.add_rectangle( **(self.get_position(room) ["t_bottom_left"]))

            elif (door_wall, door_side) in [("north", "left"), ("east", "top")]:
                room.add_rectangle( **(self.get_position(room) ["bottom_left"]))

            elif door_wall == "north" and door_side == "right":
                room.add_rectangle( **(self.get_position(room) ["t_top_left"]))

                
        elif wind_wall == "north":
            if (door_wall,door_side) in [("south","left"),("east","bottom")]:
                room.add_rectangle( **(self.get_position(room) ["t_bottom_right"]))

            elif (door_wall,door_side) in [("south","right"),("west","bottom")]:
                room.add_rectangle( **(self.get_position(room) ["t_bottom_left"]))

            elif door_wall == "west" and door_side == "top":
                room.add_rectangle( **(self.get_position(room) ["bottom_right"]))
 
            elif door_wall == "east" and door_side == "top":
                room.add_rectangle(**(self.get_position(room) ["bottom_left"]))         


        elif wind_wall == "south":
            if (door_wall,door_side) in [("north","left"), ("east","top")]:
                room.add_rectangle( **(self.get_position(room) ["t_top_right"]))

            elif (door_wall,door_side) in [("north","right"), ("west","top")]:
                room.add_rectangle( **(self.get_position(room) ["t_top_left"]))

            elif door_wall == "west" and door_side == "bottom":
                room.add_rectangle( **(self.get_position(room) ["top_right"]))                   
        
            elif door_wall == "east" and door_side == "bottom":
                room.add_rectangle(**(self.get_position(room) ["top_left"]))

        else:
            print("Error While plotting the wardrobe.")
                    