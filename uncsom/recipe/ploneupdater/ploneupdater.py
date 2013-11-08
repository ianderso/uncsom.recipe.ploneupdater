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

    def __init__(self, admin_name, scripts2run=[]):
        self.admin_name = admin_name
        self.scripts2run = scripts2run
        self.invalid_plone_sites = []

    def log(self, msg):
        print >> sys.stdout, "*** uncsom.recipe.ploneupdater:", msg

    def authenticate(self):
        """wrap the request in admin security context
        """
        admin = self.app.acl_users.getUserById(self.admin_name)
        admin = admin.__of__(self.app.acl_users)
        newSecurityManager(None, admin)
        self.app = makerequest.makerequest(self.app)

    def pack_database(self):
        self.log("Starting to pack Database...")
        self.app.Control_Panel.Database.manage_pack()
        self.log("Database packed...")
        transaction.commit()

    def upgrade_plone(self, site):
        self.log("Beginning Plone Upgrade")
        portal = self.app[site]
        portal.REQUEST.set('REQUEST_METHOD', 'POST')
        portal.portal_migration.upgrade()
        self.log("Finished Plone Upgrade")
        transaction.commit()

   def reinstall_outdated_products(self, site):
        qi = self.app[site].portal_quickinstaller
        update = [p for p in qi.listInstalledProducts() if
                  p['installedVersion'] != qi.getProductVersion(p['id'])]
        self.log(site + "->Reinstalling: " + str(update))
        qi.reinstallProducts(update)
        self.log(site + "->Reinstalled: " + str(update))
        transaction.commit()

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
                self.log(site + "->Exception accured wile running script: "
                         + script)
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
                self.log(site + "->Exception while importing profile: "
                         + profile_id)
                self.log(site + "-> " + str(e))

    def upgrade_profiles(self, site):
        pass

    def get_plone_sites(self, app):
        pass

    def __call__(self):
        self.authenticate()
        self.pack_database()
        plone_sites = self.get_plone_sites()
        for site in plone_sites:
            self.upgrade_plone(site)
            self.upgrade_profiles(site_name)
            self.reinstall_outdated_products(site)
            self.run_scripts(site)
        transaction.commit()
