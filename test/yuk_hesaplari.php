<?php
// Yük testi için sahte öğrenci hesapları (yuk01, yuk02, ...) oluşturur ya da denemeleriyle birlikte siler.
// Doğrudan değil, test/sinav_yuk_testi.py üzerinden çağrılır:
//   docker compose exec -T -u www-data moodle php -- olustur <adet> <cmid> <sifre> < test/yuk_hesaplari.php
//   docker compose exec -T -u www-data moodle php -- sil < test/yuk_hesaplari.php

define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->dirroot . '/user/lib.php');
require_once($CFG->dirroot . '/mod/quiz/locallib.php');

const YUK_EPOSTA = '@yuk-testi.invalid';

$islem = $argv[1] ?? '';

if ($islem === 'olustur') {
    $adet = (int)($argv[2] ?? 0);
    $cmid = (int)($argv[3] ?? 0);
    $sifre = $argv[4] ?? '';
    if ($adet < 1 || !$cmid || $sifre === '') {
        cli_error('Kullanım: olustur <adet> <cmid> <sifre>');
    }
    [$kurs, $cm] = get_course_and_cm_from_cmid($cmid, 'quiz');
    $kayit = $DB->get_record('enrol', ['courseid' => $kurs->id, 'enrol' => 'manual'], '*', MUST_EXIST);
    $ogrenci = $DB->get_field('role', 'id', ['shortname' => 'student'], MUST_EXIST);
    $manual = enrol_get_plugin('manual');

    for ($i = 1; $i <= $adet; $i++) {
        $ad = sprintf('yuk%02d', $i);
        $u = $DB->get_record('user', ['username' => $ad, 'deleted' => 0]);
        if ($u) {
            if (!str_ends_with($u->email, YUK_EPOSTA)) {
                cli_error("$ad adında gerçek bir hesap var; dokunulmadı.");
            }
            update_internal_user_password($u, $sifre);
        } else {
            $u = (object)[
                'username' => $ad, 'password' => $sifre, 'firstname' => 'Yük', 'lastname' => sprintf('Testi %02d', $i),
                'email' => $ad . YUK_EPOSTA, 'auth' => 'manual', 'confirmed' => 1,
                'mnethostid' => $CFG->mnet_localhost_id, 'lang' => $CFG->lang,
            ];
            $u->id = user_create_user($u, true, false);
        }
        $manual->enrol_user($kayit, $u->id, $ogrenci);
    }
    echo json_encode(['adet' => $adet, 'cmid' => $cmid, 'kurs' => $kurs->shortname, 'sinav' => $cm->name],
        JSON_UNESCAPED_UNICODE);
    exit(0);
}

if ($islem === 'sil') {
    $hesaplar = $DB->get_records_select('user', 'deleted = 0 AND ' . $DB->sql_like('email', '?'), ['%' . YUK_EPOSTA]);
    $deneme = 0;
    foreach ($hesaplar as $u) {
        foreach ($DB->get_records('quiz_attempts', ['userid' => $u->id]) as $a) {
            quiz_delete_attempt($a, $DB->get_record('quiz', ['id' => $a->quiz], '*', MUST_EXIST));
            $deneme++;
        }
        delete_user($u);
    }
    echo json_encode(['silinen_hesap' => count($hesaplar), 'silinen_deneme' => $deneme]);
    exit(0);
}

cli_error('Kullanım: olustur <adet> <cmid> <sifre> | sil');
