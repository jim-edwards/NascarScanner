import csv
import argparse

def read_race_csv(fname):

    csvfile = open(fname, newline='')

    race_data = csv.reader(csvfile, delimiter=',')

    return race_data
    
def generate_Uniden_BC125AT_section(file, race_data, section, channel, primary=True):
    
    file.write(f"Conventional	{section}	Bank {section}	Off\n")

    if(race_data != None):
        next(race_data, None)
        for row in race_data:
            driver = row[1]
            if( primary ):
                freq = row[2]
            else:
                freq = row[4]

            # Assume decimal for freq
            if(freq != ''):
                freq = int(float(freq) * 1000000)
            
            file.write(f"C-Freq	{channel}	{driver}	{freq}	Auto	Off	Off	2	Off\n")    
            channel = channel + 1
    else:
        file.write(f"C-Freq	{channel}		0	Auto	Off	Off	2	Off\n")
        channel = channel + 1

    while (channel % 50) != 1:
        file.write(f"C-Freq	{channel}		0	Auto	Off	Off	2	Off\n")
        channel = channel + 1
    

def generate_Uniden_BC125AT(fname):

    # Output fixed headers
    file = open(fname, "w")

    file.write(f"Misc	Key	Auto	Off	8	14	6	2	USA\n")
    file.write(f"Priority	Off\n")
    file.write(f"WxPri	Off\n")
    file.write(f"Service	1	Police	Off\n")
    file.write(f"Service	2	Fire/Emergency	Off\n")
    file.write(f"Service	3	HAM Radio	Off\n")
    file.write(f"Service	4	Marine	Off\n")
    file.write(f"Service	5	Railroad	Off\n")
    file.write(f"Service	6	Civil Air	Off\n")
    file.write(f"Service	7	Military Air	Off\n")
    file.write(f"Service	8	CB Radio	Off\n")
    file.write(f"Service	9	FRS/GMRS/MURS	Off\n")
    file.write(f"Service	10	Racing	Off\n")
    file.write(f"Custom	1	Search Bnak1	25000000	27995000	Off\n")
    file.write(f"Custom	2	Search Bnak2	28000000	29695000	Off\n")
    file.write(f"Custom	3	Search Bnak3	29700000	49995000	Off\n")
    file.write(f"Custom	4	Search Bnak4	50000000	54000000	Off\n")
    file.write(f"Custom	5	Search Bnak5	108000000	136991600	Off\n")
    file.write(f"Custom	6	Search Bnak6	137000000	143995000	Off\n")
    file.write(f"Custom	7	Search Bnak7	144000000	147995000	Off\n")
    file.write(f"Custom	8	Search Bnak8	225000000	380000000	Off\n")
    file.write(f"Custom	9	Search Bnak9	400000000	449993700	Off\n")
    file.write(f"Custom	10	Search Bnak10	450000000	469993700	Off\n")
    file.write(f"CloseCall	DND	On	On	Off\n")
    file.write(f"CloseCallBands	On	On	On	On	On\n")
    file.write(f"GeneralSearch	2	On\n")

    # Output race channels
    section = 1
    channel = 1
    race_data = read_race_csv('src_race_channels.csv')

    generate_Uniden_BC125AT_section(file, race_data, section, channel, True)
    channel += 50
    section += 1

    # Output cup series
    race_data = read_race_csv('src_cup_series.csv')
    generate_Uniden_BC125AT_section(file, race_data, section, channel, True)
    channel += 50
    section += 1

    race_data = read_race_csv('src_cup_series.csv')
    generate_Uniden_BC125AT_section(file, race_data, section, channel, False)
    channel += 50
    section += 1

    # Output OReilly series
    race_data = read_race_csv('src_oreilly_series.csv')
    generate_Uniden_BC125AT_section(file, race_data, section, channel, True)
    channel += 50
    section += 1

    race_data = read_race_csv('src_oreilly_series.csv')
    generate_Uniden_BC125AT_section(file, race_data, section, channel, False)
    channel += 50
    section += 1

    # Output Truck series
    race_data = read_race_csv('src_craftsman_truck.csv')
    generate_Uniden_BC125AT_section(file, race_data, section, channel, True)
    channel += 50
    section += 1

    race_data = read_race_csv('src_craftsman_truck.csv')
    generate_Uniden_BC125AT_section(file, race_data, section, channel, False)
    channel += 50
    section += 1

    # Final empty sections
    generate_Uniden_BC125AT_section(file, None, section, channel, False)
    channel += 50
    section += 1
    generate_Uniden_BC125AT_section(file, None, section, channel, False)
    channel += 50
    section += 1
    generate_Uniden_BC125AT_section(file, None, section, channel, False)
    channel += 50
    section += 1

    file.close()



def generate_Uniden_HomePatrol_Sentinel_section(file, race_data, section_name, primary=True):
    
    file.write(f"C-Group			{section_name}	Off	0.000000	0.000000	0.0	Circle\n")

    next(race_data, None)
    for row in race_data:
        driver = row[1]
        if( primary ):
            freq = row[2]
        else:
            freq = row[4]

        # Assume decimal for freq
        if(freq != ''):
            freq = int(float(freq) * 1000000)
        else:
            freq = 0
        # !!TODO!! Freq of 0 doesn't load!
        
        file.write(f"C-Freq			{driver}	Off	{freq}	AUTO		217	Off	2	0	Off	Auto\n")


def generate_Uniden_HomePatrol_Sentinel(fname, year):

    # Output fixed headers
    file = open(fname, "w")

    file.write(f"TargetModel\tHomePatrol-1\n")
    file.write(f"FormatVersion\t2.04\n")
    file.write(f"Conventional\t\t\t{year} Nascar Season\tOff\t\tConventional\n")

    # Output race channels
    race_data = read_race_csv('src_race_channels.csv')

    generate_Uniden_HomePatrol_Sentinel_section(file, race_data, "Race Channels", True)

    # Output cup series
    race_data = read_race_csv('src_cup_series.csv')
    generate_Uniden_HomePatrol_Sentinel_section(file, race_data, "Cup Drivers - Primary", True)

    race_data = read_race_csv('src_cup_series.csv')
    generate_Uniden_HomePatrol_Sentinel_section(file, race_data, "Cup Drivers - Backup", False)

    # Output OReilly series
    race_data = read_race_csv('src_oreilly_series.csv')
    generate_Uniden_HomePatrol_Sentinel_section(file, race_data, "Xfinity Drivers - Primary", True)

    race_data = read_race_csv('src_oreilly_series.csv')
    generate_Uniden_HomePatrol_Sentinel_section(file, race_data, "Xfinity Drivers - Backup", False)

    # Output Truck series
    race_data = read_race_csv('src_craftsman_truck.csv')
    generate_Uniden_HomePatrol_Sentinel_section(file, race_data, "Truck Drivers - Primary", True)

    race_data = read_race_csv('src_craftsman_truck.csv')
    generate_Uniden_HomePatrol_Sentinel_section(file, race_data, "Truck Drivers - Backup", False)

    file.close()


def main():

    parser = argparse.ArgumentParser(description="Generate Nascar scanner files for a given year")
    parser.add_argument("--year", "-y", required=True,
                        help="Year to use in generated filenames and labels (required)")
    args = parser.parse_args()
    year = args.year

    print(f"Generating Uniden BC125AT for {year}\n")
    generate_Uniden_BC125AT(f"Uniden BC125AT\\{year}_Nascar_Season.bc125at_ss")

    print(f"Generating Uniden HomePatrol Sentinel for {year}\n")
    generate_Uniden_HomePatrol_Sentinel(f"Uniden HomePatrol Sentinel\\{year}_Nascar_Season.hpd", year)

if __name__ == "__main__":
    main()