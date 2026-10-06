<?php
// Muğla Sıtkı Koçman Üniversitesi DYS Giriş Sayfası

require_once('../config.php');
require_once('lib.php');

// Zaten giriş yapmış kullanıcıları ana sayfaya yönlendir
if (isloggedin() && !isguestuser()) {
    redirect($CFG->wwwroot . '/');
}

// Hata mesajı kontrolü
$errorcode = optional_param('errorcode', 0, PARAM_INT);
$errormsg = '';

if (!empty($SESSION->loginerrormsg)) {
    $errormsg = $SESSION->loginerrormsg;
    unset($SESSION->loginerrormsg);
} else if ($errorcode) {
    if ($errorcode == 1) {
        $errormsg = get_string('cookiesnotenabled');
    } else if ($errorcode == 2) {
        $errormsg = get_string('invalidusername');
    } else {
        $errormsg = get_string('invalidlogin');
    }
}

// Hatırlanan kullanıcı adı
$rememberedusername = get_moodle_cookie();
$logintoken = \core\session\manager::get_login_token();
?>
<!DOCTYPE html>
<html dir="ltr" lang="tr" xml:lang="tr">
<head>
    <title>Muğla Sıtkı Koçman Üniversitesi Uzaktan Eğitim Sistemi: Siteye giriş yap</title>
    <link rel="shortcut icon" href="favicon.png" />
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="keywords" content="moodle, Muğla Sıtkı Koçman Üniversitesi Uzaktan Eğitim Sistemi: Siteye giriş yap" />
    <script id="firstthemesheet" type="text/css">/** Required in order to fix style inclusion problems in IE with YUI **/</script>
    <link rel="stylesheet" type="text/css" href="all.css" />
    <meta name="robots" content="noindex" />
    <link href='https://fonts.googleapis.com/css?family=Roboto:300,400,500,600,700,300italic' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=0, minimal-ui">
    <script src="../lib/jquery/jquery-3.7.1.min.js"></script>
    <style>
    #left-cont { height: calc(100% - 60px); position: fixed; width: calc(100% - 530px); text-align:center; }
    #closeLeftSide { position: absolute; top: 5px; right: 5px; }
    #closeOnce { position: absolute; top: 5px; left: 5px; }
    #left-cont img { height: 100%; max-width: 100%; object-fit: contain; }
    @media (max-width: 767px){
        #left-cont { z-index:10; width:100%; background:rgba(0,0,0,0.4); top:0; left:0; height:100%; padding:20px; }
    }
    @media (min-width: 768px){ 
        #closeLeftSide{ display:none; }
        #closeOnce{ display:none; }
    }
    .page-login-v2:before {
        background-image: url(skype_mountain.jpg);
    }
    #blocker { display:none; position:fixed; top:0; bottom:0; left:0; right:0; width:100%; height:100%; z-index:200000; background: rgba(255,255,255,0.7); text-align: center; }
    #blocker img { top: 45%; position: relative; width: 80px; }
    #loginError { margin-bottom: 1rem; text-align: center; font-weight: bold; }
    </style>

    <script>
        function setCookie(name, value, days) {
            var expires = "";
            if (days) {
                var date = new Date();
                date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
                expires = "; expires=" + date.toUTCString();
            }
            document.cookie = name + "=" + (value || "") + expires + "; path=/";
        }
        function getCookie(name) {
            var nameEQ = name + "=";
            var ca = document.cookie.split(';');
            for (var i = 0; i < ca.length; i++) {
                var c = ca[i];
                while (c.charAt(0) == ' ') c = c.substring(1, c.length);
                if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
            }
            return null;
        }
        $(document).ready(function () {
            var activePopup = "guz2026";
            var popupOpen = getCookie(activePopup) == null ? true : false;
            if(popupOpen) {
                $(".page-content").prepend('<div id="left-cont"><div class="btn btn-warning" id="closeOnce">KAPAT</div><div class="btn btn-danger" id="closeLeftSide">Bir daha gösterme</div><a href="https://uzem.mu.edu.tr/tr/kilavuzlar-8626" target="_blank"><img src="oturum.jpg" alt="Duyuru Görseli"></a></div>');
                $("#closeLeftSide").on("click", function(e){
                    e.stopPropagation();
                    $("#left-cont").remove();	
                    setCookie(activePopup, "true", 180);
                });
                $("#closeOnce").on("click", function(e){
                    e.stopPropagation();
                    $("#left-cont").remove();	
                });
            }
        });
    </script>
</head>

<body id="page-login-index" class="format-site path-login safari dir-ltr lang-tr yui-skin-sam yui3-skin-sam dys-mu-edu-tr pagelayout-login course-1 context-1 notloggedin page-login-v2 layout-full page-dark">
    <!-- Blocker Loader -->
    <div id="blocker"><img src="ajx.svg" alt="Yükleniyor..."></div>

    <div class="page">
        <div class="page-content" style="height:100%">
            <div id="region-main-box">
                <section id="region-main">
                    <span class="notifications" id="user-notifications"></span>
                    <div role="main">
                        <span id="maincontent"></span>
                        <div class="page-brand-info">
                            <div class="brand">
                                <img src="muglason.png" class="brand-img w-350" title="Muğla Sıtkı Koçman Üniversitesi Uzaktan Eğitim Sistemi" alt="Muğla Sıtkı Koçman Üniversitesi Uzaktan Eğitim Sistemi"/>
                            </div>
                        </div>

                        <div class="page-login-main animation-slide-right animation-duration-1">
                            <div class="brand hidden-md-up text-center">
                                <img src="muglason.png" class="brand-img" title="Muğla Sıtkı Koçman Üniversitesi Uzaktan Eğitim Sistemi" alt="Muğla Sıtkı Koçman Üniversitesi Uzaktan Eğitim Sistemi"/>
                            </div>

                            <h3 class="font-size-24">Oturum Aç</h3>

                            <?php if (!empty($errormsg)): ?>
                                <div id="loginError" class="text-danger font-size-14 mb-2"><?php echo htmlspecialchars($errormsg); ?></div>
                            <?php endif; ?>

                            <form class="" action="index.php" method="post" id="login">
                                <input id="anchor" type="hidden" name="anchor" value="">
                                <input type="hidden" name="logintoken" value="<?php echo htmlspecialchars($logintoken); ?>">
                                <script>document.getElementById('anchor').value = location.hash;</script>

                                <div class="form-group">
                                    <label for="username" class="sr-only">Kullanıcı adı</label>
                                    <input type="text" class="form-control" id="username" name="username" value="<?php echo htmlspecialchars($rememberedusername); ?>" placeholder="mailadresi@posta.mu.edu.tr" required autofocus>
                                </div>

                                <div class="form-group">
                                    <label for="password" class="sr-only">Şifre</label>
                                    <input type="password" name="password" id="password" value="" class="form-control" placeholder="Parola" required>
                                </div>

                                <div class="form-group clearfix">
                                    <div class="checkbox-custom checkbox-inline checkbox-primary float-left rememberpass">
                                        <input type="checkbox" id="rememberusername" name="rememberusername" value="1" <?php if (!empty($rememberedusername)) echo 'checked'; ?>>
                                        <label for="rememberusername">Kullanıcı adını hatırla</label>
                                    </div>
                                    <a class="float-right" href="forgot_password.php">Şifremi Unuttum</a>
                                </div>

                                <button type="submit" class="btn btn-primary btn-block" id="loginbtn">Giriş yap</button>
                            </form>

                            <script>
                                $(document).ready(function(){
                                    $("#login").submit(function(){
                                        $("#blocker").show();
                                    });
                                });
                            </script>

                            <div class="hidden-xs-up mt-4" style="margin-top: 15px;">
                                Oturum desteği etkin olmalıdır
                                <a class="btn btn-link p-a-0" role="button" href="javascript:void(0);" onclick="alert('Bu site tarafından iki adet çerez kullanılır:\n1. MoodleSession: Oturumunuzun açık kalmasını sağlar.\n2. MOODLEID: Kullanıcı adınızı hatırlar.');">
                                    <i class="icon fa fa-question-circle text-info fa-fw" aria-hidden="true" title="Oturum desteği etkin olmalıdır Yardımı"></i>
                                </a>
                            </div>

                        </div>
                    </div>
                </section>
            </div>
        </div>
    </div>
</body>
</html>
