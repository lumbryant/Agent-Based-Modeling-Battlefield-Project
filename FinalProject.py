#!/usr/bin/env python
# coding: utf-8

# In[3]:


import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import copy as cp


m_init = 50 # initial mine population
mm=0  #mines can't move



s_init = 50 # initial soldier population
ms = 0.05 # magnitude of movement of soldiers
ds = 0.1 # defusal rate


cd = 0.05 # radius for collision detection
cdsq = cd ** 2

class agent:
    pass

def initialize():
    global agents, dead, defused, exploded
    agents = []
    dead = []
    defused=[]
    exploded=[]
    for i in range(m_init + s_init):
        ag = agent()
        ag.type = 'm' if i < m_init else 's'
        ag.x = random()
        ag.y = random()
        agents.append(ag)
    
    

def observe():
    global agents, dead, defused, exploded
    cla()
    mines = [ag for ag in agents if ag.type == 'm']
    if len(mines) > 0:
        x = [ag.x for ag in mines]
        y = [ag.y for ag in mines]
        plot(x, y, 'b.')
    defuse = [ag for ag in defused if ag.type == 'm']
    if len(defuse) > 0:
        x = [ag.x for ag in defuse]
        y = [ag.y for ag in defuse]
        plot(x, y, 'g.')
    explode = [ag for ag in exploded if ag.type == 'm']
    if len(explode) > 0:
        x = [ag.x for ag in explode]
        y = [ag.y for ag in explode]
        plot(x, y, 'r.')
    death = [ag for ag in dead if ag.type == 's']
    if len(death) > 0:
        x = [ag.x for ag in death]
        y = [ag.y for ag in death]
        plot(x, y, 'kx')
    soldiers = [ag for ag in agents if ag.type == 's']
    if len(soldiers) > 0:
        x = [ag.x for ag in soldiers]
        y = [ag.y for ag in soldiers]
        plot(x, y, 'ko')
    axis('image')
    axis([0, 1, 0, 1])

def update():
    global agents, dead, defused, exploded
    if agents == []:
        return

    ag = agents[randint(len(agents))]

    # simulating random movement
    m = mm if ag.type == 'm' else ms
    ag.x += uniform(-m, m)
    ag.y += uniform(-m, m)
    ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
    ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y

    # detecting collision and simulating explosion or defusion
    neighbors = [nb for nb in agents if nb.type != ag.type
                 and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]

    if ag.type == 's':
        if len(neighbors) > 0: # if a soldier comes into the radius of a bomb
            if random() > ds:  # they die and the bomb explodes
                dead.append(ag) 
                agents.remove(ag)
                for nb in neighbors:
                    exploded.append(nb)
                    agents.remove(nb)
                return
            else:             # the bomb is defused
                for nb in neighbors:
                    defused.append(nb)
                    agents.remove(nb)
    else:
        pass
    
    if len(dead)== s_init:
        print("Mines")
        print(m_init-len(exploded)-len(defused))
    if len(exploded)+len(defused)==m_init:
        print("Soldiers")
        print(s_init-len(dead))
    

def update_one_unit_time():
    global agents
    t = 0.
    while t < 1. and len(agents) > 0:
        t += 1. / len(agents)
        update()

import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])


# In[ ]:




