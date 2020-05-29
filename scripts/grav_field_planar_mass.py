# -*- coding: utf-8 -*-
"""
Created on Fri May 29 12:57:03 2020

@author: cartin
"""

from vpython import arrow, canvas, color, mag, norm, sphere, vector

#-----------------------------------------------------------------------------#

def cleanup():
    
    # Clean up field vectors
    
    try:
        for fieldVec in fieldVecList:
            fieldVec.visible = False
            del fieldVec
    except:
        pass
    
    # Clean up mass sheet
    
    try:
        for dm in massSheetList:
            dm.visible = False
            del dm
    except:
        pass
    
#-----------------------------------------------------------------------------#
        
canvas()
    
# Clean up previous field vectors, mass sheet

cleanup()

# Definitions

GRID_SIZE = 4               # Extent of grid of field vector arrows
NUM_POINTS = 2              # Number of points in grid along each axis

fieldVecList = []
spacing = GRID_SIZE / NUM_POINTS

# Create mass sheet by making a list of small spheres whose spatial
# extent overlap; use a greater number of grid points than you use
# for the gravitational field grid

massSheetList = []
scale = 10
DM = 0.01

for iii in range(-scale * NUM_POINTS, scale*NUM_POINTS + 1):
    for jjj in range(-scale * NUM_POINTS, scale * NUM_POINTS + 1):
        massSheetList += [sphere(pos = vector(iii * spacing / scale, 0, jjj * spacing / scale), mass = DM, radius = 0.3, color = color.blue)]

# Create grid of gravitational field vectors
# surrounding this mass

for iii in range(-NUM_POINTS, NUM_POINTS + 1):
    for jjj in range(-NUM_POINTS, NUM_POINTS + 1):
        for kkk in range(-NUM_POINTS, NUM_POINTS + 1):
            
            # Avoid grid points within mass sheet
            
            if jjj == 0:
                continue
            
            # For all other points
            
            nextPos = vector(iii * spacing, jjj * spacing, kkk * spacing)
            
            # Sum over all spheres within mass sheet for total grav field
            
            gravField = vector(0, 0, 0)
            
            for mmm in range(len(massSheetList)):
                    gravField += -DM / (mag(nextPos - massSheetList[mmm].pos) ** 2) * norm(nextPos - massSheetList[mmm].pos)
                    
            # Add this gravitational field vector to fieldVecList            
                        
            fieldVecList += [arrow(pos = nextPos, axis = gravField, color = color.yellow, shaftwidth = 0.1)]