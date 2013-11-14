Supported options
=================

The recipe supports the following options:

run-script
    A list of scripts to call/run. Each item of the list consist of a path to
    the script to run. The path has to start with ``portal/``.
    ex: portal/migrate_all

admin-name
    The name of the zope instance admin. The same as defined in the ``user``
    option of your zope instance. Defaults to 'admin'


Example usage
=============

We'll start by creating a buildout that uses the recipe. Let's create
a freash zope instance and create 2 plone sites inside it. We will also
install RichDocument and NuPlone into these sites::

    >>> write(sample_buildout, 'buildout.cfg', """
    ... [buildout]
    ... parts =
    ...     instance1
    ...     update-plone
    ... index = http://pypi.python.org/simple
    ... find-links =
    ...     http://download.zope.org/distribution/
    ...     http://effbot.org/downloads
    ... eggs =
    ...     Plone
    ...     Pillow
    ...
    ... [instance1]
    ... recipe = plone.recipe.zope2instance
    ... user = admin:admin
    ... eggs = ${buildout:eggs}
    ...
    ... [update-plone]
    ... recipe = collective.recipe.updateplone
    ... """)
