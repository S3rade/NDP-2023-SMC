# NDP-2023-SMC
NDP 2023 Spectator Management Committee Developments.

## NE Show Bots
| File Name | Purpose |
| --- | --- |
| final_telebot.py | Telegram Bot Codes |
| alp_progress.py | Progress Bot for Taking down Key timing|
| in_proximity.py | Geo Fencing v1 |
| geo_fence.py | Geo Fencing v2 |
| models_info_bot.py | SQLAlchemy DB Table Models |


## Blue Force Tracker Bot
| File Name | Purpose |
| --- | --- |
| /BFTT | Folder to Blue Force Tracker Bot Stuff|
| blue_force_bot.py | Internal Blue Force Bot |
| models_bftt.py | SQLAlchemy BFTT DB Table Models |


## Website Display Bot
| File Name | Purpose |
| --- | --- |
| website_display.py | Web Application Codes |
| /templates | Folder to house HTML Format |
| /staticFiles | Folder to house stylesheet for HTML |

## Common Folder
| File Name | Purpose |
| --- | --- |
| /images | Folder to house images to be sent out |

# website_display.py 
This is where the web application is initiated. This will link up to the database where the Geoloactions are updated.
The `Estimate Time of Arroval (ETA)` will be refresh on demand. A simple refresh button will be location as the stationary tool bar.
This is to reduce cost as the Google Map Routes API as it is a pay per query. 

To find out more about the costing of current Routes API click [here](https://mapsplatform.google.com/pricing/).

# final_telebot.py
NDP Info Bot for Teachers to access information and details that they require. Contains Sharing Location Function for ALP. This will then be displayed in the website.
Broadcast to 2 options, `All` & `School`. This allow you to relay message to them easily, limited to Access level 1 for NDP staff and 2 for Developers.
Users are able to easily change their school and name using the edit function.

# blue_force_bot.py
Sharing of Live location to give higher ups the visibilty of servicemen precense.

# in_proximity.py
Executes with cron job to check if the ALP is within destination Vainity (Padang / School).Auto set to NULL until triggered.  

# geo_fence.py
Detect is the user are in the vacinity of `School`,`Padang`,`Seats`. In between these locations will be automatically set a `Enroute`.

# models.py
Required to Establish the class for SQLAlchemy to detect which database & table is being uses. AKA Corellation Chart.

# /template

# /staticFiles

# /images

## Developers on this project.
Manager of Project: 
s3rade

Senior Developers:
s3rade
AcidMyke

Junior Developers:
