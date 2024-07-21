import math
from settings import *
from functions import *
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib import style


def hull_setup():

    w_tot = 0  # # total cumulative width from centre
    h_tot = 0  # total height from bottom of hull
    a_tot = 0  # total hull area (2-Dim)

    for idx, width in enumerate(section_widths[1:]):  # setup dimensions of each hull section from bottom to top

        section_height = math.sqrt((l**2)-(width**2))  # pythag
        section_heights.append(section_height)
        a_n = area_trapizium(w_tot, width, section_height)  # area between current plate section
        w_tot += width
        h_tot += section_height
        a_tot += a_n  # total cumulative area of current section and sections below
        width_cumulative.append(w_tot)
        height_cumulative.append(h_tot)
        AREA_CUMULATIVE.append(a_tot)

    n = len(section_widths)  # total sections (trapeziums) hull comprises of
    hull_mass = 2*n*p_stl*l*t  # combined mass of steel plates
    add_mass = 17500  # additional weight e.g. due to mass within hull
    total_mass = hull_mass + add_mass

    return total_mass


def hull_sbmdepth(total_area):

    section_sbm = binary_searchii(total_area, AREA_CUMULATIVE)  # returns list index for area of sections completelty submerged
    a_rem = total_area - AREA_CUMULATIVE[section_sbm]  # a_rem - area of section below the waterline (all sections below completely submerged)
    r = section_heights[section_sbm+1] / section_widths[section_sbm+1]  # ratio of height/ width for section partially submerged
    h_rem = quadratic_formula(1/r, 2*width_cumulative[section_sbm], -a_rem)
    sbmdepth = height_cumulative[section_sbm] + h_rem

    return sbmdepth  # distance between hull waterline and hull bottom


def floodDepth(A_tot):  # A_tot - total area of water within hull.  Function returns corresponding flood level

    sct_underwater = binary_searchii(A_tot, AREA_CUMULATIVE)  # returns list index for sections flooded
    a_rem = A_tot - AREA_CUMULATIVE[sct_underwater]  # area of section flooded
    r = section_heights[sct_underwater + 1] / section_widths[sct_underwater + 1]  # ratio of height/ width for section partially flooded
    h_rem = quadratic_formula(1/r, 2*width_cumulative[sct_underwater], -a_rem)
    flood_depth = height_cumulative[sct_underwater] + h_rem

    return flood_depth  # water level within the hull


def hull_image():  # create list of coords for displaying tkinter

    rhs_points = []  # right of centre line
    lhs_points = []  # left  of centre line

    for i in range(len(section_widths)):  # create points for right hand side
        x = width_cumulative[i] * scalefactor
        y = height_cumulative[i] * -1 * scalefactor
        rhs_points.append(x)
        rhs_points.append(y)

    for i in range(0, len(rhs_points), 2):  # use rhs points to generate left hand side
        x = rhs_points[(i+2)*-1] * -1
        y = rhs_points[(i*-1)-1]
        lhs_points.append(x)
        lhs_points.append(y)

    points = lhs_points + rhs_points

    return points


def video_setup(canvas, sbmdepth):  # setup up hull image and position relative to waterline

    sbmdepth = sbmdepth * scalefactor
    points = hull_image()
    translate_points(points, screen_width/2, screen_height/2)  # centre hull image
    translate_points(points, 1, sbmdepth)  # "float" ship

    waterline = canvas.create_line(0, screen_height/2, screen_width, screen_height/2, fill="blue")
    ship = canvas.create_polygon(points, outline="white")
    # floodline = canvas.create_line(screen_width / 4, (screen_height/2)+sbmdepth, screen_width * (3 / 4), (screen_height/2)+sbmdepth, fill="darkblue")

    return ship


def video_update(ship, sbmdepth, new_sbmdepth, flood_depth):  # animation of hull sinking and floodlevel rising

    dist_sunk = new_sbmdepth - sbmdepth
    dist_sunk *= scalefactor
    canvas.move(ship, 0, dist_sunk)  # sink ship by dist_sunk

    flood_level = new_sbmdepth - flood_depth
    flood_level *= scalefactor
    floodline = canvas.create_line(screen_width / 4, (screen_height / 2) + flood_level, screen_width * (3 / 4), (screen_height / 2) + flood_level, fill="darkblue")  # redraw floodline every turn

    frame.after(250, canvas.update())
    canvas.delete(floodline)


def plot_variable(c, sbmdepth, flood_depth):  # matplotlib live graph updates every turn

    x_time.append(c)
    y_sbmdepth.append(sbmdepth)
    y_floodepth.append(flood_depth)

    plt.plot(x_time, y_sbmdepth, 'g', label="Submerge_depth")
    plt.plot(x_time, y_floodepth, 'r', label="Flood depth")
    style.use('fivethirtyeight')

    plt.pause(0.05)


def main():

    ship_mass = hull_setup()
    sbmdepth = hull_sbmdepth(ship_mass / p_water)  # depth of ship bottom below waterline

    ship = video_setup(canvas, sbmdepth)  # ship- tkinter polygon
    hole_diameter = 0.01  # (m)
    hole_depth = 0.8  # distance below waterline (m)
    c = 0  # count nos of turns
    A_tot = 0  # total area of water within hull (m^2)

    while ship_mass < (AREA_CUMULATIVE[-1] * p_water):  # ship mass below point it can no longer float

        new_sbmdepth = hull_sbmdepth(ship_mass / p_water)  # calculate new submerge depth due to water taken on previous turn
        A = hole_diameter * math.sqrt(2 * g * hole_depth)  # in 2 dim- A = Area flow rate for current submerge depth
        A_tot += A
        flood_depth = floodDepth(A_tot)  # Depth of internal flooding (relative to ship bottom)
        ship_mass += (A * p_water)  # += additional weight due to flooding
        hole_depth += new_sbmdepth-sbmdepth  # add distance sunk for current turn

        video_update(ship, sbmdepth, new_sbmdepth, flood_depth)
        plot_variable(c, sbmdepth, flood_depth)

        sbmdepth = new_sbmdepth  # store for next turn
        c += 1  # each turn equivalent to 1 second

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
    plt.xlabel('Time (s)')
    plt.ylabel('Depth (m)')
    plt.plot(x_time, y_sbmdepth, 'g', label="Submerge_depth")
    plt.plot(x_time, y_floodepth, 'r', label="Flood depth")
    plt.legend(loc="lower right")

    main()
