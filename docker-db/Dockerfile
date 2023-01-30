# base image
# postgres
# FROM postgres:13-alpine


# FROM mysql/mysql-server
# # run create.sql on init
# ADD create.sql /docker-entrypoint-initdb.d

FROM mysql/mysql-server

ENV MYSQL_DATABASE=DB \
    MYSQL_ROOT_PASSWORD=password \
    MYSQL_ROOT_HOST=%

ADD schema.sql /docker-entrypoint-initdb.d

EXPOSE 3306