#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 13:07:42 2020

@author: stephen
"""
# parent material model class
class material_model:
    
    def __init__(self,stress_deviator, strain_deviator, M, sigma_o, epsilon_o):
        self.stress_deviator = stress_deviator
        self.M = M
        self.sigma_o = sigma_o
        self.epsilon_o = epsilon_o
        
    def calc_effective_stress(self):
        self.effective_stress = (3/2*self.stress_deviator*self.stress_deviator)**0.5
    
    def calc_effective_strain(self):
        self.effective_strain = (2/3*self.strain_deviator*self.strain_deviator)**0.5
    
    def calc_strain_rate (self):
        # calculate effective stress if it has not already been calculated
        if self.effective_stress is None:
            self.calc_effective_stress()
            
        return 3/2*self.epsilon_o*self.stress_deviator/self.effective_stress*(self.effective_stress/self.sigma_o)**self.M
    
    def calc_stress (self):
        if self.effective_strain is None:
            self.calc_effective_strain()
        
        return 2/3*self.sigma_o*self.stress_deviator/self.effective_strain*(self.effective_strain/self.epsilon_o)**(1/self.M)

# child closure model class
class closure(material_model):
    
    def __init__(self,avg_radius,epsilon_o,I,M,Pr,sigma_o,r):
        self.avg_radius = avg_radius
        self.epsilon_o = epsilon_o
        self.I = I
        self.M = M
        self.Pr = Pr
        self.sigma_o = sigma_o
        self.r = r
    # average closure rate
    def calc_closure_rate(self):
        
        return self.avg_radius*math.sqrt(3)/2*self.epsilon_o*self.I*(math.sqrt(3)/self.M*self.Pr/self.sigma_o/(1-(self.avg_radius/self.r)**(2/self.M)))**self.M
# ------------------------
# MAIN
#-------------------------
        
# import modules
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import math

# create matplotlib objects
fig, ax = plt.subplots()
plt.subplots_adjust(left = 0.26, bottom=0.4)

# create closure class
closure = closure(1,1,1,1,1,1,1)

# create sliders
axcolor = 'lightgoldenrodyellow'
ax_avg_radius = plt.axes([0.25,0.3,0.65,0.03], facecolor = axcolor)
ax_epsilon_o = plt.axes([0.25,0.25,0.65,0.03], facecolor = axcolor)
ax_I = plt.axes([0.25,0.2,0.65,0.03], facecolor = axcolor)
ax_M = plt.axes([0.25,0.15,0.65,0.03], facecolor = axcolor)
ax_Pr = plt.axes([0.25,0.1,0.65,0.03], facecolor = axcolor) 
ax_sigma_o = plt.axes([0.25,0.05,0.65,0.03], facecolor = axcolor)
ax_r = plt.axes([0.25,0,0.65,0.03], facecolor = axcolor)


s_avg_radius = Slider(ax_avg_radius, 'Average Radius', 0.1, 30.0, valinit=0.1,valstep=0.5)
s_epsilon_o = Slider(ax_epsilon_o, '$\epsilon_o$', 0.1, 30.0, valinit=0.1,valstep=0.5)
s_I = Slider(ax_I, 'I', 0.1, 30.0, valinit=0.1,valstep=0.5)
s_M = Slider(ax_M, 'M', 0.1, 30.0, valinit=0.1,valstep=0.5)
s_Pr = Slider(ax_Pr, 'Pr', 0.1, 30.0, valinit=0.1,valstep=0.5)
s_sigma_o = Slider(ax_sigma_o, '$\sigma_o$', 0.1, 30.0, valinit=0.1,valstep=0.5)
s_r = Slider(ax_r, 'r', 0.1, 30.0, valinit=0.1,valstep=0.5)

# update on change function
def update(val):
    closure.avg_radius = s_avg_radius.val
    closure.epsilon_o = s_epsilon_o.val
    closure.I = s_I.val
    closure.M = s_M.val
    closure.Pr = s_Pr.val
    closure.sigma_o = s_sigma_o.val
    closure.r = s_r.val
    
    average_closure_rate = closure.calc_closure_rate()
    ax.text(0.1,0.9,average_closure_rate, fontsize=15)
    fig.canvas.draw_idle()

# bind update on change function to sliders
s_avg_radius.on_changed(update)
s_avg_radius.on_changed(update)
s_epsilon_o.on_changed(update)
s_I.on_changed(update)
s_M.on_changed(update)
s_Pr.on_changed(update)
s_sigma_o.on_changed(update)
s_r.on_changed(update)

# show plot
plt.show()