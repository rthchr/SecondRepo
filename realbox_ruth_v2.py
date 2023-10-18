# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 14:33:01 2021

@author: Thibault

- Basic statistics computation over a grid box
- Plot the statistics for the HIMAWARI8 bands + chlor_a
"""
#Module
import numpy as np
import matplotlib.dates as mdates 
import matplotlib.ticker as ticker 
import matplotlib.pyplot as plt
import matplotlib.gridspec as gd
from matplotlib.ticker import FormatStrFormatter 
from matplotlib.colors import LogNorm 
from pylab import figure, cm  
import cmocean, cmocean.plots 
import xarray as xr 
import pandas as pd 
from netCDF4 import Dataset, num2date 
from datetime import *
#import myPyFunc as my

#Options
plt.rcParams['text.usetex'] = True
directory     = '/home/guinaldot/Documents/data/10-min/time_corrected'
moving_average= False #don't change this if you haven't load the module myPyFunc
savefig       = False
jmin, jmax   = 1450, 1455 #grid cells for the chosen longitude
imin, imax  = 1280, 1285 #grid cells for the chosen latitude

#Load data
file_corrected = xr.open_dataset(directory+'/H08_20160603_20160605_ROC010_FLDK.02401_02401_timecorrected.nc')
files = Dataset(directory+'/H08_20160603_20160605_ROC010_FLDK.02401_02401_timecorrected.nc') 
timess = files.variables['time'][:] 


#Read netcdf time and transform to string
datevar = num2date(files.variables['time'][:], 
                   files.variables['time'].getncattr('units'), 
                   only_use_cftime_datetimes=False,
                   only_use_python_datetimes=True)
str_time = [i.strftime("%Y-%m-%d %H:%M") for i in datevar]   


#Data analysis
chlor_a_mean = [];chlor_a_std = [];chlor_a_pxl = [];chlor_a_SNR = []
rw01_mean = [];rw01_std = [];rw01_SNR = []

rw02_mean= [];rw02_std = [];rw02_SNR = []
rw03_mean = [];rw03_std = [];rw03_SNR = []

for i in range(len(timess)):
    f1 =  file_corrected.variables['chlor_a'][i,jmin:jmax,imin:imax]
    f2 =  file_corrected.variables['Rw_01'][i,jmin:jmax,imin:imax]
    f3 =  file_corrected.variables['Rw_02'][i,jmin:jmax,imin:imax]
    f4 =  file_corrected.variables['Rw_03'][i,jmin:jmax,imin:imax]
    
    chlor_a_mean.append(f1.mean())
    chlor_a_std.append(f1.std())
    chlor_a_pxl.append(np.count_nonzero(~np.isnan(f1)))
    
    rw01_mean.append(f2.mean())
    rw01_std.append(f2.std())
    
    rw02_mean.append(f3.mean())
    rw02_std.append(f3.std())
    
    rw03_mean.append(f4.mean())
    rw03_std.append(f4.std())
    
chlor_a_SNR=np.array(chlor_a_mean)/np.array(chlor_a_std) #np.divide does not work correctly if you don't have an array first
rw01_SNR=np.array(rw01_mean)/np.array(rw01_std)
rw02_SNR=np.array(rw02_mean)/np.array(rw02_std)
rw03_SNR=np.array(rw03_mean)/np.array(rw03_std)

#Create a dataframe to handle values during the plot stage
df = pd.DataFrame({'chlor_a_mean':np.array(chlor_a_mean),'chlor_a_std':np.array(chlor_a_std),'chlor_a_SNR':chlor_a_SNR,
'rw01_mean':np.array(rw01_mean),'rw01_std':np.array(rw01_std),'rw01_SNR':rw01_SNR,
'rw02_mean':np.array(rw02_mean),'rw02_std':np.array(rw02_std),'rw02_SNR':rw02_SNR,
'rw03_mean':np.array(rw03_mean),'rw03_std':np.array(rw03_std),'rw03_SNR':rw03_SNR}, index=datevar)
data_rw = pd.DataFrame([])
data_rw = data_rw.append(df) 
data_rw.index = pd.to_datetime(data_rw.index)
data_rw = data_rw.resample('10min').asfreq()

if moving_average==True:

  data_rw['rw01_mean'] = my.moving_average(data_rw['rw01_mean'],2)
  data_rw['rw01_std'] = my.moving_average(data_rw['rw01_std'],2)
  data_rw['rw01_SNR'] = my.moving_average(data_rw['rw01_SNR'],2)
  
  data_rw['rw02_mean'] = my.moving_average(data_rw['rw02_mean'],2)
  data_rw['rw02_std'] = my.moving_average(data_rw['rw02_std'],2)
  data_rw['rw02_SNR'] = my.moving_average(data_rw['rw02_SNR'],2)
  
  data_rw['rw02_mean'] = my.moving_average(data_rw['rw02_mean'],2)
  data_rw['rw02_std'] = my.moving_average(data_rw['rw02_std'],2)
  data_rw['rw02_SNR'] = my.moving_average(data_rw['rw02_SNR'],2)

#Plot
nrows = 3
ncols = 3

fig,ax = plt.subplots(nrows, ncols, sharex='col', sharey='row',figsize=(15,15))

ax[0,0].plot(data_rw.index,data_rw['rw01_mean']); ax[0,0].title.set_text('RW01') 
ax[0,0].tick_params(axis='x',labelbottom=False)
ax[0,0].axvspan(datetime(2016, 6, 4,6,0), datetime(2016,6,4,23,0), facecolor='grey', alpha=0.25)
ax[0,0].set_ylabel('Mean (mg.m$^{-3}$)')
ax[0,0].yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

ax[1,0].plot(data_rw.index,data_rw['rw01_std'])
ax[1,0].tick_params(axis='x',labelbottom=False)
ax[1,0].axvspan(datetime(2016, 6, 4,6,0), datetime(2016,6,4,23,0), facecolor='grey', alpha=0.25)
ax[1,0].set_ylabel('Std (mg.m$^{-3}$)')
ax[1,0].yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

ax[2,0].plot(data_rw.index,data_rw['rw01_SNR'])
ax[2,0].tick_params(axis='x')
ax[2,0].set_xticklabels(data_rw.index, rotation=45)
ax[2,0].axvspan(datetime(2016, 6, 4,6,0), datetime(2016,6,4,23,0), facecolor='grey', alpha=0.25)
ax[2,0].set_ylabel('SNR')
ax[2,0].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))

ax[0,1].plot(data_rw.index,data_rw['rw02_mean']); ax[0,1].title.set_text('RW02') 
ax[0,1].tick_params(axis='x',labelbottom=False)
ax[0,1].axvspan(datetime(2016, 6, 4,6,0), datetime(2016,6,4,23,0), facecolor='grey', alpha=0.25)

ax[1,1].plot(data_rw.index,data_rw['rw02_std'])
ax[1,1].tick_params(axis='x',labelbottom=False)
ax[1,1].axvspan(datetime(2016, 6, 4,6,0), datetime(2016,6,4,23,0), facecolor='grey', alpha=0.25)

ax[2,1].plot(data_rw.index,data_rw['rw02_SNR'])
ax[2,1].tick_params(axis='x')
ax[2,1].set_xticklabels(data_rw.index, rotation=45)
ax[2,1].axvspan(datetime(2016, 6, 4,6,0), datetime(2016,6,4,23,0), facecolor='grey', alpha=0.25)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))

ax[0,2].plot(data_rw.index,data_rw['rw02_mean']); ax[0,2].title.set_text('RW03') 
ax[0,2].tick_params(axis='x',labelbottom=False)
ax[0,2].axvspan(datetime(2016, 6, 4,6,0), datetime(2016,6,4,23,0), facecolor='grey', alpha=0.25)


ax[1,2].plot(data_rw.index,data_rw['rw02_std'])
ax[1,2].tick_params(axis='x',labelbottom=False)
ax[1,2].axvspan(datetime(2016, 6, 4,6,0), datetime(2016,6,4,23,0), facecolor='grey', alpha=0.25)

ax[2,2].plot(data_rw.index,data_rw['rw02_SNR'])
ax[2,2].tick_params(axis='x')
ax[2,2].set_xticklabels(data_rw.index, rotation=45)
ax[2,2].axvspan(datetime(2016, 6, 4,6,0), datetime(2016,6,4,23,0), facecolor='grey', alpha=0.25)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
fig.autofmt_xdate()

if savefig == True:
  plt.savefig(directory+'himawari_snr_analysis.png', format='png')


