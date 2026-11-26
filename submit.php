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

// Honeypot: real people leave this hidden field blank; bots fill it. Silently drop.
if (!empty($_POST['lp_ref_k7'] ?? '')) { error_log('[RLDD form] Honeypot filled; submission dropped.'); header('Location: /thank-you.html'); exit; }

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
if (!empty($errors)) { lp_bail(implode(' ', $errors)); }

$submitted_at = date('Y-m-d H:i:s T');
$ip           = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
$subject      = 'New consultation request — ' . $name . ' (' . $region . ')';

$text_body = "A new consultation request was submitted on rldd.icona.ca.\n\n"
    . "Campaign: {$region}\n\nName:  {$name}\nEmail: {$email}\nPhone: {$phone}\n"
    . "Source: {$source}\n\nHow can we help:\n{$message}\n\n"
    . "Submitted: {$submitted_at}\nIP: {$ip}\n\n--\nRoss Lutz Dunn & Deshaye LLP\n"
    . "This message originated from a consultation request form at rldd.icona.ca. It may "
    . "contain information that is confidential and subject to solicitor-client privilege. "
    . "If you received this in error, please notify us and delete it.\n";

$e = function ($v) { return htmlspecialchars($v, ENT_QUOTES, 'UTF-8'); };
$html_body = '<!doctype html><html><body style="font-family:Arial,Helvetica,sans-serif;color:#020203;">'
    . '<h2 style="margin:0 0 12px;">New consultation request</h2>'
    . '<p>Submitted on <strong>rldd.icona.ca</strong> — campaign: <strong>' . $e($region) . '</strong>.</p>'
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
