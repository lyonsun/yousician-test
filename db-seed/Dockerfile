FROM mongo

LABEL maintainer="Liang Sun <sunly917@gmail.com>"

COPY songs.json /songs.json

CMD mongoimport --host mongodb --db ${MONGO_DBNAME} --collection songs --authenticationDatabase admin --username ${MONGO_USERNAME} --password ${MONGO_PASSWORD} --type json --file /songs.json --jsonArray