#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from app import creat_app, db
from app.models import SetPoint, NewData, FaultList, aftercheck_list, Diagnosis
from flask_script import Manager, Shell

app = creat_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, SetPoint=SetPoint,
                NewData=NewData, FaultList=FaultList,
                aftercheck_list=aftercheck_list, Diagnosis=Diagnosis)


manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
