rm components/*

#wget https://raw.githubusercontent.com/psy0rz/p1_dsmr_to_influxdb/master/p1_to_influxdb.py -P ./components/
cp ../src/p1_to_influxdb2.py components
cp ../src/config.py components
cp Dockerfile components