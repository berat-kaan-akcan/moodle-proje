<?php
// Bir sınavın bitmiş denemelerini (öğrenci, soru, yanıt, puan, CodeRunner test sonuçları) JSON olarak döker.
// Kullanım: docker compose exec -T moodle php -- <sinav_id> < scripts/sinav_dok.php
// Sınav id'si verilmezse sınav listesini döker. Yalnızca okur, veritabanını değiştirmez.

define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->dirroot . '/mod/quiz/locallib.php');

$json = JSON_UNESCAPED_UNICODE | JSON_INVALID_UTF8_SUBSTITUTE;
$sinavid = (int)($argv[1] ?? 0);

if (!$sinavid) {
    $liste = $DB->get_records_sql(
        "SELECT q.id, q.name AS ad, c.shortname AS kurs,
                (SELECT COUNT(*) FROM {quiz_attempts} a
                  WHERE a.quiz = q.id AND a.preview = 0 AND a.state = 'finished') AS deneme
           FROM {quiz} q JOIN {course} c ON c.id = q.course ORDER BY q.id");
    echo json_encode(['sinavlar' => array_values($liste)], $json);
    exit(0);
}

$sinav = $DB->get_record('quiz', ['id' => $sinavid]);
if (!$sinav) {
    cli_error("Sınav bulunamadı: $sinavid");
}

$denemeler = $DB->get_records_sql(
    "SELECT a.id, a.uniqueid, a.attempt, u.username, u.firstname, u.lastname
       FROM {quiz_attempts} a JOIN {user} u ON u.id = a.userid
      WHERE a.quiz = ? AND a.preview = 0 AND a.state = 'finished'
   ORDER BY u.username, a.attempt", [$sinavid]);

$cikti = ['sinav' => ['id' => $sinavid, 'ad' => $sinav->name], 'denemeler' => []];
foreach ($denemeler as $d) {
    $quba = question_engine::load_questions_usage_by_activity($d->uniqueid);
    $sorular = [];
    foreach ($quba->get_slots() as $slot) {
        $qa = $quba->get_question_attempt($slot);
        $q = $qa->get_question();
        $tur = $q->get_type_name();
        $soru = [
            'no'       => $slot,
            'ad'       => $q->name,
            'tur'      => $tur,
            'metin'    => question_utils::to_plain_text($q->questiontext, $q->questiontextformat),
            'tam_puan' => (float)$qa->get_max_mark(),
            'puan'     => $qa->get_mark() === null ? null : (float)$qa->get_mark(),
            'durum'    => (string)$qa->get_state(),
            'yanit'    => (string)$qa->get_response_summary(),
        ];
        if ($tur === 'coderunner') {
            // Özet kırpılmış olabilir; öğrencinin yazdığı kodun kendisini al.
            $soru['yanit'] = (string)$qa->get_last_qt_var('answer', '');
            $soru['ornek_cozum'] = (string)($q->answer ?? '');
            $ham = $qa->get_last_qt_var('_testoutcome');
            $sonuc = $ham ? @unserialize($ham) : null;
            if ($sonuc) {
                $soru['hata_mesaji'] = (string)($sonuc->errormessage ?? '');
                $soru['testler'] = [];
                foreach (($sonuc->testresults ?? []) as $t) {
                    $soru['testler'][] = [
                        'test'     => (string)$t->testcode,
                        'girdi'    => (string)$t->stdin,
                        'beklenen' => (string)$t->expected,
                        'cikan'    => (string)$t->got,
                        'dogru'    => (bool)$t->iscorrect,
                    ];
                }
            }
        } else if ($tur === 'essay') {
            $soru['degerlendirme_olcutu'] = question_utils::to_plain_text(
                $q->graderinfo ?? '', $q->graderinfoformat ?? FORMAT_HTML);
        }
        $sorular[] = $soru;
    }
    $cikti['denemeler'][] = [
        'numara' => $d->username, 'ad' => $d->firstname, 'soyad' => $d->lastname,
        'deneme' => (int)$d->attempt, 'sorular' => $sorular,
    ];
}
echo json_encode($cikti, $json);
