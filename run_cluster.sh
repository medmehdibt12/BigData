#!/bin/bash

echo "=== Construction de l'image de base Hadoop ==="
docker build -t hadoop-base:3.3.5-dorian base/

echo "=== Construction de l'image Spark ==="
docker build -t spark-base:3.4.3-dorian spark/

echo "=== Démarrage du cluster ==="
docker-compose up -d

echo "=== Attente du démarrage (30s) ==="
sleep 30

echo "=== État des containers ==="
docker ps

echo "=== Rapport HDFS ==="
docker exec -it namenode bash -c "hdfs dfsadmin -report"