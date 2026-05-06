FROM hadoop-base:3.3.5-dorian

# procps fournit la commande ps (requis par load-spark-env.sh)
RUN apt-get update && apt-get install -y procps bash && rm -rf /var/lib/apt/lists/*

ENV SPARK_HOME=/opt/spark-3.4.3-bin-hadoop3
ENV PATH=$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH

# WORKDIR doit pointer vers le vrai SPARK_HOME
WORKDIR $SPARK_HOME

ENV SPARK_MASTER_PORT=7077 \
    SPARK_MASTER_WEBUI_PORT=8080 \
    SPARK_WORKER_WEBUI_PORT=8081 \
    SPARK_WORKER_PORT=7000 \
    SPARK_MASTER="spark://spark-master:7077" \
    SPARK_WORKLOAD="master" \
    SPARK_LOG_DIR=/opt/spark-3.4.3-bin-hadoop3/logs

RUN mkdir -p $SPARK_LOG_DIR

COPY start-spark.sh /start-spark.sh
RUN chmod +x /start-spark.sh

CMD ["/start-spark.sh"]