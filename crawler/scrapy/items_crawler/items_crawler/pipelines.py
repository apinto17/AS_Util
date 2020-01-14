# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import mysql
import mysql.connector
import sshtunnel
import datetime


class MySQLPipeline(object):
    server = None
    connection = None
    mycursor = None

    def __init__(self):
        self.start()


    def start(self):
        sshtunnel.SSH_TIMEOUT = 350.0
        sshtunnel.TUNNEL_TIMEOUT = 350.0

        self.server = sshtunnel.SSHTunnelForwarder('ssh.pythonanywhere.com',
            			  ssh_username='iclam19',
            			  ssh_password='@astest@1234',
            			  remote_bind_address=('iclam19.mysql.pythonanywhere-services.com'
            			  , 3306))
        self.server.start()
        self.connect()


    def stop(self):
        self.connection.close()
        self.server.stop()

    def close_spider(self, spider):
        self.stop()


    def process_item(self, item, spider):

        for i in range(2):
            try:
                txntime_cd = datetime.datetime.utcnow()
                sql = \
                'INSERT INTO  ft_crawled_data (site_name,category,item_description,price,url,image_source,txntime,unit,item_specifications) VALUES (%s, %s,%s, %s,%s,%s,%s,%s,%s)'
                val = (item['sitename'], item['cats'], item['desc'], item['price'], item['link'],item['img'],str(txntime_cd),item['unit'], item['specs'])
                self.mycursor.execute(sql, val)
                self.connection.commit()
                break
            except:
                self.connect()


    def connect(self):

        for i in range(10):

            try:
                self.connection = mysql.connector.connect(user='iclam19',
                    password='astest1234', host='127.0.0.1',
                    port=self.server.local_bind_port,
                    database='iclam19$AssembledSupply')

                if(self.connection.is_connected()):
                    self.mycursor = self.connection.cursor()
                    break
                else:
                    self.logger.info("DB Connection lost, trying again")
                    self.stop()
                    self.start()
            except:
                self.logger.info("DB Connection lost, trying again")
                self.stop()
                self.start()


    
        
