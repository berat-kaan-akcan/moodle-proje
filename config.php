<?php
unset($CFG);
global $CFG;
$CFG = new stdClass();

$CFG->dbtype    = 'mariadb';
$CFG->dblibrary = 'native';
$CFG->dbhost    = getenv('DB_HOST') ?: 'db';
$CFG->dbname    = getenv('DB_NAME');
$CFG->dbuser    = getenv('DB_USER');
$CFG->dbpass    = getenv('DB_PASSWORD');
$CFG->prefix    = 'mdl_';
$CFG->dboptions = ['dbpersist' => 0, 'dbport' => 3306, 'dbcollation' => 'utf8mb4_unicode_ci'];

$CFG->wwwroot   = getenv('MOODLE_WWWROOT');
$CFG->dataroot  = '/var/www/moodledata';
$CFG->admin     = 'admin';
$CFG->directorypermissions = 0777;

// Geliştirme ayarları
$CFG->debug = (E_ALL | E_STRICT);
$CFG->debugdisplay = 1;

require_once(__DIR__ . '/lib/setup.php');
