# TipsForLinux (tipsforlinux.com)

## What it does

TipsForLinux is a simple website that allow users send a tips about
linux, like a blog.
It has been created using django with django-tagging, django-socialauth,
django-contact-form, django-paggination and comments (native) apps.
Users can use openid authentication system provided by twitter, google
and yahoo, but is possible to use common authentication system too
(based in django.contrib.auth).
A Twitter integration allow to post the tip name and the tip
URL (converted in tinyurl) via admin interface.

## Installation

Download the sources and install the necessaries libs.

Libs included

* python-oauth2 (github.com/brosner/python-oauth2.git)
* python-twitter (python-twitter.googlecode.com/hg)

Libs you need to install:

* pyfacebook (github.com/sciyoshi/pyfacebook/)
* hashlib (pip install hashlib)
* python-openid (github.com/openid/python-openid)
* yadis (pypi.python.org/pypi/python-yadis)
* python-oauth (oauth.googlecode.com/svn/code/python)
* simplejson (pypi.python.org/pypi/simplejson)

You can install using pip:

    pip install -r requirements.txt

