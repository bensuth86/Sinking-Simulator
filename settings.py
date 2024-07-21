screen_width = 1400  # pixels
screen_height = 700
scalefactor = 50  # for tkinter display

g = 9.81  # accln due to gravity

# density
p_stl = 8000  # density of steel (KG/m^3)
p_water = 1000 # density of water
p_air = 1  # neglible

#              length (m), thcknss (m)
steel_plate = (1, 0.02)  # each hull section comprised of 2 symetric plates
l = steel_plate[0]
t = steel_plate[1]

section_widths = [0, 0.9, 0.9, 0.8, 0.8, 0.5, 0.4, 0.4, 0.2, 0.2, 0.1, 0.1]  # effective width of each section in meters
# section_widths = [0, 0.95, 0.95, 0.9, 0.9, 0.8, 0.8, 0.7, 0.7, 0.55, 0.55, 0.4, 0.4, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1]
# section_widths = [0.99, 0.99, 0.99, 0.99, 0.01, 0.01, 0.01, 0.01]
section_heights = [0]

width_cumulative = [0]  # total width of hull at each plate section
height_cumulative = [0]  # total height of hull at each plate section
AREA_CUMULATIVE = [0]  # total hull area below each plate section

# matplotlib axis
x_time = []
y_sbmdepth = []
y_floodepth = []


# steel box (3 plates min)
def steel_box():

    w = 8  # stl plates
    h = 2

    box_area = w * h

    a = (p_stl*t)*(1/h)
    b = (p_stl*t)*(2/w)
    c = p_air
    # p_tot = (p_stl*t*((1/h)+(2/w))) + p_air

    p_tot = a+b+c

    h_min = (p_stl*w*t)/((p_water*w)-(2*p_stl*t))  # min height of box to float for given width

    d = p_stl*t*(w+(2*h))
    e = (p_water*w)
    sbm_depth = d/e  # actual submerged depth
    print(p_tot)

# steel wedge (2 plates)
def steel_wedge_ii():

    ext = 1*l
    ang = math.pi/6  # plate_angle
    w = math.sqrt(3)/2
    h = 0.5

    a = 4*p_stl*t
    b = ext*math.sin(2*ang)

    p_tot = a/b

    l_min = (4*p_stl*t) / (p_water*math.sin(2*ang))

    sbm_depth = math.sqrt(2*p_stl*ext*t*(math.tan(ang)) / p_water)
    sbm_depthii = math.sqrt((2*p_stl*ext*t*h)/(p_water*w))

    print(p_tot)
