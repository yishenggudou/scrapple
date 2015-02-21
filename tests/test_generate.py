from nose.tools import assert_is_instance, assert_in
from docopt import docopt
import os

from scrapple import cmd
from scrapple.commands import generate

doc = cmd.__doc__


import sys
from contextlib import contextmanager
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


@contextmanager
def output():
	new_out = StringIO()
	old_out = sys.stdout
	try:
		sys.stdout = new_out
		yield sys.stdout
	finally:
		sys.stdout = old_out


def test_if_generate_instance_created():
	args = docopt(doc, "generate project1 test_project")
	gc = generate.GenerateCommand(args)
	assert_is_instance(gc, generate.GenerateCommand)


def test_xpath_scraper_generate():
	args = docopt(doc, "generate project1 project")
	gc = generate.GenerateCommand(args)
	gc.execute_command()
	with open(os.path.join(os.getcwd(), 'project.py'), 'r') as f:
		program = f.read()
	assert_in("from scrapple.selectors.xpath import XpathSelector", program)
	assert_in('page0 = XpathSelector("http://www.google.com")', program)


def test_css_scraper_generate():
	args = docopt(doc, "generate project2 project2")
	gc = generate.GenerateCommand(args)
	gc.execute_command()
	with open(os.path.join(os.getcwd(), 'project2.py'), 'r') as f:
		program = f.read()
	assert_in("from scrapple.selectors.css import CssSelector", program)
	assert_in('page0 = CssSelector("http://www.google.com")', program)


def test_nonexistent_project():
	args = docopt(doc, "generate project_unknown project2")
	gc = generate.GenerateCommand(args)
	with output() as out:
		gc.execute_command()
	alert = out.getvalue().strip()
	expected_alert = "project_unknown.json does not exist. Use ``scrapple genconfig``."
	assert_in(expected_alert, alert)
