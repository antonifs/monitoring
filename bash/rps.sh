#!/bin/bash
ab -n 100 -c 10 http://www.tinkerlust.com/ > ./logs/rps_home_page.txt &
ab -n 100 -c 10 http://www.tinkerlust.com/schutz-nude-espadrilles-wedges > ./logs/rps_product_page.txt &
