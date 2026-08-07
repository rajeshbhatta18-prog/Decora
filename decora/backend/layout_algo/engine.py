import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from bookshelf import Bookshelf
from bed import Bed
from table import Table
from chair import Chair
from wardrobe import Wardrobe

# height = float(input("Enter the length of the room (in ft): "))
# width = float(input("Enter the width of the room (in ft): "))
height = 12
width = 12

# WINDOWS INPUT
wind_wall2 = None
change_layout = None
no_wind_wall = int(input("Enter the number of walls with windows (1-2): "))
# no_wind_wall = 1
if no_wind_wall == 1:
    wind_wall = input("Enter the direction of window wall: ").strip().lower()
elif no_wind_wall == 2:
    wind_wall = input("Enter the direction of first window wall: ").strip().lower()
    wind_wall2 = input("Enter the direction of second window wall: ").strip().lower()
else:
    print("Invalid number of window walls. Please enter 1 or 2.")

# DOOR INPUT
door_wall = input("Enter the direction of door wall: ").strip().lower()
if door_wall == "east" or door_wall == "west":
    door_side = input("Which side is the door in: \n Top or Bottom? ").strip().lower()
else:
    door_side = input("Which side is the door in: \n Left or Right? ").strip().lower()

#DOOR WINDOW VALIDATION
if door_wall == wind_wall or door_wall == wind_wall2:
    print("Door and window cannot be on the same wall. Please choose different walls.")
    exit()

class RoomPlotter:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.fig, self.ax = plt.subplots(figsize=(8, 6))

        # Draw room boundary
        self.ax.add_patch(
            Rectangle(
                (0, 0),
                width,
                height,
                fill=False,
                linewidth=2,
                edgecolor="black"
            )
        )

    def draw_quadrants(self):
        global cx 
        global cy 
        cx = self.width / 2
        cy = self.height / 2

        global cent_val
        cent_val = [cx, cy]
        return cent_val

    def add_rectangle(self, x, y, w, h,
                      label="",
                      color="lightgray"):

        self.ax.add_patch(
            Rectangle(
                (x, y),
                w,
                h,
                facecolor=color,
                edgecolor="black"
            )
        )

        if label:
            self.ax.text(
                x + w / 2,
                y + h / 2,
                label,
                ha="center",
                va="center",
                fontsize=10
            )

    def add_line(self, x1, y1, x2, y2,
                 color="blue",
                 width=4):
        self.ax.plot(
            [x1, x2],
            [y1, y2],
            color=color,
            linewidth=width
        )

    def add_point(self, x, y,
                  label="",
                  color="red"):

        self.ax.scatter(x, y, color=color)

        if label:
            self.ax.text(x, y, label)

    def show(self):
        self.ax.set_xlim(-1, self.width + 1)
        self.ax.set_ylim(-1, self.height + 1)

        self.ax.set_aspect('equal')
        # self.ax.grid(True)

        plt.show()


# ===========================
# MAIN PROGRAM
# ===========================

room = RoomPlotter(width, height)

# Draw quadrants
cent_val = room.draw_quadrants()
wind_width = [5,4]
door_width = [3,7]

# WINDOW POSITIONING------------------------->

windows = {
    "east":{
        "start":(0, cy - wind_width[0]/2),
        "end":(0, cy + wind_width[0]/2),
        "center":(0, cy)
    },
    "west":{
        "start":(width, cy - wind_width[0]/2),
        "end":(width, cy + wind_width[0]/2),
        "center":(width, cy)
    },
    "north":{
        "start":(cx - wind_width[0]/2, height),
        "end":(cx + wind_width[0]/2, height),
        "center":(cx, height)
    },
    "south":{
        "start":(cx - wind_width[0]/2, 0),
        "end":(cx + wind_width[0]/2, 0),
        "center":(cx, 0)
    }
}
def plot_window():
    if wind_wall in windows:
        window = windows[wind_wall]
        window1 = windows[wind_wall2] if wind_wall2 else None
        room.add_line(
            window["start"][0], window["start"][1],
            window["end"][0], window["end"][1],
            color="cyan"
        )  
        if window1:
            room.add_line(
                window1["start"][0], window1["start"][1],
                window1["end"][0], window1["end"][1],
                color="cyan"
            )
    else:
        print("Choose the correct window direction.")

plot_window()

# DOOR POSITIONING------------------------->

door = {
    "east":{
        "top":{
                "start":(0, height),
                "end":(0, height - door_width[0])
        },
        "bottom":{
                "start":(0, 0),
                "end":(0, door_width[0])
        }
    },
    "west":{
        "top":{
                "start":(width, height),
                "end":(width, height - door_width[0])
        },       
        "bottom":{
                "start":(width, 0),
                "end":(width, door_width[0])
        }
    },
    "north":{
        "left":{
                "start":(0, height),
                "end":(door_width[0], height)
        },
        "right":{
                "start":(width, height),
                "end":(width - door_width[0], height)
        }
       
    },
    "south":{
        "left":{
                "start":(0, 0),
                "end":(door_width[0], 0)
        },
        "right":{
                "start":(width, 0),
                "end":(width - door_width[0], 0)
        }
    }
}

def plot_door():
    if door_wall in door:
        if door_side in door[door_wall]:
            door_pos = door[door_wall][door_side]
            room.add_line(
                door_pos["start"][0], door_pos["start"][1],
                door_pos["end"][0], door_pos["end"][1],
                color="red"
            )
        else:
            print("Choose the correct door side.")
    else:
        print("Choose the correct door wall.")

# furniture data

table = {
    "height" : 4,
    "width" : 2,
    "gap": 0.15
}

chair = {
    "height": 1.5,
    "width": 1.5,
    "gap": 0.4
}

bed = {
    "height": 6, 
    "width": 4,
    "gap": 0.1
} 

wardrobe = {
    "height": 4,
    "width": 2,
    "gap": 0.1,
}

bookshelf = {
    "height": 3,
    "width": 1,
    "wallgap": 0.1,
    "gap": 0.3
}

dresser = {
    "height": 4,
    "width": 2,
    "gap": 0.1,
    "offset": 2
}
def main():
    #DOOR AND WINDOW PLOTTING
    plot_window()
    plot_door()
    table1 = Table(table)
    table1.place_table(room, wind_wall, door_wall, door_side , bookshelf)

    # Chair placement
    chair1 = Chair(chair)
    chair1.place_chair(room, wind_wall, door_wall, door_side , table, bookshelf)

    # Bed Placement
    bed1 = Bed(bed)
    bed1.place_bed(room, wind_wall, door_wall, door_side , height , width)

    # Wardrobe placement
    wardrobe1 = Wardrobe(wardrobe)
    wardrobe1.place_wardrobe(room, wind_wall, door_wall, door_side)

    # Bookshelf placement
    bookshelf1 = Bookshelf(bookshelf)
    bookshelf1.place_bookshelf(room, wind_wall, door_wall, door_side )

    if height < 12 or width < 12:
        print("Room is too small for a dresser.")
    else:
        from dresser import Dresser
        # Bookshelf placement
        dresser1 = Dresser(dresser)
        dresser1.place_dresser(room, wind_wall, door_wall, door_side, wardrobe , bookshelf, no_wind_wall, change_layout) 

main() 
room.show()
if no_wind_wall == 2:
    change_layout = input("Do you want to change the layout? (yes/no): ").strip().lower()
def swap_layout():
    global room, wind_wall, wind_wall2
    wind_wall, wind_wall2 = wind_wall2, wind_wall
    room = RoomPlotter(width, height)
    main()
    room.show()

if no_wind_wall == 2 and change_layout == "yes":
    swap_layout()
  
     

