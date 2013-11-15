uncsom.recipe.ploneupdater
==========================

Upgrade all of your Plone sites quickly!

- Code repository: https://github.com/ianderso/uncsom.recipe.ploneupdater


Solution
========

uncsom.recipe.ploneupdater is a buildout recipe that you can use to update
plone sites. It automatizes the following tasks:

 * pack database
 * reinstall products with the quickinstaller or GenericSetup Upgrade Steps
 * run Plone migration (portal_migration.upgrade)
 * clean up invalid GS steps
