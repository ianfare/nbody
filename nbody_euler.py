#!/usr/bin/python3
import sys
import os
import math
import numpy as np
import pygame
import pygame.camera
from pygame.locals import *

n = 50
dt = 0.01
sim_w = 10.
sim_h = 10.
sim_depth = 10.
screen_w = 200
screen_h = 200

w_factor = screen_w/sim_w
h_factor = screen_h/sim_h

pygame.init()

def initialize(n):
  # Manually hard coding initial conditions for testing
  m = [1.,1.,1.]
  pos = [np.array([7.5,5.,7.]),np.array([9.5,2.,5.]),np.array([6.5,2.,7.])]
  vel = [np.array([-0.15,0.2,0.1]),np.array([0.03,-0.2,-0.2]),np.array([0.,0.,0.1])]

#  m = []
#  pos = []
#  vel = []

 # np.random.seed(10)
 # for i in range(n):
 #   m.append(np.random.rand() + 0.5)
 #   pos.append(np.random.rand(3)*sim_w)
 #   vel.append(2*np.random.rand(3) - np.array([1.,1.,1.]))

  screen = pygame.display.set_mode((screen_w,screen_h))

  return m, pos, vel, screen


def step(stepno, m, pos, vel):

  Et = 0

  # For each body  
  for i in range(len(m)):
    
    Ei = 0

    # Get the sum of all the contributions to acceleration form other bodies
    ai = np.array([0.,0.,0.])
    for j in range(len(m)):
      if i != j :
        dist = np.linalg.norm(pos[i] - pos[j])
        aij = (m[j]/max(dist**3,0.1))*(pos[j] - pos[i])
        ai += aij

        Ei -= m[i]*m[j]/dist

    # Change velocity according to acceleration
    vel[i] += ai*dt

    # Change position according to velocity
    pos[i] += vel[i]*dt

    Ei += 0.5*m[i]*np.linalg.norm(vel[i])**2
    Et += Ei

  if stepno%100 == 0:
    print(Et)

#  if stepno > 1620 and stepno < 1630:
#    print(stepno)
#    print(Et)
#    for i in range(len(m)):
#      for j in range(len(m)):
#        if i != j:
#          print(max((np.linalg.norm(pos[i] - pos[j])**3),0.1))
#    print('')
    

def draw(pos,vel):

  # Fill screen with black
  screen.fill((0,0,0))

  # Draw bodies
  for i in range(len(m)):
    pygame.draw.circle(screen,(max(min(255,pos[i][2]*25.5),0),max(min(255,pos[i][2]*25.5),0),max(min(255,pos[i][2]*25.5),0)), (math.floor(pos[i][0]*w_factor), math.floor(pos[i][1]*h_factor)), max(math.floor(pos[i][2]**2/10.),1))

  # Flip display
  pygame.display.flip()

# Create bodies
m,pos,vel, screen = initialize(n)

file_num = 0

# Do simulation
for i in range(3000):
  if i%50 == 0:
    print('Step: ' + str(i))
  step(i,m,pos,vel)
  draw(pos,vel)

  file_num = file_num + 1
  filename = "./video/%04d.png" % file_num
  pygame.image.save(screen,filename)


os.system("avconv -r 100 -f image2 -i video/%04d.png -y -qscale 0 -s " + str(screen_w) + "x" + str(screen_h) + " -aspect 1:1 result.mp4")
os.system("rm video/*")
