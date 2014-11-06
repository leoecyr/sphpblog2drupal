sphpblog2drupal
===============

sphpblog2drupal is a python script which will read a content/ directory from an sphpblog install and extract all the posts from the directory structure and insert them into a drupal database as blog entries with the correct date and time. 
sphpblog2drupal is provided AS IS with no warranty.  Use it at your own risk.  It is distributed under the GNU GPL.

sphpblog2drupal is a python script which will read a content/ directory from an sphpblog install and extract all the posts from the directory structure and insert them into a drupal database as blog entries with the correct date and time. They will default to published in the drupal system. To enable drupal to serve as a drop in replacement for sphpblog you will also require a patch to your drupal's root index.php file. The patch to index.php is not necessary to successfully add the blog entries from a sphpblog site to a drupal site. The patch is only to allow drupal to continue serving the old sphpblog url's.  A patched index.php file is included for drupal 5.2 and 5.3.

Running the migration:
0) Test this script on a copy of your sphpblog and drupal sites before trusting it will not destroy your site.  Then backup all files and databases on the production site before running sphpblog2drupal.
1) Edit sphpblog2python.py.  At the top of the file are some settings you'll need to make.  Set the names for the source sphpblog directory, destination drupal database, user, and password.
2) run sphpblog2drupal.py on the command line.  It will prompt you to verify your source and destination.  If it all checks out type "Yes" to continue.  If you have around 500 or fewer entires on a modern machine with a low load it will take less than five seconds to complete.
(OPTIONAL)
3) If you want drupal to serve up your old sphpblog blog entries' URLs copy index.php to your drupal document root after backing up your old index.php.

This software is provided AS-IS by leo@raeleo.com.

