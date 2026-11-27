#!/usr/bin/env python3
"""Bake the landing page and thank-you page from content.json.
  python3 build.py              -> uses the "gtm" container ID in content.json (none = no tracking snippet)
  python3 build.py GTM-XXXXXXX  -> overrides it for this build
Copy edits go in content.json, never in the HTML.
"""
import html
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(ROOT, "content.json"), encoding="utf-8"))
GTM = sys.argv[1] if len(sys.argv) > 1 else C.get("gtm", "")
FONTS = "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Playfair+Display:ital,wght@0,400;0,500;0,700;1,400&display=swap"


def t(s):
    return html.escape(s.replace("'", "’"), quote=True)


def gtm_head(push):
    if not GTM:
        return ""
    return ("<script>window.dataLayer=window.dataLayer||[];window.dataLayer.push(" + push + ");</script>\n"
            "<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});"
            "var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;"
            "j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);"
            "})(window,document,'script','dataLayer','" + GTM + "');</script>\n")


def gtm_body():
    if not GTM:
        return ""
    return ('<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=' + GTM +
            '" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n')


FAVICON = ("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2032%2032'%3E%3Crect%20"
           "width='32'%20height='32'%20fill='%23020203'/%3E%3Ctext%20x='16'%20y='22'%20font-family='Georgia,serif'%20"
           "font-size='15'%20fill='%23C3964B'%20text-anchor='middle'%3ER%3C/text%3E%3C/svg%3E")

CSS = """
:root{--dark:#020203;--char:#303030;--mid:#5D5D5E;--soft:#B7B7B8;--pale:#F5F5F5;--gold:#C3964B;--white:#fff;--line:#2D2D2D;
--serif:'Playfair Display',Georgia,serif;--sans:'Inter',Arial,sans-serif;--pad:1.25rem;--sec:3.5rem}
@media(min-width:700px){:root{--pad:3rem;--sec:4.5rem}}
@media(min-width:1100px){:root{--pad:4.5rem;--sec:6rem}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;font-family:var(--sans);font-size:1rem;line-height:1.5;color:var(--char);background:var(--white);-webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}
a{color:inherit}
h1,h2,h3{font-family:var(--serif);font-weight:400;margin:0;letter-spacing:-.035em;line-height:1.1}
.wrap{max-width:87.5rem;margin:0 auto;padding-inline:var(--pad)}
.label{font-size:.875rem;font-weight:600;letter-spacing:.125em;text-transform:uppercase;color:var(--gold);margin:0 0 1rem}
.btn{display:inline-flex;align-items:center;justify-content:center;padding:1.05rem 1.5rem;border:1px solid var(--white);color:var(--white);font-weight:600;font-size:.95rem;line-height:1.2;letter-spacing:.06em;text-transform:uppercase;text-decoration:none;background:transparent;cursor:pointer;font-family:var(--sans)}
.btn:hover,.btn:focus-visible{background:rgba(255,255,255,.12)}
.btn--gold{background:var(--gold);border-color:var(--gold);color:var(--dark)}
.btn--gold:hover,.btn--gold:focus-visible{background:#d2a75e}
.top{background:var(--dark)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding-block:1.1rem}
.top img{height:54px;width:auto}
.top .btn{padding:.8rem 1.1rem;font-size:.85rem;white-space:nowrap}
.hero{background:var(--dark);color:var(--soft);padding-block:2.5rem var(--sec)}
.hero__grid{display:grid;gap:2.5rem}
.hero h1{color:var(--white);font-size:clamp(2.4rem,5vw,3.75rem);line-height:1.05;margin-bottom:1.25rem}
.stat{margin:2rem 0 0}.stat .k{font-size:.875rem;font-weight:600;letter-spacing:.125em;text-transform:uppercase;color:var(--white);margin:0 0 .35rem}.stat .v{font-family:var(--serif);font-size:clamp(2.2rem,4.2vw,3.1rem);line-height:1;letter-spacing:-.03em;color:var(--gold);margin:0}
.hero__sub{font-size:1.15rem;max-width:34rem;margin:0 0 1.5rem}
.points{list-style:none;margin:0 0 2rem;padding:0;display:grid;gap:.6rem}
.points li{padding-left:1.4rem;position:relative;color:var(--white)}
.points li:before{content:"";position:absolute;left:0;top:.6em;width:.6rem;height:1px;background:var(--gold)}
.card{background:var(--white);color:var(--char);padding:1.75rem 1.5rem}
.card h2{font-size:1.6rem;color:var(--dark);margin-bottom:.75rem}
.card p{margin:0 0 1.1rem;font-size:.95rem}
form{display:grid;gap:.85rem}
.row{display:grid;gap:.85rem}
label{font-size:.8rem;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--mid);display:block;margin-bottom:.3rem}
input[type=text],input[type=email],input[type=tel],textarea{width:100%;font:inherit;color:var(--char);background:var(--white);border:1px solid #c9c9ca;border-radius:0;padding:.75rem .85rem}
textarea{min-height:6.5rem;resize:vertical}
input:focus,textarea:focus{outline:2px solid var(--gold);outline-offset:1px;border-color:var(--gold)}
.check{display:grid;grid-template-columns:auto 1fr;gap:.6rem;align-items:start;font-size:.85rem;text-transform:none;letter-spacing:0;font-weight:400;color:var(--char)}
.check input{margin-top:.2rem;width:1rem;height:1rem;accent-color:var(--gold)}
.hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
form .btn{width:100%;margin-top:.25rem}
.fine{font-size:.78rem;color:var(--mid);margin:0}
.photo{background:var(--dark)}
.photo .wrap{padding-inline:0}
.photo img{width:100%;height:auto}
.sec{padding-block:var(--sec)}
.sec h2{font-size:clamp(2rem,4vw,3.125rem);margin-bottom:1rem}
.intro{font-size:1.15rem;max-width:44rem;margin:0 0 2.5rem}
.pale{background:var(--pale)}
.cols{display:grid;gap:1.25rem}
.box{background:var(--white);padding:1.75rem 1.5rem;border-top:2px solid var(--gold)}
.box h3{font-size:1.5rem;margin-bottom:.75rem;color:var(--dark)}
.box p{margin:0}
.charc{background:var(--char);color:var(--soft)}
.charc h2{color:var(--white)}
.step{border-top:1px solid var(--mid);padding-top:1.25rem}
.step .n{font-family:var(--serif);font-size:2rem;color:var(--gold);line-height:1;margin-bottom:.75rem}
.step h3{font-size:1.35rem;color:var(--white);margin-bottom:.5rem}
.step p{margin:0}
.team{display:grid;grid-template-columns:repeat(2,1fr);gap:1.5rem 1rem}
.person .ph{aspect-ratio:302/383;background:#dcdcdd;display:flex;align-items:center;justify-content:center;font-family:var(--serif);font-size:2rem;color:#9a9a9b;overflow:hidden}
.person .ph img{width:100%;height:100%;object-fit:cover;object-position:center top}
.person .nm{font-family:var(--serif);font-size:1.15rem;color:var(--dark);margin:.8rem 0 .15rem;line-height:1.2}
.person .rl{font-size:.82rem;letter-spacing:.06em;text-transform:uppercase;color:var(--mid);margin:0}
.cta{background:var(--dark);color:var(--soft);text-align:center}
.cta h2{color:var(--white)}
.cta p{font-size:1.15rem;margin:0 auto 2rem;max-width:36rem}
.cta .btns{display:flex;flex-wrap:wrap;gap:1rem;justify-content:center}
.foot{background:var(--white);border-top:1px solid var(--pale);padding-block:2.5rem;font-size:.85rem;color:var(--mid)}
.foot .wrap{display:grid;gap:1.25rem}
.foot img{height:60px;width:auto}
.foot p{margin:0;max-width:52rem}
.callbar{position:fixed;left:0;right:0;bottom:0;z-index:20;display:flex;align-items:center;justify-content:center;padding:1rem;padding-bottom:calc(1rem + env(safe-area-inset-bottom));background:var(--gold);color:var(--dark);font-family:var(--sans);font-weight:600;font-size:1rem;line-height:1.2;letter-spacing:.06em;text-transform:uppercase;text-decoration:none;transform:translateY(100%);visibility:hidden;transition:transform .25s ease,visibility .25s}
.callbar.on{transform:none;visibility:visible}
body{padding-bottom:3.4rem}
body:has(form :is(input,textarea):focus) .callbar{display:none}
@media(min-width:700px){.photo{padding-bottom:var(--sec)}.photo .wrap{padding-inline:var(--pad)}.row{grid-template-columns:1fr 1fr}.cols{grid-template-columns:repeat(3,1fr)}.team{grid-template-columns:repeat(3,1fr);gap:2rem 1.5rem}.card{padding:2.25rem 2rem}.top img{height:64px}.callbar{display:none}body{padding-bottom:0}}
@media(min-width:1000px){.hero{padding-top:3.5rem}.hero__grid{grid-template-columns:1.05fr .95fr;gap:4.5rem;align-items:start}.team{grid-template-columns:repeat(5,1fr)}}
"""


def page():
    c = C
    url = "https://%s/%s/" % (c["domain"], c["slug"])
    push = "{'lp_region':'%s','lp_practice':'%s','page_type':'landing'}" % (c["region"], c["practice"])
    points = "".join("<li>%s</li>" % t(p) for p in c["hero_points"])
    offences = "".join('<div class="box"><h3>%s</h3><p>%s</p></div>' % (t(o["title"]), t(o["body"])) for o in c["offences"])
    steps = "".join('<div class="step"><div class="n">%d</div><h3>%s</h3><p>%s</p></div>' % (i + 1, t(s["title"]), t(s["body"]))
                    for i, s in enumerate(c["steps"]))
    people = []
    for p in c["team"]:
        rel = "assets/img/team/%s.jpg" % p["slug"]
        if os.path.exists(os.path.join(ROOT, c["slug"], rel)):
            ph = '<img src="%s" alt="%s" width="302" height="383" loading="lazy">' % (rel, t(p["name"]))
        else:
            ph = "".join(w[0] for w in p["name"].replace(",", "").split()[:2] if w[0].isalpha())
        people.append('<div class="person"><div class="ph">%s</div><p class="nm">%s</p><p class="rl">%s</p></div>'
                      % (ph, t(p["name"]), t(p["role"])))
    tel = '<a class="btn" href="tel:%s">Call %s</a>' % (c["phone_tel"], t(c["phone_display"]))
    tel_gold = tel.replace('class="btn"', 'class="btn btn--gold" id="hc"')
    callbar = '<a class="callbar" href="tel:%s">Call %s</a>\n' % (c["phone_tel"], t(c["phone_display"]))
    callbar += ("<script>(function(){var b=document.querySelector('.callbar'),h=document.getElementById('hc');"
                "if(!b||!h||!('IntersectionObserver' in window)){if(b)b.classList.add('on');return;}"
                "new IntersectionObserver(function(e){var r=e[0];b.classList.toggle('on',!r.isIntersecting&&r.boundingClientRect.top<0);}).observe(h);})();</script>\n")

    def form(fid):
        return ('<form method="post" action="/submit.php" id="%s">'
                '<input type="hidden" name="region" value="%s">'
                '<input type="hidden" name="utm_source"><input type="hidden" name="utm_medium">'
                '<input type="hidden" name="utm_campaign"><input type="hidden" name="gclid"><input type="hidden" name="lp_t">'
                '<div class="hp" aria-hidden="true"><input type="text" name="lp_ref_k7" value="" tabindex="-1" autocomplete="off" data-1p-ignore data-lpignore="true" data-bwignore data-form-type="other"></div>'
                '<div><label for="%s-name">Name</label><input type="text" id="%s-name" name="name" required autocomplete="name"></div>'
                '<div class="row"><div><label for="%s-email">Email</label><input type="email" id="%s-email" name="email" required autocomplete="email"></div>'
                '<div><label for="%s-phone">Phone</label><input type="tel" id="%s-phone" name="phone" required autocomplete="tel" inputmode="tel" placeholder="403-555-0123"></div></div>'
                '<div><label for="%s-message">How can we help?</label><textarea id="%s-message" name="message"></textarea></div>'
                '<label class="check"><input type="checkbox" name="consent" value="1" required><span>%s</span></label>'
                '<button class="btn btn--gold" type="submit">%s</button>'
                '<p class="fine">%s</p></form>'
                % (fid, t(c["region"]), fid, fid, fid, fid, fid, fid, fid, fid, t(c["consent"]), t(c["form_button"]), t(c["form_fine"])))

    return ('<!DOCTYPE html>\n<html lang="en-CA">\n<head>\n' + gtm_head(push) +
            '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>%s</title>\n<meta name="description" content="%s">\n<meta name="author" content="%s">\n'
            '<meta name="robots" content="noindex, nofollow">\n<meta name="theme-color" content="#020203">\n'
            '<link rel="canonical" href="%s">\n<link rel="icon" href="%s">\n'
            '<meta property="og:type" content="website">\n<meta property="og:site_name" content="%s">\n'
            '<meta property="og:locale" content="en_CA">\n<meta property="og:title" content="%s">\n'
            '<meta property="og:description" content="%s">\n<meta property="og:url" content="%s">\n'
            '<meta property="og:image" content="%sassets/img/hero.jpg">\n<meta property="og:image:width" content="1200">\n'
            '<meta property="og:image:height" content="630">\n<meta name="twitter:card" content="summary_large_image">\n'
            '<meta name="twitter:title" content="%s">\n<meta name="twitter:description" content="%s">\n'
            '<meta name="twitter:image" content="%sassets/img/hero.jpg">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link href="%s" rel="stylesheet">\n<style>%s</style>\n</head>\n<body>\n'
            % (t(c["title"]), t(c["description"]), t(c["firm"]), url, FAVICON, t(c["firm"]), t(c["social_title"]),
               t(c["social_description"]), url, url, t(c["social_title"]), t(c["social_description"]), url,
               html.escape(FONTS), CSS.strip().replace("\n", ""))
            + gtm_body() +
            '<header class="top"><div class="wrap"><img src="assets/img/logo-white.svg" alt="%s" width="167" height="80">%s</div></header>\n'
            % (t(c["firm"]), tel) +
            '<main>\n<section class="hero"><div class="wrap hero__grid"><div>'
            '<p class="label">%s</p><h1>%s</h1><p class="hero__sub">%s</p><ul class="points">%s</ul>%s<div class="stat"><p class="k">%s</p><p class="v">%s</p></div></div>'
            '<div class="card"><h2>%s</h2><p>%s</p>%s</div></div></section>\n'
            % (t(c["hero_label"]), t(c["h1"]), t(c["hero_sub"]), points, tel_gold, t(c["stat_label"]), t(c["stat_value"]), t(c["form_title"]), t(c["form_intro"]), form("f1")) +
            '<section class="photo"><div class="wrap"><img src="assets/img/hero.jpg" alt="%s" width="1200" height="630"></div></section>\n' % t(c["photo_alt"]) +
            '<section class="sec pale"><div class="wrap"><p class="label">%s</p><h2>%s</h2><p class="intro">%s</p><div class="cols">%s</div></div></section>\n'
            % (t(c["offences_label"]), t(c["offences_title"]), t(c["offences_intro"]), offences) +
            '<section class="sec charc"><div class="wrap"><p class="label">%s</p><h2>%s</h2><div class="cols" style="margin-top:2.5rem">%s</div></div></section>\n'
            % (t(c["steps_label"]), t(c["steps_title"]), steps) +
            '<section class="sec"><div class="wrap"><p class="label">%s</p><h2>%s</h2><p class="intro">%s</p><div class="team">%s</div></div></section>\n'
            % (t(c["team_label"]), t(c["team_title"]), t(c["team_intro"]), "".join(people)) +
            '<section class="sec cta"><div class="wrap"><h2>%s</h2><p>%s</p><div class="btns">%s<a class="btn btn--gold" href="#f1">%s</a></div></div></section>\n'
            % (t(c["cta_title"]), t(c["cta_body"]), tel, t(c["form_title"])) +
            '</main>\n<footer class="foot"><div class="wrap"><img src="assets/img/logo-dark.svg" alt="%s" width="175" height="84">'
            '<p>%s<br>%s · <a href="tel:%s">%s</a></p><p>%s</p></div></footer>\n'
            % (t(c["firm"]), t(c["firm"]), t(c["address"]), c["phone_tel"], t(c["phone_display"]), t(c["footer_disclaimer"])) +
            callbar +
            "<script>(function(){var p=new URLSearchParams(location.search);['utm_source','utm_medium','utm_campaign','gclid'].forEach(function(k){"
            "var v=p.get(k);if(!v)return;document.querySelectorAll('input[name=\"'+k+'\"]').forEach(function(i){i.value=v;});});document.querySelectorAll('form').forEach(function(f){var ph=f.querySelector('input[name=\"phone\"]'),t=f.querySelector('input[name=\"lp_t\"]');function chk(){var d=ph.value.replace(/\\D/g,'');if(d.length===11&&d.charAt(0)==='1')d=d.slice(1);ph.setCustomValidity(/^[2-9][0-9]{2}[2-9][0-9]{6}$/.test(d)?'':'Please enter a 10-digit phone number, including area code.');}['input','change','blur'].forEach(function(e){ph.addEventListener(e,chk);});f.querySelector('button').addEventListener('click',chk);f.addEventListener('submit',function(){if(t)t.value=Math.round(performance.now());});});})();</script>\n"
            "</body>\n</html>\n")


def thanks():
    c = C
    push = ("{'page_type':'thank_you','lead_type':'form','lp_practice':'%s',"
            "'lp_region':(new URLSearchParams(location.search).get('r')||'')}" % c["practice"])
    css = ("*{box-sizing:border-box}body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px;"
           "background:#020203;font-family:'Inter',Arial,sans-serif;color:#303030}"
           ".c{background:#fff;max-width:560px;width:100%;padding:52px 40px;text-align:center}"
           ".c img{height:70px;width:auto;margin:0 auto 28px;display:block}"
           "h1{font-family:'Playfair Display',Georgia,serif;font-weight:400;letter-spacing:-.03em;color:#020203;font-size:clamp(28px,5vw,36px);line-height:1.15;margin:0 0 16px}"
           "p{font-size:17px;line-height:1.6;margin:0 0 14px}"
           ".b{display:inline-block;margin-top:10px;background:#C3964B;color:#020203;text-decoration:none;font-weight:600;font-size:15px;letter-spacing:.06em;text-transform:uppercase;padding:16px 28px}"
           ".f{font-size:12.5px;color:#5D5D5E;margin-top:26px}")
    return ('<!DOCTYPE html>\n<html lang="en-CA">\n<head>\n' + gtm_head(push) +
            '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>Thank You | %s</title>\n<meta name="robots" content="noindex, nofollow">\n<meta name="theme-color" content="#020203">\n'
            '<link rel="icon" href="%s">\n<link href="%s" rel="stylesheet">\n<style>%s</style>\n</head>\n<body>\n'
            % (t(c["firm"]), FAVICON, html.escape(FONTS), css) + gtm_body() +
            '<main class="c"><img src="/%s/assets/img/logo-dark.svg" alt="%s" width="175" height="84">'
            '<h1>%s</h1><p>%s</p><p>%s</p><a class="b" href="tel:%s">Call %s</a><p class="f">%s</p></main>\n</body>\n</html>\n'
            % (c["slug"], t(c["firm"]), t(c["thanks_title"]), t(c["thanks_body"]), t(c["thanks_urgent"]), c["phone_tel"],
               t(c["phone_display"]), t(c["consent"]).replace("I understand that sending this form", "Sending information through this form")))


os.makedirs(os.path.join(ROOT, C["slug"]), exist_ok=True)
open(os.path.join(ROOT, C["slug"], "index.html"), "w", encoding="utf-8").write(page())
open(os.path.join(ROOT, "thank-you.html"), "w", encoding="utf-8").write(thanks())
print("built /%s/index.html and /thank-you.html%s" % (C["slug"], " with " + GTM if GTM else " (no GTM)"))
