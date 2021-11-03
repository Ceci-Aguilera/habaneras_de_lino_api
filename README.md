#mom_style_api

This website is an online store to sell clothes such as guayaberas, guayamisas, filipinas, ...
It does not require the client to have an account to buy, instead, it uses the ip address and a token to make each cart/order unique.

### Contents
[Installation](#installation)

[Models](#models)

[TODOS](#todos)

<a name='#installation'></a>

### Installation

To run this application locally do the following 

1. Clone repo from ==Github== and replicate python's virtual environment. This commands are for virtualenv and virtualenvwrapper:

   ```shell
   git clone git@github.com:Ceci-Aguilera/mom_style_api.git
   cd mom_style_api
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

   

3. Change the settings file in settings/__init__.py from heroku_test.py to dev.py.

4. Set local environment variables on a .env file inside settings with the following variables:

   - DB name, user, password, host, port.
   - Stripe keys.
   - Email user and password.
   - Django secret key.
   - Cloudinary credentials.

5. Run the migrations and finally run the app locally:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```

     

<a name='#models'></a>

### Models

The models: __product__, __category__, and __order__ do what they are expected to. The __cart__ model works for anonymous users which are the only users so far. It registers a token that is stored in the browser by the frontend and the user's ip address. The __product variations__ model stores the changes made to a __product__ by the user, and so it is the final product that is added to the __cart__. In other words, the admin creates the __products__ and the user adds the __product variation__. The __payment__ model is linked to the __order__, and it also keeps track of the user's ip address while the order keeps track of the __cart__.



<a name='#todos'></a>

### TODOS

1. Improve the admin site so it can be more legible for the store owner (view the cart in the order, and the products of the cart) or create an admin panel from zero.
2. Add basic statistics to the admin panel.
3. Create subcategories, for example, a category can be camisas and a subcategory can be guayaberas or guayamisas. Find how to modify this in product variations. DONE: added subtag filter
4. Create Users (Admins and Staff). Admins can modify content while staff can only view it.
5. Create send email templates.