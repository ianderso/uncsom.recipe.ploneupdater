# -*- coding: utf-8 -*-
"""Recipe updateplone"""

import os
import time
import shutil
import tempfile
import sys

def quote_command(command):
    # Quote the program name, so it works even if it contains spaces
    command = " ".join(['"%s"' % x for x in command])
    if sys.platform[:3].lower() == 'win': 
        # odd, but true: the windows cmd processor can't handle more than 
        # one quoted item per string unless you add quotes around the 
        # whole line. 
        command = '"%s"' % command 
    return command


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

    def install(self):
        """Installer"""

        runonce = 'run-once' in self.options and \
                   self.options['run-once'].lower() or 'true'
        #We'll use the existance of this file as flag for the run-once option
        file_name = os.path.join(self.buildout['buildout']['directory'],
                                 'var', "%s.cfg" % self.name)

        if runonce not in ['false', 'off', 'no']:
            if os.path.exists(file_name):
                print "\n************************************************"
                print "Skipped: [%s] already ran" % self.name
                print "If you want to run it again set the run-once option"
                print "to false or delete %s" % file_name
                print "************************************************\n"
                return
            else:
                open(file_name, 'w').write('1')

        #Backup the Data.fs if asked to
        backup = 'backup-db' in self.options and \
                  self.options['backup-db'].lower() in ['true', 'on'] or False
        if backup:
            print os.sys.stdout, "Backup Data.fs..."
            data_fs = os.path.join(self.buildout['buildout']['directory'],
                                   'var', 'filestorage', 'Data.fs')
            data_fs_backup = "%s.%s" % (data_fs, time.strftime("%Y%m%d%H%M%S"))
            if os.path.exists(data_fs):
                shutil.copyfile(data_fs, data_fs_backup)
                print >>os.sys.stdout, "Backup Data.fs done..."
            else:
                print >>os.sys.stdout, "No Data.fs found. Backup skipped..."
        else:
            print >>os.sys.stdout, "Backup Data.fs skipped..."

        #get the instances and their plone sites
        plones = [p for p in self.options['plone-site'].splitlines() if p]
        instances = {}
        for plone in plones:
            instance_name, site_name = plone.split('.')
            if instance_name in instances:
                instances[instance_name].append(site_name)
            else:
                instances[instance_name] = [site_name]

        #get the options that will be used in the generated script
        migrate_plone = 'migrate-plone' in self.options and \
                  self.options['migrate-plone'].lower() in ['true', 'on', 'yes'] or False
        install = 'install' in self.options and \
                  [p for p in self.options['install'].splitlines() if p] or []
        uninstall = 'uninstall' in self.options and \
                    [p for p in self.options['uninstall'].splitlines() if p ] \
                    or []
        scripts = 'run-script' in self.options and \
                  [p for p in self.options['run-script'].splitlines() if p] \
                  or []
        profiles = 'run-profile' in self.options and \
                  [p for p in self.options['run-profile'].splitlines() if p] \
                  or []
        pack_db = 'pack-db' in self.options and \
                  self.options['pack-db'].lower() in ['true', 'on', 'yes'] or False
        admin_name = 'admin-name' in self.options and \
                     self.options['admin-name'] or 'admin'

        #genrate a script for each instance and run it with
        #a command like: ./bin/instance run script_name     
        for instance, sites in instances.items():
            #first, get the zeo script if we have a zeo setup
            zeo = ""
            if 'zeo-client' in self.buildout[instance] and \
                self.buildout[instance]['zeo-client'].lower() in ['true', 'on', 'yes']:
                for section_name in self.buildout:
                    if 'recipe' in self.buildout[section_name] and \
                       self.buildout[section_name]['recipe']=='plone.recipe.zope2zeoserver':
                       zeo = os.path.join(self.buildout['buildout']['bin-directory'], 
                                                       section_name)
            #second, get the instance script
            instance_ctl = os.path.join(
                                   self.buildout['buildout']['bin-directory'],
                                   instance)
            
            if sys.platform == 'win32':
                instance_ctl += '.exe'
                zeo += '.exe'
                service_exe = os.path.join(
                    self.buildout['buildout']['bin-directory'], 
                    'zeoservice.exe')
                if os.path.exists(service_exe):
                    zeo = service_exe

            if zeo and not os.path.exists(zeo):
                print "Skipped: %s not found" % zeo
                continue

            if not os.path.exists(instance_ctl):
                print "Skipped: %s not found" % instance_ctl
                continue

            #third, generate a temporary script
            recipe_egg_path = os.path.dirname(__file__)[:-len(self.options['recipe'])].replace("\\","/")
            template_file = os.path.join(os.path.dirname(__file__), 'script.py_tmpl').replace("\\","/")
            template = open(template_file, 'r').read()
            template = template % dict(sites = sites,
                                       pack_db = pack_db,
                                       migrate_plone = migrate_plone,
                                       install = install,
                                       uninstall = uninstall,
                                       scripts = scripts,
                                       profiles = profiles,
                                       admin_name = admin_name,
                                       recipe_egg_path = recipe_egg_path)

            tmp_file = tempfile.mktemp().replace("\\","/")
            open(tmp_file, 'w').write(template)
            
            #and now do the job
            #run the zeo server if we have a zeo setup
            if zeo:
                os.system(quote_command([zeo, "start"]))

            #run the script
            os.system(quote_command([instance_ctl, "run", tmp_file]))

            #stop the zeo server if we have a zeo setup
            if zeo:
                os.system(quote_command([zeo, "stop"]))
        
        return tuple()

    def update(self):
        """Updater"""
        self.install()

