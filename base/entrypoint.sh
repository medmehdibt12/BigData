#!/bin/bash

# Fonction pour corriger les variables d'environnement Hadoop
addProperty() {
  local path=$1
  local name=$2
  local value=$3

  local entry="<property><name>$name</name><value>${value}</value></property>"
  local escapedEntry=$(echo $entry | sed 's/\//\\\//g')
  sed -i "s/<\/configuration>/${escapedEntry}\n<\/configuration>/" $path
}

configure() {
  local path=$1
  local module=$2
  local envPrefix=$3

  local var
  local value

  echo "Configuring $module"
  for c in `printenv | perl -sne 'print "$1 " if m/^${envPrefix}_(.+?)=.*/' -- -envPrefix=$envPrefix`; do
    name=`echo ${c} | perl -pe 's/___/-/g; s/__/@/g; s/_/./g; s/@/_/g;'`
    var="${envPrefix}_${c}"
    value=${!var}
    echo " - Setting $name=$value"
    addProperty $path $name $value
  done
}docker exec -it spark-master bash

configure /etc/hadoop/core-site.xml core CORE_CONF
configure /etc/hadoop/hdfs-site.xml hdfs HDFS_CONF
configure /etc/hadoop/yarn-site.xml yarn YARN_CONF
configure /etc/hadoop/httpfs-site.xml httpfs HTTPFS_CONF
configure /etc/hadoop/kms-site.xml kms KMS_CONF
configure /etc/hadoop/mapred-site.xml mapred MAPRED_CONF

if [ "$MULTIHOMED_NETWORK" = "1" ]; then
  echo "Configuring for multihomed network"
  # Permettre l'écoute sur toutes les interfaces
  addProperty /etc/hadoop/hdfs-site.xml dfs.namenode.rpc-bind-host 0.0.0.0
  addProperty /etc/hadoop/hdfs-site.xml dfs.namenode.servicerpc-bind-host 0.0.0.0
  addProperty /etc/hadoop/hdfs-site.xml dfs.namenode.http-bind-host 0.0.0.0
  addProperty /etc/hadoop/hdfs-site.xml dfs.namenode.https-bind-host 0.0.0.0
  addProperty /etc/hadoop/hdfs-site.xml dfs.client.use.datanode.hostname true
  addProperty /etc/hadoop/yarn-site.xml yarn.resourcemanager.bind-host 0.0.0.0
  addProperty /etc/hadoop/yarn-site.xml yarn.nodemanager.bind-host 0.0.0.0
  addProperty /etc/hadoop/yarn-site.xml yarn.timeline-service.bind-host 0.0.0.0
  addProperty /etc/hadoop/mapred-site.xml yarn.nodemanager.bind-host 0.0.0.0
fi

if [ -n "$SERVER_GID" ]; then
  groupmod -g "$SERVER_GID" hadoop > /dev/null 2>&1
fi

exec $@