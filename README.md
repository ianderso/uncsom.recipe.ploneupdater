uncsom.recipe.ploneupdater
==========================
.. contents::

- Code repository: https://github.com/ianderso/uncsom.recipe.ploneupdater

Problem
===========

After executing your buildout to deploy your Plone project you have to start
the zope instance and then go on the ZMI to update the plone sites. This is
boring!


Solution
========

uncsom.recipe.ploneupdater is a buildout recipe that you can use to update
plone sites. It automatizes the following tasks:

 * Backup database
 * pack database
 * reinstall products with the quickinstaller
 * run GS profiles
 * run Plone migration (portal_migration.upgrade)
