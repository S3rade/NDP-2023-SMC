from models_info_bot import DbSession,DB_LOCATION_TABLE,DB_SHOW_DATES
from sqlalchemy import select, update
from geopy import distance
import requests


with DbSession() as s: 
    radius =1 #in kilometer
    loop_list= s.scalars(select(DB_LOCATION_TABLE)).all()
    for c in loop_list:
        if c.LOCATION_LATITUDE is not None:
            if c.DESTINATION_LOCATION == "Padang":
                lat , long = s.execute(select(DB_SHOW_DATES.DROPOFF_LOC_LAT,DB_SHOW_DATES.DROPOFF_LOC_LON).where(DB_SHOW_DATES.School == c.TELE_USER_SCH)).first().tuple()
                
            elif c.DESTINATION_LOCATION == "School":
                lat , long = s.execute(select(DB_SHOW_DATES.DROPOFF_LOC_LAT,DB_SHOW_DATES.DROPOFF_LOC_LON).where(DB_SHOW_DATES.School == c.TELE_USER_SCH)).first().tuple()
            
            current_location=(str(c.LOCATION_LATITUDE) , str(c.LOCATION_LONGTITUDE))
            destination_pos=(str(lat),str(long))
            
            dis = distance.distance(current_location, destination_pos).km
            if dis <= radius:
                s.execute(update(DB_LOCATION_TABLE).where(DB_LOCATION_TABLE.LOCATION_ID == c.LOCATION_ID).values(RADIUS="YES"))
                s.commit()
            else:
                s.execute(update(DB_LOCATION_TABLE).where(DB_LOCATION_TABLE.LOCATION_ID == c.LOCATION_ID).values(RADIUS="NO"))
                s.commit()
        else:
            pass