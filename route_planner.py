import pySBB
import googlemaps

from datetime import datetime, timedelta


gmaps = googlemaps.Client(key='AIzaSyA7np_5xrO87IWaW8GgKENp5q7bO-x_DxE')

geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))


def get_timestamp_7am():
    # Get today's datetime
    dtnow = datetime.now()

    # Create datetime variable for 6 AM
    dt6 = None

    # If today's hour is < 6 AM
    if dtnow.hour < 7:

        # Create date object for today's year, month, day at 6 AM
        dt6 = datetime(dtnow.year, dtnow.month, dtnow.day, 7, 0, 0, 0)

    # If today is past 6 AM, increment date by 1 day
    else:

        # Get 1 day duration to add
        day = timedelta(days=1)

        # Generate tomorrow's datetime
        tomorrow = dtnow + day

        # Create new datetime object using tomorrow's year, month, day at 6 AM
        dt6 = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 7, 0, 0, 0)

    # Create timestamp from datetime object
    # timestamp = time.mktime(dt6.timetuple())

    # print(timestamp)
    return dt6



def EstimateCommuteTime(apartments):
    idx = 0
    for idx in range(len(apartments)):

        adr = apartments['address'][idx]
        # print(idx, adr)

        #  ToDO: set departure time for sbb
        # Commute to Mellingen
        try:
            connections = pySBB.get_connections(adr, 'Mellingen Heitersberg')
            commute_mell = sorted(connections, key=lambda x: x.duration.seconds)[0].duration.seconds / 60.
            apartments['T_mellingen'][idx] = commute_mell

            # Commute to DECTRIS
            connections = pySBB.get_connections(adr, '5405 Dättwil AG, Täfernweg 1')
            commute_dectris = sorted(connections, key=lambda x: x.duration.seconds)[0].duration.seconds / 60.
            apartments['T_dectris'][idx] = commute_dectris
        except IndexError:
            apartments['T_mellingen'][idx] = 100
            apartments['T_dectris'][idx] = 100
            # idx-=1
            # continue
        except ValueError:  # occurs when number of search limits reached
            directions_result = gmaps.directions(adr,
                                                 'Mellingen Heitersberg',
                                                 mode="transit",
                                                 departure_time=get_timestamp_7am())
            try:
                commute_mell = directions_result[0]['legs'][0]['duration']['value'] / 60
                apartments['T_mellingen'][idx] = commute_mell

                directions_result = gmaps.directions(adr,
                                                     '5405 Dättwil AG, Täfernweg 1',
                                                     mode="transit",
                                                     departure_time=get_timestamp_7am())

                commute_dectris = directions_result[0]['legs'][0]['duration']['value'] / 60
                apartments['T_dectris'][idx] = commute_dectris

            except IndexError:
                apartments['T_mellingen'][idx] = 100
                apartments['T_dectris'][idx] = 100

        # By car to Kontrol Systeme
        directions_result = gmaps.directions(adr,
                                             "Blumentalstrasse 10, 8707 Uetikon am See",
                                             mode="driving",
                                             departure_time=get_timestamp_7am())

        t_drive_work = directions_result[0]['legs'][0]['duration']['value'] / 60
        apartments['T_ks'][idx] = t_drive_work

        # By car to BMS
        directions_result = gmaps.directions(adr,
                                             "Krämerackerstrasse 15, 8610 Uster",
                                             mode="driving",
                                             departure_time=get_timestamp_7am())

        t_drive_school = directions_result[0]['legs'][0]['duration']['value'] / 60
        apartments['T_bms'][idx] = t_drive_school

        apartments['T_total_dectris'][idx] = apartments['T_dectris'][idx] + t_drive_school + t_drive_work
        apartments['T_total_mellingen'][idx] = apartments['T_mellingen'][idx] + t_drive_school + t_drive_work

        idx += 1

    return apartments

# print(apartments)

# Marking too long connections
def evaluateCommutes(apartments):
    naprts = len(apartments)
    # naprts = 2
    for iaprt in range(naprts):
        if apartments['T_ks'].values[iaprt] > 40 or apartments['T_bms'].values[iaprt] > 40 or apartments['T_mellingen'].values[iaprt] > 60:
            apartments['option'].values[iaprt] = False
        else:
            apartments['option'].values[iaprt] = True
    return apartments
