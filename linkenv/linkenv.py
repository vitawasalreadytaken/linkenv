#!/usr/bin/env python

from __future__ import print_function
import os, shutil, sys



def findPackages(root):
	packages = set()
	for (dir, dirs, filenames) in os.walk(root):
		for filename in filter(lambda x: x == 'top_level.txt', filenames):
			path = os.path.join(dir, filename)
			with open(path) as f:
				for package in f:
					package = package.strip()
					for name in (package, package + '.py'):
						if os.path.exists(os.path.join(root, name)):
							print('Found {} in {}.'.format(name, path))
							packages.add(name)

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
	if '--copy' in argv:
		copy = True
		argv.remove('--copy')
	else:
		copy = False

	if len(argv) != 3:
		print('Usage: {} [--copy] path/to/site-packages/ path/to/target/dir/'.format(argv[0]))
		print('\nWill look for packages in your `site-packages\' directory and symlink (or copy if the --copy flag is present) them to the target directory.')
		return

	sitePackages = argv[1]
	target = argv[2]

	if not os.path.exists(sitePackages):
		print('Error: source directory `{}\' does not exist!'.format(sitePackages))
		return

	packages = findPackages(sitePackages)
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
