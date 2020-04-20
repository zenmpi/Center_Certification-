import telebot
from telebot import types
from datetime import date, datetime
import time
import os.path, fnmatch
import multiprocessing
import pymysql
from config import *
import shutil
#import socket

import logging

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


import urllib.request
import re


API_TOKEN = '964752203:AAEwuyg8I7ZVZk0OBk0Xwt338X86rjfPr10'
bot = telebot.TeleBot(API_TOKEN)


class CertificationBot:

    TODAY = date.today()

    logger = telebot.logging

    telebot.logging.basicConfig(filename="log/LOG.log", level=logging.INFO)

    @bot.message_handler(commands=['start'])
    def LaunchBot(message):
        start.LoadKeyboard(message)
        #keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        #keyboard.add(*[types.KeyboardButton(name) for name in ['Authorization 🔑']])
        #bot.send_message(message.chat.id, 'Please authorization.', reply_markup=keyboard)
        #bot.register_next_step_handler(message, start.Authorization)
    
    def Authorization(self, message):
        logger = logging.getLogger('BotApp.Authorization')
        get_id = message.from_user.id
        if message.text == 'Authorization 🔑':
            try:
                connect = pymysql.connect(server, login, password, DB)
                with connect:
                    cur = connect.cursor()
                    cur.execute("SELECT id FROM user")
                    rows = cur.fetchone()
                    user_id = rows[0]

                if user_id == get_id:
                    bot.send_message(message.chat.id, 'Authorization was successful\n'+
                    'Hello - {}'.format(message.from_user.first_name))
                    start.LoadKeyboard(message)
                else:
                    bot.send_message(message.chat.id, 'Access denied 😝')

            except Exception:
                bot.send_message(message.chat.id, 'The connection to the database server has timed out. Unable to connect by address {}'.format(server))
                logger.error('The connection to the database server has timed out. Unable to connect by address %s', (server))
                   
    def LoadKeyboard(self, message):
        logger = logging.getLogger('BotApp.LoadKeyboard')
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True) # add one_time_keyboar=True remove for a while
        keyboard.add(*[types.KeyboardButton(name) for name in ['Issue certificate 🔐', 'Root certificate 🧾']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Readme 📄', 'Setting ⚙️']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Developer 👨‍💻', 'Project 💻', 'Donation 💰']])
        logger.info('%s function started to work' % (start.LoadKeyboard.__name__))
        bot.send_message(message.chat.id, 'Hello, I am a bot that issues certificates. Issuance of certificates will occur about 10:30. Please await!', reply_markup = keyboard)

    @bot.message_handler(content_types=['text'])
    def ExecutingMenuCommands(message):
        logger = logging.getLogger('BotApp.BOT.ExecutingMenuCommands')

        if message.text == 'Issue certificate 🔐':
            bot.send_message(message.chat.id, "Enter your email: ")
            bot.register_next_step_handler(message, start.ManualIssuanceOfCertificates)

        elif message.text == 'Root certificate 🧾':
            bot.send_message(message.chat.id, 'One second, creating cert')
            time.sleep(1)
            try:
                os.system('python3 CA.py --ca --cert-org Yaroslav.OOO --cert-ou Yaroslav.OOO')
                caFile = open('keys/ca.crt', 'rb')
                bot.send_document(message.chat.id, caFile)
                logger.info('Create root certificate')
            except FileNotFoundError:
                logger.error('Error create root certificate,  sbecause - ', FileNotFoundError)
                bot.send_message(message.chat.id, 'Error create root certificate. Please looke log error and warning.')

        elif message.text == 'Readme 📄':
            bot.send_message(
                message.chat.id, 
                '#Requirements\n'+
                '1.Python\n'+
                '2.The pyopenssl library.\n'+
                '#Usage\n'+
                'First generate the CA file\n'+
                'python ssl_gen.py --ca --cert-org example --cert-ou example\n'+
                'This will dump the ca keys in a folder aptly named keys\n'+
                'Generate the client certificate\n'+
                'python ssl_gen.py --client --cert-name cert_name\n'+
                'Generate a pfx certificate\n'+
                'python ssl_gen.py --pfx --cert-name cert_name\n',
            )

        elif message.text == 'Setting ⚙️':
            logger.info('User moved in settings for editing file config!')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['Sign in']])
            keyboard.add(*[types.KeyboardButton(name) for name in ['Menu']])
            bot.send_message(message.chat.id, 'Welcome to the settings wizard', reply_markup=keyboard)

        elif message.text == 'Developer 👨‍💻':
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.add(
                telebot.types.InlineKeyboardButton(
                    'Developer', url = 'telegram.me/Karlinsky_Yaroslav'
                )
            )
            photo = open('yaroslav.jpg', 'rb')
            bot.send_photo(message.chat.id, photo, reply_markup=keyboard)

        elif message.text == 'Project 💻':
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.add(
                telebot.types.InlineKeyboardButton(
                'GitHub', url='https://github.com/HackerKarl/Bot_Certifiaction.git'
                )
            )
            bot.send_message(
                message.chat.id,
                'Welcome to Outlook Certification Bot Project\n' +
                ' - This bot is able to generate certificates for encryption of letters in Outlook.\n' +
                ' - You will automatically receive a message in the chat which email was,' +
                'issued and the certificate itself in the container pfx.\n' +
                ' - There is also a function for manual issuance, that is, if the email is not' +
                'in the database, the user can issue a certificate, and the email name\n' +
                'will go to the database and will be automatically tracked.\n' +
                ' - If any errors are detected, then you need to contact the developer Yaroslav Karlinsky who will fix it in the near future.\n'+
                ' - You can also support the project financially. Donat function will soon work.',
                reply_markup=keyboard
            )
        elif message.text == 'Donation 💰':
            bot.send_message(message.chat.id, 'Soon this function will appear, it will be possible to pay for universal cryptocurrency from the developer of Yaroslav Karlinsky')
        
        elif message.text == 'Menu':
            start.LoadKeyboard(message)
            logger.info('Return in function %s', (start.LoadKeyboard.__name__))
            logger.info('User %s exited settings', (message.from_user.first_name))

        elif message.text == 'Sign in':
            get_id = message.from_user.id #get id user in telegram
            logger = logging.getLogger('BotApp.Login_User')
            try:
                connect = pymysql.connect(server, login, password, DB)
                with connect:
                    cur = connect.cursor()
                    cur.execute("SELECT id FROM user")
                    rows = cur.fetchone()
                    user_id = rows[0]
                if user_id == get_id:
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(*[types.KeyboardButton(name) for name in ['Edit config', 'Add admin']])
                    keyboard.add(*[types.KeyboardButton(name) for name in ['Menu']])
                    bot.send_message(message.chat.id, 'Global settings are activated - you are logged in as a developer under the name: - {}'.format(message.from_user.first_name), reply_markup=keyboard)
                    logger.warning('User %s login system', (message.from_user.first_name))
                    research = urllib.request.urlopen('http://2ip.ru/').read()
                    ip = (re.search(b'\d+\.\d+\.\d+\.\d+', research).group())
                    logger.info('Ip address user %s', (ip))
                else:
                    bot.send_message(message.chat.id, 'Access denied for user {} because you don`t admin!'.format(message.from_user.first_name))
            except Exception:
                logger.error('The connection to the database server has timed out. Unable to connect by address - %s', (server))
                bot.send_message(message.chat.id, 'The connection to the database server has timed out. Unable to connect by address {}'.format(server))
                    
        elif message.text == 'Edit config':
            bot.send_message(message.chat.id, 'In developering')
            logger.info('Edit config - user %s', (message.from_user.first_name))

        elif message.text == 'Add admin':
            bot.send_message(message.chat.id, 'In developing')
        
    def ManualIssuanceOfCertificates(self, message):
        logger = logging.getLogger('BotApp.ManualIssuanceOfCertificates')
        logger.info('Start function - %s', (start.ManualIssuanceOfCertificates.__name__))
        email = message.text
        try:
            connect = pymysql.connect(server, login, password, DB)
            with connect:
                cur = connect.cursor()
                cur.execute("INSERT INTO email (email, date) VALUES (%s, %s)", (email, self.TODAY))
                bot.send_message(message.chat.id, 'Please expect..')
                time.sleep(2)
        except Exception:
            bot.send_message(message.chat.id, 'Error connect to Mysql server, please see error log')
            logger.error('The connection to the database server has timed out. Unable to connect by address - %s' , (server))
        try:
            os.system('python3 CA.py --client --cert-name {}'.format(email))
            os.system('python3 CA.py --pfx --cert-name {}'.format(email))
            filePFX = open('keys/{}.pfx'.format(email), 'rb')
            bot.send_message(message.chat.id, '{} has been added to the database and monitored for automatic delivery.'.format(email))
            logger.info('%s has been added to the database and monitored for automatic delivery.', (email))
            time.sleep(1)
            bot.send_document(message.chat.id, filePFX)
            logger.info('Certificate created for email -  %s' % (email))
        except Exception:
            bot.send_message(message.chat.id, 'Error create certificate for email - {}'.format(email))
            logger.warning('Error create certificate for email - %s', (email))
        
        start.SendEmailWithAttachment(email)


    def SendEmailWithAttachment(self, email):
        logger = logging.getLogger('BotApp.SendEmailWithAttachment')
        logger.info('Start function %s ', (start.SendEmailWithAttachment.__name__))

        general_email = 'skypework1234@gmail.com'
        password = '*787*977*'
        subject = 'Bot certification from Yaroslav Karlinsky'
        message = 'This email {} is automatically generated by the bot for issuing certificates.'.format(email)

        try:
            file_location = 'keys/{}.pfx'.format(email)
        except FileNotFoundError:
            logging.warning('File %s.pfx not found error', (email))

        outlook = MIMEMultipart()
        outlook['From'] = general_email
        outlook['To'] = general_email
        outlook['Subject'] = subject

        #Attach the message to the MIMEMultipart object
        outlook.attach(MIMEText(message, 'plain'))

        filename = os.path.basename(file_location)
        attachment = open(file_location, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename= %s', filename)

        outlook.attach(part)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(general_email, password)
            text = outlook.as_string() # You now need to convert the MIMEMultipart object to a string to send
            server.sendmail(general_email, general_email, text)
            server.quit
            logger.info('Successful send file for email - %s', (email))
        except Exception:
            logger.error('Error connecting to server at address smtp.gmail.com')
            time.sleep(5) # Waiting 5 seconds
    
    
#============================================================================================#
#=============================MULTIPROCESSING IN FUNCTION MANAGER============================#
#============================================================================================#


    def Manager(self):
        logger = logging.getLogger('BotApp.Manager.Multiprocessing')
        logger.info('Start multiporcessing function %s', (start.Manager.__name__))
        print('Issuance of certificates will occur about 10:30. Please await')
        logger.warning('Issuance of certificates will occur about 10:30. Please await')
        while True:
            weekdayNum = self.TODAY.weekday()
            for i in range(6):
                if i == weekdayNum:
                    try:
                        logger.info('Database connection has beeb established.')
                        connect = pymysql.connect(server, login, password, DB)
                        with connect:
                            cur = connect.cursor()
                            cur.execute("SELECT email FROM email WHERE date = (%s)", (self.TODAY))
                            rows = cur.fetchall()
                            for row in rows:
                                email = row[0]
                                os.system('python3 CA.py --client --cert-name {}'.format(email))
                                os.system('python3 CA.py --pfx --cert-name {}'.format(email))
                                logger.info('Certificate create for email %s.' , (email))
                                currentTime = datetime.now().strftime('%H:%M')
                                setTime = '10:30'
                                if currentTime == setTime:
                                    start.SendEmailWithAttachment(email)
                                    shutil.move('keys/{}.pfx'.format(email), 'pfx')
                                    logger.info('File %s.pfx has been moved to folder pfx', (email))
                        time.sleep(86400) # The manager must sleep 24 hours
                    except Exception:
                        logger.error('The connection to the database server has timed out. Unable to connect to address - %s', (server))
                        print('The connection to the database server has timed out. Unable to connect to adress - {}'.format(server))
                        time.sleep(10) # Waiting time 10 seconds, then return to the server connection
                else:
                    logger = logging.getLogger('BotApp.DaysBan.Multiprocessing')
                    logger.info('This condition started because started today days off.')
                    while True:
                        try:
                            connect = pymysql.connect(server, login, password, DB)
                            with connect:
                                logger.info('Database connection has been established.')
                                cur = connect.cursor()
                                cur.execute("SELECT email FROM email WHERE date = (%s)", (self.TODAY))
                                rows = cur.fetchall()
                                for row in rows:
                                    email = row[0]
                                    checkFile = os.path.exists('pfx/{}.pfx'.format(email))
                                    if checkFile == False:        
                                        os.system('python3 CA.py --client --cert-name {}'.format(email))
                                        os.system('python3 CA.py --pfx --cert-name {}'.format(email))
                                        logger.info('Certificate create for email %s', (email))
                                    else:
                                        shutil.move('keys/{}.pfx'.format(email), '/pfxBan')
                                        logger.info('File %s.pfx has been moved to folder /pfxBan',(email))
                        except Exception:
                            logger.error('The connection to the database server has timed out. Unable to connect by address - %s', (server))
                            print('The connection to the database server has timed out. Unable to connect by address - {}'.format(server))
                            time.sleep(10) # Waiting time 10 seconds, then return to the server connection
            
if __name__ == "__main__":
    start = CertificationBot()
    startManager = multiprocessing.Process(target=start.Manager, args=())
    startManager.start()
    bot.polling(none_stop=True, timeout=123)
    