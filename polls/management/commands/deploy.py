import os.path
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args, **options):
        if args:
            raise CommandError('no options supported')

        subprocess.call(['hg', 'push', '--new-branch', '-b', 'default'])
        ssh = subprocess.Popen(['ssh', settings.DOMAIN], stdin=subprocess.PIPE)
        ssh.communicate("""\
DOMAIN=%s
set -eu
set -o pipefail
shopt -s dotglob
if ! [ -e ~/$DOMAIN/code ]; then
    ln -s ~/hg ~/$DOMAIN/code
fi
cd ~/$DOMAIN/code
hg update
pip install -qr requirements.txt
cd ..
rm -f passenger_wsgi.py
cp code/wsgi.py passenger_wsgi.py
code/manage.py syncdb --noinput
rm -rf public
mkdir public
for F in code/public/*; do ln -nfs "../${F}" "${F#code/}"; done
code/manage.py collectstatic -l --noinput | tail -n1
mkdir -p tmp
touch tmp/restart.txt
""" % settings.DOMAIN)

