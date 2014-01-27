# Deploying Django to DreamHost

## Presented at [PyYYC][], 2014-01-22

You have a Django site that works on your local machine, and you want to
run it on the public internet cheaply with a one-line command to
immediately push your local changes to the live site.

Here are the steps used to get the tutorial `polls` Django app in [this
mercurial repository][repo-home] running on a real web server.

[repo-home]: https://bitbucket.org/andrewdotn/deploy_polls

## Feedback and questions are welcome

If you use this and like it, have trouble getting it working, or have
questions about doing more stuff with it, drop me a note! My email is
andrew@neitsch.ca.

## Introduction

[PyYYC]: http://www.meetup.com/py-yyc/

Everyone who works with Django has worked their way through the [Django
tutorial][tutorial], building the `polls` app and running it on their local
machine. It’s fun and easy to go from there to building little Django apps
for your own use. But there’s a huge jump to go from running Django sites
on your local machine to running them on the web. Instead of a simple
`manage.py` command, you need to [configure apache modules][wsgi] and stuff
like that, which requires a publicly-accessible webserver that’s properly
configured, secured, and monitored, which can be a lot of work and expense
for a toy site.

[tutorial]: https://docs.djangoproject.com/en/stable/intro/tutorial01/
[wsgi]: https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/modwsgi/

In the old days when people wrote static web sites, deployment was easy:
you’d pay a few dollars a month for a shared web host and rsync your files
over. The host would monitor and secure the server, and if the site had
problems, you’d email support and they’d fix it for you.

It turns out you can still do that with Django: [DreamHost][] is one of the
most popular shared web hosts, and you can run as many Django sites as you
want on it using their standard hosting plan which costs $5.95–$8.95/month
depending on how many months in advance you prepay. For that you get
unlimited domains, unlimited databases, and unlimited bandwidth, full SSH
access to the server, and support when things break.

[DreamHost]: http://www.dreamhost.com/web-hosting/

This is the basic setup I’ve used for about half a dozen Django projects.
It’s allowed me to continuously deploy changes with a minimum of fuss, and
with it you can write a new app and get it running on the web in minutes,
with push-button update ability.

## Preliminary steps

First you need the resources to deploy your site to: a domain, an SSH user,
and a database.

 1. Log into the DreamHost panel.

 2. Under Domains → Manage Domains, click Add New Domain / Sub-Domain

 3. Enter the domain name, select “Create a New User” and enter a username,
    and check off the “Passenger (Ruby/Python apps only)” option. Then
    click “Fully host this domain.”

 4. Under Users → Manage Users, edit the user you just created and change
    the User Type to a Shell User. Disallow FTP while you’re in there.

 5. Under Goodies → MySQL Databases, create a new database. Pick your own
    username and password.

 6. It may take a few minutes for SSH to be enabled for the new user. Once
    it is, log in and add your SSH public key:

        $ mkdir -m 0700 .ssh
        $ (umask 0077 && cat > .ssh/authorized_keys)
        [paste ~/.ssh/id_rsa.pub from your dev machine]
        ^D

 7. Configure ssh to remember your username by adding lines like this to
    `~/.ssh/config`:

        Host newdomain.example.org
            User newuser

 8. Update the `DOMAIN` in `settings.py` to point to this new domain.

## Getting your site running on DreamHost

You’ll need to do some initial setup on the server, and then push your code
to the server.

These steps work with the code in this repository. You can fork this repo,
deploy it yourself, then pull out the `polls` app and add your own. Or, you
can look at the commit history of this repo to see the relatively few
things that were done to `polls` to make it deployable.

 1. Download the Python [source tarball][python27], unpack it, and install
    it. DreamHost servers have Python already but this gets the latest
    version and makes it easier to install additional packages.

        $ mkdir src && cd src
        $ wget 'http://www.python.org/ftp/python/2.7.6/Python-2.7.6.xz'
        $ tar xf Python-2.7.6.xz
        $ cd Python-2.7.6
        $ nice sh -c './configure --with-system-expat --prefix=$HOME/local \
            && make -j2 && make install'

 2. Add `$HOME/local/bin` to your path in `~/.bashrc` and/or
    `~/.bash_profile` as needed, then logout and log back in.

 3. Download setuptools to `~/src`, unpack it, and install it:

        $ cd ~/src
        $ curl -LO 'https://pypi.python.org/packages/source/s/setuptools/setuptools-2.1.tar.gz'
        $ tar xf setuptools-2.1.tar.gz
        $ cd setuptools-2.1
        $ python setup.py install

 4. Use `easy_install` to install `pip` and `mercurial`.

        $ easy_install pip mercurial

 5. Set up the mysql configuration file:

        (umask 0077 && echo '[client]
        password="password"
        host="mysql.example.org"
        user="username"
        database="database_name"' > ~/.my.cnf)

 6. Push your code to the server.

    On the server:

         $ mkdir ~/hg
         $ cd ~/hg
         $ hg init

    Then on your local machine, update `.hg/hgrc` with the new path:

         [paths]
         default-push = ssh://newdomain.example.org/hg

    and run `hg push`.

 7. Now run `./manage.py deploy` on your local machine and you’re good to
    go!

 8. To add a superuser on the server, run

        ssh -t newhost.example.org newhost.example.org/code/manage.py createsuperuser

[python27]: http://www.python.org/ftp/python/2.7.6/Python-2.7.6.xz
[pip]: https://pypi.python.org/packages/source/p/pip/pip-1.5.1.tar.gz

## Deploying changes to DreamHost

Run `./manage.py deploy`. That’s it!

## Demo

Andrew logs in to the DreamHost web panel, creates a new subdomain, updates
`DOMAIN` in `settings.py`, waits for DNS to propagate, runs `deploy`, and
immediately gets a deployed website. “Hello world” is added to a page,
`deploy` is run, and the live site picks up the new text.

The actual presentation did not go quite this smoothly, and I sort of
blamed DreamHost, but it was really my forgetting to configure
[`ALLOWED_HOSTS`][ALLOWED_HOSTS] properly.

[ALLOWED_HOSTS]: https://www.djangoproject.com/weblog/2013/feb/19/security/

## Questions

  - How scalable is this?

    One website I helped set up with this was once linked to by a very
    popular blog and started getting around 15 requests/s at which point it
    basically fell over. My friend tweaked some things like caching and
    moving some things to be served statically instead of dynamically, and
    subsequent testing showed that it would be able to stand 30 requests/s.

    I think we were using a DreamHost VPS at that point though—if your
    site is using tons of CPU or you want better performance, you can move
    it from the shared hosting environment at DreamHost to a VPS that you
    get root access on for around $50/month extra.

  - My site uses a third-party library like `markdown`. How do I deploy
    that?

    Just add it to `requirements.txt`, commit, and run `manage.py deploy`.
    The deploy script automatically installs everything in there.

  - What about database migrations?

    Add [South][] to `requirements.txt`, and update the `deploy` management
    command to pass `--migrate` to `syncdb`, or wait for [Django 1.7][].

[South]: http://south.aeracode.org
[Django 1.7]: https://www.kickstarter.com/projects/andrewgodwin/schema-migrations-for-django

## Next steps

  - [Pingdom][] is an awesome web service that checks your website every
    minute to make sure it’s up and displaying the right stuff. It has two
    great functions with DreamHost: it alerts you to check your code and/or
    contact DreamHost support if there’s ever a problem with your site, and
    since it visits your site every minute, the Django processes on the
    server never time out and you don’t get a delayed load when someone
    first visits your low-traffic site.

[Pingdom]: https://www.pingdom.com

  - See the [Django Deploying Checklist][deployment-checklist] for other
    Django-specific deployment steps.

  - See the [Web Operations][] textbook for guidance on keeping your site
    running smoothly and professionally, setting up logging, monitoring,
    and alerting, tuning your database, and much more.

  - See [Continuous Delivery][] for how to build more advanced
    high-availability deployment pipelines.

[Web Operations]: http://www.amazon.ca/dp/1449377440
[Continuous Delivery]: http://www.amazon.ca/dp/0321601912
[deployment-checklist]: https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

## Future work

If anyone’s interested, or if I need the functionality myself, here are
some ways that this could be extended:

  - This setup doesn’t let your site send email, but DreamHost absolutely
    allows you to send email. These instructions could be updated to
    include how to set that up.

 - Automating database and log file backups. This is made easier by the
   fact that DreamHost unix users can install crontabs.

 - The deployment command could take a revision argument to support
   rollbacks.

 - Instead of requiring people to add deployment stuff to individual sites,
   the `deploy` command and the stuff it needs could be packaged as its own
   [PyPI][] module. Instead of forking this module or reproducing the steps
   in the commit history, making a project deployment could be as simple as
   adding a module to `requirements.txt` and `INSTALLED_APPS`.

[PyPI]: http://cheeseshop.python.org

 - DreamHost actually offers an [API][] that lets you create and edit
   domains, users, databases, and email addresses. All the steps in this
   document could be totally automated and packaged in a module. That way,
   you could just add a new deployment app to the project, and run
   something like `./manage.py --deploy --initial newsubdomain.example.org`
   to have everything automatically set up for you.

[API]: http://wiki.dreamhost.com/Application_programming_interface

It would be really cool if this grew into something that could automate
initial and continuous deployment of Django apps to different web hosts!
