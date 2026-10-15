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
// Özel giriş sayfası; DB'deki sabit localhost adresi yerine wwwroot'u takip etsin
$CFG->alternateloginurl = $CFG->wwwroot . '/login/index_auth.php';
// Girişten sonra kontrol paneli (/my) yerine site ana sayfası açılsın (0 = HOMEPAGE_SITE)
$CFG->defaulthomepage = 0;

// Sınav ayarı: hata ayıklama kapalı (geliştirirken açmak için: debug = E_ALL, debugdisplay = 1)
$CFG->debug = 0;
$CFG->debugdisplay = 0;

require_once(__DIR__ . '/lib/setup.php');
