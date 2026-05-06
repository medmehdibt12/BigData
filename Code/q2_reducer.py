#!/usr/bin/python3
import sys

# Q2 - Item le plus vendu selon le chiffre d'affaires
# Input (trié): item \t cost
# Output: item_max \t maxSales (un seul résultat)

maxKey = None
totalSales = 0
maxSales = 0
oldKey = None

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2:
        continue

    thisKey, thisSales = data_mapped

    if oldKey and oldKey != thisKey:
        if totalSales > maxSales:
            maxKey = oldKey
            maxSales = totalSales
        totalSales = 0

    oldKey = thisKey
    totalSales += float(thisSales)

# Vérifier le dernier groupe
if oldKey is not None:
    if totalSales > maxSales:
        maxKey = oldKey
        maxSales = totalSales

if maxKey is not None:
    print(f"{maxKey}\t{maxSales}")