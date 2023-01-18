#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 12:54:13 2023

@author: marialozano

"""

import sys
import cdsapi
import schedule
from datetime import datetime
from joblib import Parallel, delayed
from datetime import datetime, timedelta

def download_ERA5_single_levels(year, month, variable, shortname, output_path):
    print('Working on {0} {1}'.format(month, year))
    c = cdsapi.Client()
    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type': 'reanalysis',
            'format': 'netcdf',
            'variable': variable,
            'area': [
                90, -180,
                -90, 180,
            ],
            'year': year,
            'month': month,
            'day': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
                '13', '14', '15',
                '16', '17', '18',
                '19', '20', '21',
                '22', '23', '24',
                '25', '26', '27',
                '28', '29', '30',
                '31',
            ],
            'time': [
                '00:00', '01:00', '02:00',
                '03:00', '04:00', '05:00',
                '06:00', '07:00', '08:00',
                '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00',
                '15:00', '16:00', '17:00',
                '18:00', '19:00', '20:00',
                '21:00', '22:00', '23:00',
            ],
        },
        '{3}/era5_{2}_{0}_{1}.nc'.format(year, month, shortname, output_path))

def scheduled_download(funct, dates, variable, short, output_path):
    N = len(dates)
    Parallel(n_jobs=4)(delayed(funct)
                        (dates[i][1], dates[i][0], variable, short, output_path) for i in range(N))

if __name__ == '__main__':

    variable = '2m_temperature'
    short = 'T2m'
    output_path = '/Users/marialozano/Python/ERA5_data/SLP_MM'

    start_year = 2010
    end_year = datetime.now().year
    start_month = 1
    end_month = 12

    dates = []
    for i in range(start_year, end_year+1):
        for j in range(start_month, end_month+1):
            dates.append(('{:02d}'.format(j), str(i)))

    schedule.every(30).day.at('23:30').do(scheduled_download(download_ERA5_single_levels, dates, variable, short, output_path))
    schedule.clear('daily-tasks')