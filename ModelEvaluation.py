# Model evaluation 

import datetime
import numpy as np
import xarray as xr
import pandas as pd
import sklearn as sk
import cartopy.crs as ccrs
import matplotlib.cm as cm
import cartopy.feature as cf
import matplotlib.pyplot as plt
import matplotlib.ticker as tck

from tqdm import tqdm

import DataExploration as de
import DataPreparation as dp 
import DataDownloader as dd
import Metrics as me
import GPModels as gpm
import Sampling as sa


mask_filepath = 'Data/ERA5_Upper_Indus_mask.nc'

def single_loc_evaluation():

    metric_list = []
    coord_list = sa.random_location_generator(UIB=True)
    n = len(coord_list)

    for i in tqdm(range(n)):
        try: 
            xtrain, xval, xtest, ytrain, yval, ytest = dp.multivariate_data_prep(number=None, EDA_average=False, coords=list(coord_list[i]))
            m = gpm.multi_gp(xtrain, xval, ytrain, yval)

            training_R2 = me.R2(m, xtrain, ytrain)
            training_RMSE = me.RMSE(m, xtrain, ytrain)
            val_R2 = me.R2(m, xval, yval)
            val_RMSE = me.RMSE(m, xval, yval)

            metric_list.append([coord_list[i,0], coord_list[i,1], training_R2, training_RMSE, val_R2, val_RMSE])
        
        except Exception:
            pass 

    df = pd.DataFrame(metric_list, columns=['latitude', 'longitude', 'training_R2', 'training_RMSE', 'val_R2', 'val_RMSE'])
    df.to_csv('Data/single-locations-eval-2020-07-07')
    '''
    print(df.mean(axis=0))
    '''
    df_prep = df.set_index(['latitude', 'longitude'])
    da= df_prep.to_xarray()

    plt.figure()
    ax = plt.subplot(projection=ccrs.PlateCarree())
    ax.set_extent([71, 83, 30, 38])
    da.val_R2.plot(cbar_kwargs={'label': '\n Validation R2', 'extend':'neither', 'pad':0.10})
    ax.gridlines(draw_labels=True)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')

    plt.figure()
    ax = plt.subplot(projection=ccrs.PlateCarree())
    ax.set_extent([71, 83, 30, 38])
    da.val_RMSE.plot(cbar_kwargs={'label': '\n Validation RMSE', 'extend':'neither','pad':0.10})
    ax.gridlines(draw_labels=True)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')

    plt.show()

