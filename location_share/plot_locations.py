'''
This code is part of the publication "Who Let The Trolls Out? Towards Understanding State-Sponsored Trolls" (https://arxiv.org/abs/1811.03130).
If you use this code please cite the publication.
'''


from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import json 

# Requirements
#sudo apt-get install libgeos-3.5.0
#sudo apt-get install libgeos-dev
#sudo pip install https://github.com/matplotlib/basemap/archive/master.zip


russians_df_all = pd.read_csv('../data/ira_tweets_csv_hashed.csv')
iranians_df_all = pd.read_csv('./data/iranian_tweets_csv_hashed.csv')
russians_df_all['datetime'] = pd.to_datetime(russians_df_all['tweet_time'])
iranians_df_all['datetime'] = pd.to_datetime(iranians_df_all['tweet_time'])

unique_locations = []
with open('./russians_locations.txt', 'r') as f:
    for line in f:
        unique_locations.append(line.replace('\n', ''))
unique_locations_random = []
with open('./iranians_locations.txt', 'r') as f:
    for line in f:
        unique_locations_random.append(line.replace('\n', ''))

geographic_locations = []
with open('./russians_locations_geo.txt', 'r') as f:
    for line in f:
        data = json.loads(line)
        try:
            lat = data['lat']
            lon = data['lon']
            name = data['country']
            geographic_locations.append((lat, lon, name))
        except Exception as e :
            geographic_locations.append(('False', 'False', 'False'))

geographic_locations_random = []
with open('./iranians_locations_geo.txt', 'r') as f:
    for line in f:
        try:
            data = json.loads(line)
            lat = data['lat']
            lon = data['lon']
            name = data['country']
            geographic_locations_random.append((lat, lon, name))
        except Exception as e :
            geographic_locations_random.append(('False', 'False', 'False'))
print("Done loading data....")
def plot_locations_agg(df1,df2, path, color1, color2):
    lat = df1['gmaps_lat'].values
    lon = df1['gmaps_lon'].values
    sizes = df1['num_entries']
    sizes2 = [x*0.005 for x in sizes]
    
    lat2 = df2['gmaps_lat'].values
    lon2 = df2['gmaps_lon'].values
    sizes3 = df2['num_entries']
    sizes4 = [x*0.01 for x in sizes3]
    
    lat_min =-47.8656149
    lat_max =66.8965684
    lon_min =-136.5831791
    lon_max =162.156194

    plt.figure(figsize=(24,12))
    # create map using BASEMAP
    m = Basemap(llcrnrlon=lon_min,
                llcrnrlat=lat_min,
                urcrnrlon=lon_max,
                urcrnrlat=lat_max,
                lat_0=(lat_max - lat_min)/2,
                lon_0=(lon_max-lon_min)/2,
                projection='merc',
                resolution = 'i',
                area_thresh=10000.,
                )
    #m.drawcoastlines()
    m.drawcountries()
    #m.drawstates()
    m.drawmapboundary(fill_color='#CEE2FD')
    m.fillcontinents(color = '#FFFFFF',lake_color='#CEE2FD')


    # convert lat and lon to map projection coordinates
    lons, lats = m(lon, lat)
    lons2, lats2 = m(lon2, lat2)
    # plot points as red dots
    m.scatter(lons2, lats2, sizes4, marker = '^', color=color2, zorder=5, alpha=0.5)
    m.scatter(lons, lats, sizes2, marker = 'o', color=color1, zorder=5, alpha=0.5)

    #m.scatter(lons, lats, sizes2, marker = 'o', color='#008e2a', zorder=5)

    plt.savefig(path, bbox_inches='tight')
    #plt.show()


def map_lat(loc):
    try:
        idx = unique_locations.index(loc)
        return geographic_locations[idx][0]
    except:
        return 'False'

def map_lng(loc):
    try:
        idx = unique_locations.index(loc)
        return geographic_locations[idx][1]
    except:
        return 'False'
def map_geo_name(loc):
    try:
        idx = unique_locations.index(loc)
        return geographic_locations[idx][2]
    except:
        return 'False'
    
def map_lat_r(loc):
    try:
        idx = unique_locations_random.index(loc)
        return geographic_locations_random[idx][0]
    except:
        return 'False'

def map_lng_r(loc):
    try:
        idx = unique_locations_random.index(loc)
        return geographic_locations_random[idx][1]
    except:
        return 'False'
def map_geo_name_r(loc):
    try:
        idx = unique_locations_random.index(loc)
        return geographic_locations_random[idx][2]
    except:
        return 'False'


russians_df_all['gmaps_lat'] = russians_df_all['user_reported_location'].map(map_lat)
russians_df_all['gmaps_lon'] = russians_df_all['user_reported_location'].map(map_lng)
russians_df_all['gmaps_location_name'] = russians_df_all['user_reported_location'].map(map_geo_name)

iranians_df_all['gmaps_lat'] = iranians_df_all['user_reported_location'].map(map_lat_r)
iranians_df_all['gmaps_lon'] = iranians_df_all['user_reported_location'].map(map_lng_r)
iranians_df_all['gmaps_location_name'] = iranians_df_all['user_reported_location'].map(map_geo_name_r)

def run_on_dataframes(russians, iranians, path):

    locationsdf = russians[russians.gmaps_lat!='False']
    locationsdf = locationsdf[['gmaps_lat','gmaps_lon','gmaps_location_name']]
    groups_locations = locationsdf.groupby(['gmaps_lat','gmaps_lon','gmaps_location_name']).aggregate(len).reset_index().rename(columns={0: "num_entries"})

    locationsdf_r = iranians[iranians.gmaps_lat!='False']
    locationsdf_r = locationsdf_r[['gmaps_lat','gmaps_lon','gmaps_location_name']]
    groups_locations_r = locationsdf_r.groupby(['gmaps_lat','gmaps_lon','gmaps_location_name']).aggregate(len).reset_index().rename(columns={0: "num_entries"})


    plot_locations_agg(groups_locations, groups_locations_r, path, '#e00000' ,'#005e0d' )

run_on_dataframes(russians_df_all, iranians_df_all, './locations_map_agg_russians_iranians.pdf')
