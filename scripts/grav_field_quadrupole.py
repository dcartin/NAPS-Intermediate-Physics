# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:06:56 2020

@author: cartin
"""

from vpython import arrow, canvas, color, mag, norm, sphere, vector

#-----------------------------------------------------------------------------#

def cleanup():
    
    try:
        for fieldVec in fieldVecList:
            fieldVec.visible = False
            del fieldVec
    except:
        pass
    
#-----------------------------------------------------------------------------#
        
canvas()
    
# Clean up previous field vectors

cleanup()

# Definitions

GRID_SIZE = 4               # Extent of grid of field vector arrows
NUM_POINTS = 2              # Number of points in grid along each axis

fieldVecList = []
spacing = GRID_SIZE / NUM_POINTS

# Create mass quadrupole

massList = []
DM = 2
scale = 1.5 * spacing

for iii in [-1, 1]:
    for jjj in [-1, 1]:
        massList += [sphere(pos = vector(iii * scale, jjj * scale, 0), mass = DM, radius = 0.3, color = color.blue)]

# Create grid of gravitational field vectors
# surrounding quadrupole

for iii in range(-NUM_POINTS, NUM_POINTS + 1):
    for jjj in range(-NUM_POINTS, NUM_POINTS + 1):
        for kkk in range(-NUM_POINTS, NUM_POINTS + 1):
            
            # For all other points
            
            nextPos = vector(iii * spacing, jjj * spacing, kkk * spacing)
            
            # Sum over all spheres within mass sheet for total grav field
            
            gravField = vector(0, 0, 0)
            
            for mmm in range(len(massList)):
                    gravField += -DM / (mag(nextPos - massList[mmm].pos) ** 2) * norm(nextPos - massList[mmm].pos)
                    
            # Add this gravitational field vector to fieldVecList            
                        
            fieldVecList += [arrow(pos = nextPos, axis = gravField, color = color.yellow, shaftwidth = 0.1)]