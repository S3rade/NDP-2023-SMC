import telebot
from telebot import types
import datetime
import googlemaps
import math
import os
import time
from sqlalchemy import Text, Integer, DateTime, Date, BigInteger, create_engine, select, update, insert, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session,sessionmaker
from sqlalchemy.dialects import mysql
from models_info_bot import DB_TELEGRAM_USER_DB,DB_BUS_OPS,DB_LOCATION_TABLE,DB_MRT_OPS,DB_SHOW_DATES,DbSession
import MySQLdb

gmaps = googlemaps.Client(key="GOOGLE CLOUD API TOKEN") #Replace text with Google API Token. 
Perm_to_share_location = 1


API_TOKEN = "TELEGRAM TOKEN ID" #Replace the text with the Telegram ID

bot = telebot.TeleBot(API_TOKEN)

now= datetime.datetime.now()
db = MySQLdb.connect(
            host="MYSQL_SERVER_ADDRESS",
            user="ADMIN_USERNAME",        
            passwd="ADMIN_PASSWORD",  
            db="SCHEMA",
            port=3306)
cur =db.cursor()

# Details to Receive
user_dict = {}
destination_dict = {}

class User:
    def __init__(self, name):
        self.name = name
        self.date = None
        self.school = None


class Destination:
    def _init__(self, name):
        self.location = None


@bot.message_handler(commands=["check_handler"])
def test_con(message):
    with DbSession() as s:
        data = s.scalars(select(DB_TELEGRAM_USER_DB)).all()
    if data != None:
        bot.send_message(message.chat.id, "DB is working", str(data))
    else:
        bot.send_message(message.chat.id, "MAN DOWN MAN DOWN")


# Start Handler
@bot.message_handler(commands=["start"])
def send_welcome(message):
    chat_id = message.chat.id
    User_ID = str(message.from_user.id)

    with DbSession() as s:
        data = s.scalars(
            select(DB_TELEGRAM_USER_DB).where(
                DB_TELEGRAM_USER_DB.TELE_USER_ID == User_ID
            )
        ).all()
    if len(data) != 0:
        bot.send_message(
            message.chat.id,
            "You have registered before please use /help for aid. Thank you.",
        )
    else:
        msg = bot.send_message(
            chat_id,
            "Greetings! Welcome to NDP 2023 InfoBot!\n"
            + "My name is MerMer and I will be assisting you today.\n"
            + "\n"
            + "May I know your name?",
        )

        bot.register_next_step_handler(msg, process_name_step)


# User Details Handler
def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("02/07/2023", "08/07/2023", "15/07/2023") #Date options given to user.
        msg = bot.send_message(
            chat_id, "May I know which date is your NDP Show ?", reply_markup=markup
        )
        bot.register_next_step_handler(msg, process_date)
    except Exception as e:
        bot.reply_to(message, "Please contact the Developer. Thank you.")


def process_date(message):
    try:
        chat_id = message.chat.id
        date = message.text
        user = user_dict[chat_id]
        if date in ["02/07/2023", "08/07/2023","15/07/2023"]: #Date verification option.
            user.date = date
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            bot.send_message(
                message.chat.id, "Please wait as the options load. Thank you! "
            )
            old_date = datetime.datetime.strptime(user.date, "%d/%m/%Y")
            new_date = old_date.strftime("%Y-%m-%d")
            with DbSession() as s:
                schools = s.scalars(
                    select(DB_SHOW_DATES.School)
                    .where(DB_SHOW_DATES.DATE == new_date)
                    .order_by(DB_SHOW_DATES.School.asc())
                ).all()
            for school in schools:
                markup.add(school)
            msg = bot.send_message(
                chat_id, "What school are you from? ", reply_markup=markup
            )
            bot.register_next_step_handler(msg, process_school)

        else:
            msg = bot.send_message(
                chat_id, "Improper Option. Please select an option. Thank you. "
            )
            bot.register_next_step_handler(msg, process_date)

    except Exception as e:
        bot.reply_to(message, "Please contact the Developer. Thank you.")


def process_school(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        school = message.text
        user = user_dict[chat_id]
        with DbSession() as s:
            schools = s.scalars(
                select(DB_SHOW_DATES.School).where(DB_SHOW_DATES.School == school)
            ).all()
        old_date = datetime.datetime.strptime(user.date, "%d/%m/%Y")
        new_date = old_date.strftime("%Y-%m-%d")
        if len(schools) != 0:
            user.school = school
            access_rights = "0"
            bot.send_message(
                chat_id,
                "Nice to meet you, " + user.name + " from " + user.school,
                reply_markup=types.ReplyKeyboardRemove(),
            )
            with DbSession() as s:
                new_user = DB_TELEGRAM_USER_DB(
                    TELE_USER_ID=user_id,
                    TELE_USER_SCH=user.school,
                    TELE_USER_NAME=user.name,
                    TELE_USER_ACCESS_RIGHTS=access_rights,
                    TELE_USER_NDP_DATE=new_date,
                )
                s.add(new_user)
                s.commit()
        else:
            msg = bot.send_message(
                chat_id, "Improper Option. Please select an option. Thank you. "
            )
            bot.register_next_step_handler(msg, process_school)

    except Exception as e:
        bot.reply_to(message, "Please contact the Developer. Thank you.")


# Help handler
@bot.message_handler(commands=["help"])
def help_command(message):
    with DbSession() as s:
        User_ID = str(message.from_user.id)
        final_access_rights= s.scalar(select(DB_TELEGRAM_USER_DB.TELE_USER_ACCESS_RIGHTS).where(DB_TELEGRAM_USER_DB.TELE_USER_ID ==User_ID ))
        if final_access_rights == 1:
            bot.send_message(
                message.chat.id,
                "Greetings! Welcome to NDP 2023 InfoBot!\n"
                + "My name is MerMer and I will be assisting you today.\n"
                + "These are the commands you can use in the bot:\n"
                + "/your_details to check your details.\n"
                + "/edit to edit your details.\n"
                + "/broadcast_all to broadcast to all personnel\n"
                + "/broadcast_school to broadcast to all personnel\n"
                + "/send_location, to begin the process of live location tracking function.\n"
                + "/contact_us to contact Customer Support Team.\n"
                + "\n"
                + "Thank you! ",
            )
        elif final_access_rights == 2:
            bot.send_message(
                message.chat.id,
                "Greetings! Welcome to NDP 2023 InfoBot!\n"
                + "My name is MerMer and I will be assisting you today.\n"
                + "These are the commands you can use in the bot:\n"
                + "/your_details to check your details.\n"
                + "/edit to edit your details.\n"
                + "/send_location, for the live location tracking function.\n"
                + "/broadcast_all to broadcast to all personnel\n"
                + "/broadcast_school to broadcast to all personnel\n"
                + "/loc_disable to enable or disable location sharing.\n"
                "/check_handler to check Database Connection\n\n" + "\n" + "Thank you! ",
            )

        else:
            bot.send_message(
                message.chat.id,
                "Greetings! Welcome to NDP 2023 InfoBot!\n"
                + "My name is MerMer and I will be assisting you today.\n"
                + "These are the commands you can use in the bot:\n"
                + "Please use /edit to check your details.\n"
                + "Please use /your_details to check your details.\n"
                + "Please use /info to get details of NDP shows for \n"
                + "Please use /send_location, to begin the process of live location tracking function.\n"
                + "Please use /contact_us to contact Customer Support Team.\n"
                + "\n"
                + "Thank you!",
            )


# Contact Us handler
@bot.message_handler(commands=["contact_us"])
def contact_us_command(message):
    try:
        chat_id = message.chat.id
        msg = bot.send_message(
            chat_id,
            "Please reply with the message which you would like to tell Customer Support Team. Thank you. ",
        )

        bot.register_next_step_handler(msg, contact_us_forward)
    except Exception as e:
        bot.reply_to(message, "Please contact the Developer. Thank you.")


def contact_us_forward(message):
    contact_us_chat_id = 0 #Replace the number on the left with the chat group ID. Can use Raw Data bot/ IDbot in telegram to find the ID of the chat. Please ensure the chat group is 1 Day old.
    message_from_user = message.text
    chat_id = message.chat.id
    with DbSession() as s:
        User_ID = str(message.from_user.id)
        sch, name= s.execute(select(DB_TELEGRAM_USER_DB.TELE_USER_SCH,DB_TELEGRAM_USER_DB.TELE_USER_NAME ).where(DB_TELEGRAM_USER_DB.TELE_USER_ID == User_ID )).first().tuple()
        if message_from_user != None:
            bot.send_message(
                contact_us_chat_id,
                "Customer Issues/Inquiry: \n\n"
                + "From: \nName: "
                + name
                + "\n\nMessage for Customer:\n\n "
                + str(message_from_user)
                + "\n\n"
                + "\nSchool: " + sch
            )
            bot.send_message(contact_us_chat_id, "[Click here to reply](tg://user?id="+ str(chat_id)+ ")",parse_mode="MarkdownV2")
            bot.send_message(
                chat_id,
                "Message has been sent to Customer Support Team. \n\nWe will get back to you as soon as possible.\n\n Thank you !",
            )

        else:
            msg = bot.send_message(message.chat.id, "Please send message again")
            bot.register_next_step_handler(msg, contact_us_forward)


# Edit name and school
@bot.message_handler(commands=["edit"])
def edit_db_details(message):
    try:
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Edit Name", "Edit School")
        msg = bot.send_message(
            chat_id,
            "May I know which details would you like to change? \n\n ",
            reply_markup=markup,
        )

        bot.register_next_step_handler(msg, edit_filter)
    except Exception as e:
        bot.reply_to(message, "Please contact the Developer. Thank you.")


def edit_filter(message):
    try:
        filter_message = message.text
        if filter_message == ("Edit Name"):
            msg = bot.send_message(
                message.chat.id,
                "Please reply with the name you want to change to. Thank you.",
            )
            bot.register_next_step_handler(msg, edit_name)

        elif filter_message == ("Edit School"):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("02/07/2023", "08/07/2023", "15/07/2023") #Date options given to user.
            msg = bot.send_message(
                message.chat.id,
                "Please select the correct date of your NE Show. Thank you",
                reply_markup=markup,
            )
            bot.register_next_step_handler(msg, edit_date)
        else:
            msg = bot.send_message(
                message.chat.id, "Please select an option. Thank you."
            )
            bot.register_next_step_handler(msg, edit_filter)
    except Exception as e:
        bot.reply_to(message, "Please contact the Developer. Thank you.")


def edit_name(message):
    try:
        User_ID = str(message.from_user.id)
        with DbSession() as s:
            chat_id = message.chat.id
            name = message.text
            s.execute(update(DB_TELEGRAM_USER_DB).where(DB_TELEGRAM_USER_DB.TELE_USER_ID ==User_ID).values(TELE_USER_NAME = name))
            s.commit()
            bot.send_message(
                chat_id,
                "Your name has been updated, please use /your_details to check. Thank you ! ",
                reply_markup=types.ReplyKeyboardRemove(),
            )
    except Exception as e:
            bot.reply_to(message, "Please contact the Developer. Thank you.")


def edit_date(message):
    try:
        with DbSession() as s:
            chat_id = message.chat.id
            date = message.text
            try:
                parsed = datetime.datetime.strptime(date, "%d/%m/%Y")
                sql_date = parsed.strftime("%Y-%m-%d")
            except ValueError:
                bot.send_message(message.chat.id, "Please choose the correct date.")
                bot.register_next_step_handler(msg, edit_date)

            if date in ["02/07/2023", "08/07/2023","15/07/2023"]: #Change the Date verification Check
                chat_id = message.chat.id
                s.execute(update(DB_TELEGRAM_USER_DB).where(DB_TELEGRAM_USER_DB.TELE_USER_ID == chat_id).values(TELE_USER_NDP_DATE= sql_date))
                s.commit()
                random_handler(chat_id, sql_date)

            else:
                msg = bot.send_message(
                    chat_id, "Improper Option. Please select an option. Thank you. "
                )
                bot.register_next_step_handler(msg, edit_date)

    except Exception as e:
        bot.reply_to(message, "Please contact the Developer. Thank you.")


def random_handler(chat_id, sql_date):
    try:
        bot.send_message(chat_id, "Please wait as the options load. Thank you! ")
        with DbSession() as s:
            data= s.scalars(select(DB_SHOW_DATES.School).where(DB_SHOW_DATES.DATE == sql_date).order_by(DB_SHOW_DATES.School.asc())).all()
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            for school2 in data:
                markup.add(school2)
            msg = bot.send_message(
                chat_id, "What school are you from? ", reply_markup=markup
            )
            bot.register_next_step_handler(msg, edit_school)

    except Exception as e:
        bot.register_next_step_handler(random_handler)


def edit_school(message):
    try:
        chat_id = message.chat.id
        school_received = message.text
        with DbSession() as s:
            data = s.scalar(select(DB_SHOW_DATES.School).where(DB_SHOW_DATES.School == school_received))
            if len(data) != 0:
                s.execute(update(DB_TELEGRAM_USER_DB).where(DB_TELEGRAM_USER_DB.TELE_USER_ID == chat_id).values(TELE_USER_SCH = data))
                s.commit()
                bot.send_message(
                    chat_id,
                    "Your school has been updated, please use /your_details to check. Thank you ! ",
                    reply_markup=types.ReplyKeyboardRemove(),
                )
            else:
                msg = bot.send_message(
                    chat_id, "Improper Option. Please select an option. Thank you. "
                )
                bot.register_next_step_handler(msg, edit_school)

    except Exception as e:
        bot.reply_to(message, "Please contact the Developer. Thank you.")


# Your Details Handler
@bot.message_handler(commands=["your_details"])
def edit_db_details(message):
    try:
        with DbSession() as s:
            chat_id = message.chat.id
            name, school = s.execute(select(DB_TELEGRAM_USER_DB.TELE_USER_NAME,DB_TELEGRAM_USER_DB.TELE_USER_SCH).where(DB_TELEGRAM_USER_DB.TELE_USER_ID==chat_id)).first().tuple()
            msg = (
                "Hello! Here are your details \n\n"
                + "Your name is "
                + name
                + ".\n\n You are from "
                + school
                + ".\n\n Do use the command /edit to change details if they are inaccurate."
            )
            bot.send_message(chat_id, msg)

    except Exception as e:
        bot.reply_to(message, "Please contact the Developer. Thank you.")


# Info Handler
@bot.message_handler(commands=["info"])
def info_command(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with DbSession() as s:
        user_school = s.scalar(select(DB_TELEGRAM_USER_DB.TELE_USER_SCH).where(DB_TELEGRAM_USER_DB.TELE_USER_ID == user_id))

        # get whether school is bus/mrt
        transport_type = s.scalar(select(DB_SHOW_DATES.TRANSPORT).where(DB_SHOW_DATES.School == user_school))

        bus_opts = {
            "NE Show No.": "NE Show",
            "Transport Mode": "Transport Mode (Check)",
            "Main Route": "Main Route",
            "Departure Timings": "departure",
            "Arrival Timings": "arrival",
            "Direction Of Arrival": "Direction",
            "Liaison Personnel": "liaison",
            "Seating Sector": "SEAT SECTOR",
        }

        mrt_opts = {
            "NE Show No.": "SHOW ALLOCATION (MRT)",
            "Start Station": "Nearest MRT Name",
            "End Station": "End Station",
            "MRT Line": "Line",
            "Departure Timings": "departure",
            "Arrival Timings": "arrival",
            "Liaison Personnel": "liaison",
            "Seating Sector": "SEAT SECTOR",
            "Directions from MRT to Padang": "route",
        }

        user_opts = bus_opts if transport_type == "BUS" else mrt_opts
        opts_display = []
        for opt in user_opts:
            opts_display.append(opt)

        # generate markup based on col names
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Quit", *opts_display)
        msg = bot.send_message(chat_id, "What would you like to know?", reply_markup=markup)
        args = {
            "transport_type": transport_type,
            "user_school": user_school,
            "user_opts": user_opts,
        }
        bot.register_next_step_handler(msg, process_option, args)


    # takes in a mysql datetime (yyyy-mm-dd HH:MM:SS)
    # and converts it to (HH:MM am/pm (dd Mon))
def fmt_datetime(raw_datetime: datetime.datetime) -> str:
        return raw_datetime.strftime("%I:%M %p (%d %b)")


def process_option(message, args):
    with DbSession() as s:
        transport_type = args["transport_type"]
        table_name = "BUS_OPS" if transport_type == "BUS" else "MRT_OPS"
        user_school = args["user_school"]
        user_opts = args["user_opts"]
        chosen_opt = message.text
        if chosen_opt == "Quit":
            bot.send_message(
                message.chat.id,
                "Successfully exited /info",
                reply_markup=types.ReplyKeyboardRemove(),
            )
            return

        if chosen_opt == "Arrival Timings":
            if transport_type == "BUS":
                    # ASSEMBLIED FOR BUS
                    # BOARDED BUS, DEPARTURE
                    # REACH DEBUS POINT
                    # REACH SEATING GALLERY
                    # SEATED
                assemble,board,debus,seating,seated = s.execute(select(DB_BUS_OPS.ASSEMBLIED_FOR_BUS,DB_BUS_OPS.BOARDED_BUS_DEPARTURE,DB_BUS_OPS.REACH_DEBUS_POINT,DB_BUS_OPS.REACH_SEATING_GALLERY,DB_BUS_OPS.SEATED).where(DB_BUS_OPS.School == user_school)).first().tuple()

                data = (
                        "Your Arrival to Padang Timings are as follows:\n\n"
                        f"<b>Assembled For Bus:</b> {fmt_datetime(assemble)}\n\n"
                        f"<b>Board Bus, Departure:</b> {fmt_datetime(board)}\n\n"
                        f"<b>Reach Debus Point:</b> {fmt_datetime(debus)}\n\n"
                        f"<b>Reach Seating Gallery:</b> {fmt_datetime(seating)}\n\n"
                        f"<b>Seated:</b> {fmt_datetime(seated)}"
                    )
            else:
                    # LEAVE SCHOOL
                    # REACH MRT STATION
                    # BOARD TRAIN
                    # DEPARTURE
                    # ARRIVAL @ MRT (for Padang)
                    # Reach Seating Gallery
                    # Seated
                leave_school,reach_mrt,train_depart,arrive_padang,reach_gallery,mrt_seated = s.execute(select(DB_MRT_OPS.LEAVE_SCHOOL,DB_MRT_OPS.REACH_MRT_STATION,DB_MRT_OPS.DEPARTURE,DB_MRT_OPS.Arrival_MRT_for_Padang,DB_MRT_OPS.Reach_Seating_Gallery,DB_MRT_OPS.Seated).where(DB_MRT_OPS.School == user_school)).first().tuple()
                data = (
                        "Your Arrival Timings are as follows:\n\n"
                        f"<b>Leave School:</b> {fmt_datetime(leave_school)}\n\n"
                        f"<b>Reach MRT Station:</b>  {fmt_datetime(reach_mrt)}\n\n"
                        f"<b>Train Departure:</b> {fmt_datetime(train_depart)}\n\n"
                        f"<b>Arrival at Destination Station:</b> {fmt_datetime(arrive_padang)}\n\n"
                        f"<b>Reach Seating Gallery:</b> {fmt_datetime(reach_gallery)}\n\n"
                        f"<b>Seated:</b> {fmt_datetime(mrt_seated)}\n"
                    )
        elif chosen_opt == "Departure Timings":
            if transport_type == "BUS":
                    # LEAVE SEATS
                    # REACH PICKUP PT
                    # DEPARTURE TIME
                    # ARRIVE AT SCHOOL
                    leave_seat,reach_pickup,depart_padang,back_to_school = s.execute(select(DB_BUS_OPS.LEAVE_SEATS,DB_BUS_OPS.REACH_PICKUP_PT,DB_BUS_OPS.DEPARTURE_TIME,DB_BUS_OPS.ARRIVE_AT_SCHOOL).where(DB_BUS_OPS.School == user_school)).first().tuple()
                    data = (
                        "Your Departure from Padang Timings are as follows:\n\n"
                        f"<b>Leave Seats:</b> {fmt_datetime(leave_seat)}\n\n"
                        f"<b>Reach Pickup Point:</b> {fmt_datetime(reach_pickup)}\n\n"
                        f"<b>Departure Time:</b> {fmt_datetime(depart_padang)}\n\n"
                        f"<b>Arrive At School:</b> {fmt_datetime(back_to_school)}"
                    )
            else:
                # LEAVE SEATS
                # REACH DEPARTURE STATION
                # DEPARTURE TIME
                # REACH MRT
                # WALK & REACH SCHOOL

                mrt_leave_seat,mrt_reach_depart,mrt_depart_time,reach_final_mrt,walk_to_sch = s.execute(select(DB_MRT_OPS.LEAVE_SEATS,DB_MRT_OPS.REACH_DEPARTURE_STATION,DB_MRT_OPS.DEPARTURE_TIME,DB_MRT_OPS.REACH_MRT,DB_MRT_OPS.WALK_REACH_SCHOOL).where(DB_MRT_OPS.School == user_school)).first().tuple()
                data = (
                    "Your Departure Timings are as follows:\n\n"
                    f"<b>Leave Seats:</b> {fmt_datetime(mrt_leave_seat)}\n\n"
                    f"<b>Reach Departure Station:</b> {fmt_datetime(mrt_reach_depart)}\n\n"
                    f"<b>Departure Time:</b> {fmt_datetime(mrt_depart_time)}\n\n"
                    f"<b>Reach Destination MRT:</b> {fmt_datetime(reach_final_mrt)}\n\n"
                    f"<b>Walk & Reach School:</b> {fmt_datetime(walk_to_sch)}"
                )
        elif chosen_opt == "Liaison Personnel":
            if table_name == "MRT_OPS":
                ALP1,ALP1NO,ALP2,ALP2NO= s.execute(select(DB_MRT_OPS.ALP_1_PRI,DB_MRT_OPS.ALP_PHONE_NO,DB_MRT_OPS.ALP_2_ALT,DB_MRT_OPS.ALP_2_PHONE_NO).where(DB_MRT_OPS.School == user_school)).first().tuple()
                data = (
                    "Your Army Liaison Personnel are:\n\n"
                    f"Primary: <b>{ALP1}</b> ({ALP1NO})\n\n"
                )
                if ALP2 != "":
                    data += f"Alternate: <b>{ALP2}</b> ({ALP2NO})\n\n"
            else:
                ALP1,ALP1NO,ALP2,ALP2NO= s.execute(select(DB_BUS_OPS.ALP_1_PRI,DB_BUS_OPS.ALP_PHONE_NO,DB_BUS_OPS.ALP_2_ALT,DB_BUS_OPS.ALP_2_PHONE_NO).where(DB_BUS_OPS.School == user_school)).first().tuple()
                data = (
                    "Your Army Liaison Personnel are:\n\n"
                    f"Primary: <b>{ALP1}</b> ({ALP1NO})\n\n"
                )
                if ALP2 != "":
                    data += f"Alternate: <b>{ALP2}</b> ({ALP2NO})\n\n"

        elif chosen_opt == "Directions from MRT to Padang":
            if table_name == "MRT_OPS":
                mrt_station = s.scalar(select(DB_MRT_OPS.End_Station).where(DB_MRT_OPS.School == user_school))
                bot.send_message(message.chat.id, "Please wait while the route guide loads...")
                try:
                    if mrt_station == "RAFFLES PLACE":
                        photo_url = "/scripts/images/Raffles.png"
                        bot.send_photo(
                            message.chat.id,
                            photo=open(photo_url, "rb"),
                            caption="Route from Raffles Place MRT to Padang (1/1)",
                        )
                    elif mrt_station == "ESPLANADE":
                        photo_url_1 = "/scripts/images/Esplanade_1.png"
                        photo_url_2 = "/scripts/images/Esplanade_2.png"
                        bot.send_photo(
                            message.chat.id,
                            photo=open(photo_url_1, "rb"),
                            caption="Route from Esplanade MRT to Padang (1/2)",
                        )
                        bot.send_photo(
                            message.chat.id,
                            photo=open(photo_url_2, "rb"),
                            caption="Route from Esplanade MRT to Padang (2/2)",
                        )
                    else:
                        photo_url_1 = "/scripts/images/Promenade_1.png"
                        photo_url_2 = "/scripts/images/Promenade_2.png"
                        bot.send_photo(
                            message.chat.id,
                            photo=open(photo_url_1, "rb"),
                            caption="Route from Promenade MRT to Padang (1/2)",
                        )
                        bot.send_photo(
                            message.chat.id,
                            photo=open(photo_url_2, "rb"),
                            caption="Route from Promenade MRT to Padang (2/2)",
                        )
                    # reprompt user
                    opts_display = []
                    for opt in user_opts:
                        opts_display.append(opt)

                    # generate markup based on col names
                    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    markup.add("Quit", *opts_display)
                    msg = bot.send_message(
                        message.chat.id,
                        "What else would you like to know?",
                        reply_markup=markup,
                    )
                    bot.register_next_step_handler(msg, process_option, args)
                    return
                except:
                    data = "Something went wrong, please try again."
            else:

                # reprompt user
                opts_display = []
                for opt in user_opts:
                    opts_display.append(opt)

                    # generate markup based on col names
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup.add("Quit", *opts_display)
                msg = bot.send_message(
                        message.chat.id,
                        "What else would you like to know?",
                        reply_markup=markup,
                )
                bot.register_next_step_handler(msg, process_option, args)

        elif chosen_opt == "Seating Sector":
            if table_name == "BUS_OPS":
                seat_sector = s.scalar(select(DB_BUS_OPS.SEAT_SECTOR).where(DB_BUS_OPS.School == user_school))
            else:
                seat_sector = s.scalar(select(DB_MRT_OPS.SEAT_SECTOR).where(DB_MRT_OPS.School == user_school))
            show_date = s.scalar(select(DB_SHOW_DATES.DATE).where(DB_SHOW_DATES.School == user_school))
            if show_date == datetime.date(2023, 7, 2):
                ne_show = "NE1"
            elif show_date == datetime.date(2023, 7, 8):
                ne_show = "NE2"
            else:
                ne_show = "NE3"

            # fetch image and send
            photo_dir_url = f"/scripts/images/{ne_show}/{ne_show}-{seat_sector}"
            print(photo_dir_url)
            bot.send_message(
                message.chat.id,
                f"Your <b>{chosen_opt}</b> is <b>{seat_sector}</b>",
                parse_mode="HTML",
            )
            bot.send_message(message.chat.id, "Please wait while the sector guide loads...")
            photos = [p for p in os.listdir(photo_dir_url)]
            print(photos)
            try:
                for photo in photos:
                    bot.send_photo(
                        message.chat.id,
                        photo=open(f"{photo_dir_url}/{photo}", "rb"),
                    )
            except:
                bot.send_message(message.chat.id, "Something went wrong, please try again.")

            # reprompt
            opts_display = []
            for opt in user_opts:
                opts_display.append(opt)

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("Quit", *opts_display)
            msg = bot.send_message(
                message.chat.id, "What else would you like to know?", reply_markup=markup
            )
            bot.register_next_step_handler(msg, process_option, args)
            return
        elif chosen_opt == "Direction Of Arrival":
            raw_data = s.scalar(select(DB_BUS_OPS.Direction).where(DB_BUS_OPS.School == user_school))

            if raw_data == "":
                data2 = "Data not available"
            elif raw_data == "SPED":
                data2 = "Parliament Lane into Supreme Court Lane"
            else:
                data2 = raw_data

            data = f"Your <b>{chosen_opt}</b> is <b>{data2}</b>"

        elif chosen_opt in user_opts:
            col_name = user_opts[chosen_opt]
            cur =db.cursor()
            cur.execute(
                f'select `{col_name}` from {table_name} where SCHOOL = "{user_school}"'
            )
            raw_data = cur.fetchall()[0][0]
            cur.close()
            if raw_data == "":
                raw_data = "Data not available"
            data = f"Your <b>{chosen_opt}</b> is <b>{raw_data}</b>"
        else:
            data = "Please enter a valid option"


        bot.send_message(message.chat.id, data, parse_mode="HTMl")

        # reprompt user
        opts_display = []
        for opt in user_opts:
            opts_display.append(opt)

        # generate markup based on col names
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Quit", *opts_display)
        msg = bot.send_message(
            message.chat.id, "What else would you like to know?", reply_markup=markup
        )
        bot.register_next_step_handler(msg, process_option, args)


@bot.message_handler(commands=["broadcast_all"])
def broadcast_all_command(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # check access level either 1/2 (i.e. not 0)
    with DbSession() as s:
        user_rights = s.scalar(select(DB_TELEGRAM_USER_DB.TELE_USER_ACCESS_RIGHTS).where(DB_TELEGRAM_USER_DB.TELE_USER_ID == user_id))

        # user not rights
        if user_rights != 1 and user_rights != 2:
            return

        # ask them to type msg
        msg = bot.send_message(
            chat_id,
            "Please enter the message you wish to broadcast: \n<i>(Send any single character to cancel broadcast)</i>",
            parse_mode="HTML",
        )

        # get list of user_id in db
        users = s.execute(select(DB_TELEGRAM_USER_DB.TELE_USER_ID)).all()
        args = {"users": users}
        bot.register_next_step_handler(msg, process_broadcast_message, args)


@bot.message_handler(commands=["broadcast_school"])
def broadcast_school_command(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    # check access level either 1/2 (i.e. not 0)
    with DbSession() as s:
        user_rights = s.scalar(select(DB_TELEGRAM_USER_DB.TELE_USER_ACCESS_RIGHTS).where(DB_TELEGRAM_USER_DB.TELE_USER_ID == user_id))
        # user not rights
        if user_rights != 1 and user_rights != 2:
            return

        # prompt for school to broadcast
        schools = s.scalars(select(DB_SHOW_DATES.School).order_by(DB_SHOW_DATES.School.asc())).all()
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for school in schools:
            markup.add(school)
        msg = bot.send_message(
            chat_id,
            "Which school would you like to broadcast the message to?",
            reply_markup=markup,
        )

        bot.register_next_step_handler(msg, process_broadcast_school)


def process_broadcast_school(message):
    chat_id = message.chat.id
    message_school = message.text
    with DbSession() as s:
    # get list of user_id in db by coy
        users = s.scalars(select(DB_TELEGRAM_USER_DB.TELE_USER_ID).where(DB_TELEGRAM_USER_DB.TELE_USER_SCH == message_school))
        if len(users) < 1:
            bot.send_message(chat_id, "No users registered from that school.")
            return

        # ask them to type msg
        msg = bot.send_message(
            chat_id,
            "Please enter the message you wish to broadcast: \n<i>(Send any single character to cancel broadcast)</i>",
            parse_mode="HTML",
        )

        args = {"users": users}
        bot.register_next_step_handler(msg, process_broadcast_message, args)


def process_broadcast_message(message, args):
    chat_id = message.chat.id
    users = args["users"]
    broadcast_msg = message.text

    if len(broadcast_msg) <= 1:
        bot.send_message(
            chat_id,
            "Broadcast has been cancelled. Please use the command again to broadcast the message.",
        )
        return

    bot.send_message(chat_id, "Broadcasting message...")

    # send msg to all user_id with interval of 7ms (7/1000 s) (20msg/second)
    for user in users:
        try:
            user_id = user[0]
            bot.send_message(
                user_id,
                f"<b>Broadcast Message:</b>\n{broadcast_msg}",
                parse_mode="HTML",
            )
            time.sleep(7 / 1000)
        except:
            user_id = user[0]
            bot.send_message(
                chat_id,
                "Failed to send to user"
                + "[Click here to message the user directly](tg://user?id="
                + str(user_id)
                + ")",
                parse_mode="MarkdownV2",
            )

    bot.send_message(chat_id, "Message successfully broadcast!")


# Send Location handler
@bot.message_handler(commands=["send_location"])
def get_directions(message):
    global Perm_to_share_location
    if Perm_to_share_location == 1:
        try:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("School", "Padang")
            msg = bot.send_message(
                message.chat.id,
                "May I know which direction are you heading ?",
                reply_markup=markup,
            )
            bot.register_next_step_handler(msg, set_direction)

        except Exception as e:
            bot.reply_to(message, "Please contact the Developer. Thank you.")
    else:
        bot.send_message(
            message.chat.id,
            "Location sharing is currently turn off. Please contact Administrator if the service is required.",
        )

def set_direction(message):
    try:
        with DbSession() as s:
            location = message.text
            user_id = message.from_user.id
            name = s.scalar(select(DB_TELEGRAM_USER_DB.TELE_USER_NAME).where(DB_TELEGRAM_USER_DB.TELE_USER_ID ==user_id))
            school = s.scalar(select(DB_TELEGRAM_USER_DB.TELE_USER_SCH).where(DB_TELEGRAM_USER_DB.TELE_USER_ID ==user_id))
            transport_mode = s.scalar(select(DB_SHOW_DATES.TRANSPORT).where(DB_SHOW_DATES.School ==school))
            if transport_mode == "BUS":
                Arrival_direction = s.scalar(select(DB_BUS_OPS.Direction).where(DB_BUS_OPS.School == school))
                Departure_wave = s.scalar(select(DB_BUS_OPS.DEPARTURE_WAVE).where(DB_BUS_OPS.School == school))
            else:
                Arrival_direction = s.scalar(select(DB_MRT_OPS.Line).where(DB_MRT_OPS.School == school))
                Departure_wave = s.scalar(select(DB_MRT_OPS.Line).where(DB_MRT_OPS.School == school))

            if location in ["School","Padang"]:
                user_id = message.from_user.id
                s.execute(insert(DB_LOCATION_TABLE).values(TELE_USER_ID = user_id,  TELE_USER_NAME = name, TELE_USER_SCH=school,Arrival_direction =Arrival_direction ,Departure_direction=Departure_wave, DESTINATION_LOCATION= location))
                s.commit()
                bot.send_message(
                    message.chat.id,
                    "You may now share your location now.\n Here is the guide as well.Please wait as the guide load.",
                    reply_markup=types.ReplyKeyboardRemove(),
                )
                photo_guide = "/scripts/images/Tele_guide.png"
                bot.send_photo(
                    message.chat.id,
                    photo=open(photo_guide, "rb"),
                )
            else:
                msg = bot.send_message(
                    message.chat.id, "Improper Option. Please select an option. Thank you. "
                )
                bot.register_next_step_handler(msg, set_direction)

    except Exception as e:
        bot.reply_to(message, "Please contact the Developer. Thank you.")

# Location Sharing
@bot.message_handler(commands=["loc_disable"])
def handle_location2(message):
    global Perm_to_share_location
    chat_id = 0 #Replace The number 0 on the left to the Developers Telegram ID to receive message on if Location Sharing Perm Status
    if Perm_to_share_location == 0:
        Perm_to_share_location = 1
        bot.send_message(
            chat_id,
            "Perm to share location has been enabled.\n\n"
            + "Status:"
            + str(Perm_to_share_location),
        )
    elif Perm_to_share_location == 1:
        Perm_to_share_location = 0
        bot.send_message(
            chat_id,
            "Perm to share location has been disabled.\n\n"
            + "Status:"
            + str(Perm_to_share_location),
        )


# Location Handlers
@bot.message_handler(content_types=["location"])
def handle_location(message):
    global Perm_to_share_location
    user_id = message.from_user.id
    if Perm_to_share_location == 1:
        with DbSession() as s:
            location = s.scalar(select(DB_LOCATION_TABLE).where(DB_LOCATION_TABLE.TELE_USER_ID == user_id))
            try:
                if location is not None:
                    Location_latitude = str(message.location.latitude)
                    Location_longitude = str(message.location.longitude)
                    now = datetime.datetime.now()
                    if message.location.live_period == "None":
                        bot.send_message(
                            message.chat.id, "Location is not live, Please use the command /send_location again. "
                        )
                        bot.delete_message(message.chat.id, message.id)
                    else:
                        s.execute(update(DB_LOCATION_TABLE).where(DB_LOCATION_TABLE.TELE_USER_ID== user_id).values(LOCATION_LATITUDE = Location_latitude, LOCATION_LONGTITUDE = Location_longitude , LOCATION_SENT_TIME = now))
                        s.commit()
                        bot.send_message(message.chat.id, "Location Received")
                else:
                    bot.send_message(
                        message.chat.id,
                            "Please use the command /send_location first before sharing your location. Thank you!",
                        )
                    bot.delete_message(message.chat.id, message.id)

            except Exception as e:
                bot.send_message(
                        message.chat.id,
                        "Location Sharing has been disabled by Admin.\nPlease contact Administrator if the service is required.\nThank you and have a nice Day.",
                    )
                bot.delete_message(message.chat.id, message.id)
    else:
        bot.send_message(
            message.chat.id,
            "Location Sharing has been disabled by Admin.\nPlease contact Administrator if the service is required.\nThank you and have a nice Day.",
        )
        bot.delete_message(message.chat.id, message.id)


@bot.edited_message_handler(content_types=["location"])
def get_updated_location(message):
    global Perm_to_share_location
    Location_latitude = message.location.latitude
    Location_longitude = message.location.longitude
    user_id = str(message.from_user.id)
    now = datetime.datetime.now()
    with DbSession() as s:
        if Perm_to_share_location == 1:
            if message.location.live_period == None:
                # Delete Statement
                s.execute(delete(DB_LOCATION_TABLE).where(DB_LOCATION_TABLE.TELE_USER_ID == user_id))
                s.commit()
            else:
                s.execute(update(DB_LOCATION_TABLE).where(DB_LOCATION_TABLE.TELE_USER_ID== user_id).values(LOCATION_LATITUDE = Location_latitude, LOCATION_LONGTITUDE = Location_longitude , LOCATION_SENT_TIME = now))
                s.commit()
        else:
            bot.delete_message(message.chat.id, message.id)

bot.infinity_polling()
