#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Plot monthly contact sheets
"""

import os, glob
import imageio
import numpy as np
import numpy.ma as ma
import pandas as pd
import xarray as xr
import matplotlib
#matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import colors as mcol
from matplotlib.cm import ScalarMappable
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
from cartopy.io import shapereader
import cartopy.feature as cf
from cartopy.util import add_cyclic_point
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import seaborn

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

#----------------------------------------------------------------------------
# DARK BACKGROUND THEME
#----------------------------------------------------------------------------

plt.rcParams.update({
    "lines.color": "white",
    "patch.edgecolor": "white",
    "text.color": "black",
    "axes.facecolor": "white",
    "axes.edgecolor": "lightgray",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "lightgray",
    "figure.facecolor": "black",
    "figure.edgecolor": "black",
    "savefig.facecolor": "black",
    "savefig.edgecolor": "black"
})

#----------------------------------------------------------------------------
# PLOT: total precipitation field: 
#----------------------------------------------------------------------------

#ds = xr.open_dataset('era5_tp_1950_1979.nc')
ds = xr.open_dataset('era5_tp_1979_2020.nc')
lat = ds.latitude # [90.0,89.75,...,-90.0]
lon = ds.longitude # [0.0,0.25,...,359.75]
par = ds.tp
time = ds.time

# NEXT STEP: calculate anomalies from 1961-1990 baseline

N = np.floor(par.shape[0]/12).astype(int)
for i in range(N):

    p = ccrs.Orthographic(0, 0); threshold=0
    fig, axs = plt.subplots(3,4, figsize=(15,10), subplot_kw=dict(projection=p))        

    for j in range(12):

        if j == 0: r=0; c=0
        elif j == 1: r=0; c=1
        elif j == 2: r=0; c=2
        elif j == 3: r=0; c=3
        elif j == 4: r=1; c=0
        elif j == 5: r=1; c=1
        elif j == 6: r=1; c=2
        elif j == 7: r=1; c=3
        elif j == 8: r=2; c=0
        elif j == 9: r=2; c=1
        elif j == 10: r=2; c=2
        elif j == 11: r=2; c=3

#       v = (par[i*12+j,:,:] - np.nanmean(par[i*12+j,:,:])) / np.nanstd(par[i*12+j,:,:])          # ERA5: 1950-1978 format
        v = (par[i*12+j,0,:,:] - np.nanmean(par[i*12+j,0,:,:])) / np.nanstd(par[i*12+j,0,:,:])    # ERA5: 1979-2020 format
        vmin = -3.0
        vmax = 3.0
        x, y = np.meshgrid(lon,lat)
        
        g = v.plot( 
                ax = axs[r,c],
                # robust = True, 
                # cmap = 'RdBu_r',
                # cmap = 'gist_earth', # green-brown-white
                # cmap = 'gist_yarg',  # grey-black (high contrast)
                # cmap = 'gist_ncar', # lime-orange-white (high contrast)
                cmap = 'nipy_spectral', # teal-orange-lightgrey (high contrast)
                transform=ccrs.PlateCarree(),
                vmin = -3.0, # z-score
                vmax = 3.0,  # z-score     
                # cbar_kwargs={'orientation':'vertical','extend':'both','shrink':0.8,'aspect':40,'label':'ERA5 monthly reanalysis: total precipitation (standard-scores)'},                        
        )
        cb = g.colorbar
        if (j != 3) & (j != 7) & (j != 11):
            cb.remove()   
        axs[r,c].set_title(str(time[i*12+j])[36:43], color='white')
        axs[r,c].set_global()
        axs[r,c].coastlines()
        
    plt.savefig('tp_' + str(i+29).zfill(len(str(N))) +'.png')    # append 29 years of ERA5: 1979-2020 GIFs
#   plt.savefig('tp_' + str(i).zfill(len(str(N))) +'.png')       # 29 years of ERA5: 1950-1978 GIFs
    plt.close()

images = sorted(glob.glob('tp_*.png'))
var = [imageio.imread(file) for file in images]
imageio.mimsave('tp.gif', var, fps = 10)

# COVERT GIF to MP4
# ffmpeg -i tp.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" tp.mp4

# -----------------------------------------------------------------------------
print('** END')
