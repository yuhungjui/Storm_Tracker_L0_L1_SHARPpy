"""
Convert Level-0 Storm Tracker data to Level-1 SHARPpy format for skew-T plot using SHARPpy.

Hungjui Yu
20200517
"""

# %%
import pandas as pd
from datetime import datetime 
import pytz
from metpy.calc import dewpoint_from_relative_humidity
from metpy.units import units

# %%
# Set ST node number:

ST_no = 2968

# %%
# Set ST launch time (UTC):

launch_time_from_log = '20210503184852'

# %%
# Specified timezones:

# pytz.all_timezones
tz_utc = pytz.timezone('UTC')
tz_fc = pytz.timezone('US/Mountain')

# %%
# Specified the launch time in UTC:

launch_time = datetime.strptime(launch_time_from_log, '%Y%m%d%H%M%S')
launch_time_utc = tz_utc.localize(launch_time)

# %%
# Load raw data:
L0_raw_data = pd.read_csv('../L0/' + launch_time_from_log[:8] + '/no_{}.csv'.format(ST_no))

# %%
# Convert the data time to datetime object:

L0_raw_data['Time'] = pd.to_datetime(L0_raw_data['Time'], utc=tz_utc)

# %%
# Calculate dew-point temperature in raw data:

L0_raw_data['dT(degC)'] = dewpoint_from_relative_humidity((L0_raw_data['Temperature(degree C)'].to_numpy() * units.degC).to(units.K), L0_raw_data['Humidity(%)'].to_numpy() / 100.)

# %%
# Convert wind speed in raw data:

L0_raw_data['WS(kts)'] = (L0_raw_data['Speed(km/hr)'].to_numpy() * units.kilometer_per_hour).to(units.knot)

# %%
# Convert wind direction in raw data:

L0_raw_data.loc[L0_raw_data['Direction(degree)'] <= 180, 'WDIR'] = L0_raw_data['Direction(degree)'] + 180
L0_raw_data.loc[L0_raw_data['Direction(degree)'] > 180, 'WDIR'] = L0_raw_data['Direction(degree)'] - 180
L0_raw_data.loc[L0_raw_data['Speed(km/hr)'] == 0, 'WDIR'] = 0

# %%
# Find the launch time in ST Time:

L1_data_sharppy = L0_raw_data[L0_raw_data['Time'] >= launch_time_utc][ \
                                                                      ['Pressure(hPa)', \
                                                                       'Height(m)', \
                                                                       'Temperature(degree C)', \
                                                                       'dT(degC)', \
                                                                       'WDIR', \
                                                                       'WS(kts)'] \
                                                                     ]

# %%
# Output L1 data (ascii format):

L1_sharppy_filename = 'no_{}_L1_sharppy.txt'.format(ST_no)

with open(L1_sharppy_filename, 'w') as file:
    
    file.write('%TITLE%\n')
    file.write(' CSU-PRECIP-ST-{}'.format(ST_no) + ' ' + launch_time_from_log[2:8] + '/' + launch_time_from_log[8:12] + '\n')
    file.write('\n')
    file.write('   LEVEL       HGHT       TEMP       DWPT       WDIR       WSPD\n')
    file.write('-------------------------------------------------------------------\n')
    file.write('%RAW%\n')

L1_data_sharppy.to_csv(L1_sharppy_filename, mode='a', header=False, index=False)
    
with open(L1_sharppy_filename, 'a') as file:
      
    file.write('%END%')