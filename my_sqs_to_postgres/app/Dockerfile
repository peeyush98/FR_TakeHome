FROM postgres:13

# Create a database and user
ENV POSTGRES_DB postgres
ENV POSTGRES_USER localhost
ENV POSTGRES_PASSWORD 1234

# Copy SQL scripts or database initialization files
COPY init.sql /docker-entrypoint-initdb.d/

# Expose PostgreSQL port (optional)
EXPOSE 5432