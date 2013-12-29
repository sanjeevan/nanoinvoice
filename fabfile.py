from fabric.api import *
from fabric.colors import green, red
from fabric.contrib.project import rsync_project

env.use_ssh_config = True

# git repo
GIT_REPO = "git@github.com:sanjeevan/nanoinvoice.com.git"
GIT_BRANCH = "master"
PROJ_FOLDER = "/var/www/nanoinvoice.com"

RSYNC_EXCLUDE = (
    '*.DS_Store',
    '.hg',
    '*.pyc',
    '*.w2p',
    '*.log',
    '*.master',
    'fabfile.py',
    '.git/*'
)

def git_clone(branch="master"):
    """Clone the git repo"""
    with lcd("dist"):
        local("git clone %s" % GIT_REPO)
        local("git checkout %s" % branch)
    print(green("Cloned git repo"))

def git_cleanup():
    """Removed checked out git project"""
    local("rm -Rf dist/nanoinvoice.com")
    print(green("Cleaned up git files"))

def upload_project():
    rsync_project(PROJ_FOLDER, "dist/nanoinvoice.com/", exclude=RSYNC_EXCLUDE, ssh_opts="-p4200")
    print(green("Project synced to server"))

def live():
    env.user = "sanjeevan"
    env.hosts = ["linode2"] # in .ssh/config 
    env.nick = "live"

def build():
    git_clone()
    upload_project()
    git_cleanup()
