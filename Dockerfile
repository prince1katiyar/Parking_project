
FROM milvusdb/milvus:v2.3.10-standalone
WORKDIR /milvus
COPY ./volumes /milvus/volumes
EXPOSE 19530
EXPOSE 9091
CMD ["milvus", "run", "standalone"]
