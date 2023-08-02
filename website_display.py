import os 
from flask import Flask, request ,redirect,render_template
from flask_mysqldb import MySQL
import random
import datetime 
import time 
from flask import *
from flask import url_for
from flask_bootstrap import Bootstrap
import json
from sqlalchemy import Text, Integer, DateTime, Date, BigInteger, create_engine, select, update, insert, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session,sessionmaker
from sqlalchemy.dialects import mysql
import googlemaps
import math
from models_info_bot import DbSession,DB_BUS_OPS,DB_MRT_OPS,DB_LOCATION_TABLE,DB_SHOW_DATES,DB_TELEGRAM_USER_DB,Progress,Progress_V2

gmaps = googlemaps.Client(key='GOOGLE CLOUD API TOKEN')
app = Flask(__name__, template_folder='templates', static_folder='staticFiles')
now = datetime.datetime.now()

#init programme 
bootstrap= Bootstrap(app)

@app.route('/',methods=['GET'])
def index():
    with DbSession() as s:
        results= s.execute(select(DB_LOCATION_TABLE.LOCATION_ID,DB_LOCATION_TABLE.TELE_USER_NAME,DB_LOCATION_TABLE.TELE_USER_SCH,DB_LOCATION_TABLE.Arrival_direction,DB_LOCATION_TABLE.Departure_direction,DB_LOCATION_TABLE.DESTINATION_LOCATION,DB_LOCATION_TABLE.LOCATION_SENT_TIME,DB_LOCATION_TABLE.RADIUS,DB_LOCATION_TABLE.ETA).where(DB_LOCATION_TABLE.LOCATION_LATITUDE !=  None).order_by(DB_LOCATION_TABLE.RADIUS.desc(),DB_LOCATION_TABLE.ETA.desc()))
        ProgressV2_results = s.scalars(select(Progress_V2)).all()
        tuple_of_schools= s.execute(select(DB_SHOW_DATES.School).where(DB_SHOW_DATES.DATE == '2023-07-15'))
        List_of_schools=[]
        for i in tuple_of_schools:
            List_of_schools.append(i.School)
        table_data=[]
        table_data_school =[]
        count_padang=0
        count_school=0
        count_enroute=0
        count_seat=0
        count_alp=0
        headers_School_name=['Missing School','School','Enroute','Padang','Seated']
        school_name_at_school=[]
        school_name_at_padang=[]
        school_name_at_seats=[]
        school_name_enroute=[]
        headers_count =['School','Enroute','Padang','Seated']
        for c in ProgressV2_results:
            if c.STATUS == 0:
                count_school += 1
                count_alp+=1
                school_name_at_school.append( c.TELE_USER_SCH)
                List_of_schools.remove(c.TELE_USER_SCH)
            elif c.STATUS == 1:
                count_padang += 1
                count_alp+=1
                school_name_at_padang.append(c.TELE_USER_SCH)
                List_of_schools.remove(c.TELE_USER_SCH)
            elif c.STATUS == 2:
                count_seat += 1
                count_alp+=1
                school_name_at_seats.append(c.TELE_USER_SCH)
                List_of_schools.remove(c.TELE_USER_SCH)
            else:
                count_enroute += 1
                count_alp+=1
                school_name_enroute.append(c.TELE_USER_SCH)
                List_of_schools.remove(c.TELE_USER_SCH)
            
    
    return render_template('eta_table.html',headers_count = headers_count, count =(count_school,count_enroute,count_padang,count_seat),headers_School_name = headers_School_name,School_names=(List_of_schools,school_name_at_school,school_name_enroute,school_name_at_padang,school_name_at_seats), results=results)

@app.route('/bftt',methods=['GET'])
def bftt_table():
    return render_template('bftt.html')


@app.route('/geteta',methods=['POST'])
def get_ETA():
    with DbSession() as s:
        if request.method == 'POST':
            location_id= request.form['LocId']
            if location_id == "ALL":
                    results_list=s.scalars(select(DB_LOCATION_TABLE).where(DB_LOCATION_TABLE.LOCATION_LATITUDE != None)).all()
                    for c in results_list:
                            try:                                    
                                destination_check= s.scalar(select(DB_TELEGRAM_USER_DB.TELE_USER_SCH).where(DB_TELEGRAM_USER_DB.TELE_USER_ID == (c.TELE_USER_ID))) 
                                Location_table_id= c.LOCATION_ID
                                Location_latitude=c.LOCATION_LATITUDE
                                Location_longitude=c.LOCATION_LONGTITUDE
                                # Get School / Padang Geolocation -> Destination
                                if c.DESTINATION_LOCATION == "School":
                                    destination_check_final,des_latitude,des_longitde = s.execute(select(DB_SHOW_DATES.TRANSPORT,DB_SHOW_DATES.LOCATION_LATITUDE,DB_SHOW_DATES.LOCATION_LONGTITUDE).where(DB_SHOW_DATES.School== destination_check)).first().tuple()
                                    #Get mode of transport.
                                    if destination_check_final== "BUS":
                                        time_distance = gmaps.distance_matrix(origins=(Location_latitude,Location_longitude), destinations= (des_latitude,des_longitde), mode="driving",departure_time=now, traffic_model="pessimistic" )
                                    elif destination_check_final == "MRT":
                                        time_distance = gmaps.distance_matrix(origins=(Location_latitude,Location_longitude), destinations= (des_latitude,des_longitde), mode="transit",transit_mode="train",departure_time=now,traffic_model="pessimistic" )
                                        
                                elif c.DESTINATION_LOCATION == "Padang":
                                    destination_check_final,des_latitude,des_longitde = s.execute(select(DB_SHOW_DATES.TRANSPORT,DB_SHOW_DATES.DROPOFF_LOC_LAT,DB_SHOW_DATES.DROPOFF_LOC_LON).where(DB_SHOW_DATES.School== destination_check)).first().tuple()
                                     #Get mode of transport.
                                    if destination_check_final== "BUS":
                                        time_distance = gmaps.distance_matrix(origins=(Location_latitude,Location_longitude), destinations= (des_latitude,des_longitde), mode="driving",departure_time=now, traffic_model="optimistic" )
                                                
                                    elif destination_check_final == "MRT":
                                        time_distance = gmaps.distance_matrix(origins=(Location_latitude,Location_longitude), destinations= (des_latitude,des_longitde), mode="transit",transit_mode="train",departure_time=now,traffic_model="optimistic" )
                                time.sleep(0.04)
                                Get_rows= time_distance['rows']
                                Remove_list1 =Get_rows[0]
                                Get_Elements=Remove_list1['elements']
                                Remove_list2=Get_Elements[0]
                                Get_duration=Remove_list2['duration']
                                Eta=Get_duration['value']
                                final_eta=math.ceil(Eta/60)
                                s.execute(update(DB_LOCATION_TABLE).where(DB_LOCATION_TABLE.LOCATION_ID == Location_table_id).values(ETA = final_eta))
                                s.commit()                        
                            except Exception as e:
                                return redirect("/")
                    return redirect("/")            
                    

@app.route('/tracker_table',methods=['GET'])
def progress_tracker():
    with DbSession() as s:
        Progress_results = s.scalars(select(Progress).where(Progress.id > 150)).all()
        if Progress_results != None :
                #Table Headers
                Table_data= []
                headers = [ 'NO.',
                            'SCHOOL',
                            'USER NAME',
                            'TRANSPORT',
                            'STAGE',
                            'LAST UPDATE',
                            'TIMING NET DIFFERENCE'
                            ]
                count_at_school = 0
                count_at_padang = 0
                count_enroute = 0
                count_seated = 0
                pax_count = 0
                alp_count = 0
                #Printing Results from the query.
                for c in Progress_results:
                    completeTable = {}
                    school_name , transport = s.execute(select(DB_SHOW_DATES.School, DB_SHOW_DATES.TRANSPORT).where(DB_SHOW_DATES.SCHOOL_ID == c.school_id)).first().tuple()
                    
                    completeTable['NO.']=str(c.id)
                    #Retreiving the school name from DB Query
                    completeTable['SCHOOL']= str(school_name)                
                    #Retreiving the user name from DB Query
                    name_results= s.scalar(select(DB_TELEGRAM_USER_DB.TELE_USER_NAME).where(DB_TELEGRAM_USER_DB.TELE_USER_ID==c.user_id))
                    completeTable['USER NAME']= str(name_results)
                    completeTable['TRANSPORT']= str(transport)
                    if transport=="BUS":
                        depart_sch,reach_padang,seating,seated,leave_seat,reach_depart,depart_padang,return_school,pax_no,ALP_report_timing=s.execute(select(DB_BUS_OPS.BOARDED_BUS_DEPARTURE,DB_BUS_OPS.REACH_DEBUS_POINT,DB_BUS_OPS.REACH_SEATING_GALLERY,DB_BUS_OPS.SEATED,DB_BUS_OPS.LEAVE_SEATS,DB_BUS_OPS.REACH_PICKUP_PT,DB_BUS_OPS.DEPARTURE_TIME,DB_BUS_OPS.ARRIVE_AT_SCHOOL,DB_BUS_OPS.Total_No_of_Pax,DB_BUS_OPS.ALP_report_timing).where(DB_BUS_OPS.School == school_name)).first().tuple()
                    else:
                        depart_sch,reach_padang,seating,seated,leave_seat,reach_depart,depart_padang,return_school,pax_no,ALP_report_timing =s.execute(select(DB_MRT_OPS.LEAVE_SCHOOL,DB_MRT_OPS.Arrival_MRT_for_Padang,DB_MRT_OPS.Reach_Seating_Gallery,DB_MRT_OPS.Seated,DB_MRT_OPS.LEAVE_SEATS,DB_MRT_OPS.REACH_DEPARTURE_STATION,DB_MRT_OPS.DEPARTURE_TIME,DB_MRT_OPS.REACH_MRT,DB_MRT_OPS.Pax_including_ALP_HW,DB_MRT_OPS.ALP_report_timing).where(DB_MRT_OPS.School == school_name)).first().tuple()
                                           
                    return_school=return_school #Point 12, At School
                    depart_padang=depart_padang #Point 10, Enroute (Last Bus to leave Padang),
                    reach_depart=reach_depart #Point 9, First to board Bus Padang, 
                    leave_seat=leave_seat #Point 8, Padang, 
                    seated=seated #Point 7, Last Seated,
                    seating=seating #Point 6, Padang,
                    reach_padang=reach_padang #Point 5, Padang,
                    depart_sch=depart_sch  #Point 3, Enroute,
                    ALP_report_timing=ALP_report_timing#Point 1, At School,
                  
                    timing_diff = datetime.timedelta()
                    if c.p_12 is not None: #Point 12
                        alp_count += 1
                        count_at_school += 1
                        diff=(return_school-c.p_12)
                        timing_diff = diff
                        completeTable['STAGE'] = "REACH SCH"
                    elif c.p_11 is not None: #Point 11
                        alp_count += 1
                        count_enroute += 1
                        diff=(depart_padang-c.p_10)
                        timing_diff = diff
                        completeTable['STAGE'] = "FIRST BUS REACH SCH/REACH SCH MRT"
                    elif c.p_10 is not None: #Point 10
                        alp_count += 1
                        count_enroute += 1
                        diff=(depart_padang-c.p_10)
                        timing_diff = diff
                        completeTable['STAGE'] = "LAST BUS LEFT PADANG/MRT DEPARTED"
                    elif c.p_9B is not None: #Point 9B
                        alp_count += 1
                        count_at_padang += 1
                        diff=(reach_depart-c.p_9)
                        timing_diff = diff
                        completeTable['STAGE'] = "FIRST BUS LEFT PADANG"
                    elif c.p_9A is not None: #Point 9A
                        alp_count += 1
                        count_at_padang += 1
                        diff=(reach_depart-c.p_9)
                        timing_diff = diff
                        completeTable['STAGE'] = "LAST BUS BOARDED"                    
                    elif c.p_9 is not None: #Point 9
                        alp_count += 1
                        count_at_padang += 1 
                        diff=(reach_depart-c.p_9)
                        timing_diff = diff
                        completeTable['STAGE'] = "FIRST TO BOARD BUS/REACH PADANG MRT"
                    elif c.p_8 is not None: #Point 8
                        alp_count += 1
                        count_at_padang += 1
                        diff=(leave_seat-c.p_8)
                        timing_diff = diff
                        completeTable['STAGE'] = "LEFT SEATS"
                    elif c.p_7 is not None: #Point 7
                        alp_count += 1
                        pax_count+= pax_no
                        count_seated += 1
                        diff=(seated-c.p_7)
                        timing_diff = diff
                        completeTable['STAGE'] = "LAST CLASS SEATED"
                    elif c.p_6 is not None: #Point 6
                        alp_count += 1
                        count_at_padang += 1
                        diff=(seating-c.p_6)
                        timing_diff = diff
                        completeTable['STAGE'] = "FIRST CLASS SEATED"
                    elif c.p_5 is not None: #Point 5
                        alp_count += 1
                        count_at_padang += 1
                        diff=(reach_padang-c.p_5)
                        timing_diff = diff
                        completeTable['STAGE'] = "LAST BUS REACH PADANG/REACH PADANG MRT"
                    elif c.p_4 is not None: #Point 4
                        alp_count+=1
                        if transport == "BUS":
                            count_at_padang += 1
                            diff=(depart_sch-c.p_3)
                            timing_diff = diff
                            completeTable['STAGE'] = "FIRST BUS REACH PADANG"
                        else:
                            count_enroute += 1
                            diff=(depart_sch-c.p_3)
                            timing_diff = diff
                            completeTable['STAGE'] = "MRT DEPARTED"
                    elif c.p_3 is not None: #Point 3
                        alp_count += 1
                        count_enroute += 1
                        diff=(depart_sch-c.p_3)
                        timing_diff = diff
                        completeTable['STAGE'] = "LAST BUS LEFT SCH/REACH BOARDING MRT  "
                    elif c.p_2 is not None: #Point 2
                        alp_count += 1
                        count_enroute += 1
                        diff=(ALP_report_timing-c.p_1)
                        timing_diff = diff
                        completeTable['STAGE'] = "FIRST BUS LEAVE SCH/LEFT SCHOOL MRT"
                    elif c.p_1 is not None: #Point 1
                        alp_count += 1
                        count_at_school += 1
                        diff=(ALP_report_timing-c.p_1)
                        timing_diff = diff
                        completeTable['STAGE'] = "ALP REACH SCHOOL"
                    else:
                        alp_count+=1
                        completeTable['STAGE'] = "ALP YET TO REACH SCH"
                        
                    completeTable['LAST UPDATE']= fmt_datetime(c.last_click)
                    completeTable['TIMING NET DIFFERENCE']=str(math.floor(timing_diff.total_seconds() / 60)) + 'mins'
                    completeTable['is_recent'] = (datetime.datetime.now() - c.last_click).total_seconds() < 5 * 60
                    
                    #add to thenlist 
                    Table_data.append(completeTable)
                
                 
    return render_template('progress_tracker.html', headers=headers, Table_data = Table_data, Summarized=(alp_count,count_at_school,count_enroute,count_at_padang,count_seated,pax_count))

def fmt_datetime(raw_datetime: datetime) -> str:
        return raw_datetime.strftime("%H:%M:%S")

@app.route('/geo_fencing',methods=['GET'])
def geo_tracker():
    with DbSession() as s:
        results= s.execute(select(DB_LOCATION_TABLE.LOCATION_ID,DB_LOCATION_TABLE.TELE_USER_NAME,DB_LOCATION_TABLE.TELE_USER_SCH,DB_LOCATION_TABLE.Arrival_direction,DB_LOCATION_TABLE.Departure_direction,DB_LOCATION_TABLE.DESTINATION_LOCATION,DB_LOCATION_TABLE.LOCATION_SENT_TIME,DB_LOCATION_TABLE.RADIUS,DB_LOCATION_TABLE.ETA).where(DB_LOCATION_TABLE.LOCATION_LATITUDE !=  None).order_by(DB_LOCATION_TABLE.RADIUS.desc(),DB_LOCATION_TABLE.ETA.desc()))
        ProgressV2_results = s.scalars(select(Progress_V2)).all()
        tuple_of_schools= s.execute(select(DB_SHOW_DATES.School).where(DB_SHOW_DATES.DATE == '2023-07-15'))
        List_of_schools=[]
        for i in tuple_of_schools:
            List_of_schools.append(i.School)
        count_padang=0
        count_school=0
        count_enroute=0
        count_seat=0
        count_alp=0
        headers_School_name=['Missing School','School','Enroute','Padang','Seated']
        school_name_at_school=[]
        school_name_at_padang=[]
        school_name_at_seats=[]
        school_name_enroute=[]
        headers_count =['School','Enroute','Padang','Seated']
        for c in ProgressV2_results:
            try:
                if c.STATUS == 0:
                    count_school += 1
                    count_alp+=1
                    school_name_at_school.append( c.TELE_USER_SCH)
                    List_of_schools.remove(c.TELE_USER_SCH)
                elif c.STATUS == 1:
                    count_padang += 1
                    count_alp+=1
                    school_name_at_padang.append(c.TELE_USER_SCH)
                    List_of_schools.remove(c.TELE_USER_SCH)
                elif c.STATUS == 2:
                    count_seat += 1
                    count_alp+=1
                    school_name_at_seats.append(c.TELE_USER_SCH)
                    List_of_schools.remove(c.TELE_USER_SCH)
                else:
                    count_enroute += 1
                    count_alp+=1
                    school_name_enroute.append(c.TELE_USER_SCH)
                    List_of_schools.remove(c.TELE_USER_SCH)
            except Exception as e:
                pass
            
    
    return render_template('geo_fencing.html',headers_count = headers_count, count =(count_alp,count_school,count_enroute,count_padang,count_seat),headers_School_name = headers_School_name,School_names=(List_of_schools,school_name_at_school,school_name_enroute,school_name_at_padang,school_name_at_seats))

#Running the programme on localhost
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080, debug=True)
    
