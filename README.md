# p1-influxdb


### Prerequisites
*Download hypriot and flash:* 

https://github.com/hypriot/flash


*Expose Docker to dev machine:*
- SSH into hypriot
- sudo nano /lib/systemd/system/docker.service
- Change this line: ExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0:2375
- sudo systemctl daemon-reload
- sudo systemctl restart docker 

### Run
cd docker/components

Add a deploy.sh: docker -H 192.168.0.155 run --restart=always --privileged --device /dev/ttyUSB0 p1-to-influxdb -e ENVIRONMENT_VARIABLES
./prepareComponents.sh && ./build.sh && ./deploy.sh