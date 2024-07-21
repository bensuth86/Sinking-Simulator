import math
from settings import *
from functions import *
from tkinter import *

def translate_points(points, i, j):

    for x in range(0,len(points), 2):
        points[x] += i

    for y in range(1,len(points), 2):
        points[y] += j


def scale_points(points, i, j):

    for x in range(0,len(points), 2):  # scale x coords by factor i
        points[x] *= i

    for y in range(1,len(points), 2):  # scale y coords by factor j
        points[y] *= j

    print(points)


# steel wedge (n plates)
def hull_setup():

    w_tot = 0
    h_tot = 0
    a_tot = 0

    for idx, width in enumerate(section_widths[1:]):  # setup dimensions of each hull section from bottom to top

        section_height = math.sqrt((l**2)-(width**2))
        section_heights.append(section_height)
        a_n = area_trapizium(w_tot, width, section_height)  # area between current plate section
        w_tot += width  # total cumulative width from centre
        h_tot += section_height  # total height from bottom of hull
        a_tot += a_n  # total cumulative area of current section and sections below
        width_cumulative.append(w_tot)
        height_cumulative.append(h_tot)
        area_cumulative.append(a_tot)

    n = len(section_widths)  # total sections (trapeziums) hull comprises of
    hull_mass = 2*n*p_stl*l*t  # combined mass of steel plates
    add_mass = 12500  # additional weight e.g. due to mass within hull
    total_mass = hull_mass + add_mass
    total_area = total_mass / p_water  # total area of water displaced
    return total_area


def hull_sbmdepth(total_area):

    # n = len(section_widths)  # total sections (trapeziums) hull comprises of
    # hull_mass = 2*n*p_stl*l*t  # combined mass of steel plates
    # add_mass = 12500  # additional weight e.g. due to mass within hull
    # total_mass = hull_mass + add_mass
    # total_area = total_mass / p_water  # total area of water displaced
    section_sbm = binary_searchii(total_area, area_cumulative)  # returns list index for area of sections completelty submerged
    a_rem = total_area - area_cumulative[section_sbm]
    r = section_heights[section_sbm+1] / width_cumulative[section_sbm+1]  # ratio of height/ width for section partially submerged
    h_rem = quadratic_formula(r, width_cumulative[section_sbm+1], -a_rem)
    sbmdepth = height_cumulative[section_sbm] + h_rem

    return sbmdepth  # distance between hull waterline and hull bottom


def sinking(d, H):  # d = hole diameter,  H = distance below waterline

    A = d * math.sqrt(2*g*H)   # in 2 dim- A = Volumetric flow rate (Area flow rate)
    sct_underwater = binary_searchii(A, area_cumulative)  # returns list index for sections underwater
    a_rem = A - area_cumulative[sct_underwater]
    r = section_heights[sct_underwater + 1] / width_cumulative[sct_underwater + 1]  # ratio of height/ width for section partially flooded
    h_rem = quadratic_formula(r, width_cumulative[sct_underwater+1], -a_rem)
    flood_depth = height_cumulative[sct_underwater] + h_rem

    return flood_depth  # water level within the hull


def hull_image():  # create list of coords for displaying tkinter

    rhs_points = []
    lhs_points = []

    for i in range(len(section_widths)):
        x = width_cumulative[i] * scalefactor
        y = height_cumulative[i] * -1 * scalefactor
        rhs_points.append(x)
        rhs_points.append(y)

    for i in range(0, len(rhs_points), 2):
        x = rhs_points[(i+2)*-1] * -1
        y = rhs_points[(i*-1)-1]
        lhs_points.append(x)
        lhs_points.append(y)

    points = lhs_points + rhs_points

    return points


def video_setup(canvas, sbmdepth):

    # tk = Tk()
    # frame = Frame(tk)
    # frame.pack()

    points = hull_image()
    translate_points(points, screen_width/2, screen_height/2)  # centre hull image
    translate_points(points, 1, sbmdepth*scalefactor)
    # canvas = Canvas(frame, bg="black", width=screen_width, height=screen_height)
    # canvas.pack()
    waterline = canvas.create_line(0, screen_height/2, screen_width, screen_height/2, fill = "blue")
    ship = canvas.create_polygon(points, outline="white")

    # while sbmdepth < height_cumulative[-1]:
    #     # flooddepth = sinking(0.1, 1)
    #     canvas.move(ship, 0, 5)
    #     frame.after(250, canvas.update())

    # frame.mainloop()


def main():
    # intialise tkinter
    tk = Tk()
    frame = Frame(tk)
    frame.pack()
    canvas = Canvas(frame, bg="black", width=screen_width, height=screen_height)
    canvas.pack()

    hull_area = hull_setup()
    sbmdepth = hull_sbmdepth(hull_area)

    video_setup(canvas, sbmdepth)

    while sbmdepth < height_cumulative[-1]:

        flooddepth = sinking(0.1, 1)

        # canvas.move(ship, 0, 5)
        # frame.after(250, canvas.update())

    frame.mainloop()

if __name__ == "__main__":
    main()
