
Supported options
=================

The recipe supports the following options:

plone-site
    A list of plone site to update or to create if they do not exist.
    Each item of the list consist of the zope instance name that contains 
    (will contain) the plone site, a dot and the name of the plone site. 
    ex: ``instance1.site1``

migrate-plone
    If true, the recipe will upgrade your plone site by running 
    portal_migration.upgrade(). This is only useful if you are migrating to
    a new version of plone. This option defaults to false.

uninstall
    A list of packages/products to uninstall with the quickinstaller if they
    are already installed

install
    A list of packages/products to install with the quickinstaller or to
    reinstall if they are already installed.

run-script
    A list of scripts to call/run. Each item of the list consist of a path to
    the script to run. The path has to start with ``portal/``. 
    ex: portal/migrate_all

run-profile
    A list of GS profile Ids to be run. Each id has to be given as it accepted
    by setup tool. ie: profile-ProductName:default

backup-db
    If true, the recipe will backup Data.fs before processing. Defaults to false.

pack-db
    If true, the recipe will pack Data.fs before processing. Defaults to false

admin-name
    The name of the zope instance admin. The same as defined in the ``user``
    option of your zope instance. Defaults to 'admin'

run-once
    If true the recipe will only run once. If you run the buildout many times
    the recipe will only run the first time. It does this by writing a file to
    the var directory. If you want to run the recipe again you have to delete
    the file from the var directory or set this option to false. The file name
    is the same as the section name with cfg extension. This option Defaults 
    to True.

Example usage
=============

We'll start by creating a buildout that uses the recipe. Let's create
a freash zope instance and create 2 plone sites inside it. We will also 
install RichDocument and NuPlone into these sites::

    >>> write(sample_buildout, 'buildout.cfg', """
    ... [buildout]
    ... parts = 
    ...     zope2
    ...     instance1
    ...     plone
    ...     update-plone
    ... index = http://pypi.python.org/simple
    ... find-links =
    ...     http://download.zope.org/distribution/
    ...     http://effbot.org/downloads
    ... eggs =
    ...     elementtree
    ...     PILwoTK
    ... 
    ... [zope2]
    ... recipe = plone.recipe.zope2install 
    ... url = ${plone:zope2-url}
    ... 
    ... [plone]
    ... recipe = plone.recipe.plone
    ... 
    ... [instance1]
    ... recipe = plone.recipe.zope2instance
    ... zope2-location = ${zope2:location}
    ... user = admin:admin
    ... deprecation-warnings = false
    ... eggs = 
    ...     ${buildout:eggs}
    ...     ${plone:eggs}
    ...     Products.RichDocument
    ... zcml =
    ...     Products.RichDocument
    ... products =
    ...     ${plone:products} 
    ... 
    ... [update-plone]
    ... recipe = collective.recipe.updateplone
    ... backup-db = true
    ... pack-db = true
    ... plone-site = 
    ...     instance1.site1
    ...     instance1.site2
    ... install =
    ...     Marshall
    ... uninstall =
    ... run-profile =
    ...     profile-Products.RichDocument:default
    ...     profile-Products.NuPlone:nuplone
    ... run-script =
    ... """)

Running the buildout gives us::

    >>> print system(buildout) # doctest:+ELLIPSIS
    Getting distribution for 'plone.recipe.plone'.
    ...
    Installing update-plone.
    *** collective.recipe.updateplone: Starting to pack Database...
    *** collective.recipe.updateplone: Database packed...
    *** collective.recipe.updateplone: Adding plone site: site1
    *** collective.recipe.updateplone: Added plone site: site1
    *** collective.recipe.updateplone: Adding plone site: site2
    *** collective.recipe.updateplone: Added plone site: site2
    *** collective.recipe.updateplone: site1->Nothing to uninstall
    *** collective.recipe.updateplone: site1->Installing: ['Marshall']
    *** collective.recipe.updateplone: site1->Installed: ['Marshall']
    *** collective.recipe.updateplone: site1->Running profile profile-Products.RichDocument:default
    *** collective.recipe.updateplone: site1->Ran profile profile-Products.RichDocument:default
    *** collective.recipe.updateplone: site1->Running profile profile-Products.NuPlone:nuplone
    *** collective.recipe.updateplone: site1->Ran profile profile-Products.NuPlone:nuplone
    *** collective.recipe.updateplone: site2->Nothing to uninstall
    *** collective.recipe.updateplone: site2->Installing: ['Marshall']
    *** collective.recipe.updateplone: site2->Installed: ['Marshall']
    *** collective.recipe.updateplone: site2->Running profile profile-Products.RichDocument:default
    *** collective.recipe.updateplone: site2->Ran profile profile-Products.RichDocument:default
    *** collective.recipe.updateplone: site2->Running profile profile-Products.NuPlone:nuplone
    *** collective.recipe.updateplone: site2->Ran profile profile-Products.NuPlone:nuplone
    ...
    <BLANKLINE>




