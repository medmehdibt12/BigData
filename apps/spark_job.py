#!/usr/bin/python3
"""
spark_job.py - Analyse des données de jeux vidéo avec PySpark
KPIs calculés :
  1. Session metrics      → statistiques clés par session joueur
  2. Game genre metrics   → métriques par genre de jeu (jointure games + players)
  3. Player level metrics → métriques par niveau de joueur
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql import SparkSession
import logging

# ─── Configuration du logging ────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ─── Fonctions de nettoyage ───────────────────────────────────────────────────

def clean_games_table(games_df: DataFrame) -> DataFrame:
    """
    Nettoie la table games_info :
      - Suppression des doublons sur GameID
      - Normalisation de la colonne Rating (E→Everyone, T→Teen, M→Mature)
    """
    games_df = games_df.dropDuplicates(['GameID'])

    games_df = games_df.withColumn(
        "Rating",
        F.when(F.col("Rating") == "E", "Everyone")
         .when(F.col("Rating") == "T", "Teen")
         .when(F.col("Rating") == "M", "Mature")
         .otherwise("NoRating"),
    )
    return games_df


def clean_activities_table(activities_df: DataFrame) -> DataFrame:
    """
    Nettoie la table player_activity :
      - Normalisation du Level en catégories (Beginner / Mid-Level / Advanced)
      - Conversion StartTime & EndTime en timestamp
      - Calcul de SessionDuration en minutes
    """
    # Normalisation du niveau joueur
    activities_df = activities_df.withColumn(
        "Level",
        F.when(F.col("Level") < 30, "Beginner")
         .when((F.col("Level") > 30) & (F.col("Level") < 60), "Mid-Level")
         .when(F.col("Level") > 60, "Advanced")
         .otherwise("Unknown"),
    )

    # Conversion des timestamps
    activities_df = activities_df.withColumn(
        'StartTime', F.col('StartTime').cast('timestamp')
    )
    activities_df = activities_df.withColumn(
        'EndTime', F.col('EndTime').cast('timestamp')
    )

    # Durée de session en minutes
    activities_df = activities_df.withColumn(
        'SessionDuration',
        (F.col('EndTime').cast('long') - F.col('StartTime').cast('long')) / 60,
    )
    return activities_df


# ─── Fonctions de calcul des KPIs ────────────────────────────────────────────

def session_metrics(activities_df: DataFrame) -> DataFrame:
    """
    KPI 1 - Statistiques globales de session :
      - Durée moyenne de session (minutes)
      - Moyenne de points d'expérience gagnés
      - Moyenne d'achievements débloqués
      - Moyenne de monnaie gagnée / dépensée
      - Moyenne de quêtes complétées
    """
    session_metrics_df = activities_df.select(
        F.round(F.mean(F.col("SessionDuration"))).alias("Avg_SessionDuration_minutes"),
        F.round(F.mean(F.col("ExperiencePoints"))).alias("Avg_ExperiencePoints"),
        F.round(F.mean(F.col("AchievementsUnlocked"))).alias("Avg_AchievementsUnlocked"),
        F.round(F.mean(F.col("CurrencyEarned"))).alias("Avg_CurrencyEarned"),
        F.round(F.mean(F.col("CurrencySpent"))).alias("Avg_CurrencySpent"),
        F.round(F.mean(F.col("QuestsCompleted"))).alias("Avg_QuestsCompleted"),
    ).orderBy(F.col('Avg_SessionDuration_minutes').desc())

    return session_metrics_df


def game_genre_metrics(activities_df: DataFrame, games_df: DataFrame) -> DataFrame:
    """
    KPI 2 - Métriques par genre de jeu (nécessite une jointure) :
      - Durée moyenne de session par genre
      - Total de quêtes complétées par genre
      - Longueur moyenne de jeu par genre
    """
    game_genre_metrics_df = (
        activities_df.join(games_df, on='GameID', how='inner')
        .groupBy('Genre')
        .agg(
            F.round(F.mean(F.col("SessionDuration"))).alias("Avg_SessionDuration_minutes"),
            F.sum(F.col("QuestsCompleted")).alias("Total_QuestsCompleted"),
            F.round(F.mean(F.col("Game_Length"))).alias("Avg_Game_Length_minutes"),
        )
    )
    return game_genre_metrics_df


def player_level_metrics(activities_df: DataFrame) -> DataFrame:
    """
    KPI 3 - Métriques par niveau de joueur :
      - Nombre moyen d'ennemis éliminés par niveau
      - Nombre moyen de quêtes complétées par niveau
    """
    player_lvl_metrics_df = activities_df.groupBy('Level').agg(
        F.round(F.mean(F.col("EnemiesDefeated"))).alias("Avg_EnemiesDefeated"),
        F.round(F.mean(F.col("QuestsCompleted"))).alias("Avg_QuestsCompleted"),
    )
    return player_lvl_metrics_df


# ─── Écriture dans HDFS ──────────────────────────────────────────────────────

def write_to_parquet(path: str, df: DataFrame):
    """
    Sauvegarde un DataFrame sous format Parquet dans HDFS.
    :param path : chemin HDFS de destination
    :param df   : DataFrame Spark à sauvegarder
    """
    df.write.mode("overwrite").parquet(path, compression=None)
    logger.info(f"File {path} saved to HDFS!!")


# ─── Fonction principale ──────────────────────────────────────────────────────

def main():
    with SparkSession.builder.appName("spark_project").getOrCreate() as spark:

        # Lecture des fichiers CSV depuis HDFS
        logger.info("Lecture de games_data.csv depuis HDFS...")
        games_df = spark.read.csv(
            "hdfs://namenode:9000/root/input/games_data.csv",
            inferSchema=True, header=True
        )

        logger.info("Lecture de players_data.csv depuis HDFS...")
        activities_df = spark.read.csv(
            "hdfs://namenode:9000/root/input/players_data.csv",
            inferSchema=True, header=True
        )

        # Nettoyage des données
        logger.info("Nettoyage des tables...")
        games_clean_df      = clean_games_table(games_df)
        activities_clean_df = clean_activities_table(activities_df)

        # Calcul des KPIs
        logger.info("Calcul des KPIs...")
        session_metrics_df     = session_metrics(activities_clean_df)
        game_genre_metrics_df  = game_genre_metrics(activities_clean_df, games_clean_df)
        player_level_metrics_df = player_level_metrics(activities_clean_df)

        # Sauvegarde dans HDFS (format Parquet)
        write_to_parquet(
            "hdfs://namenode:9000/root/sparkoutput/Session_metrics.parquet",
            session_metrics_df
        )
        write_to_parquet(
            "hdfs://namenode:9000/root/sparkoutput/Games_genre_metrics.parquet",
            game_genre_metrics_df
        )
        write_to_parquet(
            "hdfs://namenode:9000/root/sparkoutput/Player_level_metrics.parquet",
            player_level_metrics_df
        )

        logger.info("✅ Tous les KPIs ont été sauvegardés dans HDFS avec succès!")


if __name__ == '__main__':
    main()