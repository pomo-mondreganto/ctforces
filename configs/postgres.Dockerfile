FROM postgres:10.6

ADD ./configs/init-user-db.sh /docker-entrypoint-initdb.d/init-user-db.sh
