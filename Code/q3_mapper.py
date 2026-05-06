#!/usr/bin/python3
import sys

# Q3 - Moyenne de vente par Store
# Input: date \t time \t store \t item \t cost \t payment
# Output: store \t cost

for line in sys.stdin:
    data = line.strip().split("\t")
    if len(data) == 6:
        date, time, store, item, cost, payment = data
        try:
            float(cost)
            print(f"{store}\t{cost}")
        except ValueError:
            pass