# 🐘 Docker Hadoop + Spark Cluster

Cluster Hadoop 3.3.5 + Spark 3.4.3 entièrement conteneurisé avec Docker Compose.

---

## 🏗️ Architecture du cluster

| Conteneur | Rôle | Port(s) exposé(s) |
|---|---|---|
| `namenode` | Maître HDFS — gère les métadonnées | `9870` (UI), `9000` (RPC) |
| `datanode-1` | Stockage HDFS nœud 1 | `9864` |
| `datanode-2` | Stockage HDFS nœud 2 | `9865` |
| `resourcemanager` | Ordonnanceur YARN | `8088` (UI), `8032` |
| `nodemanager` | Exécution des tâches YARN | — |
| `historyserver` | Historique des jobs MapReduce | — |
| `spark-master` | Maître Spark standalone | `8080` (UI), `7077` (RPC) |
| `spark-worker-a` | Worker Spark A | `9091` (UI), `7000` |
| `spark-worker-b` | Worker Spark B | `9092` (UI), `7001` |

**Résumé :** 2 DataNodes · 1 NodeManager · 2 Spark Workers

---

## 🚀 Démarrage du cluster (première fois)

```bash
# 1. Build les images + démarre tout
chmod +x run_cluster.sh
./run_cluster.sh
```

Ce script fait automatiquement :
1. `docker build -t hadoop-base:3.3.5-dorian base/`
2. `docker build -t spark-base:3.4.3-dorian spark/`
3. `docker-compose up -d`
4. Attend 30 secondes
5. Affiche l'état des containers + rapport HDFS

### Démarrages suivants (images déjà buildées)

```bash
docker-compose up -d
```

### Arrêt

```bash
docker-compose down
```

---

## 🌐 Interfaces Web

| Interface | URL |
|---|---|
| HDFS NameNode UI | http://localhost:9870 |
| YARN Resource Manager | http://localhost:8088 |
| Spark Master UI | http://localhost:8080 |
| Spark Worker A | http://localhost:9091 |
| Spark Worker B | http://localhost:9092 |

---

## 📁 Préparer les données dans HDFS

Avant de lancer les jobs, il faut uploader les fichiers CSV dans HDFS depuis le namenode.

```bash
# Entrer dans le namenode
docker exec -it namenode bash

# Créer le répertoire d'entrée dans HDFS
hdfs dfs -mkdir -p /root/input

# Uploader les fichiers (ils sont montés dans /Workspace/Data)
hdfs dfs -put /Workspace/Data/games_data.csv   /root/input/
hdfs dfs -put /Workspace/Data/players_data.csv /root/input/

# Vérifier
hdfs dfs -ls /root/input
```

---

## ⚡ Lancer le job Spark

```bash
# 1. Entrer dans le spark-master
docker exec -it spark-master bash

# 2. Lancer le job (les fichiers .py sont dans /opt/spark-apps)
spark-submit \
  --master spark://spark-master:7077 \
  --conf spark.hadoop.fs.defaultFS=hdfs://namenode:9000 \
  /opt/spark-apps/spark_job.py
```

Le job calcule 3 KPIs et les sauvegarde en Parquet dans HDFS :

| Fichier de sortie | Contenu |
|---|---|
| `/root/sparkoutput/Session_metrics.parquet` | Statistiques globales de session (durée, XP, achievements…) |
| `/root/sparkoutput/Games_genre_metrics.parquet` | Métriques par genre de jeu |
| `/root/sparkoutput/Player_level_metrics.parquet` | Métriques par niveau joueur (Beginner / Mid-Level / Advanced) |

### Vérifier les résultats

```bash
# Dans le namenode
hdfs dfs -ls /root/sparkoutput/
```

---

## 🗺️ Lancer les jobs MapReduce

Les mappers/reducers sont dans `/Workspace/Code` (montés depuis `./Code`).

```bash
# Entrer dans le namenode
docker exec -it namenode bash

# Exemple pour Q1
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input  /root/input/purchases.txt \
  -output /root/output/q1 \
  -mapper /Workspace/Code/q1_mapper.py \
  -reducer /Workspace/Code/q1_reducer.py
```

Répéter avec `q2_mapper.py` / `q2_reducer.py`, etc.

---

## 📂 Structure du projet

```
docker-hadoop/
├── base/               # Image de base Hadoop (partagée par tous les services)
│   ├── Dockerfile
│   ├── entrypoint.sh
│   └── conf/           # core-site.xml, hdfs-site.xml, yarn-site.xml…
├── namenode/           # NameNode HDFS
├── datanode/           # DataNode (utilisé pour datanode-1 et datanode-2)
├── resourcemanager/    # YARN ResourceManager
├── nodemanager/        # YARN NodeManager
├── historyserver/      # MapReduce History Server
├── spark/              # Image Spark (master + workers via SPARK_WORKLOAD)
│   ├── Dockerfile
│   └── start-spark.sh
├── apps/               # spark_job.py → monté dans /opt/spark-apps
├── Code/               # Mappers & Reducers Python → montés dans /Workspace/Code
├── Data/               # Datasets CSV → montés dans /Workspace/Data
├── docker-compose.yml
├── hadoop.env          # Variables d'env Hadoop partagées
└── run_cluster.sh      # Script de démarrage complet
```

---

## 🔧 Commandes utiles

```bash
# État des containers
docker ps

# Logs d'un service
docker logs namenode
docker logs spark-master

# Rapport HDFS (datanodes connectés, espace…)
docker exec -it namenode bash -c "hdfs dfsadmin -report"

# Voir les fichiers HDFS
docker exec -it namenode bash -c "hdfs dfs -ls /root/"

# Entrer dans un container
docker exec -it namenode bash
docker exec -it spark-master bash
docker exec -it spark-worker-a bash
```

---

## ⚠️ Notes importantes

- Le namenode **ne se formate qu'à la première création** du volume. Si tu veux repartir à zéro : `docker-compose down -v` (supprime les volumes).
- Les images `hadoop-base:3.3.5-dorian` et `spark-base:3.4.3-dorian` doivent être buildées localement **avant** le `docker-compose up` (le script `run_cluster.sh` le fait automatiquement).
- Spark lit et écrit dans HDFS via `hdfs://namenode:9000`.
