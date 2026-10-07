<?php
define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->libdir.'/questionlib.php');
require_once($CFG->dirroot.'/question/format.php');
require_once($CFG->dirroot.'/question/format/xml/format.php');
$file = $argv[1]; $courseid = (int)$argv[2];
\core\session\manager::set_user(get_admin());
$course = get_course($courseid);
$context = context_course::instance($courseid);
$cat = question_get_default_category($context->id, true);
$f = new qformat_xml();
$f->setCategory($cat); $f->setContexts([$context]); $f->setCourse($course);
$f->setFilename($file); $f->setRealfilename(basename($file));
$f->setMatchgrades('error'); $f->setCatfromfile(1); $f->setContextfromfile(0); $f->setStoponerror(1);
if (!$f->importpreprocess()) die("pre fail\n");
if (!$f->importprocess()) die("process fail\n");
if (!$f->importpostprocess()) die("post fail\n");
echo "OK $file\n";
