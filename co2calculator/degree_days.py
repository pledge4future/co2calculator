import numpy as np
import xarray as xr
from datetime import date as ddate
from datetime import datetime as dtime
from distances import geocoding


def get_temp_series(location: str | tuple | list | np.ndarray, 
                    start_time: ddate | dtime, 
                    end_time: ddate | dtime):
    """
    Given a location returns an xarray dataset of hourly temperatures in Kelvin
    INPUTS:
        location: a location string, ex. "Bergheimer Straße 116, 69115 Heidelberg, Germany", 
                  or explicit longitude and latitude coordinates, ex. (10.0, 15.0)
        start_time (datetime.date or datetime.datetime): initial time from which to get temperature series
        end_time (datetime.date or datetime.datetime): initial time from which to get temperature series
    OUTPUTS:
        ds (xarray dataset): has coordinates [longitude (float32), latitude (float32), time (datetime64)]
        
    TODO: look first at a lookup table first rather than call openrouteservice every time?
    TODO: here pulls from data set "temp_data.nc", need to generalize, or store entire data set somewhere
    """
    assert isinstance(start_time, (dtime, ddate)), 'start_time should be a datetime.date or datetime.datetime'
    assert isinstance(end_time, (dtime, ddate)), 'start_time should be a datetime.date or datetime.datetime'

    if isinstance(location, str):
        # get latitude and longitude coordinates for location
        _, _, coords = geocoding(location)
    elif isinstance(location, (tuple, list, np.ndarray)):
        assert (np.shape(location) == (2,)), 'the given location coordinates are not the correct shape'
        coords = location
    else:
        raise Exception('the inputted location is not of an acceptable type')

    fn = "temp_data.nc"
    ds = xr.open_dataset(fn) # maybe in the future could optimize by not opening the entire file?
    # this takes from midnight of first day to midnight of first day of following month
    ds = ds.sel(latitude=round(coords[1])).sel(longitude=round(coords[0])).sel(time=slice(start_time, end_time))

    # interpolate missing hours of the day (sometimes data only from 06h to 22h)
    ds = ds.resample(time="1h").interpolate("linear")
    return ds


def calc_degreedays(dd_type: str, 
                    location: str | tuple | list | np.ndarray, 
                    date: ddate | dtime | str, 
                    Tref: float = None):
    """
    Calculate the degree days for a given month using the integration approach (higher fidelity). 
    For futher details see for example
        Day, & Karayiannis, T. G. (1998). Degree-days: Comparison of calculation methods. 
        Building Services Engineering Research & Technology, 19(1), 7-13. https://doi.org/10.1177/014362449801900102
    INPUTS:
        dd_type (str): either 'heating' for HDD or 'cooling' for CDD
        location (str): ex. "Bergheimer Straße 116, 69115 Heidelberg, Germany"
        date_: The desired month for which to calculate the degree days.
               Should be datetime.date object, datetime.datetime object, or string 'year-month', ex. '2020-02'
        Tref (float, optional): reference or base temperature. Default is 15.5C for HDD, 22C for CDD (standard values)
    OUTPUTS:
        dd['t2m'].values (float): Cumulative degree days for the given month
    """
    if dd_type not in ('heating','cooling'):
        print("WARNING calc_degreedays: degree days type not understood. Defaulting to type='heating'.")
        dd_type = 'heating'

    # extract month info based on imputted date type
    if isinstance(date, (dtime, ddate)):
        start_date = date.replace(day=1) # set to first day of month
    elif isinstance(date, str): # create a datetime.date object
        year , month = date.split('-')
        start_date = dtime(int(year), int(month), 1) # automatically sets to midnight of first day
    else:
        raise Exception('date type not understood:', type(date), date)
    
    end_date = start_date.replace(month=(start_date.month+1)) # set to first day of next month
    # Note: We incluce midnight of the next day because we use an integration approach.
    #       If we were to use for example the simpler UK Meteorological Office, we would only
    #       need until 11pm of the same month. This can be achieved through the addition of
    #       the following line (for datetime object): end_date = end_date - timedelta(hours=1)
    
    ds = get_temp_series(location, start_date, end_date)

    if dd_type == 'heating':
        if Tref is None:
            Tref = 288.65  # (15.5 C)
        ds['t2m'] = Tref - ds['t2m']
    else: # type == cooling
        if Tref is None:
            Tref = 295.15  # (22 C)
        ds['t2m'] = ds['t2m'] - Tref
    ds = np.maximum(ds, 0)

    # note: integrate sets each hour as unit 1, must divide by total number of hours (24 in a day) to obtain cumulative degree days
    dd = ds.integrate('time',datetime_unit='h') /24 
    # manually set a minimum value of 0.1 to avoid issues with dividing by 0
    if dd['t2m'].values < 0.1:
        print("WARNING calc_degreedays: degree days calculated to be <0.1, setting cutoff at 0.1.")
    result = min(dd['t2m'].values, 0.1)
    return result
