from collections import OrderedDict
from datetime import datetime, timedelta
from redis import StrictRedis
import os, math, urllib2, json, unicodedata

# setting global variable
path = os.getcwd()
bash_path = path + "/bash/"
logs_path = path + "/logs/"
client_id = '8b36d9fe60232d9bdfc10ae3807e5b4d'
client_secret = '67b7aa0236c081cb095f964ead4d6e1b'

from_date = datetime.now() - timedelta(hours=10)
fdate = format(from_date, '%d-%m-%Y %H:%M:%S')
from_date = format(from_date, '%d-%m-%Y %H:%M:%S')
from_date = from_date.replace(" ", "%20")

to_date = datetime.now()
tdate = format(to_date, '%H:%M:%S')
to_date = format(to_date, '%d-%m-%Y %H:%M:%S')
to_date = to_date.replace(" ", "%20")

# url
token_url = 'http://www.tinkerlust.com/internalapi/oauth2/punten?client_id='+ client_id +'&client_secret=' + client_secret

# get access token
def get_token(url):
    try:
        token = json.load(urllib2.urlopen(url))
        token = token["access_token"]
    except ValueError:
        token  = False
    return token

if get_token(token_url):
    url_online_visitor = "http://www.tinkerlust.com/internalapi/rest/visitor?access_token=" + get_token(token_url)
    url_order = "http://www.tinkerlust.com/internalapi/rest/order?from="+ from_date +"&to="+ to_date +"&access_token="+ get_token(token_url)
else:
    url_online_visitor = ""
    url_order = ""

# Execute bash script
def run_bash():

    # bash render speed
    os.system(bash_path + 'render_speed.sh')

    # bash request per second (rps) durability
    os.system(bash_path + 'rps.sh')

# get order
def get_order(url):
    order = json.load(urllib2.urlopen(url))
    return order["data"]["num_of_order"]

# Read logs files
def read_logs():

    # read render speed
    home_page_speed = parse_speed_page(logs_path + 'home_page.txt')
    product_page_speed = parse_speed_page(logs_path + 'product_page.txt')

    # read rps
    rps_home_page = parse_rps(logs_path + 'rps_home_page.txt')
    rps_product_page = parse_rps(logs_path + 'rps_product_page.txt')

    # read memory
    memory = parse_memory(logs_path + 'memory.txt')

    # get order log
    order  = [get_order(url_order)]

    return {
        'home_page_speed': home_page_speed,
        'product_page_speed': product_page_speed,
        'rps_home_page': rps_home_page,
        'rps_product_page': rps_product_page,
        "memory": memory,
        "order": order,
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

def parse_memory(fname):
    data = OrderedDict()
    try:
        with open(fname) as f:
            line = f.readlines()
            for key, mem in enumerate(line):

                if key < 5:
                    mem = mem.lstrip()
                    item = mem.split(" ")
                    # print item[0], item[2]

                    data[item[2]] = item[0]

    except ValueError:
            print "There is something wrong with your bash script."
    return data

# Store the return of second action into db
def save_report(temp):
    r = StrictRedis()
    r.set("performance", temp)

# Create an email content in HTML mode
def generate_report():
    logs = read_logs()

    rps_home_page = logs['rps_home_page']
    rps_product_page = logs['rps_product_page']
    home_page_speed = logs['home_page_speed']
    product_page_speed = logs['product_page_speed']
    memory = logs['memory']
    order = logs["order"]

    temp = """
    + Order: {} ({} - {})
    + RPS Home Page: {} req/sec
    + RPS Product Page: {} req/sec
    + Home Page Speed: {} Min {} Sec
    + Product Page Speed: {} Min {} Sec
    + Memory:
      - Total {} kb
      - Used {} kb
      - Active {} kb
      - Inactive {} kb
      - Free {} kb
    """.format(
        order[0],
        fdate,
        tdate,
        rps_home_page[0],
        rps_product_page[0],
        home_page_speed[0],
        home_page_speed[1],
        product_page_speed[0],
        product_page_speed[1],
        memory['total'],
        memory['used'],
        memory['active'],
        memory['inactive'],
        memory['free'],
    )

    save_report(temp)

    return temp

# Send email to PIC
def serve_report():
    return generate_report()

def main():
    print generate_report()

if __name__ == "__main__": main()