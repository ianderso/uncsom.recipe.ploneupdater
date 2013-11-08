# -*- coding: utf-8 -*-
"""Recipe updateplone"""

import os


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

    def install(self):
        """Installer"""

        scripts = 'run-script' in self.options and \
            [p for p in self.options['run-script'].splitlines() if p] or []
        admin_name = 'admin-name' in self.options and \
                     self.options['admin-name'] or 'admin'
        bin_dir = self.buildout['buildout']['bin-directory']

        recipe_egg_path = os.path.dirname(__file__)[:-len(
            self.options['recipe'])].replace("\\", "/")
        template_file = os.path.join(os.path.dirname(__file__),
                                     'script.py_tmpl').replace("\\", "/")
        template = open(template_file, 'r').read()
        template = template % dict(scripts=scripts,
                                   admin_name=admin_name,
                                   recipe_egg_path=recipe_egg_path)

        open(bin_dir + 'ploneUpdater', 'w+').write(template)
        return tuple()

    def update(self):
        """Updater"""
        self.install()
