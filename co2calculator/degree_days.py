import numpy as np
import os
import openrouteservice
import xarray as xr
from datetime import timedelta
from datetime import date as ddate

#TODO: Is this the correct way to load this API Key for openrouteservice??
# Load environment vars (TODO: Use pydantic.BaseSettings)
ORS_API_KEY = os.environ.get("ORS_API_KEY")

def get_temp_series(location):
    """
    Given a location returns an xarray dataset of hourly temperatures in Kelvin
    INPUTS:
        location (str): ex. "Bergheimer Straße 116, 69115 Heidelberg, Germany"
    OUTPUTS:
        ds (xarray dataset): has coordinates [longitude (float32), latitude (float32), time (datetime64)]
        
    TODO: specify time bounds (here pulls entire data set for given location)
    TODO: look first at a lookup table first rather than call openrouteservice every time
    TODO: add option for location to be given directly in latitude and longitude
    TODO: here pulls from data set "temp_data.nc", need to generalize, or store entire data set somewhere
    """
    # get latitude and longitude coordinates for location
    clnt = openrouteservice.Client(key=ORS_API_KEY)
    call = openrouteservice.geocode.pelias_search(clnt, location)
    for feature in call["features"]:
        geom = feature["geometry"]["coordinates"]

    fn = "temp_data.nc"
    ds = xr.open_dataset(fn)
    ds = ds.sel(latitude=round(geom[1])).sel(longitude=round(geom[0]))

    # interpolate missing hours of the day (sometimes data only from 06h to 22h)
    ds = ds.resample(time="1h").interpolate("linear")
    return ds

def get_month_endpoints(date_str, include_midnight = True):
    """
    Given a year-month string, return the endpoints required for the timeslice to select temperatures of a given month
    INPUTS:
        date_str (str): should be 'year-month', ex. '2020-02'
        include_midnight (bool, optional): whether or not to include first day of next month at midnight. Needed for
            integration approach to include 11pm to midnight of last day in the integration
    OUTPUTS:
        start_str (str): string for first day of month, ex. '2020-02-01'
        end_str (str): if include_midnight = True, string for first day of next month at midnight, ex. '2020-03-01-00'
                       if include_midnight = False, string for last day of month at 11pm, ex. '2020-03-31-23'
    """
    start_year , start_month = date_str.split('-')
    assert (int(start_month) <= 12), 'Error in get_month_endpoints: month can not be >12!'
    start_str = start_year + '-' + start_month + '-01'
    
    if include_midnight:
        if int(start_month) < 12:
            if include_midnight:
                end_month = '{:02d}'.format(int(start_month)+1)
            else:
                end_month = start_month
            end_year = start_year
        else: # start_month = 12
            end_month = '01'
            end_year = str(int(start_year)+1)
        end_str = end_year + '-' + end_month + '-01-00'
    else:
        end_month = '{:02d}'.format(int(start_month))
        end_year = start_year
        # The day 28 exists in every month. 4 days later, it's always next month
        next_month = ddate(int(start_year), int(start_month), 1).replace(day=28) + timedelta(days=4)
        # subtracting the number of the current day brings us back to the last dayone month
        end_str = next_month - timedelta(days=next_month.day)
        end_str = str(end_str) + '-23'

    return start_str, end_str

def calc_degreedays(type, date_str, location = "Bergheimer Straße 116, 69115 Heidelberg, Germany", Tref = None):
    """
    Calculate the degree days for a given month using the integration approach (higher fidelity). 
    For futher details see for example
        Day, & Karayiannis, T. G. (1998). Degree-days: Comparison of calculation methods. 
        Building Services Engineering Research & Technology, 19(1), 7-13. https://doi.org/10.1177/014362449801900102
    INPUTS:
        type (str): either 'heating' for HDD or 'cooling' for CDD
        date_str (str): should be 'year-month', ex. '2020-02'
        location (str): ex. "Bergheimer Straße 116, 69115 Heidelberg, Germany"
        Tref (float, optional): reference or base temperature. Default is 15.5C for HDD, 22C for CDD (standard values)
    OUTPUTS:
        dd['t2m'].values (float): Cumulative degree days for the given month
    """
    if type not in ('heating','cooling'):
        print("WARNING calc_degreedays_int: degree days type not understood. Defaulting to type='heating'.")
        type = 'heating'
    
    ds = get_temp_series(location) #TODO specify location here
    # this takes from midnight of first day to midnight of first day of following month
    month_ds = ds.sel(time=slice(*get_month_endpoints(date_str, include_midnight=True)))

    if type == 'heating':
        if Tref != None: Tref = 288.65 # (15.5 C)
        month_ds['t2m'] = Tref - month_ds['t2m']
    else: # type == cooling
        if Tref != None: Tref = 295.15 # (22 C)
        month_ds['t2m'] = month_ds['t2m'] - Tref
    month_ds = np.maximum(month_ds, 0)

    # note: integrate sets each hour as unit 1, must divide by total number of hours (24 in a day) to obtain cumulative degree days
    dd = month_ds.integrate('time',datetime_unit='h') /24 
    return dd['t2m'].values
