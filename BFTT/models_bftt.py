
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, BigInteger, DECIMAL,DateTime, select, update
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,sessionmaker
from datetime import datetime

db_engine = create_engine('mysql://ADMIN_USERNAME:ADMIN_PASSWORD@MYSQL_DB_SERVER_ADDRESS/MYSQL_SCHEMA', pool_pre_ping=True)
DbSession = sessionmaker(bind=db_engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class DB_Location(Base):
    __tablename__ = '#####' #Replace the #s on the the left with the MySQL DB table Name

    LOCATION_ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    TELE_USER_ID: Mapped[int] = mapped_column(BigInteger, nullable=True)
    TELE_USER_COY: Mapped[str] = mapped_column(String(100), nullable=True)
    TELE_USER_NAME: Mapped[str] = mapped_column(String(100), nullable=True)
    LOCATION_LATITUDE: Mapped[float] = mapped_column(DECIMAL(65, 7), nullable=True)
    LOCATION_LONGTITUDE: Mapped[float] = mapped_column(DECIMAL(65, 7), nullable=True)
    LOCATION_SENT_TIME: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    SIZE: Mapped[int] = mapped_column(Integer, nullable=True)

class DB_User(Base):
    __tablename__ = '#####' #Replace the #s on the the left with the MySQL DB table Name

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    TELE_USER_ID: Mapped[int] = mapped_column(BigInteger, nullable=True)
    TELE_USER_COY: Mapped[str] = mapped_column(String(100), nullable=True)
    TELE_USER_NAME: Mapped[str] = mapped_column(String(100), nullable=True)
    TELE_USER_ACCESS_RIGHTS: Mapped[int] = mapped_column(Integer, nullable=True)