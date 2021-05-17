# Storm Tracker L0-L1 SHARPpy

Convert Level-0 Storm Tracker data to Level-1 SHARPpy format for skew-T plot using SHARPpy.
The output ascii file can be directly read by SHARPpy for skew-T diagram.

More information on SHARPpy, please see: https://sharppy.github.io/SHARPpy/index.html

## Dependencies

This script uses **pandas** for data management, and **metpy** for calculating meteorological variables.

## How to run?

The scripit is written under python3.

```
python ST_L0_L1_SHARPpy.py [/path/to/ST/file/no_NNNN.csv] [recorded_launch_time_in_YYYYMMDDHHmmss] 
```

Where NNNN is the serial number of the ST.
The input launch time is a 14-digits UTC time from year to second, YYYYMMDDHHmmss.
For example,

```
python3 ST_L0_L1_SHARPpy.py ./Example/no_2968.csv 20210503184852
```
