# Base Java 17 compatível com Spark
FROM eclipse-temurin:17-jdk

# instalar python, pip, utilitários
RUN apt-get update \
    && apt-get install -y python3 python3-pip wget ca-certificates unzip \
    && apt-get clean

# Variáveis Spark
ENV SPARK_VERSION=3.5.0
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/opt/spark
ENV PATH="$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin"

# Baixar Spark 3.5 compatível com PySpark 3.5
RUN wget -q https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
 && tar -xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -C /opt \
 && mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} $SPARK_HOME \
 && rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# Diretório de trabalho
WORKDIR /app
ENV PYTHONPATH=/app

# Copiar requirements e instalar (sem pyspark)
COPY requirements.txt /app/requirements.txt
RUN pip3 install --break-system-packages --no-cache-dir -r /app/requirements.txt

# FORÇAR versão compatível do pyspark (ESSENCIAL)
RUN pip3 install --break-system-packages pyspark==3.5.0

# Copiar todo o código
COPY . /app

# Entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["bash"]
