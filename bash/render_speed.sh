#!/bin/bash

{ time wget -q -O /dev/null http://tinkerlust.com ; } 2> logs/home_page.txt &
{ time wget -q -O /dev/null http://www.tinkerlust.com/kate-spade-red-strapped-heels ; } 2> logs/product_page.txt &