# RLDD landing pages (lp.rldd.ca)

- Client: Ross Lutz Dunn & Deshaye LLP, Calgary criminal defence. Main site rldd.ca (Silverstripe 6.2). Do not change the main site's existing tags.
- Follow the icona-landing-page skill. Language en-CA. Not Quebec.
- Hosting: Plesk on Bertha (bertha.icona.ca), site lp.rldd.ca (first set up as rldd.icona.ca on 26 Nov 2026). Repo root = web root. Private config: ../private/config.php.
- GTM: the firm's existing container GTM-N6P25NPZ (shared with rldd.ca; GA4 G-DXWHVQLZC4). The ID lives in content.json ("gtm"). Every landing-page tag in GTM is prefixed `LP –` and limited to Page Hostname starting with `lp.` so it never fires on the main site.
- Mailgun sending domain: mg.rldd.ca. Real key lives in ../private/config.php on the server, never in Git.
- Lead inbox: TBD (client to confirm). Never CC ICONA on live leads.
- Copy lives in content.json; run `python3 build.py` to bake calgary/index.html and thank-you.html. Never edit the HTML by hand.
- Headshots: calgary/assets/img/team/<slug>.jpg (slugs are in content.json). Missing photo = initials placeholder.
- Google Ads: sensitive category. No remarketing tags, no enhanced conversions.
- Copy rules: no "specialist", "expert", "best", outcome promises, "free consultation", "24/7", "170+ years",
  "most reported decisions" or testimonials without the client's written OK.
- _ref/ holds reference copies of rldd.ca (not deployed, gitignored). Never deploy without Dave's OK.
- Form spam checks (submit.php): hidden trap field lp_ref_k7, page-open timer lp_t (set by the page script), 10-digit phone, no links in name/message, 5 requests/hour per IP. Every rejection shows a visible message and is written to the PHP error log; nothing is dropped silently.
