FROM mongo

LABEL developer="Liang Sun <sunly917@gmail.com>"

COPY songs.json /songs.json

CMD mongoimport --host mongodb --db ${MONGO_DBNAME} --collection songs --authenticationDatabase admin --username ${MONGO_USERNAME} --password ${MONGO_PASSWORD} --type json --file /songs.json --jsonArray
# CMD mongoimport  --host mongodb --db music --collection songs --type json --file /songs.json --jsonArray