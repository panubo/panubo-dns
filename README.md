# DNS Management UI

[![Docker Repository on Quay.io](https://quay.io/repository/panubo/panubo-dns/status "Docker Repository on Quay.io")](https://quay.io/repository/panubo/panubo-dns)

This is a web based DNS zone editor written in Django. It relies upon the following components for the heavy lifting:

- [Django DNS Manager](https://github.com/voltgrid/django-dnsmanager) - Django DNS Zone Editor
- [Squab](https://github.com/panubo/python-squab) - CouchDB bindings for Python Applications
- [CouchDB](http://couchdb.apache.org/) is used as a transport for replicating zone changes to disparate DNS slaves.

Integration with Unbound DNS is handled with [Panubo DNS Integration](https://github.com/panubo/panubo-dns-integration).

## Features

- API
- Bind compatible zone file import (via API)
- Automatic Validation / Delegation Checking
- Delegate access to sub-organisations or users.

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

    OLDIFS=$IFS; IFS=$'\n'; for l in $(cat $VIRTUAL_ENV/.env); do eval export echo "$l"; done; IFS=$OLDIFS
    
This will automatically load the _.env_ settings when entering the virtual environment. 
Which makes it easier to manually run _./manage.py_.

## Docker Install

Build the `Dockerfile` or pull the [container](https://quay.io/repository/panubo/panubo-dns).
