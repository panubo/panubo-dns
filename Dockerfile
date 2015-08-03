FROM panubo/python-bureaucrat

COPY . /srv/git

ENTRYPOINT ["/srv/git/entry.sh"]