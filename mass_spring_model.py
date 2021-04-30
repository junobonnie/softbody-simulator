# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 01:25:59 2021

@author: junob
"""

import math as m
from vectortools import *
from atom import *
        
class Element(Element):
    def __init__(self, name, mass, radius, k, c, distance, color):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.k = k
        self.c = c
        self.distance = distance
        self.color = color
    
    def __str__(self):
        return ('Element(name = ' + name + ', mass = ' + str(self.mass) + 
                ', radius = ' + str(self.radius) + ', k = ' + str(self.k) + 
                ', c = ' + str(self.c) + ', distance = ' + str(self.distance) + 
                ', color = ' + str(self.color) + ')')
        
class Cube:
    def __init__(self, element, width, height, theta, pos, vel = Vector(0, 0)):
        self.element = element
        self.width = width
        self.height = height
        self.pos = pos
        self.vel = vel
        
        self.atoms = [[None for w in range(width)] for h in range(height)]
        distance = self.element.distance
        for h in range(height):
            for w in range(width):
                position = self.pos + SO2(theta).dot(Vector(distance*w, distance*h))
                self.atoms[h][w] = Atom(element = self.element, pos = position, vel = self.vel)
        
    def __str__(self):
        return ('Cube(element = ' + self.element.name + 
                ', width = ' + str(self.width) + ', height = ' + str(self.height) + 
                ', theta = ' + str(self.theta) + 
                ', pos(' + str(self.pos.x) + ', ' + str(self.pos.y) + ')' + 
                ', vel(' + str(self.vel.x) + ', ' + str(self.vel.y) + '))')
            
    def force(self, w, h):
        result = Vector(0, 0)
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if 0 <= h+i and h+i < self.height and 0 <= w+j and w+j < self.width and not(i == 0 and j == 0):
                    if i*j == 0:
                        factor = 1
                    else:
                        factor = m.sqrt(2)
                    distance_vector = self.atoms[h][w].pos - self.atoms[h+i][w+j].pos
                    delta_vel_vector = self.atoms[h][w].vel - self.atoms[h+i][w+j].vel
                    spring_force =  -1*self.element.k*(distance_vector - factor*self.element.distance*distance_vector/abs(distance_vector))
                    damping_force = -1*self.element.c*(distance_vector.dot(delta_vel_vector))*distance_vector/distance_vector.dot(distance_vector)
                    result = result + spring_force + damping_force
        return result
    
class Simulator:
    def __init__(self, dt, walls, cubes, gravity, render):
        self.dt = dt
        self. walls = walls
        self.cubes = cubes
        self.gravity = gravity
        self.other_atoms = []
        for cube in cubes:
            for h in range(cube.height):
                for w in range(cube.width):
                    self.other_atoms.append(cube.atoms[h][w])
        self.render = render
        
    def simulation(self):
        self.render.screen.fill(pg.Color('white'))
        for wall in self.walls:
            self.render.wall(wall)
            for other_atom in self.other_atoms:
                wall.collision(other_atom)
              
        x_ = []
        v_ = []
        for cube in self.cubes:
            for h in range(cube.height):
                for w in range(cube.width):
                    atom = cube.atoms[h][w]
                    
                    for other_atom in self.other_atoms:
                        atom.collision(other_atom)
                    new_v = atom.vel + self.gravity*self.dt + cube.force(w, h)/atom.element.mass*self.dt
                    v_.append(new_v) # - 0.1*atom.vel*dt
                    x_.append(atom.pos + new_v*self.dt)
                    self.render.atom(atom)
                    
        count = 0
        for cube in self.cubes:
            for h in range(cube.height):
                for w in range(cube.width):
                    atom = cube.atoms[h][w]
                    atom.pos = x_[count]
                    atom.vel = v_[count]
                    count = count + 1