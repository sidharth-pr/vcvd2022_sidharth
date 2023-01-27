__doc__ = "file that has all main methods,functionalites of the program"


# import required libraries
import argparse
import cmath
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as mpl
from os import system, name
from time import sleep
import math
import string


# defining some constants
g = 9.81  # gravitational constant


# method to clear the output screen (code idea taken from https://www.geeksforgeeks.org/clear-screen-python/)
def clear():
    # works on Windows
    if name == 'nt':
        system('cls')

    # works on Linux or macOS
    else:
        system('clear')


# method that calculates braking distance
def braking_distance(v0, mu):
    return (pow(v0, 2)) / (2 * g * mu)


# method that calculates braking time
def braking_time(v0, a, s):
    a = 0.5 * a
    b = v0
    c = -s
    d = pow(b, 2) - (4 * a * c)
    t = (-b - cmath.sqrt(d)) / (2 * a)
    return abs(t)


# method that calculates RULE OF THUMB braking distance
def rot_braking_distance(v0):
    return pow((v0/10), 2)


# method that calculates the acceleration of the vehicle
def calc_acceleration(mu):
    return -mu * g


# method to plot the final graph
def plot_graph(v0, mu):
    # some calculations prior to graphing
    s = braking_distance(v0, mu)
    s_rot = rot_braking_distance(v0)
    a = calc_acceleration(mu)
    t = braking_time(v0, a, s)
    t_rot = braking_time(v0, a, s_rot)

    # generating matrix axes to plot the graph across
    time_axis = np.arange(0, t, t/2000)
    time_axis_rot = np.arange(0, t_rot, t_rot/2000)
    vel_axis = v0 + (a * time_axis)
    vel_axis_rot = v0 + (a * time_axis_rot)
    dist_axis = (v0 * time_axis) + (0.5 * a * np.square(time_axis))
    dist_axis_rot = (v0 * time_axis_rot) + (0.5 * a * np.square(time_axis_rot))

    # plotting the graphs
    fig, ax = mpl.subplots(2)
    fig.suptitle("BRAKING SIMULATION")
    fig.set_size_inches(11.7, 16.5)

    ax[0].plot(time_axis, vel_axis, 'tab:red')
    ax[0].set_xlabel("Time (s)")
    ax[0].set_ylabel("Velocity (m/s)")
    ax[0].grid()

    ax[1].plot(time_axis, dist_axis, 'tab:green')
    ax[1].set_xlabel("Time (s)")
    ax[1].set_ylabel("Distance (m)")
    ax[1].grid()

    # exporting to a pdf file in the same directory
    mpl.savefig("   comparison_graph.pdf", format="pdf")

    # displaying the graphs
    mpl.show()


# user input
def GUI():
    # coefficient of friction dataframes
    # mu_s = pd.DataFrame([[0.65, 0.4, 0], [0.2, 0.1, 0], [0, 0, 0.1], [0, 0, 0], [0, 0, 0]], index=[
    #     'concrete', 'ice', 'water', 'gravel', 'sand'], columns=['dry', 'wet', 'aquaplaning'])
    # unneccesary?

    mu_d = pd.DataFrame([[0.5, 0.35, 0], [0.2, 0.1, 0], [0, 0, 0.05], [0.35, 0, 0], [0.3, 0, 0]], index=[
        'concrete', 'ice', 'water', 'gravel', 'sand'], columns=['dry', 'wet', 'aquaplaning'])

    # print(mu_d)
    # dictionaries for user inputs
    # road type
    ui_1 = {
        1: 'concrete',
        2: 'ice',
        3: 'water',
        4: 'gravel',
        5: 'sand'
    }

    # road condition
    ui_2 = {
        1: 'dry',
        2: 'wet',
        3: 'aquaplaning'
    }

    # start taking user inputs
    clear()
    v0 = float(input("What is your desired vehicle velocity in [km/h] "))
    v0 = v0 / 3.6   # conversion to meter per second
    print("\nThe vehicle velocity is ", v0, " m/s")
    input("\n\nPress Enter to continue...\n")
    clear()

    row_int = int(input(
        "\033[4mROAD TYPES\033[0m\n\n1. Concrete\n2. Ice\n3. Water\n4. Gravel\n5. Sand\n\nWhat type of road would you like "))
    row = ui_1[row_int]
    print("\nYour chosen road type is: ", row)
    clear()

    # condition for water roads
    if row_int == 3:
        col_int = 3
        col = ui_2[col_int]
        print("\nThe road condition is: ", col)
        input("\n\nPress Enter to continue...\n")
        clear()

    # condition for gravel and sand roads
    elif row_int == 4 or row_int == 5:
        col_int = 1
        col = ui_2[col_int]
        print("\nThe road condition is: ", col)
        input("\n\nPress Enter to continue...\n")
        clear()

    else:
        col_int = int(input(
            "\033[4mROAD CONDITIONS\033[0m\n\n1. Dry\n2. Wet\n3. Aquaplaning\n\nWhat road conditions would you like "))
        col = ui_2[col_int]
        print("\nYour chosen road condition is: ", col)
        input("\n\nPress Enter to continue...\n")
        clear()

    # looks up the value of coeff of friction from the dataframe based on x,y coordinates
    mu = mu_d.loc[row][col]

    # final print of chosen values and confirmation to proceed with graph printing
    print("\033[4mCHOSEN VALUES FOR SIMULATION\033[0m\n\n")
    print("\nRoad Type: ", row)
    print("\nRoad Condition is: ", col)
    print("\nCoefficient of Friction: ", mu)
    if input("\n\nStart the simulation? (y/n) ") == 'n':
        GUI()
    else:
        plot_graph(v0, mu)


# main function call, program execution starts here
GUI()
