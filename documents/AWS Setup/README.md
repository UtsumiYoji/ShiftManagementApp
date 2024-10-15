# AWS Setup Manual

- [AWS Setup Manual](#aws-setup-manual)
  - [Note: Before starting setup](#note-before-starting-setup)
  - [Setup AWS/EC2(Nginx, gunicorn, postgresql)](#setup-awsec2nginx-gunicorn-postgresql)
    - [Make new instance](#make-new-instance)
    - [Connect with console](#connect-with-console)
    - [Set up Ubuntu](#set-up-ubuntu)
    - [Set up postgresql](#set-up-postgresql)
    - [Make SSH key in AWS](#make-ssh-key-in-aws)
      - [Make SSH](#make-ssh)
      - [Registration key for GitHub](#registration-key-for-github)
    - [Clone project](#clone-project)
    - [Make .env file](#make-env-file)
    - [Setup security Groups](#setup-security-groups)
    - [Run server as a test](#run-server-as-a-test)
    - [Setup gunicorn](#setup-gunicorn)
    - [Setup nginx](#setup-nginx)
    - [Run server with gunicorn](#run-server-with-gunicorn)
    - [Note](#note)
  - [Setup SSL(Https)](#setup-sslhttps)
  - [Document history](#document-history)


## Note: Before starting setup

This document doesn't explain how to set up python/Django environments. I assume you already clone codes through GitHub. "./program/config/setting.py" define some vars using "environ" library. It means you have to make own environment file. This is one sample of it. 

```.env
SECRET_KEY=
DEBUG=False
DATABASE_URL=sqlite:///db.sqlite3
```

This file name has to be `.env`. If you want to run this code in local computer. You can change `DEBUG=True`.  
To generate `SECRET_KEY`, you can use Django function.

```python
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
```

## Setup AWS/EC2(Nginx, gunicorn, postgresql)

### Make new instance

- Go to EC2 page.
- Launch instance > Launch instance
  - Name and tags: arbitrary name
  - Application and OS Images: Ubuntu
  - Key pair(login) > Create new key pair
    - Key pair name: arbitrary name
    - Create key pair
    - Save key file(*.pem) in your computer
  - Launch instance
  
### Connect with console

- Go to EC2 page.
- Resources > Instance (running)
- Click your Instance ID
  - Connect
  - Change tab to SSH client
  - Around bottom, there is Example which start with `ssh`, copy it

- Open terminal(e.g. PowerShell)
- Change directory which has `key_pair.pem`
- Run this commands

```shell
$ chmod 400 key_pair.pem # if using powershell, you can skip
$ Run copied command
```

### Set up Ubuntu

- Run this commands to update Ubuntu
```shell
$ cd
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo chmod o+x /home/ubuntu/
```

- Run this commands to install python3
```shell
$ sudo apt-get install python3-pip python3.12-venv python3-dev libpq-dev postgresql postgresql-contrib nginx
```

### Set up postgresql

- Run this commands to setup postgresql
  - You can change timezone depend on location.
  - You have to change user name and password.
```shell
$ sudo -u postgres psql
CREATE DATABASE djangodb;
CREATE USER django WITH PASSWORD 'password';
ALTER ROLE django SET client_encoding TO 'utf8';
ALTER ROLE django SET default_transaction_isolation TO 'read committed';
ALTER ROLE django SET timezone TO 'UTC-8';
ALTER SCHEMA public OWNER TO django;
GRANT ALL PRIVILEGES ON DATABASE djangodb TO django;
\q
```

### Make SSH key in AWS

#### Make SSH

- Move to .shh directory
```shell
$ cd ~/.ssh
```

- If there is no directory
```shell
$ mkdir ~/.ssh
$ cd ~/.ssh
```

- Make key
```shell
$ ssh-keygen -t rsa
```

- View and copy value of id_rsa.pub
```shell
$ cat id_rsa.pub
```

#### Registration key for GitHub

- Go to GiHub
- Top-right your profile > Settings
- SSH and GPG keys > New SSH key
  - Title: arbitrary name
  - Key: Paste copied id_rsa.pub
  - Add SSH key

### Clone project

- Run this commands to clone
```
$ cd
$ git clone git@github.com:UtsumiYoji/ShiftManagementApp.git
```

- Run this commands to create python-virtual-environment
```
$ cd ShiftManagementApp/program/
$ cd python3 -m venv env
$ source ./env/bin/activate
$ pip install -U pip
$ pip install -r requirements.txt
```

### Make .env file

On your Web
- Go to your instance page on EC2
- Copy Public IPv4 address

On your console
- Run this commands to make .env
```shell
$ vim .env
```

On vim editor
```
SECRET_KEY=Paste your SECRET_KEY
DEBUG=False
DATABASE_URL=postgres://django:password@localhost:/djangodb
ALLOWED_HOSTS=Paste your copied Public IPv4 address
```

```shell
$ chmod +x migrate.sh
$ migrate.sh
```

### Setup security Groups

- Go to your instance page on EC2
- Change tab to Security
- Click Security groups > your group
- Edit inbound rules
  - Add rule
  - Port range: 8000
  - Source: Anywhere-IPv4, 0.0.0.0/0

### Run server as a test

- Run this command to run server
```shell
$ python3 manage.py runserver 0.0.0.0:8000
```

On your web browser(e.g. Chrome)
- Access this url
  `Your public IPv4 address:8000`

### Setup gunicorn

Run this commands to write settings of gunicorn
```shell
$ deactivate
$ sudo vim /etc/systemd/system/gunicorn.service
```

```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/ShiftManagementApp/program
ExecStart=/home/ubuntu/ShiftManagementApp/program/env/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ubuntu/ShiftManagementApp/program/config.sock config.wsgi:application

[Install]
WantedBy=multi-user.target
```

Run this commands to start gunicorn automatically.
```shell
$ sudo systemctl start gunicorn.service
$ sudo systemctl enable gunicorn
```

### Setup nginx

Run this commands to write settings of nginx
```shell
$ sudo vim /etc/nginx/sites-available/ShiftManagementApp
```

```
server {
        listen 80;
        server_name Paste your public IPv4 address;

        location = /favicon.ico {access_log off; log_not_found off;}
        location /static/ {
                root /home/ubuntu/ShiftManagementApp/program;
        }

        location / {
                include proxy_params;
                proxy_pass http://unix:/home/ubuntu/ShiftManagementApp/program/config.sock;
        }
}
```

```shell
$ sudo ln -s /etc/nginx/sites-available/ShiftManagementApp /etc/nginx/sites-enabled/
$ sudo systemctl restart nginx
$ sudo ufw allow 'Nginx Full'
```

### Run server with gunicorn

On your security group
- inbound rules > Edit inbound rules
  - Edit rule1 which Port range is 8000
    - Type: HTTP

On your console
- run this command to run server
```
$ sudo systemctl restart gunicorn
```

On your web browser
- Access this url
  `http://Your public IPv4 address`

### Note

- **Elastic IP**
If you stop running Instance, Public IPv4 address will be changed. To avoid it, You can use Elastic IP. it might charge money to you.

- **Test data**
When you run `migrate.sh`. test data will be loaded, it include admin user with simple password. Id you want not to do, delete `python3 ./manage.py loaddata fixture.json`.


## Setup SSL(Https)

TBD(I need domain...)

## Document history

| Date | Author | Update |
| - | - | - |
| 2024-10-15 | Yoji Utsumi | First issue |
