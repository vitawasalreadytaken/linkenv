link-env
========

App Engine SDK doesn't play nice with Python virtual environments but there is a way to work around it. When you deploy an app to GAE the deploy script will resolve any symbolic links inside your project directory and upload their actual targets. This script will create those links for all packages you have installed in your virtualenv.

Read more at http://ze.phyr.us/appengine-virtualenv/

## Instalation

	pip install git+https://github.com/ze-phyr-us/linkenv.git

## Usage

To create package symlinks in directory `gaenv` (for example), go to the root of your project and run

	linkenv env/lib/python2.7/site-packages gaenv

The first argument indicates where your virtualenv packages are installed. After the script finishes you need to make sure that `gaenv` is in your import path. One easy way is to add these lines to your `appengine_config.py`:

	import os, sys
	sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'gaenv'))

After this you will be able to use the virtualenv in your local environment, as well as deploy the packages to production servers.


## TODO

  - Follow paths in `.egg-link` files as well.
