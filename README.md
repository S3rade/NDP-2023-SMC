![42 SAR DATA TEAM LOGO](images/42%20Data%20Team%20logo.gif)

This was the work of 42 SAR NDP Data Team, comprising of NSF only.

## Developers on this project.
Manager of Project: 
[s3rade](https://github.com/S3rade)

Developers:
[s3rade](https://github.com/S3rade),
[acidMyke](https://github.com/acidMyke),
[nerospark](https://github.com/nerospark),
[notyumin](https://github.com/notyumin)


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

## ALP Bot
| File Name | Purpose |
| --- | --- |
| /ALP_Bot | Folder to Blue Force Tracker Bot Stuff|
| alp_app.py | Internal Blue Force Bot |
| alp_models.py | SQLAlchemy BFTT DB Table Models |



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
The `Estimate Time of Arroval (ETA)` will be refreshed on demand. A simple refresh button will be location as the stationary tool bar.
This is to reduce cost as the Google Map Routes API as it is a pay per query. 

To find out more about the costing of current Routes API click [here](https://mapsplatform.google.com/pricing/).

# final_telebot.py
NDP Info Bot for Teachers to access information and details that they require. Contains Sharing Location Function for ALP. This will then be displayed in the website.
Broadcast to 2 options, `All` & `School`. This allow you to relay message to them easily, limited to Access level 1 for NDP staff and 2 for Developers.
Users are able to easily change their school and name using the edit function.

# blue_force_bot.py
Sharing of Live location to give higher ups the visibilty of servicemen precense.

# in_proximity.py
Executes with cron job to check if the ALP is within destination Vainity (Padang / School). 

Auto set to NULL until triggered.  

# geo_fence.py
Detect is the user are in the vacinity of `School`, `Padang`, `Seats`. In between these locations will be automatically set a `Enroute`.

# alp_app.py
This bot are for Army Liason Personnel to use when they are ferrying the kids to and from schools with the checkpoints to tracked the timing required for documentation to display if they have hit the required KPIs. 

# models_info_bot.py
Required to Establish the class for SQLAlchemy to detect which database & table is being uses. AKA Corellation Chart.

# models_bftt.py
Required to Establish the class for SQLAlchemy to detect which database & table is being uses. AKA Corellation Chart.

# alp_models.py
Required to Establish the class for SQLAlchemy to detect which database & table is being uses. AKA Corellation Chart.

# /template
This folder contains all the HTML Template for each page.

# /staticFiles
This folder contains the CSS for the HTML Template.

# /images
This Folder contains the documents that we need to send out for the Debian Server can retrieve from.

# Lines to change
### Google Maps API Token:
1. Line 14 in final_telebot.py
2. Line 12 in BFTT/blue_force_bot.py
3. Line 18 in website_display.py

### Telegram API Token:
1. Line 18 in final_telebot.py<sup>*</sup> 
2. Line 14 in BFTT/blue_force_bot.py<sup>*</sup> 
3. Line 13 in ALP_Bot/alp_app.py<sup>**</sup> 

`*` : Token 1 

`**` : Token 2

### MYSQL DB Server Details
1. Line 24 - 28 in final_telebot.py
2. Line 7 in models_info_bot.py
3. Line 6 in BFTT/models_bftt.py
4. Line 415 in ALP_Bot/alp_app.py

### Other Things to Change
1. Username of NDP NE Info Bot(Main) in ALP_Bot/alp_app.py Line 14. 


## Guides 
| Name  | Link to Guide | Purpose |
| --- | --- | --- |
|Creation of AWS Free Account | *[Click Here for Guide](https://repost.aws/knowledge-center/create-and-activate-aws-account)*| Server|
|Setting up an AWS EC2 Instance | *[Click Here for Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html)*| Housing all the codes |
|Setting up an AWS RDS MySQL Server | *[Click Here for Guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.MySQL.html)*| Housing all the data|
|Setting up an FTP Server | *[Click Here for Guide](https://www.linkedin.com/pulse/configure-ftp-aws-ec2linux-ami-iftesum-ul-bashri/)* | Easy transfer files between user and server|
|Setting up an SSH Server in EC2 | *[Click Here for Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html)*| Connect into server from laptop for easier access|
|Installation of Python |*[Click Here for guide](https://www.scaler.com/topics/python/install-python-on-linux/)*| Installing Python Programming Language for codees to be able to run|
|Setting up an SQL on the EC2 |*[Click Here for Guide](https://www.geeksforgeeks.org/how-to-install-mysql-on-linux/)*| Prerequisites to be able to connect to AWS RDS MYSQL Server |
|Importing Data in MYSQL Database Server|*[Click Here for Guide](https://blog.skyvia.com/how-to-import-csv-file-into-mysql-table-in-4-different-ways/)*| Uploading data required|
|Making a script into a Service |*[Click Here for Guide](https://tecadmin.net/run-shell-script-as-systemd-service/)*| Running the codes 24/7 without interuption|




