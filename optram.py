# MODULE                                             # DESCRIPTION
import numpy as np                                   # scientific computing
import numpy.ma as ma                                # numpy masked arrays
import pandas as pd                                  # data analysis and manipulation
import geopandas as gpd                              # geospatial data analysis
import utm                                           # bidirectional UTM-WGS84 converter
import folium                                        # interactive data visualization
import re                                            # regular expressions
from osgeo import gdal, gdalconst                    # raster and geospatial data proc.
import rasterio as rs                                # raster and geospatial data proc.
import matplotlib.pyplot as plt                      # create visualizations
import seaborn as sns                                # create visualizations
import datetime                                      # datetime manipulation
import glob                                          # unix pathname expansion
import haversine as hs                               # distances between points
import dask                                          # parallel computing
from dask.distributed import Client                  # set custom parameters in cluster
import dask.dataframe as dd                          # manipulation of lazy dask dfs
import datashader as ds                              # visualization for big data
import colorcet as cc                                # colormaps for datashader 
from sklearn import linear_model                     # regression 
from sklearn.metrics import mean_absolute_error      # to compute MAE
from sklearn.metrics import mean_squared_error       # to compute RMSE
from sklearn.metrics import r2_score                 # to compute R^2
import xarray as xr                                  # efficent ND arrays manipulation
import rioxarray                                     # rasterio xarray extension
from matplotlib.colors import LinearSegmentedColormap# create custom color maps
from shapely import geometry                         # manipulate planar features
from shapely.geometry import Point                   # manipulate planar features
import pickle                                        # load/save pickle datasets
import os                                            # miscellaneous OS interfaces
from pathlib import Path                             # 
import math                                          #
import random                                        #                          

def utm_to_latlon(coords, zone_number = 12, zone_letter = 'N'):
    easting = coords[0]
    northing = coords[1]
    return utm.to_latlon(easting, northing, zone_number, zone_letter)

def S2_getDate(filename) :
    basename = Path(filename).stem  
    try :
        found = re.search('S2(A|B)2A_(\d+)_.*',basename).group(2)
        dt = datetime.datetime.strptime(found, '%Y%m%d')
        
    except AttributeError:
        raise ValueError('Error: Date can not be extracted from filename %s .' % filename)
        
    return dt

def S2_getIndex(BASE_DIR, date) :
    
    if (isinstance(date, datetime.date)) : 
        date_str = date.strftime("%Y%m%d")
    
    elif (isinstance(date, str)):
        print('"str" type object detected, converting to datetime.')
        date_obj = datetime.datetime.strptime(date, "%Y%m%d") 
        date_str = date_obj.strftime("%Y%m%d")
        
    else : 
        raise TypeError('Error:  %s encountered, but "str" o "datetime.date" expected' % type(date))
    
    pattern = BASE_DIR + '*' + date_str + '*'
    
    try: 
        filepath = glob.glob(pathname = pattern)
        return filepath[0]
    
    except AttributeError: 
        print('Error: File with pattern %s not found' % pattern)
        
def S2_get_sensing_dt(boa_fp):
    days_offset = 1
    start_dt = S2_getDate(boa_fp) - datetime.timedelta(days=days_offset)
    end_dt   = S2_getDate(boa_fp) + datetime.timedelta(days=days_offset)
    
    start_dt = start_dt.strftime('%Y-%m-%d')
    end_dt   = end_dt.strftime('%Y-%m-%d')

    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    print('[%s] : Requesting image metadata between %s <-> %s...' % (now, start_dt, end_dt))
    # bash callback: 
    # dts = ! Rscript ./sen2r/sat_sensing_dt.R $start_dt $end_dt ./sen2r/Walnut-Gulch.geojson 2> /dev/null
    dts = subprocess.Popen(['./sen2r/sat_sensing_dt.R %s %s 2> /dev/null' % (start_dt, end_dt)], shell = True)
    print('[%s] : Done\n' % datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    sensing_datetime = datetime.datetime.strptime(dts[1], '                                        "%Y-%m-%d %H:%M:%S UTC" ')
    return sensing_datetime


def get_px_coords_from_raster(boa, no_data, band) :
    print('[%s] : Retrieving px location coords...' % (datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
    dataset = boa
    val = boa.read(band, masked = True)
    geometry = [Point(dataset.xy(x,y)[0],dataset.xy(x,y)[1]) for x,y in np.ndindex(val.shape) if val[x,y] != no_data]
    coords_utm = [(point.x, point.y)  for point in geometry]
    print('[%s] : Done\n' % datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    return (zip(*coords_utm))


def build_inSitu_obs(df, dest_lat_lng, sensor_df, dists, sensor_name, utm_n = 12, utm_z = 'N') :
    
    # Calculate the closest image pixel(row) to the sensor
    x = df.loc[:,'utm_x'].tolist()
    y = df.loc[:,'utm_y'].tolist()

    df['dist'] = dists
    df['sensor_name'] = sensor_name
    print('[%s] : Sorting %d rows...' % (datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), len(df)))
    df.sort_values('dist', inplace = True)
    print('[%s] : Done\n' % datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    df = df.head(1)
    df.set_index('datetime', inplace = True) # indexing is costly, but only one 1 obs, see previous line
    
    # Get the corresponding sensor obs to the pixel
    #https://stackoverflow.com/questions/32237862/find-the-closest-date-to-a-given-date
    def nearest(items, pivot):
        return min(items, key=lambda x: abs(x - pivot))
              
    nearest_dt = nearest(items = sensor_df.index, pivot = df.index[0])
    val = sensor_df.loc[sensor_df.index == nearest_dt, 'SM5'].values
    print('nearest_dt: %s, %s'% (nearest_dt, val))
    df.loc[:,'SM5'] = float(val)
    df.loc[:,'theta_d'] = float(sensor_df.loc[:,"SM5"].dropna().min())
    df.loc[:,'theta_w'] = float(sensor_df.loc[:,"SM5"].dropna().max())
    return df


def get_haversine_dist_df(utm_coords, sensor_coords, sensor_name, utm_n = 12, utm_z = 'N') : 
    print('[%s] : Calculating haversine distance for sensor %s...'
          % (datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), sensor_name))
    
    dists = [  hs.haversine(utm_to_latlon(utm_coord, utm_n, utm_Z),
                            sensor_coords, unit = hs.Unit.METERS)
        
               for utm_coord in utm_coords 
    ]
    
    print('[%s] : Done\n' % datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    dists = [float(dist) for dist in dists]
    return(dists)

def get_distances_pxs_to_sensor(boa_dummy, sensors_coords, utm_x, utm_y):
    h_dists = { sensor_name : get_haversine_dist_df(utm_coords = zip(utm_x, utm_y),
                                                    sensor_coords = sensors_coords[sensor_name],
                                                    sensor_name = sensor_name) 
                    for sensor_name, sensor_coords in sensors_coords.items()} 
    return (h_dists)

def resample_raster_gdal_nn(input_file, ref_file, out_file):
    # Opening input
    input = gdal.Open(input_file, gdalconst.GA_ReadOnly)
    inputProj = input.GetProjection()
    inputTrans = input.GetGeoTransform()

    # Opening ref
    reference = gdal.Open(ref_file, gdalconst.GA_ReadOnly)
    referenceProj = reference.GetProjection()
    referenceTrans = reference.GetGeoTransform()
    bandreference = reference.GetRasterBand(1)    
    x = reference.RasterXSize 
    y = reference.RasterYSize

    # Resampling
    driver= gdal.GetDriverByName('GTiff')
    output = driver.Create(out_file,x,y,1,bandreference.DataType)
    output.SetGeoTransform(referenceTrans)
    output.SetProjection(referenceProj)
    gdal.ReprojectImage(input,output,inputProj,referenceProj,gdalconst.GRA_NearestNeighbour)
    del output
    del input
    del reference

def add_scl_col(scl_fp, ndvi_fp, local_df, date,  scl_dir = "./sen2r/out/SCL_res10/"):
    if os.path.isdir(scl_dir):
        pass
    else:
        os.mkdir(scl_dir)
    
    if (isinstance(date, datetime.date)) : 
        date_str = date.strftime("%Y%m%d")
    
    elif (isinstance(date, str)):
        print('"str" type object detected, converting to datetime.')
        date_obj = datetime.datetime.strptime(date, "%Y%m%d") 
        date_str = date_obj.strftime("%Y%m%d")
        
    else : 
        raise TypeError('Error:  %s encountered, but "str" o "datetime.date" expected' % type(date))
        
    scl_10_fp = os.path.join(scl_dir, date_str + "_SCL_10m_resampled_by_gdal.tif")
    resample_raster_gdal_nn(input_file = scl_fp,
                            ref_file   = ndvi_fp,
                            out_file   = scl_10_fp)

    scl_10_dataset  = rs.open(scl_10_fp)
    scl_10          = scl_10_dataset.read(1, masked = True)
    scl_10_flatten  = np.ndarray.flatten(scl_10) 

    # TODO: May this be precomputed for speed-up ?
    #   - Theoretically yes, since the SCL resampled rasters should have the same dims 
    x,y = get_px_coords_from_raster(scl_10_dataset,
                                    no_data = 0,
                                    band = 1) 

    scl_10_df = pd.DataFrame({
        'utm_x' : x,
        'utm_y' : y,
        'scl_value' : np.delete(scl_10_flatten, scl_10_flatten == 0)
    })
    scl_10_df = scl_10_df.astype('int')    
    local_df = pd.merge(local_df, scl_10_df, on = ["utm_x", "utm_y"], how = "left")
    return(local_df)