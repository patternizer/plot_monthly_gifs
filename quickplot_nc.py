#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Ascenison Island extraction
"""

import os, glob
import imageio
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib
#matplotlib.use('agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io import shapereader

#----------------------------------------------------------------------------
# PLOT: total precipitation field: 
#----------------------------------------------------------------------------

ds = xr.open_dataset('era5_tp_1950_1979.nc')
#ds = xr.open_dataset('era5_tp_1979_2020.nc')
lat = ds.latitude # [90.0,89.75,...,-90.0]
lon = ds.longitude # [0.0,0.25,...,359.75]
par = ds.tp
time = ds.time

N = par.shape[0]

for i in range(N):
#   var = par[i,:,:]
#   var = (par[i,0,:,:] - np.nanmean(par[i,0,:,:])) / np.nanstd(par[i,0,:,:])
    var = (par[i,:,:] - np.nanmean(par[i,:,:])) / np.nanstd(par[i,:,:])
    fig, axis = plt.subplots(1, 1, subplot_kw=dict(projection=ccrs.PlateCarree()))
#    fig, axis = plt.subplots(1, 1)
    p = var.plot( 
              ax = axis,
              robust = False, 
#             cmap = 'RdBu_r',
#             cmap = 'gist_earth', # green-brown-white
#             cmap = 'gist_yarg',  # grey-black (high contrast)
#              cmap = 'gist_ncar', # lime-orange-white (high contrast)
              cmap = 'nipy_spectral', # teal-orange-lightgrey (high contrast)
              transform=ccrs.PlateCarree(),
#              col = 'time',
#              col_wrap = 3,
              vmin = -3.0, # z-score
              vmax = 3.0,  # z-score              
              cbar_kwargs={'orientation':'horizontal','extend':'both','shrink':0.8,'aspect':40,'label':'ERA5 monthly reanalysis: total precipitation (standard-scores)'},    
    )
    axis.coastlines(),
    plt.title(str(time[i])[36:46])
#   plt.savefig('tp_' + str(i+348).zfill(len(str(N))) +'.png')    
    plt.savefig('tp_' + str(i).zfill(len(str(N))) +'.png')    
    plt.close()

images = sorted(glob.glob('tp_*.png'))
var = [imageio.imread(file) for file in images]
imageio.mimsave('tp.gif', var, fps = 10)

# COVERT GIF to MP4
# ffmpeg -i tp.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" tp.mp4

# -----------------------------------------------------------------------------
print('** END')
