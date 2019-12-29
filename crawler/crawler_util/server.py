import mysql
import mysql.connector
import sshtunnel
import logging
import datetime


class Server:

    server = None
    connection = None
    mycursor = None

    def __init__(self):
        sshtunnel.SSH_TIMEOUT = 350.0
        sshtunnel.TUNNEL_TIMEOUT = 350.0

        self.server = sshtunnel.SSHTunnelForwarder('ssh.pythonanywhere.com',
            			  ssh_username='iclam19',
            			  ssh_password='@astest@1234',
            			  remote_bind_address=('iclam19.mysql.pythonanywhere-services.com'
            			  , 3306))
        self.server.start()


    def write_to_db(self, desc, link, img, price, unit, sitename, cats, specs):

        for i in range(2):
            try:
                txntime_cd = datetime.datetime.utcnow()
                sql = \
                'INSERT INTO  ft_crawled_data (site_name,category,item_description,price,url,image_source,txntime,unit,item_specifications) VALUES (%s, %s,%s, %s,%s,%s,%s,%s,%s)'
                val = (str(sitename), str(cats), str(desc), str(price), str(link),str(img),str(txntime_cd),str(unit), str(specs))
                self.mycursor.execute(sql, val)
                self.connection.commit()
                break
            except:
                self.connect()



    def __del__(self):
        self.connection.close()
        self.server.stop()


    def connect(self):

        while(True):

            try:
                self.connection = mysql.connector.connect(user='iclam19',
                    password='astest1234', host='127.0.0.1',
                    port=self.server.local_bind_port,
                    database='iclam19$AssembledSupply')

                if(self.connection.is_connected()):
                    self.mycursor = self.connection.cursor()
                    break
                else:
                    logging.info("Connection lost, trying again")
            except Error as e:
                logging.info("Connection lost, trying again")

