# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 11:27:41 2018

@author: dl923
"""
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.ndimage
import numpy as np
import pandas as pd
import xlrd
from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.patches as mpatches


#%% Target file
T1_ph_file='SMECel6A_nmol_red_sugar_min_MEAN.xls'

#%% Extract and format data
def extract_ph_temp_bivaraite_and_interpolate(infile, pH_start, pH_end, temp_start, temp_end, sheetname, interpolation_int):
    print('NB/ PH start/end is ROW, Temp start/end is COL')
    workbook=xlrd.open_workbook(infile)
    datasheet=workbook.sheet_by_name(sheetname)
    pH_values=[]
    Temperature_values=[]
    value_dict={}
    for col in list(range(temp_start-1, temp_end+1)):
        for row in list(range(pH_start-1, pH_end)):
            if datasheet.cell_value(row, 0) not in pH_values:
                 pH_values.append(datasheet.cell_value(row, 0))
            if not col == 0:     
                 if datasheet.cell_value(pH_start-2, col) not in Temperature_values:
                     Temperature_values.append(datasheet.cell_value(pH_start-2, col))
            if col >= 1:
                if datasheet.cell_value(pH_start-2, col) not in value_dict:
                    value_dict[datasheet.cell_value(pH_start-2, col)]={}
                if datasheet.cell_value(row, 0) not in value_dict[datasheet.cell_value(pH_start-2, col)]:
                     value_dict[datasheet.cell_value(pH_start-2, col)][datasheet.cell_value(row, 0)]={}
                value_dict[datasheet.cell_value(pH_start-2, col)][datasheet.cell_value(row, 0)]=datasheet.cell_value(row, col) 
     #Create a dataframe from the above dictionary containing the data values for bivariate experiment
    Z_value_df=pd.DataFrame.from_dict(value_dict)
    Z_value_df=Z_value_df.T
    Z_value_df = scipy.ndimage.zoom(Z_value_df, interpolation_int)
    #Create a 'mesh' dataframe for contour function to map to, for both pH and Temperatures or other variables  
   # return pH_values, Temperature_values
    pH, Temp = np.meshgrid(pH_values, Temperature_values) 
    pH = scipy.ndimage.zoom(pH, interpolation_int)
    Temp = scipy.ndimage.zoom(Temp, interpolation_int)
    print('Returns raw data dict, interpolated data df, interpolated pH as list, interpolated Temps as list')
    return value_dict, Z_value_df, pH, Temp, pH_values, Temperature_values

T1_value_dict, T1_z_value_df, T1_pH, T1_Temp, pH_full, Temp_full=extract_ph_temp_bivaraite_and_interpolate(T1_ph_file, 2, 9, 1, 8, 'Sheet1', 10)

#%% Plot data with interpolation
############################## PLOTS ##################################
fig, ax1 = plt.subplots(figsize=(8,6)) 


###global params#####
phbivar_ticksize=16
phbivartiskzie=16
countour_labelsize=16
x_y_labelsize=16
cbartisksize=16
tickpad=5
label_pad=0
label_pad_bottom=0.25
ms=3
#####################

ax1.set_xlabel('T ($^o$C)', fontsize=x_y_labelsize, labelpad=label_pad)
ax1.set_ylabel('pH', fontsize=x_y_labelsize, labelpad=label_pad-10)
contours=ax1.contour(T1_Temp, T1_pH, T1_z_value_df, levels=[20,40,60,80,100], colors='black')
ax1.tick_params(axis='both', which='major', labelsize=phbivar_ticksize)
ax1.clabel(contours, inline=True, fontsize=countour_labelsize, fmt='%3.0f')
map1=ax1.contourf(T1_Temp, T1_pH, T1_z_value_df, 1000, cmap='jet',  alpha=0.95, ZLabelString='Activity')
ax1.set_xticks([15,25,35,45,50])
ax1.set_yticks([4, 5, 6, 7, 7.5])
ax1.set_yticklabels(['4','5','6','7','7.5'])
ax1.tick_params(axis='both', which='major', labelsize=phbivartiskzie, pad=tickpad)

####CBAR#####
cbar = fig.colorbar(map1)
#corrds are left, bottom, width, height
#cbar_ax = fig.add_axes([0.424, 0.125, 0.6, 0.75])
#cbar=plt.colorbar(map1, ax=cbar_ax)
cbar.set_ticks([20,40,60,80,100])
cbar.ax.tick_params(labelsize=cbartisksize)
cbar.ax.set_ylabel('Relative activity (%)', size=x_y_labelsize)
cbar.ax.yaxis.set_label_position("left")
cbar_ax.axis('off')
ax1.tick_params(axis='both', labelsize=phbivar_ticksize, pad=tickpad)
