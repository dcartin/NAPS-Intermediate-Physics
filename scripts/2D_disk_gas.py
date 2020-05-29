# -*- coding: utf-8 -*-
"""
Created on Tue May 26 12:31:10 2020

@author: cartin
"""

from vpython import canvas, cos, curve, cylinder, random, pi, rate, sin, sqrt, vector

#=============================================================================#
    
canvas()

# Constants

L = 2
NUM_DISKS = 200
MAX_TIME = 5
t = 0
dt = 0.01

# Create disks with random starting positions, velocities

# Set disk size. We want to make it easier to find a random list
# of positions for the disks, so we must make sure that the area
# of all the disks is less than the total area of the square. To
# do this, we assume
#
#        (NUM_DISKS * pi * R^2) / (2 * L)^2 << 1
#
# Specficially, the ratio is set to the value AREA_RATIO, and the
# resulting radius R is solved for.

AREA_RATIO = 0.1
R = L * sqrt(AREA_RATIO / (NUM_DISKS * pi))

# Initial speed of all disks

INIT_SPEED = 1
                
# Create lists for starting disk positions, velocities

diskPosList = []
diskVelList = []
diskObjList = []
    
for iii in range(NUM_DISKS):

    # Random position; the center of the disk must be
    # at least one disk radius away from box edge
    
    x = (L - R) * (1 - 2 * random())
    y = (L - R) * (1 - 2 * random())
    z = 0
    
    # Random direction for velocity; all disk speeds
    # are set to be the same value INIT_SPEED
    
    Q = 2 * pi * random()
    vx = INIT_SPEED * cos(Q)
    vy = INIT_SPEED * sin(Q)
    vz = 0
    
    # Put these
    
    diskPosList += [[x, y, z]]
    diskVelList += [[vx, vy, vz]]
    diskObjList += [cylinder(pos = vector(x, y, z), axis = vector(0, 0, 0.01), radius = R)]

# Create boundary of square for disks

boundary = curve(radius = 0.01)
boundary.append(vector(L, L, 0), vector(L, -L, 0), vector(-L, -L, 0), vector(-L, L, 0), vector(L, L, 0))

# Time evolution

while t < MAX_TIME:
    rate(100)
    
    # Go through all the disks, check for collisions, and
    # then update the position, velocity of the disk
    
    for jjj in range(NUM_DISKS):
        
        old_vel = diskVelList[jjj]
    
        # Check for wall collisions
        
        # Check to see if the disk is too close to the walls;
        # flip the direction of the appropriate velocity
        # component if this does happen
        
        if abs(diskPosList[jjj][0]) >= (L - R):
            diskVelList[jjj][0] = -diskVelList[jjj][0]
        if abs(diskPosList[jjj][1]) >= (L - R):
            diskVelList[jjj][1] = -diskVelList[jjj][1]    
            
        # If a disk has gotten loose, use modular arithmetic
        # to put it back in the box on the inside
            
        if abs(diskPosList[jjj][0]) > L:
            diskPosList[jjj][0] = (diskPosList[jjj][0] + 2 * L) % L
            
        if abs(diskPosList[jjj][1]) > L:
            diskPosList[jjj][1] = (diskPosList[jjj][1] + 2 * L) % L
        
        # Check for disk collisions; to save computational
        # time, only check for collisions with disks having
        # numerical labels greater than the current disk
        
        for kkk in range(jjj + 1, NUM_DISKS):
            if sqrt((diskPosList[jjj][0] - diskPosList[kkk][0]) ** 2 + (diskPosList[jjj][1] - diskPosList[kkk][1]) ** 2) <= 2 * R:
                
                # Transfer from lab frame to CM frame
                
                CM_vel = [0.5 * (diskVelList[jjj][0] + diskVelList[kkk][0]), 0.5 * (diskVelList[jjj][1] + diskVelList[kkk][1])]
                disk1_CM_vel = [diskVelList[jjj][0] - CM_vel[0], diskVelList[jjj][1] - CM_vel[1]]
                disk2_CM_vel = [diskVelList[kkk][0] - CM_vel[0], diskVelList[kkk][1] - CM_vel[1]]
                
                # Using initial velocities and Newton's 2nd law in
                # momentum terms, find final velocities of disks
                
                r_mag = sqrt((diskPosList[jjj][0] - diskPosList[kkk][0]) ** 2 + (diskPosList[jjj][1] - diskPosList[kkk][1]) ** 2)
                distUnitVec = [(diskPosList[jjj][0] - diskPosList[kkk][0]) / r_mag, (diskPosList[jjj][1] - diskPosList[kkk][1]) / r_mag]
                
                dot_prod1 = disk1_CM_vel[0] * distUnitVec[0] + disk1_CM_vel[1] * distUnitVec[1]
                disk1_CM_vel = [disk1_CM_vel[0] - 2 * dot_prod1 * distUnitVec[0], disk1_CM_vel[1] - 2 * dot_prod1 * distUnitVec[1]]
                
                dot_prod2 = disk2_CM_vel[0] * distUnitVec[0] + disk2_CM_vel[1] * distUnitVec[1]
                disk2_CM_vel = [disk2_CM_vel[0] - 2 * dot_prod2 * distUnitVec[0], disk2_CM_vel[1] - 2 * dot_prod2 * distUnitVec[1]]
                
                # Transfer from CM frame back to lab frame
                
                disk1_vel = [disk1_CM_vel[0] + CM_vel[0], disk1_CM_vel[1] + CM_vel[1], 0]
                disk2_vel = [disk2_CM_vel[0] + CM_vel[0], disk2_CM_vel[1] + CM_vel[1], 0]
        
        # Update positions, velocities in lists
        
        diskPosList[jjj] = [diskPosList[jjj][0] + diskVelList[jjj][0] * dt, diskPosList[jjj][1] + diskVelList[jjj][1] * dt, diskPosList[jjj][2] + diskVelList[jjj][2] * dt]
            
        # Update visible disks
        
        diskObjList[jjj].pos = vector(diskPosList[jjj][0], diskPosList[jjj][1], diskPosList[jjj][2])
        
        new_vel = diskVelList[jjj]
        
    # Update time
    
    t = t + dt