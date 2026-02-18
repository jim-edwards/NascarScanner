NASCAR Driver and Officials Frequencies

Sources: 
* https://wiki.radioreference.com/index.php/NASCAR
* https://www.speedwaydigest.com/index.php/scanner-frequencies/nascar-cup-series-frequencies

# BC125AT

Use the BC125AT Software.  Go to File->Open, select the file/season and it will set all the banks.

# HomePatrol Sentinel

Use the HomePatrol Software.  Copy the file to your settings folder, found in Tools->Settings.  Default is C:\Users\<user>\Documents\Uniden\HomePatrol\FavoritesList.  Rename the file so it fits the list file format, or modify to suite.

# Generation instructions

## HTML -> CSV

`python .\html_to_csv.ph --html .\src_speedwaydigest_nascar_cup.html --csv .\src_cup_series.csv`

Manually copy the race channels to src_race_channels.csv

`python .\html_to_csv.ph --html .\src_speedwaydigest_nascar_oreilly.html --csv .\src_oreilly_series.csv`

Manually remove and verify the race channels match src_race_channels.csv

`python .\html_to_csv.ph --html .\craftsman_truck.html --csv .\src_craftsman_truck.csv`

Manually remove and verify the race channels match src_race_channels.csv

## CSV -> Scanner files

`python .\generate_all.py --year 2026`
