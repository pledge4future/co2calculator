import xarray as xr
import os
from fnmatch import fnmatch
import geopandas as gpd

# adapt these file paths
gadm_dir = "/home/salohr/Documents/weather_correction/countries/" 
# "https://github.com/pledge4future/co2calculator/tree/dev-era5download/data/countries"

era5 = "/home/salohr/Documents/weather_correction/adaptor.mars.internal-1653931184.6044545-27675-10-90177a1a-903d-4c14-97ca-8193c514342a.nc"
# upload era5 file

# clip era5 with country geometry
cntry_list = []
for paths, subdirs,files in os.walk(gadm_dir):# go through all subdirectories
    for subdir in subdirs:
        for paths,subdirs,files in os.walk(gadm_dir+subdir):
            [cntry_list.append(gadm_dir+subdir + "/"+ name) for name in files if fnmatch(name, "*0.shp")]
            
for cntry_file in cntry_list:
    # get country geometry: 
    gadm = gpd.read_file(cntry_file)
    geom = gadm.geometry[0]
    
    # open era5 data
    ds = xr.open_dataset(era5)
    ds.rio.set_spatial_dims(x_dim="longitude", y_dim="latitude", inplace=True)
    ds.rio.write_crs("epsg:4326", inplace=True)

    # clip era5 data first with a bbox of the respective cntry and then with the geometry
    if geom.geom_type == 'Polygon':
        clipped = ds.rio.clip_box(minx=geom.bounds[0], miny=geom.bounds[1], maxx=geom.bounds[2], maxy=geom.bounds[3],
                                  auto_expand=True)  # !!!!! make sure to understand the auto_expand function!
        cropped_da = clipped.rio.clip([geom], drop=False)
    elif geom.geom_type == 'MultiPolygon':
        clipped = ds.rio.clip_box(minx=geom.bounds[0], miny=geom.bounds[1], maxx=geom.bounds[2], maxy=geom.bounds[3],
                                  auto_expand=True)  # !!!!! make sure to understand the auto_expand function!
        cropped_da = clipped.rio.clip(geom, drop=False)
    else:
        print("Unknown geometry type:", geom)
    
    # save cropped cntry-specific era5 file
    cropped_da.to_netcdf(cntry_file[:-6]+"_era5.nc")
