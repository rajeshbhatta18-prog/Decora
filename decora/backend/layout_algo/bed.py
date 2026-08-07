
bed_gap = 0.1
class Bed:
    def __init__(self, bed):
          self.height = bed["height"]
          self.width = bed["width"]
          self.gap = bed["gap"]

    def place_bed(self, room, wind_wall, door_wall, door_side, height, width ):
        if wind_wall == "east":
            if door_wall == "south" and door_side == "left":
                room.add_rectangle(
                    x =  width - self.width - bed_gap,
                    y = height - self.height -  bed_gap,
                    h = self.height,
                    w = self.width,
                    label = "Bed" ,
                    color = "lightgray"
                )
            elif door_wall == "north" and door_side == "left":
                    room.add_rectangle(
                    x =  width - self.width - bed_gap,
                    y = bed_gap,
                    h = self.height,
                    w = self.width,
                    label = "Bed" ,
                    color = "lightgray"
                )
            else:  
                room.add_rectangle(
                    x = bed_gap,
                    y = bed_gap,
                    h = self.width,
                    w = self.height,
                    label = "Bed" ,
                    color = "lightgray"
                )

        elif wind_wall == "west":
            if door_wall == "north" and door_side == "right":
                room.add_rectangle(
                        x = bed_gap,
                        y = bed_gap,
                        h = self.height,
                        w = self.width,
                        label = "Bed" ,
                        color = "lightgray"        
                )
            elif door_wall == "south" and door_side == "right":
                room.add_rectangle(
                        x = bed_gap,
                        y = height - self.height - bed_gap,
                        h = self.height,
                        w = self.width,
                        label = "Bed" ,
                        color = "lightgray"        
                )
            else:
                room.add_rectangle(
                    x = width - bed_gap - self.height,
                    y = bed_gap,
                    h = self.width,
                    w = self.height,
                    label = "Bed" ,
                    color = "lightgray"        
                )

        elif wind_wall == "north":
            if door_wall == "east" and door_side == "top":
                room.add_rectangle(
                        x = width - bed_gap - self.height,
                        y = bed_gap,
                        h = self.width,
                        w = self.height,
                        label = "Bed" ,
                        color = "lightgray"        
                )
            elif door_wall == "west" and door_side == "top":
                room.add_rectangle(
                        x = bed_gap,
                        y = bed_gap,
                        h = self.width,
                        w = self.height,
                        label = "Bed" ,
                        color = "lightgray"        
                )
            else:
                room.add_rectangle(
                    x = width - bed_gap - self.width,
                    y = height - self.height,
                    h = self.height,
                    w = self.width,
                    label = "Bed" ,
                    color = "lightgray"        
                )

        elif wind_wall == "south":
            if door_wall == "east" and door_side == "bottom":
                room.add_rectangle(
                    x = width - self.height - bed_gap,
                    y = height - self.width - bed_gap,
                    h = self.width,
                    w = self.height,
                    label = "Bed" ,
                    color = "lightgray"        
                )
            elif door_wall == "west" and door_side == "bottom":
                    room.add_rectangle(
                        x = bed_gap,
                        y = height - self.width - bed_gap,
                        h = self.width,
                        w = self.height,
                        label = "Bed" ,
                        color = "lightgray"        
                    )
            else:
                room.add_rectangle(
                    x = bed_gap,
                    y = bed_gap,
                    h = self.height,
                    w = self.width,
                    label = "Bed",
                    color = "lightgray"        
                )