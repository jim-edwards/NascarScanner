import csv
import argparse
import gzip
import os
import sys

def read_race_csv(fname):

    csvfile = open(fname, newline='')

    race_data = csv.reader(csvfile, delimiter=',')

    return race_data
    
def generate_Uniden_BC125AT_section(file, race_data, section, channel, primary=True):
    
    file.write(f"Conventional\t{section}\tBank {section}\tOff\n")

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
            
            file.write(f"C-Freq\t{channel}\t{driver}\t{freq}\tAuto\tOff\tOff\t2\tOff\n")    
            channel = channel + 1
    else:
        file.write(f"C-Freq\t{channel}\t\t0\tAuto\tOff\tOff\t2\tOff\n")
        channel = channel + 1

    while (channel % 50) != 1:
        file.write(f"C-Freq\t{channel}\t\t0\tAuto\tOff\tOff\t2\tOff\n")
        channel = channel + 1
    

def generate_Uniden_BC125AT(fname):

    # Output fixed headers
    file = open(fname, "w")

    file.write(f"Misc\tKey\tAuto\tOff\t8\t14\t6\t2\tUSA\n")
    file.write(f"Priority\tOff\n")
    file.write(f"WxPri\tOff\n")
    file.write(f"Service\t1\tPolice\tOff\n")
    file.write(f"Service\t2\tFire/Emergency\tOff\n")
    file.write(f"Service\t3\tHAM Radio\tOff\n")
    file.write(f"Service\t4\tMarine\tOff\n")
    file.write(f"Service\t5\tRailroad\tOff\n")
    file.write(f"Service\t6\tCivil Air\tOff\n")
    file.write(f"Service\t7\tMilitary Air\tOff\n")
    file.write(f"Service\t8\tCB Radio\tOff\n")
    file.write(f"Service\t9\tFRS/GMRS/MURS\tOff\n")
    file.write(f"Service\t10\tRacing\tOff\n")
    file.write(f"Custom\t1\tSearch Bnak1\t25000000\t27995000\tOff\n")
    file.write(f"Custom\t2\tSearch Bnak2\t28000000\t29695000\tOff\n")
    file.write(f"Custom\t3\tSearch Bnak3\t29700000\t49995000\tOff\n")
    file.write(f"Custom\t4\tSearch Bnak4\t50000000\t54000000\tOff\n")
    file.write(f"Custom\t5\tSearch Bnak5\t108000000\t136991600\tOff\n")
    file.write(f"Custom\t6\tSearch Bnak6\t137000000\t143995000\tOff\n")
    file.write(f"Custom\t7\tSearch Bnak7\t144000000\t147995000\tOff\n")
    file.write(f"Custom\t8\tSearch Bnak8\t225000000\t380000000\tOff\n")
    file.write(f"Custom\t9\tSearch Bnak9\t400000000\t449993700\tOff\n")
    file.write(f"Custom\t10\tSearch Bnak10\t450000000\t469993700\tOff\n")
    file.write(f"CloseCall\tDND\tOn\tOn\tOff\n")
    file.write(f"CloseCallBands\tOn\tOn\tOn\tOn\tOn\n")
    file.write(f"GeneralSearch\t2\tOn\n")

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
    
    file.write(f"C-Group\t\t\t\t{section_name}\tOff\t0.000000\t0.000000\t0.0\tCircle\n")

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
        
        file.write(f"C-Freq\t\t\t\t{driver}\tOff\t{freq}\tAUTO\t\t\t217\tOff\t2\t0\tOff\tAuto\n")


def generate_Uniden_HomePatrol_Sentinel(fname, year):

    # Output fixed headers
    file = open(fname, "w")

    file.write(f"TargetModel\tHomePatrol-1\n")
    file.write(f"FormatVersion\t2.04\n")
    file.write(f"Conventional\t\t\t\t{year} Nascar Season\tOff\t\t\tConventional\n")

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
    generate_Uniden_HomePatrol_Sentinel_section(file, race_data, "OReilly Drivers - Primary", True)

    race_data = read_race_csv('src_oreilly_series.csv')
    generate_Uniden_HomePatrol_Sentinel_section(file, race_data, "OReilly Drivers - Backup", False)

    # Output Truck series
    race_data = read_race_csv('src_craftsman_truck.csv')
    generate_Uniden_HomePatrol_Sentinel_section(file, race_data, "Truck Drivers - Primary", True)

    race_data = read_race_csv('src_craftsman_truck.csv')
    generate_Uniden_HomePatrol_Sentinel_section(file, race_data, "Truck Drivers - Backup", False)

    # Final marker line expected by the HomePatrol format/tools
    file.write("File\tHomePatrol Export File\n")
    file.close()


SECRET = 0x0C
def convert_hpd_to_hpe(inpath: str, outpath: str) -> int:
    """Compress and obfuscate an HPD file into an HPE file.

    Returns the number of bytes written to the HPE file.
    """
    if not os.path.isfile(inpath):
        raise FileNotFoundError(f"Input file not found: {inpath}")

    with open(inpath, "rb") as f:
        data = f.read()

    gz_bytes = gzip.compress(data)
    xored = bytes(b ^ SECRET for b in gz_bytes)

    with open(outpath, "wb") as outf:
        outf.write(xored)

    return len(xored)


def generate_CHIRP_csv(fname):
    file = open(fname, "w", newline='')
    writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)

    # Write header in the exact order requested by user
    header = ["Location","Name","Frequency","Duplex","Offset","Tone","rToneFreq","cToneFreq","DtcsCode","DtcsPolarity","RxDtcsCode","CrossMode","Mode","TStep","Skip","Power","Comment","URCALL","RPT1CALL","RPT2CALL","DVCODE"]
    writer.writerow(header)

    location = 1

    def write_series(race_csv, col_index, series_label, series_prefix, primary_only=False):
        nonlocal location
        race_data = read_race_csv(race_csv)
        next(race_data, None)
        for row in race_data:
            driver = row[1]
            freq = row[col_index]
            if freq != '':
                # suffix codes
                if primary_only:
                    suffixes = [("PR", "Primary")]
                else:
                    suffixes = [("PR", "Primary"), ("BK", "Backup")] if col_index != 4 else [("BK", "Backup")]

                for short_suf, full_suf in suffixes:
                    name = f"{series_prefix} {driver} {short_suf}"
                    duplex = ""
                    offset = "0.000000"
                    tone = ""
                    rToneFreq = "88.5"
                    cToneFreq = "88.5"
                    DtcsCode = "023"
                    DtcsPolarity = "NN"
                    RxDtcsCode = "023"
                    CrossMode = "Tone->Tone"
                    Mode = "FM"
                    TStep = "5.00"
                    Skip = ""
                    Power = "5W"
                    Comment = f"{series_label} {driver} {full_suf}"
                    URCALL = ""
                    RPT1CALL = ""
                    RPT2CALL = ""
                    DVCODE = ""

                    writer.writerow([location, name, freq, duplex, offset, tone, rToneFreq, cToneFreq, DtcsCode, DtcsPolarity, RxDtcsCode, CrossMode, Mode, TStep, Skip, Power, Comment, URCALL, RPT1CALL, RPT2CALL, DVCODE])
                    location += 1

    # Race channels - primary only
    write_series('src_race_channels.csv', 2, "Race Channels", "R", primary_only=True)

    # Cup series - primary then backup
    write_series('src_cup_series.csv', 2, "Cup Series", "C", primary_only=True)
    write_series('src_cup_series.csv', 4, "Cup Series", "C", primary_only=False)

    # OReilly series - primary then backup
    write_series('src_oreilly_series.csv', 2, "OReilly Series", "O", primary_only=True)
    write_series('src_oreilly_series.csv', 4, "OReilly Series", "O", primary_only=False)

    # Truck series - primary then backup
    write_series('src_craftsman_truck.csv', 2, "Truck Series", "T", primary_only=True)
    write_series('src_craftsman_truck.csv', 4, "Truck Series", "T", primary_only=False)

    file.close()



def generate_BTECH_GMRS_PRO_csv(year: str):
    # Hard-coded UV Pro / GMRS-PRO CSV header (based on Blank_Import_UV_Pro.csv)
    header = [
        'title',
        'tx_freq',
        'rx_freq',
        'tx_sub_audio(CTCSS=freq/DCS=number)',
        'rx_sub_audio(CTCSS=freq/DCS=number)',
        'tx_power(H/M/L)',
        'bandwidth(12500/25000)',
        'scan(0=OFF/1=ON)',
        'talk around(0=OFF/1=ON)',
        'pre_de_emph_bypass(0=OFF/1=ON)',
        'sign(0=OFF/1=ON)',
        'tx_dis(0=OFF/1=ON)',
        'mute(0=OFF/1=ON)',
        'rx_modulation(0=FM/1=AM)',
        'tx_modulation(0=FM/1=AM)'
    ]

    outdir = os.path.join('BTECH GMRS-PRO')
    os.makedirs(outdir, exist_ok=True)

    def collect_entries(race_csv, col_index, primary_only=False):
        entries = []
        race_data = read_race_csv(race_csv)
        next(race_data, None)
        for row in race_data:
            driver = row[1]
            freq = row[col_index]
            if not freq:
                continue
            try:
                freq_int = int(float(freq) * 1000000)
            except Exception:
                freq_int = ''
            entries.append((driver, freq_int))
        return entries

    def write_chunks(entries, series_key, suffix):
        # split into chunks with 29 real entries; first slot left empty (reserved)
        max_per_file = 29
        if not entries:
            return
        for i in range(0, len(entries), max_per_file):
            chunk = entries[i:i+max_per_file]
            part = (i // max_per_file) + 1
            part_suffix = f"_part{part}" if len(entries) > max_per_file else ""
            filename = f"{year}_{series_key}{suffix}{part_suffix}.csv"
            path = os.path.join(outdir, filename)
            with open(path, 'w', newline='') as out_file:
                writer = csv.writer(out_file)
                writer.writerow(header)
                # Reserve slot 1 by writing an empty row so the first real channel can be filled on-radio
                writer.writerow([''] * len(header))
                for driver, freq_int in chunk:
                    row_out = [driver, freq_int, freq_int, '', '', 'H', '25000', '1', '0', '0', '0', '0', '0', '0', '0']
                    writer.writerow(row_out)

    # Collect and write per-series files
    # Race channels - primary only
    race_entries = collect_entries('src_race_channels.csv', 2, primary_only=True)
    write_chunks(race_entries, 'RaceChannels', '_Primary')

    # Cup series - primary then backup
    cup_primary = collect_entries('src_cup_series.csv', 2, primary_only=True)
    cup_backup = collect_entries('src_cup_series.csv', 4, primary_only=False)
    write_chunks(cup_primary, 'CupSeries', '_Primary')
    write_chunks(cup_backup, 'CupSeries', '_Backup')

    # OReilly series - primary then backup
    xfin_primary = collect_entries('src_oreilly_series.csv', 2, primary_only=True)
    xfin_backup = collect_entries('src_oreilly_series.csv', 4, primary_only=False)
    write_chunks(xfin_primary, 'OReillySeries', '_Primary')
    write_chunks(xfin_backup, 'OReillySeries', '_Backup')

    # Truck series - primary then backup
    truck_primary = collect_entries('src_craftsman_truck.csv', 2, primary_only=True)
    truck_backup = collect_entries('src_craftsman_truck.csv', 4, primary_only=False)
    write_chunks(truck_primary, 'TruckSeries', '_Primary')
    write_chunks(truck_backup, 'TruckSeries', '_Backup')


def main():

    parser = argparse.ArgumentParser(description="Generate Nascar scanner files for a given year")
    parser.add_argument("--year", "-y", required=True,
                        help="Year to use in generated filenames and labels (required)")
    args = parser.parse_args()
    year = args.year
    
    print(f"Generating CHIRP CSV for {year}\n")
    generate_CHIRP_csv(f"CHIRP\\{year}_Nascar_Season.csv")

    print(f"Generating BTECH GMRS-PRO CSV for {year}\n")
    generate_BTECH_GMRS_PRO_csv(year)

    print(f"Generating Uniden BC125AT for {year}\n")
    generate_Uniden_BC125AT(f"Uniden BC125AT\\{year}_Nascar_Season.bc125at_ss")

    print(f"Generating Uniden HomePatrol Sentinel for {year}\n")
    generate_Uniden_HomePatrol_Sentinel(f"Uniden HomePatrol Sentinel\\{year}_Nascar_Season.hpd", year)
    # Convert produced .hpd into obfuscated .hpe and remove .hpd when successful
    inp = f"Uniden HomePatrol Sentinel\\{year}_Nascar_Season.hpd"
    out = f"Uniden HomePatrol Sentinel\\{year}_Nascar_Season.hpe"
    try:
        written = convert_hpd_to_hpe(inp, out)
        try:
            os.remove(inp)
        except Exception as e:
            print(f"Warning: failed to remove {inp}: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Error generating HPE: {e}", file=sys.stderr)
  
if __name__ == "__main__":
    main()
