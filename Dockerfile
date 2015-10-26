FROM panubo/python-bureaucrat

# Install requirements first so this can be cached
COPY requirements.txt /srv/git/
RUN /srv/ve27/bin/pip install -r /srv/git/requirements.txt

COPY . /srv/git

ENTRYPOINT ["/srv/git/entry.sh"]

CMD ["/usr/local/bin/voltgrid.py", "/srv/ve27/bin/bureaucrat", "init", "--venv", "/srv/ve27", "--envfile", "/srv/env", "--app", "/srv/git", "--logpath", "-", "--no-create-pid"]
