class Dresser:
    def __init__(self, dresser):
        self.height = dresser["height"]
        self.width = dresser["width"]
        self.gap = dresser["gap"]
        self.offset = dresser["offset"]

    def get_position(self, room, wardrobe, bookshelf):
        height = room.height
        width = room.width
        return {
            "bottom_left": {
                "x": self.gap,
                "y": wardrobe["gap"] + wardrobe["height"] + self.gap,
                "h": self.height,
                "w": self.width,
                "color": "blue",
                "label": "dresser" 
            },
            "top_left": {
                "x": self.gap,
                "y": height - self.height - self.gap -wardrobe["height"] - wardrobe["gap"],
                "h": self.height,
                "w": self.width,
                "color": "blue",
                "label": "dresser" 
            },
            "top_right": {
                "x": width - self.width - self.gap,
                "y": height - self.height - self.gap - wardrobe["height"] - wardrobe["gap"],
                "h": self.height,
                "w": self.width,
                "color": "blue",
                "label": "dresser"  
            },
            "bottom_right": {
                "x": width - self.width - self.gap,
                "y": wardrobe["gap"] + wardrobe["height"] + self.gap,
                "h": self.height,
                "w": self.width,
                "color": "blue",
                "label": "dresser" 
            },

            "t_bottom_left": {
                "x": wardrobe["gap"] + wardrobe["height"] + self.gap,
                "y": self.gap,
                "h": self.width,
                "w": self.height,
                "color": "blue",
                "label": "dresser" 
            },
            "t_top_left": {
                "x": wardrobe["gap"] + wardrobe["height"] + self.gap,
                "y": height - self.width - self.gap,
                "h": self.width,
                "w": self.height,
                "color": "blue",
                "label": "dresser"  
            },
            "t_top_right": {
                "x": width - self.height - self.gap - wardrobe['gap'] - wardrobe["height"],
                "y": height - self.gap - self.width,
                "h": self.width,
                "w": self.height,
                "color": "blue",
                "label": "dresser"
            },
            "t_bottom_right": {
                "x": width - self.height - self.gap - wardrobe['gap'] - wardrobe["height"],
                "y":self.gap,
                "h": self.width,
                "w": self.height,
                "color": "blue",
                "label": "dresser"
            },
        } 

    def place_dresser(self, room, wind_wall, door_wall, door_side, wardrobe , bookshelf, no_wind_wall, change_layout):
                    
        if wind_wall == "east":  
            if door_wall == "south" and door_side == "left":
                room.add_rectangle( **(self.get_position(room, wardrobe, bookshelf) ["t_bottom_right"]))                
                
            elif (door_wall, door_side) in [("south","right"),("west","bottom")]:
                    room.add_rectangle( **(self.get_position(room, wardrobe, bookshelf) ["top_right"]))

            elif door_wall == "north" and door_side == "left":
                room.add_rectangle(**(self.get_position(room, wardrobe, bookshelf)["t_top_right"]))

            elif (door_wall == "north" and  door_side == "right"):
                if no_wind_wall == 2:
                    room.add_rectangle( **(self.get_position(room, wardrobe, bookshelf) ["t_top_right"]))
                else:
                    room.add_rectangle( **(self.get_position(room, wardrobe, bookshelf) ["bottom_right"]))  

            elif (door_wall == "west" and door_side == "top"):
                room.add_rectangle( **(self.get_position(room, wardrobe, bookshelf) ["bottom_right"]))    

        elif wind_wall == "west":
            if (door_wall,door_side) in [("south","left"),("east","bottom")]:   
                room.add_rectangle( **(self.get_position(room , wardrobe, bookshelf) ["top_left"]))

            elif door_wall == "south" and door_side == "right":
                room.add_rectangle( **(self.get_position(room, wardrobe, bookshelf) ["t_bottom_left"]))

            elif (door_wall, door_side) in [("north", "left")]:
                if no_wind_wall == 2:
                    room.add_rectangle( **(self.get_position(room, wardrobe, bookshelf) ["t_top_right"]))
                else:
                    room.add_rectangle( **(self.get_position(room, wardrobe, bookshelf) ["bottom_left"]))

            elif (door_wall, door_side) in [("east", "top")]:
                    room.add_rectangle( **(self.get_position(room, wardrobe, bookshelf) ["bottom_left"]))

            elif door_wall == "north" and door_side == "right":
                room.add_rectangle( **(self.get_position(room, wardrobe, bookshelf) ["t_top_left"]))

                
        elif wind_wall == "north":
            if (door_wall,door_side) in [("south","left")]:
                room.add_rectangle( **(self.get_position(room, wardrobe, bookshelf) ["t_bottom_right"]))

            elif (door_wall,door_side) in [("east","bottom")]:
                if no_wind_wall == 2:
                    room.add_rectangle( **(self.get_position(room, wardrobe, bookshelf) ["bottom_left"]))
                else:
                    room.add_rectangle( **(self.get_position(room, wardrobe, bookshelf) ["t_bottom_right"]))

            elif (door_wall,door_side) in [("south","right")]:
                room.add_rectangle( **(self.get_position(room, wardrobe, bookshelf) ["t_bottom_left"]))

            elif (door_wall,door_side) in [("west","bottom")]:    
                    room.add_rectangle( **(self.get_position(room, wardrobe, bookshelf) ["t_bottom_left"]))

            elif door_wall == "west" and door_side == "top":
                room.add_rectangle( **(self.get_position(room, wardrobe, bookshelf) ["bottom_right"]))
 
            elif door_wall == "east" and door_side == "top":
                room.add_rectangle(**(self.get_position(room, wardrobe, bookshelf) ["bottom_left"]))         


        elif wind_wall == "south":
            if (door_wall,door_side) in [("north","left")]:
                room.add_rectangle( **(self.get_position(room, wardrobe, bookshelf) ["t_top_right"]))

            elif (door_wall,door_side) in [("east","top")]:
                if no_wind_wall == 2:
                    room.add_rectangle( **(self.get_position(room, wardrobe, bookshelf) ["top_right"]))
                else:
                    room.add_rectangle( **(self.get_position(room, wardrobe, bookshelf) ["t_top_right"]))          
            
            elif (door_wall,door_side) in [("north","right")]:
                room.add_rectangle( **(self.get_position(room, wardrobe, bookshelf) ["t_top_left"]))

            elif (door_wall,door_side) in [("west","top")]:
                if no_wind_wall == 2:
                    room.add_rectangle( **(self.get_position(room, wardrobe, bookshelf) ["top_right"]))
                else:
                    room.add_rectangle( **(self.get_position(room, wardrobe, bookshelf) ["t_top_left"]))

            elif door_wall == "west" and door_side == "bottom":
                room.add_rectangle( **(self.get_position(room, wardrobe, bookshelf) ["top_right"]))                   
        
            elif door_wall == "east" and door_side == "bottom":
                room.add_rectangle(**(self.get_position(room, wardrobe, bookshelf) ["top_left"]))

        else:
            print("Error While plotting the dresser.")

