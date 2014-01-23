# Deploying Django to DreamHost

You have a site that works on your local machine, and you want to run it on
DreamHost. Here are the steps.

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

 6. It may take a few minutes for the SSH user to be created. Once it is,
    log in and add your SSH public key:

        $ mkdir -m 0700 .ssh
        $ (umask 0077 && cat > .ssh/authorized_keys)
        [paste ~/.ssh/id_rsa.pub from your dev machine]
        ^D

 7. Configure ssh to remember your username by adding lines like this to
    `~/.ssh/config`:

        Host newdomain.example.org
            User newuser

## Getting your site running on DreamHost

 1. Install Python. Download the [source tarball][python27]

        $ mkdir src && cd src
        $ wget 'http://www.python.org/ftp/python/2.7.6/Python-2.7.6.xz'
        $ tar xf Python-2.7.6.xz
        $ cd Python-2.7.6
        $ nice sh -c './configure --with-system-expat --prefix=$HOME/local \
            && make -j2 && make install'

 2. Add `$HOME/local/bin` to your path in `~/.bashrc` and/or
    `~/.bash_profile` as needed, then logout and log back in.

 3. Download setuptools to `~/src`, unpack it, and install it:
        $ curl -LO 'https://pypi.python.org/packages/source/s/setuptools/setuptools-2.1.tar.gz'
        $ tar xf setuptools-2.1.tar.gz
        $ cd setuptools-2.1
        $ python setup.py install

 4. Use `easy_install` to install `pip` and `mercurial`.

        $ easy_install pip mercurial

 5. Push your code to the server.

    On the server:

         $ mkdir ~/hg
         $ cd ~/hg
         $ hg init

    Then on your local machine, update `.hg/hgrc` with the new path:

         [paths]
         default-push = ssh://newdomain.example.org/hg

    and run `hg push`.

 6. Now run `./manage.py deploy` and you’re good to go!

 7. To add a superuser on the server, run

        ssh -t newhost.example.org newhost.example.org/code/manage.py createsuperuser

[python27]: http://www.python.org/ftp/python/2.7.6/Python-2.7.6.xz
[pip]: https://pypi.python.org/packages/source/p/pip/pip-1.5.1.tar.gz

## Deploying changes to DreamHost

Run `./manage.py deploy`. That’s it!

## Next steps

  - Use MySQL in production

  - Set up email

  - Pingdom

  - See the [Django Deploying Checklist][deployment-checklist] for other
    deployment steps.

  - See the [Web Operations][] for guidance on tuning your database,
    setting up logging, monitoring, and alerting.

[Web Operations]: http://www.amazon.ca/dp/1449377440
[deployment-checklist]: https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
