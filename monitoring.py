import commands
import sqlite3
from collections import OrderedDict
import os, math, urllib2, json, unicodedata

# setting global variable
path = os.getcwd()
bash_path = path + "/bash/"
logs_path = path + "/logs/"
url_order = "http://128.199.211.72/tinkerapi/rest/cart?access_token=b33014934858f779ede2b5a8f9011e3b579f47af"


# variable init
home_page_speed = ""
product_page_speed = ""
rps_home_page = ""
rps_product_page = ""

# Execute bash script
def run_bash():

    # bash render speed
    os.system(bash_path + 'render_speed.sh')

    # bash request per second (rps) durability
    os.system(bash_path + 'rps.sh')

# Read logs files
def read_logs():

    # read render speed
    home_page_speed = parse_speed_page(logs_path + 'home_page.txt')
    product_page_speed = parse_speed_page(logs_path + 'product_page.txt')

    # read rps
    rps_home_page = parse_rps(logs_path + 'rps_home_page.txt')
    rps_product_page = parse_rps(logs_path + 'rps_product_page.txt')

    # get order log
    order  = json.load(urllib2.urlopen(url_order))

    if isinstance(order["message"], unicode):
        str_order = unicodedata.normalize('NFKD', order["message"]).encode('ascii','ignore')
    else:
        str_order = order["message"]

    return {
        'home_page_speed': home_page_speed,
        'product_page_speed': product_page_speed,
        'rps_home_page': rps_home_page,
        'rps_product_page': rps_product_page,
        "order": str_order,
    }


def parse_speed_page(fname):
    res = []

    try:
        with open(fname) as f:
            line = f.readlines()
            for i in line:
                if "real" in i:
                    str = i.split()
                    new_str = str[1].split("m")
                    res.append(new_str[0])
                    res.append(new_str[1].replace("s", ""))
    except ValueError:
            print "There is something wrong with your bash script."

    return res

def parse_rps(fname):
    res = []

    try:
        with open(fname) as f:
            line = f.readlines()
            for i in line:
                if "Requests per second:" in i:
                    str = i.split(":")
                    str_splited = str[1].split("[")
                    new_str = str_splited[0].replace(" ", "")
                    new_str = int(math.ceil(float(new_str)))
                    res.append(new_str)
    except ValueError:
            print "There is something wrong with your bash script."

    return res

# Store the return of second action into db
def save_report():
    return ""


# Create an email content in HTML mode
def generate_report():
    return ""

# Send email to PIC
def serve_report():
    return ""

print read_logs()


# home_page_speed = commands.getoutput("time wget -pq --no-cache --delete-after www.tinkerlust.com")
# product_page_speed = commands.getoutput("time wget -pq --no-cache --delete-after http://www.tinkerlust.com/nike-pink-flex-2014-sneakers")
# memory = commands.getoutput("vmstat -s")
# memory = [s.strip() for s in memory.splitlines()]
#
# data = OrderedDict()
# for key, mem in enumerate(memory):
#     if key < 5:
#         item = mem.split(" ")
#         data[item[1]] = item[0]
#
# data["home_page_load"] = "0123"
# data["product_page_load"] = "0223"
# data["number_online_customer"] = "0193"
# data["transaction_order"] = "3"
#
# l = []
# for key, val in data.iteritems():
#     l.append(val)
#
# tup = tuple(l)
#
# def main():
#     conn = sqlite3.connect("monitoring.db")
#     db = conn.cursor()
#     # db.execute('drop table if exists monitor')
#     # db.execute('CREATE TABLE monitor '
#     #            '(total_memory varchar, '
#     #            'used_memory varchar, '
#     #            'active_memory varchar, '
#     #            'inactive_memory varchar, '
#     #            'free_memory varchar, '
#     #            'buffer_memory varchar, '
#     #            'swap_memory varchar,'
#     #            'home_page_load varchar,'
#     #            'product_page_load varchar,'
#     #            'number_online_customer varchar,'
#     #            'transaction_order varchar'
#     #            ')')
#     # db.execute('INSERT INTO monitor ('
#     #            'total_memory, '
#     #            'used_memory, '
#     #            'active_memory, '
#     #            'inactive_memory, '
#     #            'free_memory, '
#     #            'buffer_memory, '
#     #            'swap_memory, '
#     #            'home_page_load, '
#     #            'product_page_load, '
#     #            'number_online_customer, '
#     #            'transaction_order) VALUES (?, ?)', tup)
#
#     # db.commit()
#
#     # items = db.execute('SELECT activity, qty FROM monitor')
#     print tup
#
#
#     # for c in items:
#     #     print c[0], c[1]
#
# if __name__ == "__main__": main()