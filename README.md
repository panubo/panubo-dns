# DNS Management UI

This is a web based DNS management UI written in Django. It relies upon the following components for the heavy lifting:

- [Volt Grid DNS Manager](https://github.com/voltgrid/django-dnsmanager)


## Local Install

### Step 1: Create a virtual environment

Create a virtual environment. [Python Bootstrap](https://github.com/adlibre/python-bootstrap) is a handy tool for this.

### Step 2: Clone this repo 

Clone this repo to the base of your newly created virtual environment.

### Step 3: Initialise the app

After entering the virtual environment. Run the following:

    pip install bureaucrat
    cp .env.example .env  # edit as required
    bureaucrat init

Running `bureaucrat init` will run the deployment steps, and start the app.

Optionally: Add the following to _bin/activate_:

    OLDIFS=$IFS; IFS=$'\n'; for l in $(cat $VIRTUAL_ENV/.env); do eval export echo $l; done; IFS=$OLDIFS
    
This will automatically load the _.env_ settings when entering the virtual environment. Which makes it easier to manually run _./manage.py_.
