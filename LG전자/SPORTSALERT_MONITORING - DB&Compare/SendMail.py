from email.message import MIMEPart
import smtplib  
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from email.generator import Generator
from email.mime.image     import MIMEImage
from email import charset
from datetime import datetime
from datetime import datetime,timedelta 
import pandas as pd
import numpy as np
from jinja2 import Environment,FileSystemLoader,Template
from Elem import*
import configparser
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
"""
self.monitoring = {} #id, pushes
self.checked = {} # checked push (id, pushes)
self.errored = {} # error push (id, pushes)
self.error_type = {} # error message (key : id, value : list of (error type, push num, push) per id)
"""

class SendMail :

    @staticmethod
    def send_simple_mail (subject, body) :
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['To'] = 'yeram.kim@lge.com'
        msg['From'] = 'aws.sports.monitoring@gmail.com'

        server = smtplib.SMTP('lgekrhqmh01.lge.com',25)
        server.connect('lgekrhqmh01.lge.com')

        server.sendmail(msg['From'],msg['To'],msg.as_string())
        server.quit()

    def __init__(self,date) :
        self.msg = MIMEMultipart()
        self.date = date

    def send_mail(self,msg) :
        
        self.msg['Subject'] = '스포츠 알람 점수 모니터링 결과 [' +self.date.strftime("%Y-%m-%d") +']'

        self.msg.attach(MIMEText(msg,'html'))

        recipients =  ['yeram.kim@lge.com','lorin.jeoung@lge.com','joohyun.seo@lge.com','kwon.wookeun@lge.com','warner.lee@lge.com','kyungmee.lee@lge.com']
        self.msg['To'] = 'yeram.kim@lge.com,lorin.jeoung@lge.com,joohyun.seo@lge.com,kwon.wookeun@lge.com,warner.lee@lge.com'
        self.msg['From'] = 'aws.sports.monitoring@gmail.com'
        self.msg['CC'] = 'kyungmee.lee@lge.com'
        
        server = smtplib.SMTP('lgekrhqmh01.lge.com',25)
        server.connect('lgekrhqmh01.lge.com')

        server.sendmail(self.msg['From'],recipients,self.msg.as_string().encode('utf-8'))
        server.quit()

    def test_send_mail(self,msg) :

        self.msg['Subject'] = '스포츠 알람 점수 모니터링 결과 [' +self.date.strftime("%Y-%m-%d") +']'
        self.msg['To'] = 'yeram.kim@lge.com'
        self.msg['From'] = 'aws.sports.monitoring@gmail.com'

        self.msg.attach(MIMEText(msg,'html'))
        
        server = smtplib.SMTP('lgekrhqmh01.lge.com',25)
        server.connect('lgekrhqmh01.lge.com')

        server.sendmail(self.msg['From'],self.msg['To'],self.msg.as_string().encode('utf-8'))
        server.quit()
