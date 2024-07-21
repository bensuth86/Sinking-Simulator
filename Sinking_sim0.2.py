import math
from settings import *
from functions import *
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib import style


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
    # total_area = total_mass / p_water  # total area of water displaced
    return total_mass


def hull_sbmdepth(total_area):

    section_sbm = binary_searchii(total_area, area_cumulative)  # returns list index for area of sections completelty submerged
    a_rem = total_area - area_cumulative[section_sbm]
    r = section_heights[section_sbm+1] / section_widths[section_sbm+1]  # ratio of height/ width for section partially submerged
    h_rem = quadratic_formula(1/r, 2*width_cumulative[section_sbm], -a_rem)
    sbmdepth = height_cumulative[section_sbm] + h_rem

    return sbmdepth  # distance between hull waterline and hull bottom


def sinking(d, H):  # d = hole diameter,  H = distance below waterline

    A = d * math.sqrt(2*g*H)   # in 2 dim- A = Volumetric flow rate (Area flow rate)
    sct_underwater = binary_searchii(A, area_cumulative)  # returns list index for sections flooded
    a_rem = A - area_cumulative[sct_underwater]
    r = section_heights[sct_underwater + 1] / section_widths[sct_underwater + 1]  # ratio of height/ width for section partially flooded
    h_rem = quadratic_formula(1/r, 2*width_cumulative[sct_underwater], -a_rem)
    flood_depth = height_cumulative[sct_underwater] + h_rem  # water level within the hull

    return A


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

    sbmdepth = sbmdepth * scalefactor
    points = hull_image()
    translate_points(points, screen_width/2, screen_height/2)  # centre hull image
    translate_points(points, 1, sbmdepth)  # "float" ship

    waterline = canvas.create_line(0, screen_height/2, screen_width, screen_height/2, fill="blue")
    ship = canvas.create_polygon(points, outline="white")
    floodlevel = canvas.create_line(screen_width / 4, (screen_height/2)+sbmdepth, screen_width * (3 / 4), (screen_height/2)+sbmdepth, fill="darkblue")

    return ship


def video_update(ship, dist_sunk):

    dist_sunk *= scalefactor
    canvas.move(ship, 0, dist_sunk)
    frame.after(50, canvas.update())


def plot_sbmdepth(c, sbmdepth):

    x_time.append(c)
    y_sbmdepth.append(sbmdepth)

    plt.plot(x_time, y_sbmdepth, 'g', label="Submerge_depth")
    style.use('fivethirtyeight')

    plt.pause(0.05)


def main():
    # intialise tkinter

    ship_mass = hull_setup()
    sbmdepth = hull_sbmdepth(ship_mass / p_water)  # depth of ship bottom below waterline

    ship = video_setup(canvas, sbmdepth)  # ship- tkinter polygon
    hole_diameter = 0.02
    hole_depth = 0.8  # distance below waterline
    c = 0
    A = 0

    while ship_mass + (A * p_water) < (area_cumulative[-1] * p_water):

        A = sinking(hole_diameter, hole_depth)  # area of water per turn
        ship_mass += (A * p_water)  # += additional weight due to flooding

        new_sbmdepth = hull_sbmdepth(ship_mass / p_water)
        dist_sunk = (new_sbmdepth-sbmdepth)
        hole_depth += dist_sunk
        video_update(ship, dist_sunk)
        plot_sbmdepth(c, sbmdepth)

        sbmdepth = new_sbmdepth
        c += 1

    print("Sunk within %s seconds" % c)

    frame.mainloop()

if __name__ == "__main__":

    # tkinter setup
    tk = Tk()
    frame = Frame(tk)
    frame.pack()
    canvas = Canvas(frame, bg="black", width=screen_width, height=screen_height)
    canvas.pack()

    # matplotlib setup
    fig = plt.figure(1)
    plt.xlabel('Time')
    plt.ylabel('Submerge Depth')


    main()
