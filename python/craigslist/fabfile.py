from fabric.api import local, task, settings
from termcolor import colored
from app import app
@task
def build():
    print colored('Building Stuff', 'blue')

@task(default=True)
def run():
  app.run()
