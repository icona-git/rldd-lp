<?php
/**
 * RLDD landing pages — Mailgun credentials (TEMPLATE)
 *
 * THIS IS A TEMPLATE. Do not paste real credentials here, and never commit the
 * real config.php to Git.
 *
 * ONE-TIME SERVER SETUP:
 *   1. Create a `private/` folder as a SIBLING of the web root (next to httpdocs/),
 *      NOT inside it.
 *   2. Copy this file there and rename to config.php.
 *   3. Paste the real Mailgun DOMAIN SENDING KEY (Mailgun -> Send -> Sending ->
 *      Domain settings -> Sending API keys -> Add sending key).
 *   4. chmod 640 private/config.php
 *
 * submit.php loads this via __DIR__ . '/../private/config.php' — the sibling
 * private/ folder, outside the web root, so it is never served.
 */

// Mailgun DOMAIN sending key (NOT the account/primary API key).
define('MAILGUN_API_KEY', 'PASTE_YOUR_MAILGUN_SENDING_KEY_HERE');

// US region. Confirm the verified sending domain for this client.
// EU accounts: change 'api' to 'api.eu'.
define('MAILGUN_API_BASE', 'https://api.mailgun.net/v3/mg.rldd.ca');

// From address (display name + verified sending subdomain).
define('MAIL_FROM', 'Ross Lutz Dunn & Deshaye LLP <landing@mg.rldd.ca>');

// Where lead notifications go — the client's intake inbox.
define('MAIL_TO', 'PASTE_LEAD_RECIPIENT_INBOX_HERE');
