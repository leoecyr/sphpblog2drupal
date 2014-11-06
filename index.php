<?php
// $Id: index.php,v 1.91 2006/12/12 09:32:18 unconed Exp $

/**
 * @file
 * The PHP page that serves all page requests on a Drupal installation.
 *
 * The routines here dispatch control to the appropriate handler, which then
 * prints the appropriate page.
 */

require_once './includes/bootstrap.inc';
drupal_bootstrap(DRUPAL_BOOTSTRAP_FULL);

$return = menu_execute_active_handler();

# begin sphpblog2drupal hack
$PARAM  = array_merge($_GET, $_POST);
$param_names = array_keys($PARAM);
$num_params = count($PARAM);
$entry=$PARAM['entry'];
if($entry != "")
{
        $result = pager_query(db_rewrite_sql("SELECT n.nid, n.created FROM {node} n, {node_revisions} nr WHERE nr.nid=n.nid AND nr.log = '$entry'"));
        while ($node = db_fetch_object($result))
        {$output .= node_view(node_load($node->nid));}
        print theme('page', $output);
        drupal_page_footer();
        exit();
}
# end sphpblog2drupal hack

// Menu status constants are integers; page content is a string.
if (is_int($return)) {
  switch ($return) {
    case MENU_NOT_FOUND:
      drupal_not_found();
      break;
    case MENU_ACCESS_DENIED:
      drupal_access_denied();
      break;
    case MENU_SITE_OFFLINE:
      drupal_site_offline();
      break;
  }
}
elseif (isset($return)) {
  // Print any value (including an empty string) except NULL or undefined:
  print theme('page', $return);

}

drupal_page_footer();
