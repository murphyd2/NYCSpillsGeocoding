# NYCSpillsGeocoding
Parsing through a csv files ~2270 lines long that consists of addresses (mixed int and str characters) spaces between ints and non alphanumeric characters between any of the above. Does this and merge sorts the addresses for every borough in NYC to find matching addresses.
The basic csv files for all addresses in NYC are BK, BX,QN, SI, MN, *_PLUTO.csv the original files can be found at 
https://www1.nyc.gov/site/planning/data-maps/open-data/dwn-pluto-mappluto.page
I highly recommend you take a look at the data dictionary, very helpful for thinking of how to approach PLUTO's huge data.

Spills_Workfile is where I sourced all the petroleum spill addresses.

Files in the order they should be run:
  expandspill.py
  merge.py
  BinSearch.py
  
  
