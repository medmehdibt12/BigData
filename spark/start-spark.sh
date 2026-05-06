#!/bin/bash
set -e

echo "SPARK_WORKLOAD=$SPARK_WORKLOAD"
echo "SPARK_HOME=$SPARK_HOME"

SPARK_WORKER_CORES=${SPARK_WORKER_CORES:-1}
SPARK_WORKER_MEMORY=${SPARK_WORKER_MEMORY:-1G}

if [ "$SPARK_WORKLOAD" = "master" ]; then
  export SPARK_MASTER_HOST="${SPARK_LOCAL_IP:-$(hostname)}"
  echo "Démarrage Master sur $SPARK_MASTER_HOST:${SPARK_MASTER_PORT:-7077}"
  exec "$SPARK_HOME/bin/spark-class" \
    org.apache.spark.deploy.master.Master \
    --ip "$SPARK_MASTER_HOST" \
    --port "${SPARK_MASTER_PORT:-7077}" \
    --webui-port "${SPARK_MASTER_WEBUI_PORT:-8080}"

elif [ "$SPARK_WORKLOAD" = "worker" ]; then
  echo "Démarrage Worker -> $SPARK_MASTER"
  exec "$SPARK_HOME/bin/spark-class" \
    org.apache.spark.deploy.worker.Worker \
    "$SPARK_MASTER" \
    --cores "$SPARK_WORKER_CORES" \
    --memory "$SPARK_WORKER_MEMORY" \
    --webui-port "${SPARK_WORKER_WEBUI_PORT:-8081}"

else
  echo "❌ SPARK_WORKLOAD invalide: $SPARK_WORKLOAD"
  exit 1
fi