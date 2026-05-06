#!/usr/bin/python3
import sys

# Q3 - Moyenne de vente par Store
# Input (trié): store \t cost
# Output: store \t moyenne_ventes

oldKey = None
listSales = []

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2:
        continue

    thisKey, thisSales = data_mapped

    if oldKey and oldKey != thisKey:
        mean_sales = sum(listSales) / len(listSales)
        print(f"{oldKey}\t{mean_sales}")
        listSales = []

    oldKey = thisKey
    listSales.append(float(thisSales))

# Traiter le dernier groupe
if oldKey is not None:
    mean_sales = sum(listSales) / len(listSales)
    print(f"{oldKey}\t{mean_sales}")