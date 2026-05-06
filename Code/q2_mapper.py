#!/usr/bin/python3
import sys

# Q2 - Item le plus vendu selon le chiffre d'affaires
# Input: date \t time \t store \t item \t cost \t payment
# Output: item \t cost (même mapper que Q1)

for line in sys.stdin:
    data = line.strip().split("\t")
    if len(data) == 6:
        date, time, store, item, cost, payment = data
        try:
            float(cost)
            print(f"{item}\t{cost}")
        except ValueError:
            pass