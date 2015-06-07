#!/usr/bin/env python

from __future__ import print_function
import os, shutil, sys
from optparse import OptionParser



def findPackages(root,ignores):
	packages = set()
	for (dir, dirs, filenames) in os.walk(root):
		for filename in filter(lambda x: x == 'top_level.txt', filenames):
			path = os.path.join(dir, filename)
			with open(path) as f:
				for package in f:
					package = package.strip()
					for name in (package, package + '.py'):
						if os.path.exists(os.path.join(root, name)):
							if name in ignores:
								print('Ignore {} in {}.'.format(name, path))
							else:
								print('Found {} in {}.'.format(name, path))
								packages.add(name)

	return packages


def ignorePackages(file):
	packages = []
	if file is None: return packages
	with open(file) as f:
		for package in f:
			packages.append(package.strip().split(' ')[0])

	return packages
	 

def dropSubpackages(packages):
	'''
	Quick and dirty way to drop subpackages and only link their parent packages/directories.
	'''
	copy = set(packages)
	for package in packages:
		drop = set()
		for p in copy:
			if (p != package) and (p.startswith(package + '/') or p.startswith(package + '\\')):
				print('Dropping subpackage {} in favor of {}.'.format(p, package))
				drop.add(p)
		copy.difference_update(drop)
	return copy



def link(sourceDir, targetDir, name, copy):
	source = os.path.join(sourceDir, name)
	target = os.path.join(targetDir, name)
	# Redefine targetDir to include any subdir paths that may have been present in target.
	targetDir = os.path.dirname(target)

	if os.path.exists(target):
		print('[!] Skipping {} (target already exists).'.format(target))
	else:
		if not os.path.exists(targetDir):
			print('[!] Creating parent directory {}'.format(targetDir))
			os.makedirs(targetDir)

		if copy:
			print('{} -> {}'.format(target, source))
			(shutil.copytree if os.path.isdir(source) else shutil.copyfile)(source, target)
		else:
			relSource = os.path.relpath(source, targetDir)
			print('{} -> {}'.format(target, relSource))
			os.symlink(relSource, target)



def main(argv = sys.argv):

	parser = OptionParser(
		usage='usage: %prog [options] [path/to/site-packages/] path/to/target/dir',
		description='Will look for packages in your `site-packages\' ' +
								'directory and symlink (or copy if the --copy flag is ' +
								'present) them to the target directory. The ' +
								'`site-packages\' directory will be auto-discovered ' +
								'if not provided.'
	)
	parser.add_option('-c', '--copy', dest='copy', action='store_true', default=False,
										help='Copy packages instead of symlinking'
									 )
	parser.add_option('-i', '--ignore-file', dest='ignorefile', action='store', metavar='FILE',
										help='FILE that lists packages to ignore'
									 )
	(options, args) = parser.parse_args()

	copy = options.copy
	ignorefile = options.ignorefile

	if len(args) == 1:
		packageDirs = [ p for p in sys.path
			if p.startswith(os.environ['VIRTUAL_ENV'])
			and p.endswith('site-packages') ]
		if len(packageDirs) != 1:
			parser.error('ambiguous source directories, must specify explicitly')
			return
		sitePackages = packageDirs[0]
	elif len(args) == 2:
		sitePackages = args[0]
	else:
		parser.error('source and target directories must be specified')
		return

	target = args[-1]

	if not os.path.exists(sitePackages):
		print('Error: source directory `{}\' does not exist!'.format(sitePackages))
		return

	packages = findPackages(sitePackages, ignorePackages(ignorefile))
	packages = dropSubpackages(packages)
	print('{} packages: {}'.format('Copying' if copy else 'Linking', ', '.join(packages)))

	for package in packages:
		link(sitePackages, target, package, copy)

	statement = \
		'import os, sys\n' + \
		'sys.path.insert(0, os.path.join(os.path.dirname(__file__), \'{}\'))'.format(target.strip('/\\'))
	print('\nAdd the following to your appengine_config.py:\n')
	print(statement, '\n\n')


if __name__ == '__main__':
	main()
