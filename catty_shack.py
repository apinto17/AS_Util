
import mysql.connector
import sshtunnel
import xlwt
import xlrd
from xlutils.copy import copy
from xlwt import Workbook


def main():

    first = True
    cats = ["backyard & farm", "chemicals & lubricants", "cutting, machining & finishing", "electrical equipment & devices", "facility & janitorial", "fasteners & hardware", "hvac", "metals & materials", "plumbing & filtration", "pneumatics & hydraulics", "power & hand tools"]
    for cat in cats:
        cats_from_site(cat, first)
        first = False

def man_cats():

    sshtunnel.SSH_TIMEOUT = 350.0
    sshtunnel.TUNNEL_TIMEOUT = 350.0

    print("Connecting")

    with sshtunnel.SSHTunnelForwarder('ssh.pythonanywhere.com',
                                  ssh_username='iclam19',
                                  ssh_password='@astest@1234',
                                  remote_bind_address=('iclam19.mysql.pythonanywhere-services.com'
                                  , 3306)) as tunnel:
        connection = mysql.connector.connect(user='iclam19',
                password='astest1234', host='127.0.0.1',
                port=tunnel.local_bind_port,
                database='iclam19$AssembledSupply')
        mycursor = connection.cursor()
        sql = "Select Distinct manual_category From iclam19$AssembledSupply.ft_manual_categories  Order by manual_category ASC"
        print("Executing query")
        mycursor.execute(sql)
        returned_categories = list(mycursor.fetchall())
        print(returned_categories)
        connection.close()


def cats_from_site(category_selection, first):

    #ssh tunnel
    sshtunnel.SSH_TIMEOUT = 350.0
    sshtunnel.TUNNEL_TIMEOUT = 350.0

    print("connecting")

    with sshtunnel.SSHTunnelForwarder('ssh.pythonanywhere.com',
                                      ssh_username='iclam19',
                                      ssh_password='@astest@1234',
                                      remote_bind_address=('iclam19.mysql.pythonanywhere-services.com'
                                      , 3306)) as tunnel:
        connection = mysql.connector.connect(user='iclam19',
                password='astest1234', host='127.0.0.1',
                port=tunnel.local_bind_port,
                database='iclam19$AssembledSupply')
        mycursor = connection.cursor()
        sql_test = "Select Distinct mc_q.manual_category,cd_q.primary_category,cd_q.secondary_category,cd_q.tertiary_category,cd_q.quartenary_category,cd_q.septenary_category From (Select Distinct mc.manual_category,mc.primary_category From iclam19$AssembledSupply.ft_manual_categories mc)mc_q left join (SELECT substring_index(category,'|',1) primary_category,site_name,case when substring_index(substring_index(category,'|',2),'|',-1) = substring_index(category,'|',1) then null else substring_index(substring_index(category,'|',2),'|',-1) end secondary_category,case when substring_index(substring_index(category,'|',3),'|',-1) = substring_index(substring_index(category,'|',2),'|',-1) then null else substring_index(substring_index(category,'|',3),'|',-1) end tertiary_category ,case when substring_index(substring_index(category,'|',4),'|',-1) = substring_index(substring_index(category,'|',3),'|',-1) then null else substring_index(substring_index(category,'|',3),'|',-1) end quartenary_category,case when substring_index(substring_index(category,'|',5),'|',-1) = substring_index(substring_index(category,'|',4),'|',-1) then null else substring_index(substring_index(category,'|',5),'|',-1) end septenary_category From iclam19$AssembledSupply.ft_crawled_data cd)cd_q on cd_q.primary_category = mc_q.primary_category where mc_q.manual_category = %s"
        #Order by mc_q.manual_category ASC = %s"
        print("fetching items")
        mycursor.execute(sql_test, (category_selection,))
        returned_items = list(mycursor.fetchall())
        print("writing to file")
        print(category_selection)
        write_to_file(returned_items, first)
        connection.close()


def write_to_file(item_cats, first):

    rb = xlrd.open_workbook("categories.xls")
    wb = copy(rb)

    sheet1 = wb.get_sheet(0)
    if(first):
        sheet1.write(0,0, "Content")

    for i in range(len(item_cats)):
        buffer = ""
        for j in range(len(item_cats[0])):
            if(str(item_cats[i][j]) != "None"):
                buffer += str(item_cats[i][j]) + " "
        sheet1.write(i + 1, 0, buffer)
        buffer = ""
    print("finished write")

    wb.save('categories.xls')



def write_to_file_mapped(item_cats, first):

    rb = xlrd.open_workbook("mapped categories.xls")
    wb = copy(rb)

    sheet1 = wb.get_sheet(0)
    if(first):
        sheet1.write(0,0, "Content")

    for i in range(len(item_cats)):
        buffer = ""
        for j in range(len(item_cats[0])):
            if(str(item_cats[i][j]) != "None" and j != 0):
                buffer += str(item_cats[i][j]) + " "
            elif(j == 0):
                buffer += str(item_cats[i][j]) + " : "
        sheet1.write(i + 1, 0, buffer)
        buffer = ""

    wb.save('mapped categories.xls')

if(__name__ == "__main__"):
    sshtunnel.SSH_TIMEOUT = 350.0
    sshtunnel.TUNNEL_TIMEOUT = 350.0

    print("connecting 123")

    with sshtunnel.SSHTunnelForwarder('ssh.pythonanywhere.com',
                                      ssh_username='iclam19',
                                      ssh_password='@astest@1234',
                                      remote_bind_address=('iclam19.mysql.pythonanywhere-services.com'
                                      , 3306)) as tunnel:
        connection = mysql.connector.connect(user='iclam19',
                password='astest1234', host='127.0.0.1',
                port=tunnel.local_bind_port,
                database='iclam19$AssembledSupply')
        mycursor = connection.cursor()
