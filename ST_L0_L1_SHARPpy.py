# %%
"""

<br>
Transform Storm Tracker L0 data to L1 SHARPpy format file.<br>
Hungjui Yu<br>
20200504<br>

"""

# %%
import pandas as pd
from datetime import datetime 
import pytz
# import metpy.calc as mpcalc
from metpy.calc import dewpoint_from_relative_humidity
from metpy.units import units

# %%
# Set ST node number:

ST_no = 2968

# %%
# Set ST launch time (UTC):

launch_time_from_log = '20210503184852'

# Specified timezones:

# pytz.all_timezones
tz_utc = pytz.timezone('UTC')
tz_fc = pytz.timezone('US/Mountain')

# Specified the launch time in UTC:

launch_time = datetime.strptime(launch_time_from_log, '%Y%m%d%H%M%S')
launch_time_utc = tz_utc.localize(launch_time)

print(launch_time_utc)

# %%
# Load raw data:
L0_raw_data = pd.read_csv('../L0/no_{}.csv'.format(ST_no))

# L0_raw_data['Time']

# %%
# Convert the data time to datetime object:

# print(L0_raw_data['Time'])
# print(L0_raw_data.info())

L0_raw_data['Time'] = pd.to_datetime(L0_raw_data['Time'], utc=tz_utc)

# print(L0_raw_data.info())
print(L0_raw_data['Time'][0])

# %%
# Calculate dew-point temperature in raw data:

# dewpoint_from_relative_humidity((np.array(temp) * units.degC).to(units.K), np.array(rh) / 100.)

# %%
# Find the launch time in ST Time:

# L0_data = L0_raw_data[['Pressure(hPa)', 'Temperature(degree C)']]
L0_data = L0_raw_data[L0_raw_data['Time'] >= launch_time_utc][['Pressure(hPa)', 'Temperature(degree C)']]

print(L0_data)

# %%
# 