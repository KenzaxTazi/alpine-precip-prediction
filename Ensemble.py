# GP ensemble

import pandas as pd
import numpy as np   

from sklearn.metrics import mean_squared_error, r2_score

import GPModels as gpm
import DataPreparation as dp
import Metrics as me

# Filepaths
mask_filepath = 'Data/ERA5_Upper_Indus_mask.nc'
khyber_mask = 'Khyber_mask.nc'
gilgit_mask = 'Gilgit_mask.nc'
ngari_mask = 'Ngari_mask.nc'


model_list = []

ytrain_pred_list = []
ytrain_std_pred_list =[]

yval_pred_list = []
yval_std_pred_list = []

xtrain_a, xval_a, xtest_a, ytrain_a, yval_a, ytest_a = dp.multivariate_data_prep()

for i in range(10):
    
    xtrain, xval, xtest, ytrain, yval, ytest = dp.multivariate_data_prep(number=i)
    
    model = gpm.multi_gpflow_gp(xtrain, xval, ytrain, yval)
    model_list.append(model)

    ytrain_pred, ytrain_std_pred = model.predict_y(xtrain)
    ytrain_pred_list.append(ytrain_pred)
    ytrain_std_pred_list.append(ytrain_std_pred)

    yval_pred, yval_std_pred = model.predict_y(xval)
    yval_pred_list.append(yval_pred)
    yval_std_pred_list.append(yval_std_pred)

# To Dataframes and calculate means

yval_pred_array = np.array(yval_pred_list) 
yval_pred_df = pd.DataFrame(yval_pred_array.reshape(10, 89))
yval_pred_df = yval_pred_df.T
yval_pred_df['mean'] = yval_pred_df.mean(axis=1)

yval_std_pred_array = np.array(yval_std_pred_list) 
yval_std_pred_df = pd.DataFrame(yval_std_pred_array.reshape(10, 89))
yval_std_pred_df = yval_std_pred_df.T
yval_std_pred_df['mean'] = yval_std_pred_df.mean(axis=1)

ytrain_pred_array = np.array(ytrain_pred_list) 
ytrain_pred_df = pd.DataFrame(ytrain_pred_array.reshape(10, 356))
ytrain_pred_df = ytrain_pred_df.T
ytrain_pred_df['mean'] = ytrain_pred_df.mean(axis=1)

ytrain_std_pred_array = np.array(ytrain_std_pred_list) 
ytrain_std_pred_df = pd.DataFrame(ytrain_std_pred_array.reshape(10, 356))
ytrain_std_pred_df = ytrain_std_pred_df.T
ytrain_std_pred_df['mean'] = ytrain_std_pred_df.mean(axis=1)

RMSE_train = mean_squared_error(ytrain_a, ytrain_pred_df['mean'])
R2_train = r2_score(ytrain_a, ytrain_pred_df['mean'])

RMSE_val = mean_squared_error(yval_a, yval_pred_df['mean'])
R2_val = r2_score(yval_a, yval_pred_df['mean'])

y_mean = np.concatenate((ytrain_pred_df['mean'], yval_pred_df['mean'])).mean()
std_mean = np.concatenate((ytrain_std_pred_df['mean'], yval_std_pred_df['mean'])).mean()
