import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import datetime

def write_to_db(desc, link, img, price, unit, sitename, cats, specs):

    val = (str(desc), str(price), str(cats), str(link), str(sitename),str(img),str(datetime.datetime.utcnow()),str(unit),specs)
 
    connection = mysql.connector.connect(host='asdbinstance.c5s3c2vl3ocv.us-west-1.rds.amazonaws.com',
                                database='AssembledSupply',
                                user='AssembledSupply',
                                password='astest1234')
    sql_insert_query = 	\
                    'INSERT INTO `crawled_data`(item_description,price, input_category,url,site_name,image_source,txntime,unit,item_specifications) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    c = connection.cursor()
    c.execute(sql_insert_query,val)
    connection.commit()
    c.close()
    connection.close()
