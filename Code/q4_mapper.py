#!/usr/bin/python3
import sys

# Q4 - Item le plus vendu pour chaque store (en nombre de ventes)
# Input: date \t time \t store \t item \t cost \t payment
# Output: store \t item \t 1  (on compte 1 vente par ligne)

for line in sys.stdin:
    data = line.strip().split("\t")
    if len(data) == 6:
        date, time, store, item, cost, payment = data
        print(f"{store}\t{item}\t1")