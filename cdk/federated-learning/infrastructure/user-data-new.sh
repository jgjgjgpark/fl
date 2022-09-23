#!/bin/bash -ex
# install nginx on Amazon linux Image2
sudo amazon-linux-extras install -y nginx1

## install uwsgi server
#sudo yum -y install gcc
#pip3 install uwsgi
#
## download and setup app
#mkdir /feedernet
#cd /feedernet
#aws s3 cp s3://bucket/deploy-app.zip .
#unip deploy-app.zip
#pip3 install -r FlaskApp/requirements.txt
#
## copy nginx config
#mv -f Deploy/nginx.conf /etc/nginx/nginx.conf
## configure upstart to run uwsgi
#mv -f Deploy/uwsgi.conf /etc/init/uwsgi.conf
#start uwsgi

# switch on nginx and configure to autostart


#sudo systemctl enable nginx
#sudo systemctl start nginx

mkdir feedernet
cd feedernet
aws s3 cp s3://federated-learning-bucket/org_api_server/deploy-app.zip .
unzip deploy-app.zip
sudo pip3 install -r requirements.txt
sudo python3 src/main.py


