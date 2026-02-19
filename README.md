NASCAR Driver and Officials Frequencies

Sources: 
* https://wiki.radioreference.com/index.php/NASCAR
* https://www.speedwaydigest.com/index.php/scanner-frequencies/nascar-cup-series-frequencies

# BC125AT

Use the BC125AT Software.  Go to File->Open, select the file/season and it will set all the banks.

# HomePatrol Sentinel

Use the HomePatrol Software.  Got to File->Import from HPE file.

# CHiRP

1. Use the CHiRP software to read an img from the existing radio.
2. Open the Year_Nascar_Season.csv file in CHiRP
3. Select all the desired rows, then right click and copy
4. Select the first row and paste, it will overwrite all values under it

# BTECH GMRS-PRO

1. Copy ALL the CSV files to your Android / iPhone
2. Click on Device Settings -> Channel and Groups
3. Click Import -> File
4. Import each file (device has a limit of 30 channels per group, and I left 1 channel at the top to put your commmunications on)


# Generation instructions

The following instructions are used to process the incoming CSV files into each individual radios format.

## HTML -> CSV

`python tools\html_to_csv.ph --html .\src_speedwaydigest_nascar_cup.html --csv .\src_cup_series.csv`

Manually copy the race channels to src_race_channels.csv

`python tools\html_to_csv.ph --html .\src_speedwaydigest_nascar_oreilly.html --csv .\src_oreilly_series.csv`

Manually remove and verify the race channels match src_race_channels.csv

`python tools\html_to_csv.ph --html .\craftsman_truck.html --csv .\src_craftsman_truck.csv`

Manually remove and verify the race channels match src_race_channels.csv

## CSV -> Scanner files

`python tools\generate_all.py --year 2026`
