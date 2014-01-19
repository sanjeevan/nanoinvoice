#!/usr/bin/env python
import os

from flask.ext.script import Manager, prompt, prompt_pass, prompt_bool

from nano import create_app
from nano.extensions import db
from nano.models import *

manager = Manager(create_app())

from nano import create_app
app = create_app()
project_root_path = os.path.join(os.path.dirname(app.root_path))

@manager.command
def run():
    """Run local server."""
    app.run(debug=True, processes=2, host='0.0.0.0')

@manager.command
def reset():
    """Reset database."""

    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.command
def create_plans():
    """Create subscription plans"""
    plans = [
        Plan(name='Free', amount=0, description='Basic subscription'),
        Plan(name='Pro', amount=5.99, billing_interval='monthly', description='Pro subscription')
    ]

    for plan in plans:
        db.session.add(plan)

    db.session.commit()

@manager.command
def add_test_user():
    """Add a new test user"""
    user = User(username='sanjeevan', email_address='sanjeevan.a@gmail.com',
                first_name='Sanjeevan', last_name='Ambalavanar', 
                is_active=True, is_super_admin=True, password='fireworks')
    db.session.add(user)
    db.session.commit()


manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()
