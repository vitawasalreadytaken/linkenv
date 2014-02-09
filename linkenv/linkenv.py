#!/usr/bin/env python

from __future__ import print_function
import os, sys



def findPackages(root):
	packages = []
	for (dir, dirs, filenames) in os.walk(root):
		for filename in filter(lambda x: x == 'top_level.txt', filenames):
			path = os.path.join(dir, filename)
			with open(path) as f:
				for package in f:
					package = package.strip()
					for name in (package, package + '.py'):
						if os.path.exists(os.path.join(root, name)):
							print('Found {} in {}.'.format(name, path))
							packages.append(name)

	return packages


def link(sourceDir, targetDir, name):
	source = os.path.join(sourceDir, name)
	target = os.path.join(targetDir, name)
	if os.path.exists(target):
		print('[!] Skipping {} (link already exists).'.format(target))
	else:
		relSource = os.path.relpath(source, targetDir)
		print('{} -> {}'.format(target, relSource))
		os.symlink(relSource, target)



def main():
	sitePackages = sys.argv[1]
	target = sys.argv[2]

	packages = findPackages(sitePackages)
	print('Linking packages:', ', '.join(packages))

	for package in packages:
		link(sitePackages, target, package)

	statement = \
		'import os, sys\n' + \
		'sys.path.insert(0, os.path.join(os.path.dirname(__file__), \'{}\'))'.format(target)

	print('Add the following to your appengine_config.py:\n')
	print(statement, '\n\n')


if __name__ == '__main__':
	main()
