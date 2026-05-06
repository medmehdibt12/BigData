FROM debian:11

# Installer les dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jdk \
    net-tools \
    curl \
    netcat \
    gnupg \
    libsnappy-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y python3 python3-setuptools python3-pip

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/

# Télécharger et vérifier Hadoop
RUN curl -O https://dist.apache.org/repos/dist/release/hadoop/common/KEYS
RUN gpg --import KEYS

ENV HADOOP_VERSION=3.3.5
ENV HADOOP_URL=https://www.apache.org/dist/hadoop/common/hadoop-3.3.5/hadoop-3.3.5.tar.gz

RUN set -x \
    && curl -fSL "$HADOOP_URL" -o /tmp/hadoop.tar.gz \
    && curl -fSL "$HADOOP_URL.asc" -o /tmp/hadoop.tar.gz.asc \
    && gpg --verify /tmp/hadoop.tar.gz.asc \
    && tar -xvf /tmp/hadoop.tar.gz -C /opt/ \
    && rm /tmp/hadoop.tar.gz*

# Lien symbolique et dossiers
RUN ln -s /opt/hadoop-3.3.5/etc/hadoop /etc/hadoop
RUN mkdir /opt/hadoop-3.3.5/logs
RUN mkdir /hadoop-data

# Variables d'environnement Hadoop
ENV HADOOP_HOME=/opt/hadoop-3.3.5
ENV HADOOP_CONF_DIR=/etc/hadoop
ENV MULTIHOMED_NETWORK=1
ENV USER=root
ENV PATH=$HADOOP_HOME/bin/:$PATH

# Entrypoint
ADD entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Fichiers de configuration
COPY conf/core-site.xml $HADOOP_CONF_DIR/core-site.xml
COPY conf/hdfs-site.xml $HADOOP_CONF_DIR/hdfs-site.xml
COPY conf/mapred-site.xml $HADOOP_CONF_DIR/mapred-site.xml
COPY conf/yarn-site.xml $HADOOP_CONF_DIR/yarn-site.xml

# ===== SPARK =====
# ✅ CORRECTION : utiliser archive.apache.org au lieu de downloads.apache.org
ENV SPARK_VERSION=3.4.3
ENV SPARK_URL=https://archive.apache.org/dist/spark/spark-3.4.3/spark-3.4.3-bin-hadoop3.tgz
ENV SPARK_HOME=/opt/spark-3.4.3-bin-hadoop3
ENV PATH=$SPARK_HOME/bin:$PATH
ENV PYSPARK_PYTHON=python3
ENV PYTHONHASHSEED=1

RUN set -x \
    && curl -fSL "${SPARK_URL}" -o /tmp/spark.tar.gz \
    && tar -xvzf /tmp/spark.tar.gz -C /opt/ \
    && rm /tmp/spark.tar.gz*

ADD conf/core-site.xml $SPARK_HOME/conf
ADD conf/yarn-site.xml $SPARK_HOME/conf