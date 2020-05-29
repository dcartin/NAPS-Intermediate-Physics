# -*- coding: utf-8 -*-
"""
Created on Fri May 29 12:57:03 2020

@author: cartin
"""

from vpython import arrow, canvas, color, mag, norm, sphere, vector

#-----------------------------------------------------------------------------#

def cleanUp():
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

# Create a single mass at origin

planet = sphere(pos = vector(0, 0, 0), mass = 5, radius = 0.3, color = color.blue)

# Create grid of gravitational field vectors
# surrounding this mass

fieldVecList = []
spacing = GRID_SIZE / NUM_POINTS

for iii in range(-NUM_POINTS, NUM_POINTS + 1):
    for jjj in range(-NUM_POINTS, NUM_POINTS + 1):
        for kkk in range(-NUM_POINTS, NUM_POINTS + 1):
            
            # Avoid problems at origin
            
            if iii == 0 and jjj == 0 and kkk == 0:
                continue
                
            # For all other positions
            
            nextPos = vector(iii * spacing, jjj * spacing, kkk * spacing)
            unitVec = norm(nextPos)
            gravField = -planet.mass / (mag(nextPos) ** 2) * unitVec
            fieldVecList += [arrow(pos = nextPos, axis = gravField, color = color.yellow, shaftwidth = 0.1)]