#!/bin/bash
{ vmstat -s } 2> logs/memory.txt &
