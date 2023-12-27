from opensky_api import OpenSkyApi
import sqlite3
import time




def get_and_store_data():

    con = sqlite3.connect("opensky.db")
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS aircraft_state (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                icao24 TEXT,
                callsign TEXT,
                origin_country TEXT,
                time_position INTEGER,
                last_contact INTEGER,
                longitude REAL,
                latitude REAL,
                geo_altitude REAL,
                on_ground BOOLEAN,
                velocity REAL,
                true_track REAL,
                vertical_rate REAL,
                sensors TEXT,
                baro_altitude REAL,
                squawk TEXT,
                spi BOOLEAN,
                position_source INTEGER,
                category INTEGER
             )''')




    api = OpenSkyApi()
    s = api.get_states()
    #print(s)


    if s:
        data = s.states

        for record in data:
            icao24 = record.icao24
            callsign = record.callsign
            origin_country = record.origin_country
            time_position = record.time_position
            last_contact = record.last_contact
            longitude = record.longitude
            latitude = record.latitude
            geo_altitude = record.geo_altitude
            on_ground = record.on_ground
            velocity = record.velocity
            true_track = record.true_track
            vertical_rate = record.vertical_rate
            sensors = record.sensors
            baro_altitude = record.baro_altitude
            squawk = record.squawk
            spi = record.spi
            position_source = record.position_source
            category = record.category



            cur.execute('''INSERT INTO aircraft_state (icao24, callsign, origin_country, time_position, last_contact, longitude, latitude,
                                              geo_altitude, on_ground, velocity, true_track, vertical_rate, sensors, baro_altitude,
                                              squawk, spi, position_source, category)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (icao24, callsign, origin_country, time_position, last_contact, longitude, latitude, geo_altitude, on_ground,
               velocity, true_track, vertical_rate, sensors, baro_altitude, squawk, spi, position_source, category))

    con.commit()
    con.close()
    print("Dados armazenados com sucesso!")

get_and_store_data()