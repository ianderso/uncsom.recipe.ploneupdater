import sys
import transaction

from Testing import makerequest
from Acquisition import aq_base
from AccessControl.SecurityManagement import newSecurityManager

_marker = object()
def shasattr(obj, attr):
    return getattr(aq_base(obj), attr, _marker) is not _marker

class PloneUpdater(object):
    """Plone sites updater
    """
    
    def __init__(self, 
                 app,             #The application instance
                 admin_name,      #The zope instance admin name
                 plone_sites,     #A list of plone site ids 
                 migrate_plone,   #Do we have to run portal_migration.upgrade 
                 p2install=[],    #A list of products to install
                 p2uninstall=[],  #A list of products to uninstall
                 scripts2run=[],  #A list of paths for scripts to run
                 profiles2run=[], #A list of GS profile ids to run
                 pack_db=True,    #If we have to pack the database
                ): 
        self.app = app
        self.admin_name = admin_name
        self.plone_sites = plone_sites
        self.migrate_plone = migrate_plone
        self.p2install = p2install
        self.p2uninstall = p2uninstall
        self.scripts2run = scripts2run
        self.profiles2run = profiles2run
        self.pack_db = pack_db
        
        self.invalid_plone_sites = []
        
    def log(self, msg):
        print >> sys.stdout, "*** collective.recipe.updateplone:", msg


    def authenticate(self):
        """wrap the request in admin security context
        """
        admin = self.app.acl_users.getUserById(self.admin_name)
        admin = admin.__of__(self.app.acl_users)
        newSecurityManager(None, admin)
        self.app = makerequest.makerequest(self.app)
    

    def add_sites(self):
        """try to create the plone sites if they are not already created.
        """
        for site_name in self.plone_sites:
            site = getattr(self.app, site_name, None)
            if site is not None:
                if site.Type() == 'Plone Site':
                    self.log("Skipped: Plone site already exists: " + site_name)
                else:
                    self.log("Cannot create plone site. An object with same id already exists: " + site_name)
                    self.invalid_plone_sites.append(site_name)
            else:
                self.log("Adding plone site: " + site_name)
                self.app.manage_addProduct['CMFPlone'].addPloneSite(site_name)
                self.log("Added plone site: " + site_name)


    def pack_database(self):
        if self.pack_db:
            self.log("Starting to pack Database...")
            self.app.Control_Panel.Database.manage_pack()
            self.log("Database packed...")
        else:
            self.log("Pack Database skipped...")


    def upgrade_plone(self, site):
        """run portal_migration.upgrade 
        """
        if not self.migrate_plone:
            return 
        portal = self.app[site]
        portal.REQUEST.set('REQUEST_METHOD', 'POST')
        portal.portal_migration.upgrade()


    def install_products(self, site):
        qi = self.app[site].portal_quickinstaller
        p2reinstall = [p for p in self.p2install if qi.isProductInstalled(p)]
        p2install = [p for p in self.p2install 
                       if qi.isProductAvailable(p) and p not in p2reinstall]
        _changed = False
        if p2install:
            self.log(site + "->Installing: " + str(p2install))
            qi.installProducts(p2install)
            self.log(site + "->Installed: " + str(p2install))
            _changed = True
        if p2reinstall:
            self.log(site + "->Reinstalling: " + str(p2reinstall))
            qi.reinstallProducts(p2reinstall)
            self.log(site + "->Reinstalled: " + str(p2reinstall))
            _changed = True
        if not _changed:
            self.log(site + "->Nothing to install or to reinstall")


    def uninstall_products(self, site):
        qi = self.app[site].portal_quickinstaller
        p2uninstall = [p for p in self.p2uninstall if qi.isProductInstalled(p)]
        if p2uninstall:
            self.log(site + "->Uninstalling: " + str(p2uninstall))
            qi.uninstallProducts(p2uninstall)
            self.log(site + "->Uninstalled: " + str(p2uninstall))
        else:
            self.log(site + "->Nothing to uninstall")


    #TODO: rewrite this method to make possible passing arguments to the script
    def run_scripts(self, site):
        portal = getattr(self.app, site)
        for script in self.scripts2run:
            if script.startswith('portal/'):
                #play safe  
                script = '/' + site + script[6:]

            self.log(site + "->Running script " + script)
            try:
                portal.restrictedTraverse(script)
                self.log(site + "->Ran script " + script)
            except Exception, e: 
                self.log(site + "->Exception accured wile running script: " + script)
                self.log(site + "-> " + str(e))
                continue                    


    def run_profiles(self, site):
        portal = getattr(self.app, site)
        setup_tool = getattr(portal, 'portal_setup')
        for profile_id in self.profiles2run:
            self.log(site + "->Running profile " + profile_id)
            try:
                if shasattr(setup_tool, 'runAllImportStepsFromProfile'):
                    if not profile_id.startswith('profile-'):
                        profile_id = "profile-%s" % profile_id
                    setup_tool.runAllImportStepsFromProfile(profile_id)
                else:
                    setup_tool.setImportContext(profile_id)
                    setup_tool.runAllImportSteps()
                self.log(site + "->Ran profile " + profile_id)
            except Exception, e:
                self.log(site + "->Exception while importing profile: " + profile_id)
                self.log(site + "-> " + str(e))

    #TODO: add a buildout option upgrade-profile to run profile migration steps
    def upgrade_profiles(self, site):
	    pass


    def __call__(self):
        self.authenticate()
        self.pack_database()
        self.add_sites()
        for site_name in self.plone_sites:
            if site_name not in self.invalid_plone_sites:
                self.upgrade_plone(site_name)
                self.uninstall_products(site_name)
                self.install_products(site_name)
                self.run_scripts(site_name)
                self.run_profiles(site_name)
                self.upgrade_profiles(site_name)

        transaction.commit()

