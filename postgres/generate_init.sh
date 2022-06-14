  #!/bin/bash

declare -a databases=("adplist")

for database in "${databases[@]}"
do
   echo "
CREATE USER $database WITH PASSWORD '$database';
ALTER USER $database WITH SUPERUSER;
CREATE DATABASE $database;
GRANT ALL PRIVILEGES ON DATABASE $database TO $database;"
done
