from datetime import datetime, timezone
from os import environ
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes, filters, MessageHandler, Updater, ConversationHandler, CallbackQueryHandler, ApplicationBuilder, PicklePersistence
from alp_models import User, Show, Progress, progress_step_type
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import sessionmaker, Session
from asyncio import create_task, sleep
from telegram.helpers import escape_markdown

environ['TZ'] = 'Asia/Singapore'

BOT_TOKEN = '<<BOT TOKEN>>'
MAIN_BOT_USERNAME = '<<Main User BOT NAME>>'

bus_progress_data = {
	'0': {
		'start': True,
		'buttons': {
			'next': {
				'label': 'I have reach school',
				'step': '1'
			},
		}
	},
	'1': {
		'checked': "Reach school",
		# 'unchecked': "",
		'buttons': {
			'next': {
				'label': 'First bus has leave school',
				'step': '2'
			},
			'back': {
				'label': 'Back, I have not reach school',
				'step': '0'
			}
		}
	},
	'2': {
		'checked': "First bus had left school",
		# 'unchecked': "",
		'buttons': {
			'next': {
				'label': 'Last bus has leave school',
				'step': '3'
			},
			'back': {
				'label': 'Back, first bus has not leave school',
				'step': '1'
			}
		}
	},
	'3': {
		'checked': "Last bus had left school",
		# 'unchecked': "",
		'buttons': {
			'next': {
				'label': 'The first bus has reach esplanade drive',
				'step': '4'
			},
			'back': {
				'label': 'Back, last bus has not leave school',
				'step': '2'
			}
		}
	},
	'4': {
		'checked': "First bus had reach esplanade drive",
		# 'unchecked': "",
		'buttons': {
			'next': {
				'label': 'The last bus has reach esplanade drive',
				'step': '5'
			}, 
			'back': {
				'label': 'Back, first bus has not reach esplanade drive',
				'step': '3'
			}
		}
	},
	'5': {
		'checked': "Last bus had reach esplanade drive",
		# 'unchecked': "",
		'buttons': {
			'next': {
				'label': 'The first class has been seated',
				'step': '6'
			},
			'back': {
				'label': 'Back, last bus has not reach esplanade drive',
				'step': '4'
			}
		}
	},
	'6': {
		'checked': "First class seated",
		# 'unchecked': "",
		'buttons': {
			'next': {
				'label': 'The last class has been seated (Fully seated)',
				'step': '7'
			},
			'back': {
				'label': 'Back, first class has not been seated',
				'step': '5'
			}
		}
	},
	'7': {
		'checked': "Fully seated",
		'footnote': "*The following buttons are only to be used after NDP*",
		# 'unchecked': "",
		'buttons': {
			'next': {
				'label': 'Everyone has left seating gallery',
				'step': '8'
			},
			'back': {
				'label': 'Back, last class has not been seated',
				'step': '6'
			}
		}
	},
	'8': {
		'checked': "Left seating gallery",
		# 'unchecked': "",
		'buttons': {
			'next': {
				'label': 'Started boarding first bus',
				'step': '9'
			},
			'back': {
				'label': 'Back, everyone has not left seating gallery',
				'step': '7'
			}
		}
	},
	'9': {
		'checked': "Started boarding first bus",
		# 'unchecked': "",
		'buttons': {
			'next': {
				'label': 'Started boarding last bus',
				'step': '9A'
			},
			'alt': {
				'label': 'First bus has left padang',
				'step': '9B'
			},
			'back': {
				'label': 'Back, haven\'t started boarding first bus',
				'step': '8'
			}
		}
	},
	'9A': {
		'checked': "Started boarding last bus",
		# 'unchecked': "",
		'buttons': {
			'next': {
				'label': 'Last bus has left padang',
				'step': '10',
				'show': lambda p: p.p_9B != None,
			},
			'alt': {
				'label': 'First bus has left padang',
				'step': '9B',
				'show': lambda p: p.p_9B == None,
			},
			'back': {
				'label': 'Back, haven\'t started boarding last bus',
				'step': '9',
			}
		}
	},
	'9B': {
		'checked': "First bus had left padang",
		# 'unchecked': "",
		'buttons': {
			'alt': {
				'label': 'Last bus has left padang',
				'step': '10',
				'show': lambda p: p.p_9A != None,
			},
			'next': {
				'label': 'Started boarding last bus',
				'step': '9A',
				'show': lambda p: p.p_9A == None,
			},
			'back': {	
				'label': 'Back, first bus has not left padang',
				'step': '9',
				'show': lambda p: p.p_9A != None,
			},
			'back-alt': {
				'label': 'Back, first bus has not left padang',
				'step': '9A',
				'show': lambda p: p.p_9A == None,
			}
		}
	},
	'10': {
		'checked': "Last bus had left padang",
		# 'unchecked': "",
		'buttons': {
			'next': {
				'label': 'First bus has reach school',
				'step': '11'
			},
			'back': {
				'label': 'Back, last bus has not left padang',
				'step': '9A',
				'show': lambda p: p.p_9A == None,
			},
			'back-alt': {
				'label': 'Back, last bus has not left padang',
				'step': '9B',
				'show': lambda p: p.p_9A != None,
			}
		}
	},
	'11': {
		'checked': "First bus had reach school",
		# 'unchecked': "",
		'buttons': {
			'next': {
				'label': 'Last bus has reach school',
				'step': '12'
			},
			'back': {
				'label': 'Back, first bus has not reach school',
				'step': '10'
			}
		}
	},
	'12': {
		'checked': "Last bus had reach school",
		'end': True,
	}
}

mrt_progress_data = {
	'0': {
		'start': True,
		'buttons': {
			'next': {
				'label': 'I have reach school',
				'step': '1'
			},
		}
	},
	'1': {
		'checked': "Reach school",
		# 'unchecked': "",
		'buttons': {
			'next': {
				'label': 'Leave school for MRT',
				'step': '2'
			},
			'back': {
				'label': 'Back, haven\'t reach school',
				'step': '0'
			}
		}
	},
	'2': {
		'checked': "Left school for boarding station",
		# 'unchecked': "",
		'buttons': {
			'next': {
				'label': 'Reach boarding station',
				'step': '3'
			},
			'back': {
				'label': 'Back, haven\'t left school',
				'step': '1'
			}
		}
	},
	'3': {
		'checked': "Reach boarding station",
		# 'unchecked': "",
		'buttons': {
			'next': {
				'label': 'Train has depart from boarding station',
				'step': '4'
			},
			'back': {
				'label': 'Back, haven\'t reach boarding station',
				'step': '2'
			}
		}
	},
	'4': {
		'checked': "Train had departed from boarding station",
		# 'unchecked': "",
		'buttons': {
			'next': {
				'label': 'Reach destination station',
				'step': '5'
			},
			'back': {
				'label': 'Back, train has not departed from boarding station',
				'step': '3'
			}
		}
	},
	'5': {
		'checked': "Reach destination station",
		# 'unchecked': "",
		'buttons': {
			'next': {
				'label': 'The first class has been seated',
				'step': '6'
			},
			'back': {
				'label': 'Back, haven\'t reach destination station',
				'step': '4'
			}
		}
	},
	'6': {
		'checked': "First class seated",
		# 'unchecked': "",
		'buttons': {
			'next': {
				'label': 'The last class has been seated (Fully seated)',
				'step': '7'
			},
			'back': {
				'label': 'Back, first class has not been seated',
				'step': '5'
			}
		}
	},
	'7': {
		'checked': "Fully seated",
		'footnote': "*The following buttons are only to be used after NDP*",
		# 'unchecked': "",
		'buttons': {
			'next': {
				'label': 'Everyone has left seating gallery',
				'step': '8'
			},
			'back': {
				'label': 'Back, not fully seated',
				'step': '6'
			}
		}
	},
	'8': {
		'checked': "Left seating gallery",
		# 'unchecked': "",
		'buttons': {
			'next': {
				'label': 'Reach boarding station',
				'step': '9'
			},
			'back': {
				'label': 'Back, haven\'t left seating gallery',
				'step': '7'
			}
		}
	},
	'9': {
		'checked': "Reach boarding station",
		# 'unchecked': "",
		'buttons': {
			'next': {
				'label': 'Train has depart from boarding station',
				'step': '10'
			},
			'back': {	
				'label': 'Back, haven\'t reach boarding station',
				'step': '8'
			}
		}
	},
	'10': {
		'checked': "Train has departed from boarding station",
		# 'unchecked': "",
		'buttons': {
			'next': {
				'label': 'Reach destination station',
				'step': '11'
			},
			'back': {	
				'label': 'Back, train has not departed from boarding station',
				'step': '9'
			}
		}
	},
	'11': {
		'checked': "Reach destination station",
		# 'unchecked': "",
		'buttons': {
			'next': {
				'label': 'Reach school',
				'step': '12'
			},
			'back': {
				'label': 'Back, haven\'t reach destination station',
				'step': '10'
			}
		}
	},
	'12': {
		'checked': "Reach school",
		'end': True,
	}
}
# Database
engine = create_engine(
	'mysql://ADMIN_USERNAME:ADMIN_PASSWORD@nMYSQL_DB_SERVER_ADDRESS/MYSQLDB_SCHEMA',
	pool_pre_ping=True
)

def get_c_text(v):
	r = v.get('checked', None)
	return r
	
def get_p_time(p, s):
	r = getattr(p, f'p_{s}', None)
	return r

async def send_edit_progress(update: Update, context: ContextTypes.DEFAULT_TYPE, p: Progress, force_send = False):
	chat_id = p.user_id
  
	msg_key = f'progress_{p.id}_msg_id'
	if force_send and msg_key in context.user_data:
		try:
			await context.bot.delete_message(chat_id, context.user_data[msg_key])
		except Exception as e:
			print(e)
		del context.user_data[msg_key]

	cp = p.cur_p
	is_bus = p.is_bus
	data = bus_progress_data if is_bus else mrt_progress_data
	cd = data[cp]
	msg_content = 'Progress: '
	if cp != '0':
		checked_timings = sorted(
			[('✅ ' + get_c_text(v), get_p_time(p,s)) for s,v in data.items() if get_p_time(p,s) is not None and get_c_text(v) is not None ],
			key=lambda t: t[1]
		)
		msg_content += '\n\t' + '\n\t'.join([t[0] for t in checked_timings])
	else:
		msg_content += 'None'
		
	reply_markup = None
	is_end = isinstance(cd, dict) and cd.get('end', False)
	msg_content = escape_markdown(msg_content)
	if not is_end:
		if 'footnote' in cd:
			msg_content += '\n\n' + cd['footnote']
		reply_markup = InlineKeyboardMarkup.from_column([
			InlineKeyboardButton(v['label'], callback_data=d) for d, v in cd['buttons'].items() if 'show' not in v or ( 'show' in v and v['show'](p) )
		])
  
	msg_content += escape_markdown(f'\n\n*Last updated at {datetime.now().strftime("%H:%M:%S")}*')
	
	try:
		if msg_key in context.user_data:
			await context.bot.edit_message_text(msg_content, chat_id, context.user_data[msg_key], reply_markup=reply_markup, parse_mode='Markdown')
		else:
			msg = await context.bot.send_message(chat_id, msg_content, reply_markup=reply_markup, parse_mode='Markdown')
			context.user_data[msg_key] = msg.message_id
			p.msg_id = msg.message_id
	except Exception as e:
		print(f'Error sending/editing message for progress {p.id}: {e}')
		raise e

	if is_end:
		await context.bot.send_message(chat_id, 'You have completed all the progress steps! Thank you for using the ALP Progress Tracker Bot!!\n\nHave a safe trip home!')
		return

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
	with Session(engine) as session:
		res = session.execute(
			select(User, Show)
			.where(User.tele_user_id == update.effective_user.id)
			.join_from(User, Show, Show.school == User.tele_user_sch)
		).first()
		if res is None:
			await update.effective_chat.send_message(
				'Welcome to the ALP Progress Tracker Bot!! \nYou are not registered. Please switch to the main bot and register there.',
				reply_markup=InlineKeyboardMarkup.from_column([
					InlineKeyboardButton('Switch to Main Bot', url=f'tg://resolve?domain={MAIN_BOT_USERNAME}'),
					InlineKeyboardButton('I have registered', callback_data='_start')
				])
			)
			return ConversationHandler.END
		else:
			user, show = res.tuple()
			context.user_data['user'] = user
			context.user_data['show'] = show
			progress = session.scalars(
				select(Progress)
				.where(Progress.user_id == user.tele_user_id)
				.where(Progress.school_id == show.school_id)
			).first()
			if progress is not None:
				is_end = progress.cur_p is not None and (bus_progress_data if progress.is_bus else mrt_progress_data)[progress.cur_p].get('end', False)
				if is_end:
					await update.effective_chat.send_message(
						f'Welcome back to the ALP Progress Tracker Bot!!\n\nYou had finished the journey for {show.school}.\nPlease switch to the main bot to change the school.',
						reply_markup=InlineKeyboardMarkup.from_column([
							InlineKeyboardButton('Switch to Main Bot', url=f'tg://resolve?domain={MAIN_BOT_USERNAME}'),
							InlineKeyboardButton('I have update my data', callback_data='_start')
						])
					)
					return 
				elif progress.cur_p is None:
					msg_key = f'progress_{progress.id}_msg_id'			
					message = await update.effective_chat.send_message(
						f'Welcome to the ALP Progress Tracker Bot!!\nI\'ll record your progress and the time of indication for each stage of the journey.\n\nPlease confirm the following info:\n\tName: {user.tele_user_name}\n\tSchool: {show.school}\n\tTransport: {show.transport}\n\nIf any of the above is incorrect, please switch to the main bot and change it there.',
						reply_markup=InlineKeyboardMarkup.from_column([
							InlineKeyboardButton(
								'Confirm', callback_data='next'),
							InlineKeyboardButton(
								'Switch to Main Bot', url=f'tg://resolve?domain={MAIN_BOT_USERNAME}')
						])
					)
					context.user_data[msg_key] = message.message_id
					pass
				else:
					await update.effective_chat.send_message(
						'Welcome back to the ALP Progress Tracker Bot!!\n\nI\'ll pick up where we left off last time.'
					)
					await send_edit_progress(update, context, progress, True)
			else:
				progress = Progress(
					user_id=user.tele_user_id,
					school_id=show.school_id,
					is_bus=show.transport == 'BUS',
					last_click=datetime.now(),
					# cur_p='0'
				)
				session.add(progress)
				session.commit()
				msg_key = f'progress_{progress.id}_msg_id'			
				message = await update.effective_chat.send_message(
					f'Welcome to the ALP Progress Tracker Bot!!\nI\'ll record your progress and the time of indication for each stage of the journey.\n\nPlease confirm the following info:\n\tName: {user.tele_user_name}\n\tSchool: {show.school}\n\tTransport: {show.transport}\n\nIf any of the above is incorrect, please switch to the main bot and change it there.',
					reply_markup=InlineKeyboardMarkup.from_column([
						InlineKeyboardButton(
							'Confirm', callback_data='next'),
						InlineKeyboardButton(
							'Switch to Main Bot', url=f'tg://resolve?domain={MAIN_BOT_USERNAME}')
					])
				)
				context.user_data[msg_key] = message.message_id
			context.user_data['progress_id'] = progress.id
			
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
	if update.callback_query.data == '_start':
		await update.effective_message.edit_text('Restarting...')
		return await start(update, context)

	with Session(engine) as session:
		if 'progress_id' not in context.user_data:
			await update.effective_message.edit_text('The bot has been restarted\nTracker restarting...\n\nDon\'t worry, the previously recorded data are saved')
			await start(update, context)
			return
		progress = session.get(Progress, context.user_data['progress_id'])

		if progress is None:
			await update.effective_message.edit_text(
				'Your data has been deleted by developer\nPlease restart the tracker',
				reply_markup=InlineKeyboardMarkup.from_button(InlineKeyboardButton('Restart', callback_data='_start'))
			)
			await start(update, context)
			return
		else:
			now = datetime.now()
			prev = progress.cur_p
			is_bus = progress.is_bus
			data = bus_progress_data if is_bus else mrt_progress_data
			cur = data[prev]['buttons'][update.callback_query.data]['step'] if prev != None else '0'
			progress.cur_p = cur
			progress.last_click = now
			print(f'clicked for {progress.id}: {update.callback_query.data} at {now}')
			if not update.callback_query.data.startswith('back'):
				setattr(progress, f'p_{cur}', now)
			else:
				setattr(progress, f'p_{prev}', None)
			await send_edit_progress(update, context, progress)
			session.commit()

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
	now = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(tz=None)
	msg_time = update.message.date.replace(tzinfo=timezone.utc).astimezone(tz=None)
	delta = now - msg_time
	m = await update.effective_chat.send_message(f'Pong!\n\nMessage time: {msg_time.time()}\nServer time: {now.time()}\nDelta: {delta.total_seconds()}')
	now = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(tz=None)
	msg_time = m.date.replace(tzinfo=timezone.utc).astimezone(tz=None)
	delta = now - msg_time
	await update.effective_chat.send_message(f'Return trip\n\nMessage time: {msg_time.time()}\nServer time: {now.time()}\nDelta: {delta.total_seconds()}')

async def admin_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
	if update.message.from_user.id != 1940038812:
		return

	progress_id = context.args[0]
	with Session(engine) as session:
		progress = session.get(Progress, progress_id)
		if progress is None:
			await update.effective_chat.send_message('No such progress')
			return
		m = await context.bot.send_message(
			chat_id=progress.user_id,
			text=f'Your progress has been edited by admin\n\n'
		)
		await send_edit_progress(update, context, progress, True)
		await sleep(5)
		await m.delete()
  
async def plus(update: Update, context: ContextTypes.DEFAULT_TYPE):
	if update.message.from_user.id != 1940038812:
		return

	progress_id = context.args[0]
	with Session(engine) as session:
		progress = session.get(Progress, progress_id)
		if progress is None:
			await update.effective_chat.send_message('No such progress')
			return
		progress.cur_p = str(int(progress.cur_p) + 1)
		session.commit()
		await send_edit_progress(update, context, progress, True)
	

PERSISTENCE = True
def main():
	builder = ApplicationBuilder().token(BOT_TOKEN).concurrent_updates(5)
	if PERSISTENCE:
		persistence = PicklePersistence(filepath="data.pickle")
		builder = builder.persistence(persistence)
	app = builder.build()
	app.add_handler(CommandHandler('start', start, block=True))
	app.add_handler(CallbackQueryHandler(handle_callback, block=True))
	app.add_handler(CommandHandler('ping', ping, block=True))
	app.add_handler(CommandHandler('admin_update', admin_update))
	app.run_polling()

main()
