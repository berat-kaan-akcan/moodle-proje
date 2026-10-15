<?php
// Üst gezinme çubuğundaki site adı yerine üniversite logosunu (küçük logo) ayarlar.
// Kullanım: docker compose exec -T moodle php < scripts/logo_ayarla.php

define('CLI_SCRIPT', true);
require('/var/www/html/config.php');

$kaynak = $CFG->dirroot . '/login/favicon.png';
if (!is_readable($kaynak)) {
    cli_error("Logo dosyası bulunamadı: $kaynak");
}

$fs = get_file_storage();
$context = context_system::instance();
$fs->delete_area_files($context->id, 'core_admin', 'logocompact');
$fs->create_file_from_pathname([
    'contextid' => $context->id,
    'component' => 'core_admin',
    'filearea'  => 'logocompact',
    'itemid'    => 0,
    'filepath'  => '/',
    'filename'  => 'msku-logo.png',
], $kaynak);

set_config('logocompact', '/msku-logo.png', 'core_admin');
theme_reset_all_caches();

echo "Küçük logo ayarlandı.\n";
