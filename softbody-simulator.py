# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 21:12:37 2021

@author: junob
"""
import math as m
from vectortools import *
from mass_spring_model import *
import pygame as pg

width = 1000
height = 800

screen = pg.display.set_mode((width, height))

render = Render(screen, width, height)

clock = pg.time.Clock() 

red = pg.Color('red')
green = pg.Color('green')
blue = pg.Color('blue')
white = pg.Color('white')

#Wall(width, height, theta, pos, color)
wall1 = Wall(1000, 50, 0, Vector(-500, -400), blue)
wall2 = Wall(50, 800, 0, Vector(-500, -400), blue)
wall3 = Wall(50, 800, 0, Vector(450,-400), blue)
wall4 = Wall(1000, 50, 0, Vector(-500, 350), blue)
wall5 = Wall(100, 50, m.pi/4, Vector(-300, 0), blue)

#Element(name, mass, radius, k, c, distance, color)
e1 = Element('steel', 5, 5, 90, 1, 25, red)
e2 = Element('toy model', 10, 10, 10, 2, 50, green)
e3 = Element('toy model', 10, 10, 0.1, 2, 100, blue)
cube1 = Cube(e1, 10, 3, m.pi/6, Vector(-250, 200))
cube2 = Cube(e2, 3, 3, 0, Vector(200, -200))
cube3 = Cube(e3, 1, 1, 0, Vector(200, 200))
cube4 = Cube(e1, 5, 5, 0, Vector(0, 0))
# cube1.atoms[0][0].pos += Vector(-10, -10)
# cube1.atoms[0][cube1.width-1].pos += Vector(-10, 10)
# cube1.atoms[cube1.height-1][0].pos += Vector(10, -10)
# cube1.atoms[cube1.height-1][cube1.width-1].pos += Vector(10, 10)
# cube2.atoms[0][0].pos += Vector(-20, -20)
# cube2.atoms[cube2.height-1][cube2.width-1].pos += Vector(+20, +20)

walls = [wall1, wall2, wall3, wall4, wall5]
cubes = [cube1, cube2, cube3]

                    
gravity = Vector(0, -1.0)
simulator = Simulator(0.01, walls, cubes, gravity, render)

import sys
import random as r

count = 0
while True:
    simulator.simulation()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
            
        elif event.type == pg.MOUSEBUTTONDOWN:
            x, y = event.pos
            new_e = Element('toy model', 10, 10, 10, 20*0.1, 50, pg.Color(r.randint(0,255), r.randint(0,255), r.randint(0,255)))
            new_cube = Cube(new_e, 3, 3, 0, Vector(x-width/2, -y+height/2))
            cubes.append(new_cube)
            for h in range(new_cube.height):
                for w in range(new_cube.width):
                    simulator.other_atoms.append(new_cube.atoms[h][w])
                           
    clock.tick(100)
    pg.display.update()
    
    # count += 1
    # img = 'images/elastic_cube_demo_2/%08d.png' % (count)
    # pg.image.save(screen, img)
