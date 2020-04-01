#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 13:07:42 2020

@author: stephen
"""
print("Initiating...")
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
import matplotlib.ticker as ticker
import math

if __name__ == '__main__':
    print("Loading...")
    # create matplotlib objects
    fig, ax = plt.subplots()
    plt.subplots_adjust(left = 0.26, bottom=0.4)
    # Setup a plot such that only the bottom spine is shown
    def setup(ax):
        ax.spines['right'].set_color('none')
        ax.spines['left'].set_color('none')
        ax.yaxis.set_major_locator(ticker.NullLocator())
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.tick_params(which='major', width=1.00)
        ax.tick_params(which='major', length=5)
        ax.tick_params(which='minor', width=0.75)
        ax.tick_params(which='minor', length=2.5)
        ax.set_xlim(0, 5)
        ax.set_ylim(0, 1)
        ax.patch.set_alpha(0.0)

    setup(ax)
    ax.xaxis.set_major_locator(ticker.AutoLocator())
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.set_title('$\overline{v}$')
    l,= plt.plot(0,0,'ro')


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


    s_avg_radius = Slider(ax_avg_radius, 'Average Radius', 1, 1000, valinit=1,valstep=10)
    s_epsilon_o = Slider(ax_epsilon_o, '$\epsilon_o$', 0, 1, valinit=0,valstep=0.1)
    s_I = Slider(ax_I, 'I', 1, 1.2, valinit=1,valstep=0.01)
    s_M = Slider(ax_M, 'M', 0, 1000, valinit=0,valstep=10)
    s_Pr = Slider(ax_Pr, 'Pr', 0, 1000, valinit=0,valstep=10)
    s_sigma_o = Slider(ax_sigma_o, '$\sigma_o$', 0, 1000, valinit=0,valstep=10)
    s_r = Slider(ax_r, 'r', 1, 1000, valinit=1,valstep=10)

    # update on change function
    def update(val):
        #remove previous text
        for text in ax.texts:
            text.set_visible(False)
            
        closure.avg_radius = s_avg_radius.val
        closure.epsilon_o = s_epsilon_o.val
        closure.I = s_I.val
        closure.M = s_M.val
        closure.Pr = s_Pr.val
        closure.sigma_o = s_sigma_o.val
        closure.r = s_r.val
        
        average_closure_rate =  closure.calc_closure_rate()
    
        l.set_xdata(average_closure_rate)
        
        ax.relim()
        ax.autoscale(axis = 'x')
        ax.text(sum(ax.get_xlim())/2,0.1,average_closure_rate)
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

