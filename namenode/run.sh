#!/bin/bash

# ⚠️ CORRECTION CRITIQUE : formater le namenode seulement si pas déjà fait
namedir=`echo $HDFS_CONF_dfs_namenode_name_dir | perl -pe 's#file://##'`
if [ ! -d $namedir ]; then
  echo "Le répertoire du namenode n'existe pas, formatage en cours..."
  $HADOOP_HOME/bin/hdfs namenode -format -force -nonInteractive
else
  echo "Répertoire namenode existant, pas de reformatage"
fi

$HADOOP_HOME/bin/hdfs namenode