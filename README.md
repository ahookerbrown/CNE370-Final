# MariaDB MaxScale Sharded Database Docker image


## Running
This configuration simulates a basic sharded database environment with two MariaDB shards. 
shard1: contains zipcodes_one database
shard2: contains zipcodes_two database

MaxScale is set up as a query router, distributing SQL queries across the 
appropriate shards based on database name.

To start the cluster, navigate to the directory and run:

```
docker-compose build
docker-compose up -d
```
This will start up MaxScale along with two MariaDB shard containers. 
After a few seconds, you can begin routing queries through MaxScale.

MaxScale exposes ports for client connections:

Port 4000 – Generic SQL routing

Port 8989 – MaxCtrl admin interface

MaxScale and the databses use the following credentials:
```
username: maxuser
password: password
```

Example using the MariaDB client:
```
$ mysql -umaxuser -ppassword -h 127.0.0.1 -P 4000 zipcodes_one
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 1
Server version: 5.5.5-10.3.39-MariaDB-1:10.3.39+maria~ubu2004 mariadb.org binary distribution

Copyright (c) 2000, 2025, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 

```
You can edit the [`maxscale.cnf`](./maxscale.cnf)
file and recreate the MaxScale container to change the configuration.

How to recreate the containers after updating the configuration:

```
docker-compose down -v
docker-compose up --build -d
```

How to get info on what docker containers are running:
```
docker ps
```

How to run maxctrl in the container to see the status of the cluster:
```
$ docker-compose exec maxscale maxctrl list servers
┌────────┬─────────┬──────┬─────────────┬─────────────────┬──────┬───────────────┐                        
│ Server │ Address │ Port │ Connections │ State           │ GTID │ Monitor       │                        
├────────┼─────────┼──────┼─────────────┼─────────────────┼──────┼───────────────┤                        
│ shard1 │ shard1  │ 3306 │ 0           │ Master, Running │      │ MySQL-Monitor │                        
├────────┼─────────┼──────┼─────────────┼─────────────────┼──────┼───────────────┤                        
│ shard2 │ shard2  │ 3306 │ 0           │ Running         │      │ MySQL-Monitor │                        
└────────┴─────────┴──────┴─────────────┴─────────────────┴──────┴───────────────┘  

```

Once complete, to remove the cluster and maxscale containers:

```
docker-compose down -v
```

To run the main.py file to query the database, you will need python
and mysql-connector-python installed.

Commands to install/run the python script:


```
chmod +rx main.py
sudo apt install python3-venv -y
python3 -m venv venv
source venv/bin/activate
pip install mysql-connector-python
python main.py
```

The script will perform the following queries and print the
output to the console:

-The largest zipcode in zipcodes_one
-All zipcodes where state=KY (Kentucky). You may return just the zipcode column, or all columns.
-All zipcodes between 40000 and 41000 
-The TotalWages column where state=PA (Pennsylvania)


## Thanks! :)