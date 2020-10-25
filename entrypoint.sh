#!bin/bash
until nc -z -v -w30 db 3306
do
  echo "Waiting a second until the database is receiving connections..."
  # wait for a second before checking again
  sleep 1
done

echo "mysql started"

flask create-db
flask run -h 0.0.0.0
