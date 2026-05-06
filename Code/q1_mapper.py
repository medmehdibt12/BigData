#!/usr/bin/python3
import sys

# Q1 - Chiffres d'affaires par item
# Input: date \t time \t store \t item \t cost \t payment
# Output: item \t cost

for line in sys.stdin:
    data = line.strip().split("\t")
    if len(data) == 6:
        date, time, store, item, cost, payment = data
        try:
            float(cost)  # Vérifier que cost est un nombre valide
            print(f"{item}\t{cost}")
        except ValueError:
            pass  # Ignorer les lignes avec des données invalides