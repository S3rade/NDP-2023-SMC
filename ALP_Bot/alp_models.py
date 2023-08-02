from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from typing import Optional, List, Literal
from sqlalchemy import String, CHAR, BigInteger, DateTime, Boolean, TIMESTAMP, ForeignKey, INT, DATETIME, TEXT, FLOAT, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy.dialects.mysql as mysql
from uuid import uuid4

class Base(DeclarativeBase):
	pass

"""
CREATE TABLE `PROGRESS` (
  `id` int NOT NULL AUTO_INCREMENT,
  `school_id` int DEFAULT NULL,
  `user_id` bigint DEFAULT NULL,
  `is_bus` tinyint(1) DEFAULT NULL,
  `p_1` datetime DEFAULT NULL COMMENT 'COMMON: ALP reach school',
  `p_2` datetime DEFAULT NULL COMMENT 'BUS: First bus to leave school, MRT: Leave school for boarding station',
  `p_3` datetime DEFAULT NULL COMMENT 'BUS: Last bus to leave school, MRT: Reach boarding station',
  `p_4` datetime DEFAULT NULL COMMENT 'BUS: First bus to reach esplanade drive, MRT: MRT Depart from boarding station',
  `p_5` datetime DEFAULT NULL COMMENT 'BUS: Last bus to reach esplanade drive, MRT: MRT Reach destination station',
  `p_6` datetime DEFAULT NULL COMMENT 'COMMON: First class to be seated',
  `p_7` datetime DEFAULT NULL COMMENT 'COMMON: Last class to be seated',
  `p_8` datetime DEFAULT NULL COMMENT 'COMMON: Left seating gallery',
  `p_9` datetime DEFAULT NULL COMMENT 'BUS: First Bus Boarded, MRT: Reach boarding station',
  `p_9A` datetime DEFAULT NULL COMMENT 'BUS Only: Last Bus Boarded',
  `p_9B` datetime DEFAULT NULL COMMENT 'BUS Only: First Bus left esplanade drive',
  `p_10` datetime DEFAULT NULL COMMENT 'BUS: Last Bus left esplanade drive, MRT: MRT Depart from boarding station',
  `p_11` datetime DEFAULT NULL COMMENT 'BUS: First Bus to reach school, MRT: Reach destination station',
  `last_click` datetime DEFAULT NULL,
  `cur_p` VARCHAR(2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

  """

progress_step_type = Literal['0', '1','2','3','4','5','6','7','8','9','9A','9B','10','11','12']

class Progress(Base): 
  __tablename__ = 'PROGRESS'
  
  id: Mapped[int] = mapped_column(INT, primary_key=True, nullable=False, autoincrement=True)
  school_id: Mapped[int] = mapped_column(INT, nullable=False)
  user_id: Mapped[int] = mapped_column(INT, nullable=False)
  is_bus: Mapped[bool] = mapped_column(mysql.TINYINT(1), nullable=False)
  p_1: Mapped[datetime] = mapped_column(DATETIME, nullable=True)
  p_2: Mapped[datetime] = mapped_column(DATETIME, nullable=True)
  p_3: Mapped[datetime] = mapped_column(DATETIME, nullable=True)
  p_4: Mapped[datetime] = mapped_column(DATETIME, nullable=True)
  p_5: Mapped[datetime] = mapped_column(DATETIME, nullable=True)
  p_6: Mapped[datetime] = mapped_column(DATETIME, nullable=True)
  p_7: Mapped[datetime] = mapped_column(DATETIME, nullable=True)
  p_8: Mapped[datetime] = mapped_column(DATETIME, nullable=True)
  p_9: Mapped[datetime] = mapped_column(DATETIME, nullable=True)
  p_9A: Mapped[datetime] = mapped_column(DATETIME, nullable=True)
  p_9B: Mapped[datetime] = mapped_column(DATETIME, nullable=True)
  p_10: Mapped[datetime] = mapped_column(DATETIME, nullable=True)
  p_11: Mapped[datetime] = mapped_column(DATETIME, nullable=True)
  p_12: Mapped[datetime] = mapped_column(DATETIME, nullable=True)
  last_click: Mapped[datetime] = mapped_column(DATETIME, nullable=True)
  cur_p: Mapped[progress_step_type] = mapped_column(String(2), nullable=True)
  msg_id: Mapped[int] = mapped_column(Integer, nullable=True)

""" 
CREATE TABLE `SHOW_DATES` (
  `SCHOOL_ID` int NOT NULL AUTO_INCREMENT,
  `School` text,
  `DATE` date DEFAULT NULL,
  `TRANSPORT` text,
  `LOCATION_LATITUDE` decimal(65,7) DEFAULT NULL,
  `LOCATION_LONGTITUDE` decimal(65,7) DEFAULT NULL,
  `DROPOFF_LOC_LAT` decimal(65,7) DEFAULT NULL,
  `DROPOFF_LOC_LON` decimal(65,7) DEFAULT NULL,
  PRIMARY KEY (`SCHOOL_ID`),
  UNIQUE KEY `SCHOOL_ID_UNIQUE` (`SCHOOL_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=202 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

class Show(Base):
  __tablename__ = 'SHOW_DATES'

  school_id: Mapped[int] = mapped_column("SCHOOL_ID", INT, primary_key=True, nullable=False, autoincrement=True)
  school: Mapped[str] = mapped_column("School", String, nullable=False)
  date: Mapped[datetime] = mapped_column("DATE", DATETIME, nullable=False)
  transport: Mapped[Literal["BUS", "MRT"]] = mapped_column("TRANSPORT", String, nullable=False)
  location_latitude: Mapped[float] = mapped_column("LOCATION_LATITUDE", FLOAT, nullable=False)
  location_longtitude: Mapped[float] = mapped_column("LOCATION_LONGTITUDE", FLOAT, nullable=False)
  dropoff_loc_lat: Mapped[float] = mapped_column("DROPOFF_LOC_LAT", FLOAT, nullable=False)
  dropoff_loc_lon: Mapped[float] = mapped_column("DROPOFF_LOC_LON", FLOAT, nullable=False)
  
"""
CREATE TABLE `TELEGRAM_USER_DB` (
  `USER_ID` int NOT NULL AUTO_INCREMENT,
  `TELE_USER_ID` bigint NOT NULL,
  `TELE_USER_SCH` varchar(45) NOT NULL,
  `TELE_USER_NAME` varchar(100) NOT NULL,
  `TELE_USER_ACCESS_RIGHTS` tinyint NOT NULL,
  `TELE_USER_NDP_DATE` date NOT NULL,
  PRIMARY KEY (`USER_ID`),
  UNIQUE KEY `USER_ID_UNIQUE` (`USER_ID`),
  UNIQUE KEY `TELEGRAM_USER_ID_UNIQUE` (`TELE_USER_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

class User(Base):
  __tablename__ = 'TELEGRAM_USER_DB'
  
  user_id: Mapped[int] = mapped_column("USER_ID", INT, primary_key=True, nullable=False, autoincrement=True)
  tele_user_id: Mapped[int] = mapped_column("TELE_USER_ID", INT, nullable=False)
  tele_user_sch: Mapped[str] = mapped_column("TELE_USER_SCH", String, nullable=False)
  tele_user_name: Mapped[str] = mapped_column("TELE_USER_NAME", String, nullable=False)
  tele_user_access_rights: Mapped[int] = mapped_column("TELE_USER_ACCESS_RIGHTS", INT, nullable=False)
  tele_user_ndp_date: Mapped[datetime] = mapped_column("TELE_USER_NDP_DATE", DATETIME, nullable=False)

