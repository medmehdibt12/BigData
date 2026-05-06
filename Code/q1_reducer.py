#!/usr/bin/python3
import sys

# Q1 - Chiffres d'affaires par item
# Input (trié): item \t cost
# Output: item \t totalSales

oldKey = None
totalSales = 0

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2:
        continue

    thisKey, thisSales = data_mapped

    if oldKey and oldKey != thisKey:
        print(f"{oldKey}\t{totalSales}")
        totalSales = 0

    oldKey = thisKey
    totalSales += float(thisSales)

# Afficher le dernier groupe
if oldKey is not None:
    print(f"{oldKey}\t{totalSales}")