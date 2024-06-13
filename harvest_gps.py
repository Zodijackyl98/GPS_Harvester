import serial
import pynmea2
import pandas as pd
import numpy as np
from datetime import datetime

# Open serial port
ser = serial.Serial('/dev/serial0', 9600, timeout=2)

# set_rate_5hz = b'\xB5\x62\x06\x08\x06\x00\x64\x00\x01\x00\x01\x00\x7A\x12'
# ser.write(set_rate_5hz)

main_dict = {'GNGGA_Latitude': [],
             'GNGGA_Longitude': [],
             'GNGGA_Time': [],
             'GNGGA_Altitude': [],
             'GNGGA_Fix_Q': [],
             'GNRMC_Speed': [],
             'GNRMC_Course': [],
             'GNRMC_Time': [],
             'GNRMC_Longitude': [],
             'GNRMC_Latitude': [],
             'GNRMC_Date': [],
             'GPGSA_Mode1': [],
             'GPGSA_Mode2': [],
             'GPGSA_Satellites_Used': [],
             'GPGSA_No_Satellites': [],
             'GPGSA_PDOP': [],
             'GPGSA_HDOP': [],
             'GPGSA_VDOP': [],
             'GPGSV_Num_Sentences': [],
             'GPGSV_Sentence_Number': [],
             'GPGSV_Satellites_in_View': []
            }

count_list = []

def convert_to_decimal(coord_str):
    # Split the coordinate string into degrees and minutes

    coord_str = ''.join([''.join(i.replace(' ', '')) for i in coord_str])[:-1]
    
    if coord_str.startswith("0") == True:
        coord_str = coord_str[1:]
    else:
        pass
    try:
        #coord_str = ''.join(i for i in coord_str if i.startswith)
        if coord_str[2] == "0":
            degrees = float(coord_str[:2])
            minutes = float(coord_str[3:])
        else:
            degrees = float(coord_str[:2])
            minutes = float(coord_str[2:])

        # Convert minutes to decimal degrees
        decimal_degrees = (degrees) + (minutes / 60.0)
        return decimal_degrees
    
    except IndexError:
        # print('Returnin nan values to coordnates')
        return np.nan

try:
    while True: #condition can be put
        # time.sleep(0.2) #5Hz
        line = ser.readline().decode('ascii', errors = 'replace').strip()
        # print(line)

        if line.startswith('$GNGGA'):
            try:
                msg = pynmea2.parse(line)
                timestamp = msg.timestamp
                latitude = convert_to_decimal(f"{msg.lat} {msg.lat_dir}")
                longitude = convert_to_decimal(f"{msg.lon} {msg.lon_dir}")
                altitude = f"{msg.altitude} {msg.altitude_units}"
                Fix_Quality = msg.gps_qual

                main_dict['GNGGA_Latitude'].append(latitude)
                main_dict['GNGGA_Longitude'].append(longitude)
                main_dict['GNGGA_Time'].append(timestamp)
                main_dict['GNGGA_Altitude'].append(altitude)
                main_dict['GNGGA_Fix_Q'].append(Fix_Quality)

                print('Fix Q = ', Fix_Quality, ' Altitude = ', altitude)


            except pynmea2.ParseError as e:
                print(f"Parse error: {e}")

        if line.startswith('$GNRMC'):
            try:
                msg = pynmea2.parse(line)
                latitude = convert_to_decimal(f"{msg.lat} {msg.lat_dir}")
                longitude = convert_to_decimal(f"{msg.lon} {msg.lon_dir}")
                timestamp = msg.timestamp
                speed = msg.spd_over_grnd
                course = msg.true_course
                date = msg.datestamp
                
                main_dict['GNRMC_Latitude'].append(latitude)
                main_dict['GNRMC_Longitude'].append(longitude)
                main_dict['GNRMC_Time'].append(timestamp)
                main_dict['GNRMC_Speed'].append(speed)
                main_dict['GNRMC_Course'].append(course)
                main_dict['GNRMC_Date'].append(date)

                print("GNRMC", timestamp)

            except pynmea2.ParseError as e:
                print(f"Parse error: {e}")

        elif line.startswith('$GPGSA'):
            try:
                msg = pynmea2.parse(line)
                satellites_used = [getattr(msg, f"sv_id{i:02d}", "") for i in range(1, 13)]
                main_dict['GPGSA_Mode1'].append(msg.mode)
                # 1: No fix
                # 2: 2D fix (only horizontal position is known)
                # 3: 3D fix (both horizontal and vertical positions are known)
                main_dict['GPGSA_Mode2'].append(msg.mode_fix_type)
                main_dict['GPGSA_Satellites_Used'].append(','.join(filter(None, satellites_used)))
                no_of_sat = len(','.join(filter(None, satellites_used)).split(','))
                main_dict['GPGSA_No_Satellites'].append(no_of_sat)
                main_dict['GPGSA_PDOP'].append(msg.pdop)
                main_dict['GPGSA_HDOP'].append(msg.hdop)
                main_dict['GPGSA_VDOP'].append(msg.vdop)
        
                print('Mode = ', msg.mode, ' Mode Fix Type = ', msg.mode_fix_type, ' No. of Sat = ', no_of_sat, sep = '' )
                print(50*'-')

            except pynmea2.ParseError as e:
                print(f"Parse error: {e}")

        # elif line.startswith('$GPGSV'):
        #     try:
        #         msg = pynmea2.parse(line)
        #         num_sentences = msg.num_messages
        #         sentence_number = msg.msg_num
        #         satellites_in_view = msg.num_sv_in_view

        #         main_dict['GPGSV_Num_Sentences'].append(num_sentences)
        #         main_dict['GPGSV_Sentence_Number'].append(sentence_number)
        #         main_dict['GPGSV_Satellites_in_View'].append(satellites_in_view)
                
        #         print(msg.data)

                # Parse the satellites data
                # for i in range(4, len(msg.data), 4):
                #     prn = msg.data[i]
                #     elev = msg.data[i + 1]
                #     azim = msg.data[i + 2]
                #     snr = msg.data[i + 3]

                #     main_dict['prn_snr'].append((prn,snr))

                #     main_dict['GPGSV_Satellite_PRN'].append(prn)
                #     main_dict['GPGSV_Satellite_Elevation'].append(elev)
                #     main_dict['GPGSV_Satellite_Azimuth'].append(azim)
                #     main_dict['GPGSV_Satellite_SNR'].append(snr)

                    

            # except IndexError:
            #     print("Index error while parsing SNR value. Skipping this satellite.")

            # except pynmea2.ParseError as e:
            #     print(f"Parse error: {e}")

        # elif line.startswith('$BDGSV'):
        #     try:
        #         msg = pynmea2.parse(line)
        #         num_messages = msg.data[0]
        #         msg_num = msg.data[1]
        #         num_sv = msg.data[2]
        #         satellites = []
        #         for i in range(3, len(msg.data), 4):
        #             prn = msg.data[i]
        #             elev = msg.data[i + 1]
        #             azim = msg.data[i + 2]
        #             snr = msg.data[i + 3]
        #             satellites.append({
        #                 "Satellite PRN": prn,
        #                 "Elevation": elev,
        #                 "Azimuth": azim,
        #                 "SNR": snr
        #             })

                
        #     except pynmea2.ParseError as e:
        #         print(f"Parse error: {e}")
        
            try:
                time_format = "%Y-%m-%dT%H:%M:%S.%f"
                start_time = datetime.strptime(datetime.now().isoformat(), time_format)

                df_main = pd.DataFrame(main_dict)
                df_main.to_csv("./df_main.csv", index=True, header = True, sep = '\t')

                end_time = datetime.strptime(datetime.now().isoformat(), time_format)
                # print(end_time - start_time)

            except ValueError:
                col_list = ' '.join(list(main_dict.keys())).split(' ')
                
                for i in col_list:
                    count_list.append((i,len(main_dict[i])))


                max_num = max([i[1] for i in count_list])
                missing_value = list(set([i[1] for i in count_list if i[1] < max_num]))[0]
                cols_to_nan = [i[0] for i in count_list if i[1] == missing_value]

                # print(count_list, max_num, missing_value, cols_to_nan, end = 5*'\n')
                
                count_list.clear()
                
                for i in cols_to_nan:
                    main_dict[i].append(np.nan)

                # print(max_num - missing_value)

                # for key, value in main_dict.items():
                #     print(f"Length of {key}: {len(value)}")
                time_format = "%Y-%m-%dT%H:%M:%S.%f"
                start_time = datetime.strptime(datetime.now().isoformat(), time_format)
                df_main = pd.DataFrame(main_dict)
                df_main.to_csv("./df_main.csv", index=True, header = True, sep = '\t')
                end_time = datetime.strptime(datetime.now().isoformat(), time_format)
                interval = end_time - start_time
                # 
                # sprint(interval)

                    
except KeyboardInterrupt:
    ser.close()

# except IndexError:
    # df_main.to_csv("./df_main_5hz.csv", index=False, header = True, sep = '\t')
    # print('Check Antenna')

# Create a DataFrame from the list of dictionaries
# Save the DataFrame to a CSV file
