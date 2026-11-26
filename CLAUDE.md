# RLDD landing pages (rldd.icona.ca for now; lp.rldd.ca once the firm's IT adds the DNS record)

- Client: Ross Lutz Dunn & Deshaye LLP, Calgary criminal defence. Main site rldd.ca (Silverstripe 6.2, GTM-N6P25NPZ — do not touch).
- Follow the icona-landing-page skill. Language en-CA. Not Quebec.
- Hosting: Plesk on Bertha (bertha.icona.ca), subdomain rldd.icona.ca. Repo root = web root. Moving to lp.rldd.ca later: change "domain" in content.json, rebuild, add the new hostname in Plesk.
- GTM: dedicated container for lp.rldd.ca — ID TBD. Build with `python3 build.py GTM-XXXXXXX`.
- Mailgun sending domain: mg.rldd.ca. Real key lives in ../private/config.php on the server, never in Git.
- Lead inbox: TBD (client to confirm). Never CC ICONA on live leads.
- Copy lives in content.json; run `python3 build.py` to bake calgary/index.html and thank-you.html. Never edit the HTML by hand.
- Headshots: calgary/assets/img/team/<slug>.jpg (slugs are in content.json). Missing photo = initials placeholder.
- Google Ads: sensitive category. No remarketing tags, no enhanced conversions.
- Copy rules: no "specialist", "expert", "best", outcome promises, "free consultation", "24/7", "170+ years",
  "most reported decisions" or testimonials without the client's written OK.
- _ref/ holds reference copies of rldd.ca (not deployed, gitignored). Never deploy without Dave's OK.
