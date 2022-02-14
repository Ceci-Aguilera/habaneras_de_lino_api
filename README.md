#habaneras_de_lino_api

This website is an online store to sell clothes such as guayaberas, guayamisas, filipinas, ...
It does not require the client to have an account to buy, instead, it uses the ip address and a token to make each cart/order unique.

### Contents
[Installation](#installation)

[TODOS](#todos)

<a name='#installation'></a>

### Installation

To run this application locally do the following 

1. Clone repo from __Github__ and replicate python's virtual environment. These commands are for virtualenv and virtualenvwrapper:

   ```shell
   git clone git@github.com:Ceci-Aguilera/habaneras_de_lino_api.git
   cd habaneras_de_lino_api
   mkvirtualenv env_name
   workon env
   pip install -r requirements.txt
   ```

2. Set up the database (currently using PostgreSQL). To do it on Ubuntu:

   ```sql
   sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib
   
   sudo su - postgres
   
   psql
   
   CREATE DATABASE myproject;
   
   CREATE USER myprojectuser WITH PASSWORD 'password';
   
   ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
   
   ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
   
   ALTER ROLE myprojectuser SET timezone TO 'UTC';
   
   GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
   
   \q
   
   exit
   
   sudo service postgresql start
   ```


3. Set local environment variables on a .env file inside settings with the following variables:

   - DB name, user, password, host, port.
   - Stripe keys.
   - Email user and password.
   - Django secret key.
   - Cloudinary credentials.

4. Run the migrations and finally run the app locally:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```


<a name='#todos'></a>

### TODOS

1. Improve the admin site so it can be more legible for the store owner (view the cart in the order, and the products of the cart) or create an admin panel from zero.
2. Add basic statistics to the admin panel.