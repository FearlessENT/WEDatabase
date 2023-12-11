# Use the official MySQL image as a base
FROM mysql:8.0

# Add your SQL script to the docker-entrypoint-initdb.d directory
COPY init-db.sql /docker-entrypoint-initdb.d/
