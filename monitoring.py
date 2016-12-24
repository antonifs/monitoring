import commands
import sqlite3
from collections import OrderedDict
import os

path = os.getcwd()
bash_path = path + "/bash/"
logs_path = path + "/logs/"

# Execute bash script
def run_bash():

    # bash homepage
    os.system(bash_path + 'render_speed.sh')

    # bash product page

    # bash request per second



# Read logs files


# Store the return of seccond action into db


# Create an email content in HTML mode


# Send email to PIC


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