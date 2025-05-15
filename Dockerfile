# Use the official Milvus image as the base
FROM milvusdb/milvus:v2.3.10-standalone

# Set the working directory inside the container
WORKDIR /milvus

# Copy any local configuration or files if needed (adjust this part as needed)
COPY ./volumes /milvus/volumes

# Expose the necessary ports for Milvus
EXPOSE 19530
EXPOSE 9091

# Start Milvus when the container runs
CMD ["milvus", "run", "standalone"]
