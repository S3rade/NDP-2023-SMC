
import telebot
from telebot import types
import MySQLdb
import datetime
import googlemaps
import math
import time
from models_bftt import DB_Location , DB_User,DbSession 
from sqlalchemy import Text, Integer, DateTime, Date, BigInteger, create_engine, select, update, insert, delete, String

gmaps = googlemaps.Client(key='<<Google Cloud Services API Token>>') #Replace text with your own API Token Google Cloud Services

API_TOKEN = '<< Telegram API Token >>' #Replace with your own API Token Telegram
Perm_to_share_location = 0

bot = telebot.TeleBot(API_TOKEN)

now= datetime.now()

#Details to Receive 
user_dict = {}
destination_dict = {}

class User:
    def __init__(self, name):
        self.name = name
        self.coy = None
        
    
class Destination: 
    def _init__(self,name):
        self.location = None
        
@bot.message_handler(commands=[ 'check_handler']) #Command for Developer Team can use to check DB Connection if needed.
def test_con(message):
        with DbSession() as session:
            users = session.scalars(select(DB_User.TELE_USER_ID))
        
        
#Start Handler
@bot.message_handler(commands=[ 'start']) #One Time Start command to begin registration for Users.
def send_welcome(message):
        chat_id = message.chat.id
        User_ID= str(message.from_user.id)        
        with DbSession() as session:
            user2 = session.scalar(select(DB_User.TELE_USER_ID).where(DB_User.TELE_USER_ID==User_ID))
            
        if  user2 is not None:
            bot.send_message(message.chat.id, "You have registered before please use /help for aid. Thank you.")
        else:
            msg = bot.send_message(
            chat_id, "Greetings! Welcome to 42 SAR NDP 2023 Bot!\n" +
            "My name is MerMer and I will be assisting you today.\n" +
            '\n'+'May I know your name?')
        
            bot.register_next_step_handler(msg, process_name_step)

#User Details Handler 
def process_name_step(message): #Select Coy with user is from.
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('HQ','J','K','L','S')
        msg = bot.send_message(chat_id, 'May I know which coy are you from ?',reply_markup=markup)
        bot.register_next_step_handler(msg, process_coy)
    except Exception as e:
        bot.reply_to(message, 'Please contact the Developer. Thank you.')
        

def process_coy(message): #Process the reply and assigning of access rights. 
    try:
        chat_id = message.chat.id
        coy = message.text
        user=user_dict[chat_id] 
        if coy in ['HQ', 'J', 'K', 'L', 'S']:
            user.coy = coy
            access_rights= "0"
            photo_url= '/scripts/images/Tele_guide.png'
            bot.send_photo(message.chat.id,photo=open(photo_url,'rb'))
            with DbSession() as session:
                user3 = DB_User(
                    TELE_USER_ID=chat_id,
                    TELE_USER_COY=coy,
                    TELE_USER_NAME=user.name,
                    TELE_USER_ACCESS_RIGHTS=access_rights
                )
                session.add(user3)
                session.commit()
            msg = bot.send_message(chat_id, 'Please do the following steps: \n1) Use the command /send_location \n2)using the guide above to share location.',reply_markup=types.ReplyKeyboardRemove())
        else:
            msg = bot.send_message(chat_id, 'Improper Option. Please select an option. Thank you. ')
            bot.register_next_step_handler(msg, process_coy)
            
    except Exception as e:
        bot.reply_to(message, 'Please contact the Developer. Thank you.')

#Help handler   
@bot.message_handler(commands=['help']) 
def help_command(message):
    try:
        User_ID= str(message.from_user.id)
        with DbSession() as session:
            access_right = session.scalar(select(DB_User.TELE_USER_ACCESS_RIGHTS).where(DB_User.TELE_USER_ID==User_ID))

        if access_right == 1:
            bot.send_message(
                message.chat.id, 
                "Greetings! Welcome to NDP 2023 InfoBot!\n" + "My name is MerMer and I will be assisting you today.\n" +
                "These are the commands you can use in the bot:\n"+
                '/your_details to check your details.\n'+
                '/edit to edit your details.\n'+
                '/find_my_way to display the rerouting directions.\n'+
                '/send_location, for the live location tracking function.\n'+
                '/broadcast_all to broadcast to 42 SAR personnel.\n'+
                '/broadcast_coy to broadcast to 42 SAR personnel.\n'+
                '/contact_us to contact Customer Support Team.\n'+
                '\n'+'Thank you! '
            )
        elif access_right == 2 :
            bot.send_message(
                message.chat.id, 
                "Greetings! Welcome to NDP 2023 InfoBot!\n" + "My name is MerMer and I will be assisting you today.\n" +
                "These are the commands you can use in the bot:\n"+
                '/your_details to check your details.\n'+
                '/edit to edit your details.\n'+
                '/send_location, for the live location tracking function.\n'+
                '/broadcast_all to broadcast to 42 SAR personnel.\n'+
                '/loc_disable to toggle permission to send location.\n'
                '/check_handler to check Database Connection.\n\n'+
                '\nThank you! '
                )
        
        else:
            bot.send_message(
                message.chat.id, 
                "Greetings! Welcome to NDP 2023 InfoBot!\n" + "My name is MerMer and I will be assisting you today.\n" +
                "These are the commands you can use in the bot:\n"+
                '/your_details to check your details.\n'+
                '/edit to edit your details.\n'+
                '/find_my_way to display the rerouting directions.\n'+
                '/send_location, for the live location tracking function.\n'+
                '/contact_us to contact Customer Support Team.\n'+
                '\n'+'Thank you!',
                
            )
    except:
        pass
        
# Contact Us handler   
@bot.message_handler(commands=['contact_us'])
def contact_us_command(message):
    try:
        chat_id = message.chat.id
        msg = bot.send_message(
                chat_id, "Please reply with the message which you would like to tell Customer Support Team. Thank you. ")
            
        bot.register_next_step_handler(msg, contact_us_forward)
    except Exception as e:
        bot.reply_to(message, 'Please contact the Developer. Thank you.')
    
        
def contact_us_forward(message): #Send help message from user to customer support chat group 
    try: 
        contact_us_chat_id = 0 #Replace the number on the left with the chat group ID. Can use Raw Data bot/ IDbot in telegram to find the ID of the chat. Please ensure the chat group is 1 Day old.
        message_from_user = message.text
        chat_id = message.chat.id
        if message_from_user != None:
            with DbSession() as session:
                name, coy = session.execute(select(DB_User.TELE_USER_COY,DB_User.TELE_USER_NAME).where(DB_User.TELE_USER_ID==chat_id)).first().tuple()
            
            bot.send_message(contact_us_chat_id,"Customer Issues/Inquiry: \n\n"+"From: \nName: "+ name+ "\nSchool: "+ coy+"\n\nMessage for Customer:\n\n "+str(message_from_user)+"\n\n"+"[Click here to reply](tg://user?id="+ str(chat_id) +")",parse_mode="MarkdownV2")
            bot.send_message(chat_id, "Message has been sent to Customer Support Team. \n\nWe will get back to you as soon as possible.\n\n Thank you !" )  

        else:
            msg=bot.send_message(message.chat.id, "Please send message again" )
            bot.register_next_step_handler(msg, contact_us_forward) 
    except Exception as e:
        bot.reply_to(message, 'Please contact the Developer. Thank you.')
 
# Edit name and school
@bot.message_handler(commands=['edit'])
def edit_db_details(message):
    try:
        chat_id= message.chat.id
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Edit Name','Edit Coy')
        msg = bot.send_message(chat_id, "May I know which details would you like to change? \n\n ",reply_markup=markup)
            
        bot.register_next_step_handler(msg, edit_filter)
    except Exception as e:
        bot.reply_to(message, 'Please try again. Thank you.')

def edit_filter(message):
    try:
        filter_message = message.text
        if filter_message == ("Edit Name"):
            msg= bot.send_message(message.chat.id,"Please reply with the name you want to change to. Thank you.")
            bot.register_next_step_handler(msg, edit_name)
        
        elif filter_message == ("Edit Coy"):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('HQ','J','K','L','S')
            msg= bot.send_message(message.chat.id,"Please select the correct Coy. Thank you",reply_markup=markup)
            bot.register_next_step_handler(msg, edit_date)
        else:
            msg= bot.send_message(message.chat.id,"Please select an option. Thank you.")
            bot.register_next_step_handler(msg, edit_filter)
    except Exception as e:
        bot.reply_to(message, 'Please try again. Thank you.')

def edit_name(message):
    try:
        chat_id = message.chat.id
        name = message.text
        with DbSession() as session:
            session.execute(update(DB_User).where(DB_User.TELE_USER_ID == chat_id).values(TELE_USER_NAME = name))
            session.commit()
        bot.send_message(chat_id,"Your name has been updated, please use /your_details to check. Thank you ! ",reply_markup=types.ReplyKeyboardRemove())
    except Exception as e:
        bot.reply_to(message, 'Please try again. Thank you.')      
      
def edit_date(message):
    try:
        chat_id = message.chat.id
        COY=message.text

        if COY not in ['HQ', 'J', 'K', 'L', 'S']:
            msg = bot.send_message(chat_id, 'Improper Option. Please select an option. Thank you. ')
            bot.register_next_step_handler(msg, edit_date)
        else:
            with DbSession() as session:
                session.execute(update(DB_User).where(DB_User.TELE_USER_ID == chat_id).values(TELE_USER_COY = COY))
                session.commit()
            bot.send_message(chat_id,"Your coy has been updated, please use /your_details to check. Thank you ! ",reply_markup=types.ReplyKeyboardRemove())
        
    except Exception as e:
        bot.reply_to(message, 'Please try again. Thank you.')

@bot.message_handler(commands=['find_my_way'])
def find_my_way(message):   
    chat_id=message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('City Hall', 'North Bridge Road')
    msg= bot.send_message(chat_id,"Please select a starting location. Thank you",reply_markup=markup)
    bot.register_next_step_handler(msg,load_options)
    
def load_options(message):
    try:
        chat_id=message.chat.id
        start_point = message.text
        if start_point == "City Hall":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('National Gallery Singapore', 'Suntec City')
            msg = bot.send_message(chat_id,"Please select which is your desired end location.",reply_markup=markup)
            bot.register_next_step_handler(msg,sharing_directions)
        
        elif start_point == "North Bridge Road":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('Victoria Concert Hall')
            msg = bot.send_message(chat_id,"Please select which is your desired end location.",reply_markup=markup)
            bot.register_next_step_handler(msg,sharing_directions)
            
        else:
            msg = bot.send_message(chat_id, 'Improper Option. Please select an option. Thank you. ')
            bot.register_next_step_handler(msg, load_options)
    except Exception as e:
        bot.reply_to(message, 'An error occured. Please try aagian. Thank you.')     
            
    
def sharing_directions(message):
    chat_id = message.chat.id
    destination= message.text
    if destination == "National Gallery Singapore":
        bot.send_message(chat_id,"Here is the guide. Please wait as it sends. Thank you!",reply_markup=types.ReplyKeyboardRemove())
        photo_url = "/scripts/images/NGS.png"
        bot.send_photo(chat_id, photo=open(photo_url, "rb"), caption="Route from City Hall MRT to National Gallery Singapore.")
        
    elif destination == "Suntec City":
        bot.send_message(chat_id,"Here is the guide. Please wait as it sends. Thank you!",reply_markup=types.ReplyKeyboardRemove())
        photo_url = "/scripts/images/Suntec_City.png"
        bot.send_photo(chat_id, photo=open(photo_url, "rb"), caption="Route from City Hall MRT to Suntec City.")
        
    elif destination == "Victoria Concert Hall":
        bot.send_message(chat_id,"Here is the guide. Please wait as it sends. Thank you!",reply_markup=types.ReplyKeyboardRemove())
        photo_url = "/scripts/images/VCH.png"
        bot.send_photo(chat_id, photo=open(photo_url, "rb"), caption="Route from North Bridge Road MRT to Victoria Concert Hall.")

# Your Details Handler
@bot.message_handler(commands=['your_details'])
def edit_db_details(message):
    try:
        chat_id = message.chat.id
        with DbSession() as session:
            name, coy = session.execute(select(DB_User.TELE_USER_NAME, DB_User.TELE_USER_COY).where(DB_User.TELE_USER_ID == chat_id)).first().tuple()
        msg = "Hello! Here are your details \n\n"+"Your name is "+ name +".\n\n You are from " + coy +\
            ".\n\n Do use the command /edit to chang details if they are inaccurate."
        bot.send_message(chat_id, msg)  
    except Exception as e:
        bot.reply_to(message, 'Please try again. Thank you.')         
        
#Send Location handler   
@bot.message_handler(commands=['send_location'])
def get_directions(message):
    global Perm_to_share_location
    if Perm_to_share_location == 1:
        try:
            user_id= message.from_user.id
            with DbSession() as session:
                coy, name = session.execute(select(DB_User.TELE_USER_COY, DB_User.TELE_USER_NAME).where(DB_User.TELE_USER_ID == user_id)).first().tuple()
                session.add(DB_Location(
                    TELE_USER_ID=user_id,
                    TELE_USER_COY=coy,
                    TELE_USER_NAME=name
                ))
                session.commit()
                
            photo_url= '/scripts/images/Tele_guide.png'
            bot.send_photo(message.chat.id,photo=open(photo_url,'rb'))
            bot.send_message(message.chat.id, 'Please Share your location.\n Here is the guide again.')
    
        except Exception as e:
            bot.reply_to(message, 'Please try again. Thank you.')
    else:
        bot.send_message(message.chat.id,'Location Sharing has been disabled by Admin.\nPlease contact Administrator if the service is required.\nThank you and have a nice Day.')

#Location Handlers2
@bot.message_handler(content_types=['location'])
def handle_location(message):
    global Perm_to_share_location
    if Perm_to_share_location == 1:
        user_id= message.from_user.id
        with DbSession() as session:
            location = session.scalar(select(DB_Location).where(DB_Location.TELE_USER_ID == user_id))
            if location is not None:
                Location_latitude = str(message.location.latitude)
                Location_longitude = str(message.location.longitude)
                now=datetime.now()
                if message.location.live_period == "None" :
                    bot.send_message(
                        message.chat.id,
                        "Location is not live, Please resent location "
                    )
                else:
                    
                    location.LOCATION_LATITUDE = Location_latitude
                    location.LOCATION_LONGTITUDE = Location_longitude
                    location.LOCATION_SENT_TIME = now
                    session.commit()
                    
                    bot.send_message(
                            message.chat.id,
                        "Location Received"
                    )
            else:
                coy, name = session.execute(select(DB_User.TELE_USER_COY, DB_User.TELE_USER_NAME).where(DB_User.TELE_USER_ID == user_id)).first().tuple()
                location = DB_Location(
                    TELE_USER_ID=user_id,
                    TELE_USER_COY=coy,
                    TELE_USER_NAME=name
                )
                session.add(location)           
    else:
        bot.send_message(message.chat.id,'Location Sharing has been disabled by Admin.\nPlease contact Administrator if the service is required.\nThank you and have a nice Day.')
        bot.delete_message( message.chat.id, message.id)  
        
#Location Sharing 
@bot.message_handler(commands=['loc_disable']) #Developer Rights to stop everyone from sharing the location. This deletes the exisiting live location incase the SQL sever creates a back log and cant commit over old data.
def handle_location2(message): 
    global Perm_to_share_location
    chat_id= 0 #Developer Chat ID should be replaced with the number on the left.
    if Perm_to_share_location == 0:
        Perm_to_share_location = 1
        bot.send_message(chat_id, "Perm to share location has been enabled.\n\n" + "Status:"+str(Perm_to_share_location))
    elif Perm_to_share_location == 1:
        Perm_to_share_location = 0
        bot.send_message(chat_id, "Perm to share location has been disabled.\n\n" + "Status:"+str(Perm_to_share_location))
    
     
#Detect location sharing.
@bot.edited_message_handler(content_types=['location'])
def get_updated_location(message):
    global Perm_to_share_location
    with DbSession() as session:
        if Perm_to_share_location == 1:
            Location_latitude = message.location.latitude
            Location_longitude = message.location.longitude
            User_ID= str(message.from_user.id)
            now=datetime.now()
            location = session.scalar(select(DB_Location).where(DB_Location.TELE_USER_ID == User_ID))
            if message.location.live_period == None:
                session.delete(location)
            else:
                if location == None:
                    coy, name = session.execute(select(DB_User.TELE_USER_COY, DB_User.TELE_USER_NAME).where(DB_User.TELE_USER_ID == User_ID)).first().tuple()
                    location = DB_Location(
                        TELE_USER_ID=User_ID,
                        TELE_USER_COY=coy,
                        TELE_USER_NAME=name
                    )
                    session.add(location)
                
                location.LOCATION_LATITUDE = Location_latitude
                location.LOCATION_LONGTITUDE = Location_longitude
                location.LOCATION_SENT_TIME = now
            session.commit()
                           
        else:
            bot.send_message(message.chat.id,'Location Sharing has been disabled by Admin.\nPlease contact Administrator if the service is required.\nThank you and have a nice Day.')
            bot.delete_message( message.chat.id, message.id)


@bot.message_handler(commands=["broadcast_all"])
def broadcast_all_command(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with DbSession() as session:
        user_rights = session.scalar(select(DB_User.TELE_USER_ACCESS_RIGHTS).where(DB_User.TELE_USER_ID == user_id))
    
    if user_rights != 1 and user_rights != 2:
        return

    # ask them to type msg
    msg = bot.send_message(chat_id, "Please enter the message you wish to broadcast: ")
    
    with DbSession() as session:
        users = session.scalars(select(DB_User.TELE_USER_ID)).all()
    args = {"users": users}

    bot.register_next_step_handler(msg, process_broadcast_message, args)


@bot.message_handler(commands=["broadcast_cat"])
def broadcast_cat_command(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    with DbSession() as session:
        user_rights = session.scalar(select(DB_User.TELE_USER_ACCESS_RIGHTS).where(DB_User.TELE_USER_ID == user_id))
        
    if user_rights != 1 and user_rights != 2:
        return

    # prompt for coy to broadcast
    coys = ["HQ", "Jaguar", "Kaffir", "Lion", "Serval"]
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for coy in coys:    
        markup.add(coy)
    msg = bot.send_message(
        chat_id,
        "Which coy would you like to broadcast the message to?",
        reply_markup=markup,
    )

    bot.register_next_step_handler(msg, process_coy2)


def process_coy2(message):
    chat_id = message.chat.id
    coy = message.text
    # get list of user_id in db by coy
    if coy not in ["HQ","Jaguar","Kaffir","Lion","Serval"]:
        msg =bot.send_message(chat_id, "Please select a valid option.")
        bot.register_next_step_handler(msg,process_coy2)
        return
    coys_short = {"HQ": "HQ", "Jaguar": "J", "Kaffir": "K", "Lion": "L", "Serval": "S"}
    with DbSession() as session:
        userIds = session.scalars(select(DB_User.TELE_USER_ID).where(DB_User.TELE_USER_COY == coys_short[coy])).all()

    if len(userIds) == 0:
        bot.send_message(chat_id, "No users registered from that company.")
        return

    # ask them to type msg
    msg = bot.send_message(chat_id, "Please enter the message you wish to broadcast: ")

    args = {"users": userIds}
    bot.register_next_step_handler(msg, process_broadcast_message, args)


def process_broadcast_message(message, args):
    chat_id = message.chat.id
    users = args["users"]
    broadcast_msg = message.text

    bot.send_message(chat_id, "Broadcasting message...")

    # send msg to all user_id with interval of 7ms (7/1000 s) (20msg/second)
    for user_id in users:
        bot.send_message(
            user_id, f"<b>Broadcast Message:</b>\n{broadcast_msg}", parse_mode="HTML"
        )
        time.sleep(7 / 1000)

    bot.send_message(chat_id, "Message successfully broadcast!")

bot.infinity_polling()
