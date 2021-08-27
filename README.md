## Table of Content
* [Installation](#installation)
* [File Descriptions](#file-descriptions)
* [Examples of use](#examples-of-use)
* [Bugs](#bugs)
* [Authors](#authors)
* [License](#license)

### Note: Currently I'm working on deployment and backend. For the moment it is running in a free EC2 instance http://ec2-3-15-217-168.us-east-2.compute.amazonaws.com:1337/

# Installation

1. Clone this repository `git clone https://gitlab.com/dagomez30/trading_bot.git`
2. Access to `cd trading_bot`
3. Install dependencies `pip install -r requirements.txt`
4. If you don't have postgresql installed go to `https://www.postgresql.org/download/`
5. After Install postgresql login with the database user created.
6. Create a new database user `trader` with the privilege of create databases `CREATE USER trader WITH PASSWORD 'trading2077' CREATEDB;`
8. Execute the command `python manage.py makemigrations`
9. Execute `python manage.py migrate`
10. Create the superuser `python manage.py createsuperuser`
11. Finally, run the server `python manage.py runserver`

# File Description

[entrypoint.sh](entrypoint.sh) - Script to verify that postgres is working before running the Django development server.

[entrypoint.prod.sh](entrypoint.prod.sh) - Script to verify that postgres is working before running the Django production server.

[requirements.txt](requirements.txt) - The configuration file requirements.txt allows to install the specified packages necessary for the project.

[docker-compose.yml](docker-compose.yml) - Allows to deploy, combine and configure the docker-containers Django and Postgresql for development.

[docker-compose.prod.yml](docker-compose.prod.yml) - Allows to deploy, combine and configure the docker-containers Django, Nginx and Postgresql for production.

## `nginx/` Contains the Nginx Dockerfile and the server's configuration files.
[nginx.conf](/nginx/nginx.conf) - Nginx base configuration.

[Dockerfile](/nginx/Dockerfile) - Contains the instructions to build the nginx image

## `bot/` Contains the backend development of the project
* [manage.py](bot/manage.py) - Script to run admin tasks

### `bot/bot/` Contains the setting files for the project
* [settings.py](/bot/bot/settings.py) - This file contains the settings and some environment variables.
* [urls.py](/bot/bot/urls.py) - Main urls file.


### `bot/bot_signals/` Contains the app for the bot and its stats
* [admin.py](/bot/bot_signals/admin.py) - Allows to add the models and show them in the admin dashboard.
* [bot_v1.py](/bot/bot_signals/bot_v1.py) - Test version of the bot (working on it)
* [models.py](/bot/bot_signals/models.py) - Contains the models to create the database.
* [urls.py](/bot/bot_signals/urls.py) - Contains the app urls
* [views.py](/bot/bot_signals/views.py) - Contains the app views.

### `bot/static/` Contains the static files: HTML, CSS, JS

### `bot/trading/` Contains the system to register and manage the trading operations.

