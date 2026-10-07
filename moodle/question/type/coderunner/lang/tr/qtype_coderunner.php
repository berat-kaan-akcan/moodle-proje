<?php
// This file is part of CodeRunner - http://coderunner.org.nz/
//
// CodeRunner is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// CodeRunner is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with CodeRunner.  If not, see <http://www.gnu.org/licenses/>.

/**
 * Turkish language strings for the CodeRunner question type (soru düzenleme formu).
 * Çevrilmeyen metinler İngilizce olarak görüntülenir.
 *
 * @package    qtype_coderunner
 */

defined('MOODLE_INTERNAL') || die();

$string['advanced_customisation'] = 'Gelişmiş özelleştirme';
$string['allornone'] = 'Test kodu ya tüm test durumları için ya da hiçbiri için girilmelidir.';
$string['allornothing'] = 'Hepsi ya da hiç puanlama';
$string['allornothing_help'] = '"Hepsi ya da hiç puanlama" işaretliyse, gönderimin puan alabilmesi için tüm test durumlarının başarılı olması gerekir. İşaretli değilse puan, başarılı olan test durumlarının puanları toplanıp mümkün olan en yüksek puana oranlanarak hesaplanır.';
$string['allowattachments'] = 'Ek dosyalara izin ver';
$string['allowedfilenames'] = 'İzin verilen dosya adları';
$string['answer'] = 'Örnek cevap';
$string['answerbox_group'] = 'Cevap kutusu';
$string['answerbox_group_help'] = 'Cevap kutusu için ayrılacak satır sayısını belirler. Bu değer, cevap kutusunu denetleyen arayüz öğesinin (ör. Ace) en az yüksekliğini belirler. Genişlik pencereye göre ayarlanır. Cevap kutuya sığmazsa kaydırma çubukları görüntülenir.';
$string['answerboxlines'] = 'Satır';
$string['answerpreload'] = 'Cevap kutusu başlangıç metni';
$string['attachmentoptions'] = 'Ek dosya seçenekleri';
$string['attachmentsrequired'] = 'Ek dosya zorunlu olsun';
$string['coderunnertype'] = 'Soru türü';
$string['coderunnertype_help'] = 'Programlama dilini ve soru türünü seçin. Tür seçildikten sonra ayrıntılar aşağıdaki "Soru türü ayrıntıları" bölümünde görülebilir.';
$string['cputime'] = 'Süre sınırı (sn)';
$string['customisation'] = 'Özelleştirme';
$string['customise'] = 'Özelleştir';
$string['datafiles'] = 'Destek dosyaları';
$string['display'] = 'Görünüm';
$string['equalitygrader'] = 'Tam eşleşme';
$string['expected'] = 'Beklenen çıktı';
$string['extra'] = 'Ek şablon verisi';
$string['extractcodefromjson'] = 'Ace/Scratchpad uyumlu';
$string['feedback'] = 'Geri bildirim';
$string['feedback_help'] = '"Sınav tarafından belirlenir" seçeneği, sonuç tablosunun görüntülenmesini sınavın gözden geçirme seçeneklerine (özellikle "Özel geri bildirim" ayarına) bırakır. "Her zaman göster" tabloyu her durumda gösterir, "Her zaman gizle" ise her durumda gizler.';
$string['feedback_hide'] = 'Her zaman gizle';
$string['feedback_quiz'] = 'Sınav tarafından belirlenir';
$string['feedback_show'] = 'Her zaman göster';
$string['fileheader'] = 'Destek dosyaları';
$string['filenamesexplain'] = 'Açıklama';
$string['filenamesregex'] = 'Düzenli ifade';
$string['giveup'] = 'Durdur düğmesi';
$string['giveup_aftermaxmarks'] = 'Not artık yükseltilemediğinde kullanılabilir';
$string['giveup_always'] = 'Her zaman kullanılabilir';
$string['giveup_help'] = 'Bu seçenek etkinse öğrenciler, soruyla etkileşimi durdurmak ve bunun yerine genel geri bildirimi görmek için bir düğme görür.

"Durdur ve son geri bildirimi oku" düğmesi baştan itibaren gösterilebilir ya da yalnızca ceza düzeni nedeniyle öğrenci notunu artık yükseltemediğinde gösterilebilir.';
$string['giveup_never'] = 'Hiçbir zaman kullanılamaz';
$string['globalextra'] = 'Genel ek veri';
$string['grading'] = 'Değerlendirme';
$string['hidecheck'] = 'Kontrol düğmesini gizle';
$string['hiderestiffail'] = 'Başarısız olursa kalanları gizle';
$string['hoisttemplateparams'] = 'Şablon parametrelerini üst düzeye taşı';
$string['iscombinatortemplate'] = 'Birleştirici şablon';
$string['language'] = 'Sandbox dili';
$string['languages'] = 'Diller';
$string['mark'] = 'Puan';
$string['marking'] = 'Puan dağılımı';
$string['markinggroup'] = 'Puanlama';
$string['markinggroup_help'] = '"Hepsi ya da hiç puanlama" işaretliyse, gönderimin puan alabilmesi için tüm test durumlarının başarılı olması gerekir. İşaretli değilse puan, başarılı olan test durumlarının puanları toplanıp mümkün olan en yüksek puana oranlanarak hesaplanır. Test durumu başına puanlar yalnızca "Hepsi ya da hiç puanlama" işaretli değilken belirlenebilir. Test durumlarına kısmi puan veren bir şablon değerlendirici kullanılıyorsa bu seçenek genellikle işaretlenmemelidir.

Zorunlu ceza düzeni, virgülle ayrılmış yüzde değerlerinden oluşan bir listedir (ör. 10, 20, ...). Her yanlış denemede listedeki sıradaki ceza uygulanır. Liste sonundaki üç nokta, son cezanın sonraki denemeler için de geçerli olduğunu belirtir.';
$string['maxfilesize'] = 'İzin verilen en büyük dosya boyutu (bayt)';
$string['memorylimit'] = 'Bellek sınırı (MB)';
$string['nearequalitygrader'] = 'Yaklaşık tam eşleşme';
$string['ordering'] = 'Sıralama';
$string['penaltyregimelabel'] = 'Ceza düzeni:';
$string['precheck'] = 'Ön kontrol';
$string['precheck_all'] = 'Tümü';
$string['precheck_disabled'] = 'Devre dışı';
$string['precheck_empty'] = 'Boş';
$string['precheck_examples'] = 'Örnekler';
$string['precheck_selected'] = 'Seçilenler';
$string['prototypecontrols'] = 'Prototip oluşturma';
$string['prototypeextra'] = 'Prototip ek verisi';
$string['prototypeQ'] = 'Prototip mi?';
$string['questioncheckboxes'] = 'Özelleştirme';
$string['questiontype_required'] = 'Soru türünü seçmelisiniz';
$string['questiontypedetails'] = 'Soru türü ayrıntıları';
$string['regexgrader'] = 'Düzenli ifade';
$string['resultcolumns'] = 'Sonuç sütunları';
$string['sampleanswerattachments'] = 'Örnek cevap ekleri';
$string['sandboxcontrols'] = 'Sandbox';
$string['sandboxparams'] = 'Parametreler';
$string['showsource'] = 'Şablon hata ayıklama';
$string['stdin'] = 'Standart girdi';
$string['student_answer'] = 'Öğrenci cevabı';
$string['submitbuttons'] = 'Gönder düğmeleri';
$string['template'] = 'Şablon';
$string['templatecontrols'] = 'Şablon denetimleri';
$string['templategrader'] = 'Şablon değerlendirici';
$string['templateparams'] = 'Şablon parametreleri';
$string['templateparamsevalpertry'] = 'Her öğrenci için değerlendir';
$string['templateparamslang'] = 'Ön işlemci';
$string['testcase'] = 'Test durumu {$a}';
$string['testcasecontrols'] = 'Test özellikleri:';
$string['testcases'] = 'Test durumları';
$string['testsplitterre'] = 'Test ayırıcı (düzenli ifade)';
$string['testtype'] = 'Ön kontrol test türü';
$string['testtype_both'] = 'Her ikisi';
$string['testtype_normal'] = 'Yalnızca kontrol';
$string['testtype_precheck'] = 'Yalnızca ön kontrol';
$string['twigall'] = 'Tümüne Twig uygula';
$string['twigcontrols'] = 'Şablon parametresi denetimleri';
$string['type_header'] = 'CodeRunner soru türü';
$string['typename'] = 'Soru türü';
$string['uicontrols'] = 'Girdi arayüzleri';
$string['uiparametergroup'] = 'Arayüz parametreleri';
$string['uiparameters'] = 'Arayüz parametreleri (JSON)';
$string['useace'] = 'Şablon Ace kullanır';
$string['useasexample'] = 'Örnek olarak kullan';
$string['validateonsave'] = 'Kaydederken doğrula';
