from models_info_bot import DbSession,DB_LOCATION_TABLE,DB_SHOW_DATES,Progress_V2
from sqlalchemy import select, update,insert
from geopy import distance
import requests


with DbSession() as s: 
    radius_school = 500 #in meter
    radius_seating= 200 #In meter
    radius_padang= 1800 #In meter
    loop_list= s.scalars(select(DB_LOCATION_TABLE)).all()
    for c in loop_list:
        if c.LOCATION_LATITUDE != None:
            Padang_lat , Padang_long = s.execute(select(DB_SHOW_DATES.DROPOFF_LOC_LAT,DB_SHOW_DATES.DROPOFF_LOC_LON).where(DB_SHOW_DATES.School == c.TELE_USER_SCH)).first().tuple()
            School_lat , sch_long = s.execute(select(DB_SHOW_DATES.DROPOFF_LOC_LAT,DB_SHOW_DATES.DROPOFF_LOC_LON).where(DB_SHOW_DATES.School == c.TELE_USER_SCH)).first().tuple()
            Seating_lat = 1.2905923809676245
            Seting_long = 103.8530609909847
            
            current_location=(c.LOCATION_LATITUDE ,c.LOCATION_LONGTITUDE)
            combined_lat_long_Padang=(Padang_lat,Padang_long)
            combiend_lat_long_school=(School_lat,sch_long)
            combined_lat_long_seating=(Seating_lat,Seting_long)
            dis_padang= distance.distance(current_location,combined_lat_long_Padang).m
            dis_school= distance.distance(current_location,combiend_lat_long_school).m
            dis_seating= distance.distance(current_location,combined_lat_long_seating).m
            
            
            if dis_school <= radius_school :
                status = 0 #SET PROGRESS_V2 Table AT SCHOOL
            elif dis_seating <= radius_seating :
                status = 2 #SET PROGRESS_V2 Table AT Seating Gallery
            elif dis_padang <= radius_padang:
                status = 1 #SET PROGRESS_V2 Table AT PADANG
            else:
                status = 3 #SET PROGRESS_V2 Table ENROUTE
            
            check = s.scalar(select(Progress_V2).where(Progress_V2.TELE_USER_ID == c.TELE_USER_ID))
            if check is None :
                s.execute(insert(Progress_V2).values(TELE_USER_ID = c.TELE_USER_ID, TELE_USER_SCH = c.TELE_USER_SCH, STATUS = status))
                s.commit()
            else:
                s.execute(update(Progress_V2).where(Progress_V2.TELE_USER_ID == c.TELE_USER_ID).values(STATUS = status))
                s.commit()
                