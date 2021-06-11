""" 
Functions to help dowload data given
- Basin name
- Sub-basin name
- Coordinates
"""
import xarray as xr


def select_basin(dataset, location):
    """ Interpolate dataset at given coordinates """  
    mask_filepath = find_mask(location)
    basin = apply_mask(dataset, mask_filepath) 
    return basin


def find_mask(location):
    """ Returns a mask filepath for given location """
    mask_dic = {'ngari':'Data/Masks/Ngari_mask.nc', 'khyber':'Data/Masks/Khyber_mask.nc', 
                'gilgit':'Data/Masks/Gilgit_mask.nc', 'uib':'Data/Masks/ERA5_Upper_Indus_mask.nc',
                'sutlej': 'Data/Masks/Sutlej_mask.nc', 'beas':'Data/Masks/Beas_mask.nc'}
    mask_filepath = mask_dic[location]
    return mask_filepath


def basin_finder(loc):
    """ 
    Finds basin to load data from.
    Input
        loc: list of coordinates [lat, lon] or string refering to an area.
    Output
        basin , string: name of the basin.
    """
    basin_dic ={'indus': 'indus', 'uib': 'indus', 'sutlej':'indus', 'beas':'indus',
                'khyber': 'indus', 'ngari': 'indus', 'gilgit':'indus'}
    if loc is str:
        basin = basin_dic[loc]
        return basin
    if loc is not str: # fix to search with coords
        return 'indus'


def apply_mask(data, mask_filepath):
    """
    Opens NetCDF files and applies Upper Indus Basin mask to ERA 5 data.
    Inputs:
        Data filepath, NetCDF
        Mask filepath, NetCDF
    Return:
        A Data Array
    """
    if data is str:
        da = xr.open_dataset(data)
        if "expver" in list(da.dims):
            print("expver found")
            da = da.sel(expver=1)
    else:
        da = data
    mask = xr.open_dataset(mask_filepath)
    mask = mask.rename({'latitude': 'lat', 'longitude': 'lon'})
    mask_da = mask.overlap
    masked_da = da.where(mask_da > 0, drop=True)
    return masked_da
