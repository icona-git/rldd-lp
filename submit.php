<?php
/**
 * Ross Lutz Dunn & Deshaye LLP — Landing Page Form Handler (shared)
 *
 * Every campaign page under the site posts here. A hidden `region` field says
 * which campaign. Sends a lead email via the Mailgun API, then redirects to
 * /thank-you.html. Credentials load from /private/config.php (outside the web
 * root and outside Git). Deploy this file to the web root.
 */

$config_path = __DIR__ . '/../private/config.php';
if (!file_exists($config_path)) {
    error_log('[RLDD form] Missing config at: ' . $config_path);
    http_response_code(500);
    exit('Server configuration error. Please contact the site administrator.');
}
require_once $config_path;

/** Trim, length-cap, and strip CR/LF (prevents email-header injection). */
function lp_clean($value, $max = 500) {
    $value = is_string($value) ? trim($value) : '';
    $value = mb_substr($value, 0, $max);
    return str_replace(["\r", "\n"], '', $value);
}
function lp_bail($message = 'There was a problem with your submission.') {
    http_response_code(400);
    header('Content-Type: text/plain; charset=utf-8');
    echo $message;
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405); header('Allow: POST'); exit('Method not allowed.');
}

// Refuse to run if the lead inbox is not a real address, so a lead is never silently lost.
foreach (explode(',', MAIL_TO) as $lp_to) {
    if (!filter_var(trim($lp_to), FILTER_VALIDATE_EMAIL)) {
        error_log('[RLDD form] MAIL_TO is not a valid email address. Check private/config.php.');
        http_response_code(500);
        header('Content-Type: text/plain; charset=utf-8');
        exit("Sorry — we couldn't submit your request right now. Please call (403) 264-8484.");
    }
}

$lp_call = ' If this keeps happening, please call (403) 264-8484.';
$ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';

// Spam check 1: a hidden field that people never see. Anything in it means a bot (or autofill).
// Rejected with a visible message, never a fake thank-you, so a real person knows to call.
if (!empty($_POST['lp_ref_k7'] ?? '')) {
    error_log('[RLDD form] Rejected: hidden field filled. IP ' . $ip);
    lp_bail("We couldn't verify your submission. Please reload the page and try again." . $lp_call);
}

// Spam check 2: the page's script records how long the page was open. Bots that post
// directly send nothing; a person takes more than three seconds to fill in a form.
$lp_t = $_POST['lp_t'] ?? '';
if (!ctype_digit((string) $lp_t) || (int) $lp_t < 3000) {
    error_log('[RLDD form] Rejected: timing check failed. IP ' . $ip);
    lp_bail("We couldn't verify your submission. Please reload the page and try again." . $lp_call);
}

$name    = lp_clean($_POST['name']    ?? '', 120);
$email   = lp_clean($_POST['email']   ?? '', 160);
$phone   = lp_clean($_POST['phone']   ?? '', 40);
$message = lp_clean($_POST['message'] ?? '', 2000);
$region  = lp_clean($_POST['region']  ?? '', 60) ?: 'RLDD Landing Page';
$source  = trim(lp_clean($_POST['utm_source'] ?? '', 80) . ' / ' . lp_clean($_POST['utm_medium'] ?? '', 80) . ' / ' . lp_clean($_POST['utm_campaign'] ?? '', 120), ' /');
if (lp_clean($_POST['gclid'] ?? '', 200) !== '') { $source = trim($source . ' (Google Ads click)'); }
if ($source === '') { $source = 'not tagged'; }

$errors = [];
if ($name === '')                                                { $errors[] = 'Name is required.'; }
if ($email === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) { $errors[] = 'A valid email address is required.'; }
if ($phone === '')                                               { $errors[] = 'Phone number is required.'; }
$digits = preg_replace('/\D/', '', $phone);
if (strlen($digits) === 11 && $digits[0] === '1') { $digits = substr($digits, 1); }
if ($phone !== '' && !preg_match('/^[2-9][0-9]{2}[2-9][0-9]{6}$/', $digits)) {
    $errors[] = 'Please enter a 10-digit phone number, including area code.';
} elseif ($phone !== '') {
    $phone = '(' . substr($digits, 0, 3) . ') ' . substr($digits, 3, 3) . '-' . substr($digits, 6);
}
// Spam check 3: web links in the name or message are almost always spam.
if (preg_match('~https?://|www\.|\[url|<a\s~i', $name . ' ' . $message)) {
    $errors[] = 'Please remove web links from your message and try again.';
}
if (!empty($errors)) { lp_bail(implode(' ', $errors)); }

// Spam check 4: no more than five requests an hour from one address.
$lp_file = sys_get_temp_dir() . '/rldd_lp_' . md5($ip);
$lp_now  = time();
$lp_hits = array();
foreach ((@file($lp_file, FILE_IGNORE_NEW_LINES) ?: array()) as $lp_h) {
    if ($lp_now - (int) $lp_h < 3600) { $lp_hits[] = (int) $lp_h; }
}
if (count($lp_hits) >= 5) {
    error_log('[RLDD form] Rejected: rate limit. IP ' . $ip);
    lp_bail('We have received several requests from you already. Please call (403) 264-8484.');
}
$lp_hits[] = $lp_now;
@file_put_contents($lp_file, implode("\n", $lp_hits));

$submitted_at = date('Y-m-d H:i:s T');
$subject      = 'New consultation request — ' . $name . ' (' . $region . ')';

$text_body = "A new consultation request was submitted on lp.rldd.ca.\n\n"
    . "Campaign: {$region}\n\nName:  {$name}\nEmail: {$email}\nPhone: {$phone}\n"
    . "Source: {$source}\n\nHow can we help:\n{$message}\n\n"
    . "Submitted: {$submitted_at}\nIP: {$ip}\n\n--\nRoss Lutz Dunn & Deshaye LLP\n"
    . "This message originated from a consultation request form at lp.rldd.ca. It may "
    . "contain information that is confidential and subject to solicitor-client privilege. "
    . "If you received this in error, please notify us and delete it.\n";

$e = function ($v) { return htmlspecialchars($v, ENT_QUOTES, 'UTF-8'); };
$html_body = '<!doctype html><html><body style="font-family:Arial,Helvetica,sans-serif;color:#020203;">'
    . '<h2 style="margin:0 0 12px;">New consultation request</h2>'
    . '<p>Submitted on <strong>lp.rldd.ca</strong> — campaign: <strong>' . $e($region) . '</strong>.</p>'
    . '<table cellpadding="6" cellspacing="0" border="0" style="font-size:14px;border-collapse:collapse;">'
    . '<tr><td style="background:#f2f5f7;"><strong>Name</strong></td><td>' . $e($name) . '</td></tr>'
    . '<tr><td style="background:#f2f5f7;"><strong>Email</strong></td><td><a href="mailto:' . $e($email) . '">' . $e($email) . '</a></td></tr>'
    . '<tr><td style="background:#f2f5f7;"><strong>Phone</strong></td><td><a href="tel:' . $e($phone) . '">' . $e($phone) . '</a></td></tr>'
    . '<tr><td style="background:#f2f5f7;"><strong>Source</strong></td><td>' . $e($source) . '</td></tr>'
    . '<tr><td style="background:#f2f5f7;vertical-align:top;"><strong>Message</strong></td><td>' . nl2br($e($message)) . '</td></tr>'
    . '<tr><td style="background:#f2f5f7;"><strong>Submitted</strong></td><td>' . $e($submitted_at) . '</td></tr>'
    . '</table><p style="color:#666;font-size:12px;margin-top:20px;">IP: ' . $e($ip) . '</p></body></html>';

$post_fields = http_build_query([
    'from' => MAIL_FROM, 'to' => MAIL_TO, 'subject' => $subject,
    'text' => $text_body, 'html' => $html_body,
    'h:Reply-To' => $email, 'h:X-Managed-By' => 'ICONA — ads@icona.ca',
    'o:tag' => 'rldd-lp',
]);
$ch = curl_init();
curl_setopt_array($ch, [
    CURLOPT_URL => MAILGUN_API_BASE . '/messages', CURLOPT_POST => true,
    CURLOPT_USERPWD => 'api:' . MAILGUN_API_KEY, CURLOPT_RETURNTRANSFER => true,
    CURLOPT_CONNECTTIMEOUT => 10, CURLOPT_TIMEOUT => 30, CURLOPT_POSTFIELDS => $post_fields,
]);
$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curl_err = curl_error($ch);
curl_close($ch);

if ($http_code !== 200) {
    error_log('[RLDD form] Mailgun error. HTTP ' . $http_code . ' | ' . $curl_err . ' | ' . $response);
    http_response_code(500);
    header('Content-Type: text/plain; charset=utf-8');
    exit("Sorry — we couldn't submit your request right now. Please try again shortly, or call (403) 264-8484.");
}

header('Location: /thank-you.html?r=' . rawurlencode($region));
exit;
