set(
    project = 'django-de',
    fab_hosts = ['django-de.org'],
    fab_user = 'django-de',
    used_apps = 'django-comment-utils django-extensions django-mptt django-pagination django-registration django-tagging django-threadedcomments django-gravatar',
    app_dir = '~/lib/python2.4/site-packages',
    web_root = '~/public_html',
    log_dir = '~/logs',
)

def update():
    "Updates the django-de code from the Github repository."
    run("cd %(app_dir)s/%(project)s; git pull; git gc;")

def app_status():
    "Looks at the git status of the used Django apps."
    run("for app in %(used_apps)s; do cd %(app_dir)s/\$app && git status; done")

def upgrade():
    "Upgrades all used Django apps."
    run("for app in %(used_apps)s; do cd %(app_dir)s/\$app && git pull && git gc; done")

def restart():
    "Restarts the Django proccess."
    run("touch %(web_root)s/%(project)s.wsgi")

def error_log():
    "Tail the servers error logfile."
    run('tail -f %(log_dir)s/error_log')

def access_log():
    "Tail the servers access logfile."
    run('tail -f %(log_dir)s/access_log')
