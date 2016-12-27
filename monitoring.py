import commands
from collections import OrderedDict
import os, math, urllib2, json, unicodedata
from redis import StrictRedis

# setting global variable
path = os.getcwd()
bash_path = path + "/bash/"
logs_path = path + "/logs/"

# url
token_url = 'http://www.tinkerlust.com/internalapi/oauth2/punten?client_id=8b36d9fe60232d9bdfc10ae3807e5b4d&client_secret=67b7aa0236c081cb095f964ead4d6e1b'

# get access token
def get_token(url):
    try:
        token = json.load(urllib2.urlopen(url))
        token = token["access_token"]
    except ValueError:
        token  = False

    return token

token = get_token(token_url)

if token:
    url_online_visitor = "http://www.tinkerlust.com/internalapi/rest/visitor?access_token=" + token
    url_order = "http://www.tinkerlust.com/internalapi/rest/order?from=26-12-2016%2006:00:00&to=26-12-2016%2012:00:00&access_token="+ token
else:
    url_online_visitor = ""
    url_order = ""

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
def save_report():
    return ""


# Create an email content in HTML mode
def generate_report():
    return ""

# Send email to PIC
def serve_report():
    return read_logs()

def main():
    print serve_report()

if __name__ == "__main__": main()