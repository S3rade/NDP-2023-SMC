from sqlalchemy import Text, Integer, DateTime, Date, BigInteger, create_engine, select, update, insert, delete, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session,sessionmaker
from sqlalchemy.dialects import mysql
from typing import Literal
import datetime

db_engine = create_engine('mysql://ADMIN_USERNAME:ADMIN_PASSWORD@nMYSQL_DB_SERVER_ADDRESS/MYSQLDB_SCHEMA', pool_pre_ping=True)
DbSession = sessionmaker(bind=db_engine, expire_on_commit=False)
progress_step_type = Literal['0', '1','2','3','4','5','6','7','8','9','9A','9B','10','11','12']

# declarative base class
class Base(DeclarativeBase):
    pass


class DB_BUS_OPS(Base):
    __tablename__ = "BUS_OPS"

    SN: Mapped[int] = mapped_column("S/N", Integer, primary_key=True)
    School: Mapped[str] = mapped_column(Text)
    TYPE: Mapped[str] = mapped_column(Text)
    NE_Show: Mapped[int] = mapped_column("NE SHOW", Integer)
    Distance_CAT: Mapped[str] = mapped_column("Distance CAT", Text)
    Transport_Mode: Mapped[str] = mapped_column("Transport Mode (Check)", Text)
    Duration_in_Traffic: Mapped[int] = mapped_column(
        "Duration in Traffic (mins) based on departure time at 1600", Integer
    )
    Direction: Mapped[str] = mapped_column(Text)
    No_of_Bus: Mapped[int] = mapped_column("No. of bus", Integer)
    Main_Route: Mapped[str] = mapped_column("Main Route", Text)
    Min: Mapped[int] = mapped_column("Min.", Integer)
    Max: Mapped[int] = mapped_column("Max.", Integer)
    Med: Mapped[int] = mapped_column("Med.", Integer)
    Delta_from_Data_Tm: Mapped[int] = mapped_column("Delta from Data Tm", Integer)
    ASSEMBLIED_FOR_BUS: Mapped[datetime.datetime] = mapped_column(
        "ASSEMBLIED FOR BUS", DateTime
    )
    BOARDED_BUS_DEPARTURE: Mapped[datetime.datetime] = mapped_column(
        "BOARDED BUS, DEPARTURE", DateTime
    )
    BUS_RIDE: Mapped[int] = mapped_column("BUS RIDE", Integer)
    REACH_DEBUS_POINT: Mapped[datetime.datetime] = mapped_column(
        "REACH DEBUS POINT", DateTime
    )
    REACH_SEATING_GALLERY: Mapped[datetime.datetime] = mapped_column(
        "REACH SEATING GALLERY", DateTime
    )
    SEATED: Mapped[datetime.datetime] = mapped_column(DateTime)
    ARRIVAL_WAVE: Mapped[str] = mapped_column("ARRIVAL WAVE", Text)
    DEPARTURE_WAVE: Mapped[str] = mapped_column("DEPARTURE WAVE", Text)
    LEAVE_SEATS: Mapped[datetime.datetime] = mapped_column("LEAVE SEATS", DateTime)
    REACH_PICKUP_PT: Mapped[datetime.datetime] = mapped_column(
        "REACH PICKUP PT", DateTime
    )
    DEPARTURE_TIME: Mapped[datetime.datetime] = mapped_column(
        "DEPARTURE TIME", DateTime
    )
    ARRIVE_AT_SCHOOL: Mapped[datetime.datetime] = mapped_column(
        "ARRIVE AT SCHOOL", DateTime
    )
    Total_No_of_Pax: Mapped[int] = mapped_column("Total No. of Pax", Integer)
    ALP_1_PRI: Mapped[str] = mapped_column("ALP 1 (PRI)", Text)
    ALP_PHONE_NO: Mapped[str] = mapped_column("ALP PHONE NO.", Text)
    ALP_2_ALT: Mapped[str] = mapped_column("ALP 2 (ALT)", Text)
    ALP_2_PHONE_NO: Mapped[str] = mapped_column("ALP 2 PHONE NO.", Text)
    SEAT_SECTOR: Mapped[str] = mapped_column("SEAT SECTOR", Text)
    ALP_report_timing: Mapped[datetime.datetime] = mapped_column("alp_report_timing", DateTime)


class DB_MRT_OPS(Base):
    __tablename__ = "MRT_OPS"

    SN: Mapped[int] = mapped_column("S/N", Integer, primary_key=True)
    School: Mapped[str] = mapped_column("School", Text)
    SHOW_ALLOCATION_MRT: Mapped[int] = mapped_column("SHOW ALLOCATION (MRT)", Integer)
    Nearest_MRT_Name: Mapped[str] = mapped_column("Nearest MRT Name", Text)
    End_Station: Mapped[str] = mapped_column("End Station", Text)
    Line: Mapped[str] = mapped_column("Line", Text)
    Station_Code: Mapped[str] = mapped_column("Station Code", Text)
    Direction_Bound: Mapped[str] = mapped_column("Direction Bound", Text)
    Pax_including_ALP_HW: Mapped[int] = mapped_column(
        "Pax (including ALP & HW)", Integer
    )
    Rounded_Walking_Time: Mapped[int] = mapped_column("Rounded Walking Time", Integer)
    LEAVE_SCHOOL: Mapped[datetime.datetime] = mapped_column("LEAVE SCHOOL", DateTime)
    School_to_Station_Walking_Time: Mapped[int] = mapped_column(
        "School to Station Walking Time", Integer
    )
    REACH_MRT_STATION: Mapped[datetime.datetime] = mapped_column(
        "REACH MRT STATION", DateTime
    )
    BOARD_TRAIN: Mapped[datetime.datetime] = mapped_column("BOARD TRAIN", DateTime)
    DEPARTURE: Mapped[datetime.datetime] = mapped_column("DEPARTURE", DateTime)
    Train_Traveling_Time: Mapped[int] = mapped_column("Train Traveling Time", Integer)
    Arrival_MRT_for_Padang: Mapped[datetime.datetime] = mapped_column(
        "Arrival @ MRT (for Padang)", DateTime
    )
    Walking_Time_to_Padang: Mapped[int] = mapped_column(
        "Walking Time to Padang", Integer
    )
    Reach_Seating_Gallery: Mapped[datetime.datetime] = mapped_column(
        "Reach Seating Gallery", DateTime
    )
    Seated: Mapped[datetime.datetime] = mapped_column("Seated", DateTime)
    LEAVE_SEATS: Mapped[datetime.datetime] = mapped_column("LEAVE SEATS", DateTime)
    REACH_DEPARTURE_STATION: Mapped[datetime.datetime] = mapped_column(
        "REACH DEPARTURE STATION", DateTime
    )
    DEPARTURE_TIME: Mapped[datetime.datetime] = mapped_column(
        "DEPARTURE TIME", DateTime
    )
    REACH_MRT: Mapped[datetime.datetime] = mapped_column("REACH MRT", DateTime)
    WALK_REACH_SCHOOL: Mapped[datetime.datetime] = mapped_column(
        "WALK & REACH SCHOOL", DateTime
    )
    ALP_1_PRI: Mapped[str] = mapped_column("ALP 1 (PRI)", Text)
    ALP_PHONE_NO: Mapped[str] = mapped_column("ALP PHONE NO.", Text)
    ALP_2_ALT: Mapped[str] = mapped_column("ALP 2 (ALT)", Text)
    ALP_2_PHONE_NO: Mapped[str] = mapped_column("ALP 2 PHONE NO.", Text)
    SEAT_SECTOR: Mapped[str] = mapped_column("SEAT SECTOR", Text)
    ALP_report_timing: Mapped[datetime.datetime] = mapped_column("alp_report_timing", DateTime)


class DB_SHOW_DATES(Base):
    __tablename__ = "SHOW_DATES"

    SCHOOL_ID: Mapped[int] = mapped_column("SCHOOL_ID", Integer, primary_key=True)
    School: Mapped[str] = mapped_column("School", Text)
    DATE: Mapped[datetime.date] = mapped_column("DATE", Date)
    TRANSPORT: Mapped[str] = mapped_column("TRANSPORT", Text)
    LOCATION_LATITUDE: Mapped[float] = mapped_column(
        "LOCATION_LATITUDE", mysql.DECIMAL(65, 7)
    )
    LOCATION_LONGTITUDE: Mapped[float] = mapped_column(
        "LOCATION_LONGTITUDE", mysql.DECIMAL(65, 7)
    )
    DROPOFF_LOC_LAT: Mapped[float] = mapped_column(
        "DROPOFF_LOC_LAT", mysql.DECIMAL(65, 7)
    )
    DROPOFF_LOC_LON: Mapped[float] = mapped_column(
        "DROPOFF_LOC_LON", mysql.DECIMAL(65, 7)
    )


class DB_TELEGRAM_USER_DB(Base):
    __tablename__ = "TELEGRAM_USER_DB"

    USER_ID: Mapped[int] = mapped_column("USER_ID", Integer, primary_key=True)
    TELE_USER_ID: Mapped[int] = mapped_column("TELE_USER_ID", BigInteger)
    TELE_USER_SCH: Mapped[str] = mapped_column("TELE_USER_SCH", Text)
    TELE_USER_NAME: Mapped[str] = mapped_column("TELE_USER_NAME", Text)
    TELE_USER_ACCESS_RIGHTS: Mapped[int] = mapped_column(
        "TELE_USER_ACCESS_RIGHTS", mysql.TINYINT
    )
    TELE_USER_NDP_DATE: Mapped[datetime.date] = mapped_column(
        "TELE_USER_NDP_DATE", Date
    )
class DB_LOCATION_TABLE(Base):
    __tablename__ = "LOCATION_TABLE"

    LOCATION_ID: Mapped[int] = mapped_column("LOCATION_ID", Integer, primary_key=True)
    TELE_USER_ID: Mapped[int] = mapped_column("TELE_USER_ID", BigInteger)
    TELE_USER_NAME: Mapped[str] = mapped_column("TELE_USER_NAME", Text)
    TELE_USER_SCH: Mapped[str] = mapped_column("TELE_USER_SCH",Text)
    Arrival_direction: Mapped[str]= mapped_column("Arrival_direction",Text)
    Departure_direction: Mapped[str] = mapped_column("Departure_direction",Text)
    DESTINATION_LOCATION: Mapped[str] = mapped_column('DESTINATION_LOCATION',Text)
    LOCATION_LATITUDE: Mapped[float] = mapped_column("LOCATION_LATITUDE", mysql.DECIMAL(65, 7))
    LOCATION_LONGTITUDE: Mapped[float] = mapped_column("LOCATION_LONGTITUDE", mysql.DECIMAL(65, 7))
    LOCATION_SENT_TIME: Mapped[datetime.datetime] = mapped_column("LOCATION_SENT_TIME", DateTime)
    RADIUS: Mapped[str] = mapped_column("RADIUS",Text)
    ETA: Mapped[str] = mapped_column('ETA',Text)


class Progress(Base): 
  __tablename__ = 'PROGRESS'
  
  id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True) #0
  school_id: Mapped[int] = mapped_column(Integer, nullable=False) #1
  user_id: Mapped[int] = mapped_column(Integer, nullable=False) #2
  is_bus: Mapped[bool] = mapped_column(mysql.TINYINT(1), nullable=False) #3
  p_1: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True) #4
  p_2: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True) #5
  p_3: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True) #6
  p_4: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True) #7
  p_5: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True) #8
  p_6: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True) #9
  p_7: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True) #10
  p_8: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True) #11
  p_9: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True) #12
  p_9A: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True) #13
  p_9B: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True) #14
  p_10: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True) #15
  p_11: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True) #16
  p_12: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True) #17
  last_click: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True) #18
  cur_p: Mapped[progress_step_type] = mapped_column(String(2), nullable=True) #19
  
class Progress_V2(Base):

  __tablename__ = 'PROGRESS_V2'
  
  id: Mapped[int] = mapped_column("PROGRESS_PK",Integer, primary_key=True, nullable=False, autoincrement=True) #0
  TELE_USER_ID: Mapped[int] = mapped_column("TELE_USER_ID", BigInteger)
  TELE_USER_SCH: Mapped[str] = mapped_column("TELE_USER_SCH",Text)
  STATUS: Mapped[int] = mapped_column("STATUS", BigInteger)