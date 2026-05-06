#!/usr/bin/python3
import sys

# Q4 - Item le plus vendu pour chaque store (en nombre de ventes)
# Input (trié): store \t item \t count
# Output: store \t item_le_plus_vendu \t maxCount

oldStore = None
oldItem = None
totalCount = 0
maxItemCount = 0
maxItem = None
listItems = []
listCount = []

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 3:
        continue

    thisStore, thisItem, thisCount = data_mapped

    if oldStore and oldStore == thisStore:
        # Même store: vérifier si l'item change
        if oldItem and oldItem != thisItem:
            listItems.append(oldItem)
            listCount.append(totalCount)
            totalCount = 0

    elif oldStore and oldStore != thisStore:
        # Nouveau store: finaliser l'ancien
        listItems.append(thisItem)
        listCount.append(totalCount)
        maxItemCount = max(listCount)
        maxIndex = listCount.index(maxItemCount)
        maxItem = listItems[maxIndex]
        print(f"{oldStore}\t{maxItem}\t{maxItemCount}")
        listCount = []
        listItems = []
        totalCount = 0

    oldStore = thisStore
    oldItem = thisItem
    totalCount += int(thisCount)

# Traiter le dernier store
if oldStore is not None:
    listItems.append(oldItem)
    listCount.append(totalCount)
    maxItemCount = max(listCount)
    maxIndex = listCount.index(maxItemCount)
    maxItem = listItems[maxIndex]
    print(f"{oldStore}\t{maxItem}\t{maxItemCount}")