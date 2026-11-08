"""Generates site/index.html from site_data.json. Run: python build.py"""
import json, html, pathlib
ROOT = pathlib.Path(__file__).parent
D = json.loads((ROOT / "site_data.json").read_text(encoding="utf8"))
E = html.escape

ICONS = {
 "youtube": '<path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4.5A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8ZM9.6 15.6V8.4l6.3 3.6-6.3 3.6Z"/>',
 "instagram": '<path d="M12 2.2c3.2 0 3.6 0 4.8.1 3.3.1 4.8 1.7 4.9 4.9.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 3.2-1.7 4.8-4.9 4.9-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-3.3-.1-4.8-1.7-4.9-4.9C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8C2.4 3.9 3.9 2.4 7.2 2.3 8.4 2.2 8.8 2.2 12 2.2Zm0 4.9a4.9 4.9 0 1 0 0 9.8 4.9 4.9 0 0 0 0-9.8Zm0 8.1a3.2 3.2 0 1 1 0-6.4 3.2 3.2 0 0 1 0 6.4Zm5.1-9.4a1.2 1.2 0 1 0 0 2.3 1.2 1.2 0 0 0 0-2.3Z"/>',
 "tiktok": '<path d="M19.6 6.7a4.8 4.8 0 0 1-3.8-4.2V2h-3.4v13.7a2.9 2.9 0 1 1-2-2.7V9.5a6.3 6.3 0 1 0 5.4 6.2V8.8a8.2 8.2 0 0 0 4.8 1.5V6.9l-1-.2Z"/>',
 "facebook": '<path d="M24 12a12 12 0 1 0-13.9 11.9v-8.4h-3V12h3V9.4c0-3 1.8-4.7 4.5-4.7 1.3 0 2.7.2 2.7.2v2.9h-1.5c-1.5 0-2 .9-2 1.9V12h3.4l-.5 3.5h-2.9v8.4A12 12 0 0 0 24 12Z"/>',
 "mail": '<path d="M2 5h20v14H2V5Zm2 2v.5l8 5 8-5V7H4Zm16 2.8-8 5-8-5V17h16V9.8Z"/>',
}
PLAY = '<svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>'
def svg(name): return f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'

def genre(t):
    t = t.lower()
    for key, g in [("hiphop", "Hip-Hop"), ("shatta", "Shatta"), ("salsa", "Latin"), ("arabic", "World"),
                   ("surinam", "World"), ("r&b", "R&B"), ("riddim", "Dancehall"), ("party", "Dancehall"),
                   ("pum pum", "Dancehall"), ("gods", "Dancehall")]:
        if key in t: return g
    return "Dancehall"

beats = D["beats"]
for b in beats: b["genre"] = genre(b["title"])
genres = sorted({b["genre"] for b in beats})
base_price = D["licenses"][0]["price"]

beat_cards = "\n".join(f'''      <a class="beat reveal" data-g="{E(b['genre'])}" href="{E(b['url'])}" target="_blank" rel="noopener">
        <div class="cover"><img src="{E(b['cover'])}" alt="{E(b['title'])} cover" loading="lazy" width="640" height="640"><span class="tag">{E(b['genre'])}</span><span class="play">{PLAY}</span></div>
        <div class="info"><h3>{E(b['title'])}</h3><span class="price">from €{base_price}</span></div>
      </a>''' for b in beats)
chips = '<button class="chip on" data-f="all">All</button>' + "".join(f'<button class="chip" data-f="{E(g)}">{E(g)}</button>' for g in genres)
lic_cards = "\n".join(f'''      <div class="card reveal{' hot' if l.get('hot') else ''}"><h3>{E(l['name'])}</h3><div class="price-big">€{l['price']}</div><p>{E(l['desc'])}</p><ul>{''.join(f'<li>{E(x)}</li>' for x in l['features'])}</ul></div>''' for l in D["licenses"])
socials = [s for s in D["socials"] if s.get("url")]
soc_cards = "\n".join(f'''      <a class="soc reveal" style="--c:{s['color']}" href="{E(s['url'])}" target="_blank" rel="noopener"><span class="ic">{svg(s['icon'])}</span><b>{E(s['name'])}</b><span>{E(s['handle'])}</span></a>''' for s in socials)
yt = next((s["url"] for s in socials if s["icon"] == "youtube"), D["store"])
foot_soc = " ".join(f'<a href="{E(s["url"])}" target="_blank" rel="noopener" aria-label="{E(s["name"])} {E(s["handle"])}">{E(s["name"])}</a>' for s in {x["name"]: x for x in reversed(socials)}.values())
same_as = json.dumps([s["url"] for s in socials] + [D["store"]])

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(D['title'])}</title>
<meta name="description" content="{E(D['description'])}">
<link rel="canonical" href="{D['url']}/">
<meta name="theme-color" content="#07070b">
<meta property="og:type" content="website"><meta property="og:url" content="{D['url']}/">
<meta property="og:title" content="{E(D['title'])}"><meta property="og:description" content="{E(D['description'])}">
<meta property="og:image" content="{D['url']}/assets/img/og.jpg"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/icon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="assets/img/icon-180.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preload" as="image" href="assets/img/hero.webp">
<link rel="stylesheet" href="assets/styles.css?v={D['version']}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"MusicGroup","name":"{E(D['brand'])}","alternateName":"MrGental","url":"{D['url']}/","logo":"{D['url']}/assets/img/icon-512.png","email":"{D['email']}","genre":{json.dumps(genres)},"sameAs":{same_as}}}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="nav">
  <div class="wrap">
    <a class="brand" href="#home"><img src="assets/img/icon-180.png" alt="SGP logo" width="40" height="40">SWEET GALAXY</a>
    <button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
    <ul class="menu" id="menu">
      <li><a href="#home">Home</a></li><li><a href="#beats">Music / Beats</a></li><li><a href="#licenses">Licenses</a></li>
      <li><a href="#watch">Watch</a></li><li><a href="#about">About</a></li><li><a href="#social">Social</a></li><li><a href="#contact">Contact</a></li>
    </ul>
  </div>
</header>
<main id="main">
<section class="hero" id="home">
  <div class="wrap hero-inner">
    <span class="eyebrow">Sweet Galaxy Productions</span>
    <h1>Beats from <span class="grad-text">another galaxy</span></h1>
    <p>{E(D['tagline'])}</p>
    <div class="cta">
      <a class="btn btn-primary" href="#beats">{PLAY} Listen to the beats</a>
      <a class="btn btn-ghost" href="{D['store']}" target="_blank" rel="noopener">Visit the beat store</a>
    </div>
  </div>
</section>

<div class="wrap stats">
  <div class="stat reveal"><b class="grad-text">{len(beats)}+</b><span>Beats ready to lease</span></div>
  <div class="stat reveal"><b class="grad-text">{len(genres)}</b><span>Genres</span></div>
  <div class="stat reveal"><b class="grad-text">€{base_price}</b><span>Leases from</span></div>
  <div class="stat reveal"><b class="grad-text">{len(D["licenses"])}</b><span>License options</span></div>
</div>

<section id="beats">
  <div class="wrap">
    <div class="head reveal"><span class="eyebrow">Music / Beats</span><h2>Fresh beats, <span class="grad-text">ready for your next hit</span></h2><p>Dancehall, Shatta, Hip-Hop, Latin and more. Click a beat to listen and buy it in the beat store.</p></div>
    <div class="filters reveal">{chips}</div>
    <div class="grid">
{beat_cards}
    </div>
    <div class="center"><a class="btn btn-primary" href="{D['store']}" target="_blank" rel="noopener">See all beats in the store</a></div>
  </div>
</section>

<section class="alt" id="licenses">
  <div class="wrap">
    <div class="head reveal"><span class="eyebrow">Licenses</span><h2>Simple, <span class="grad-text">honest pricing</span></h2><p>Every beat is available on a lease basis (non-exclusive). Further details about usage rights are in the license contract.</p></div>
    <div class="lic" style="grid-template-columns:repeat(auto-fit,minmax(230px,1fr))">
{lic_cards}
    </div>
    <div class="center"><p style="color:var(--muted);margin-bottom:18px">Buy 2 leases, get 1 free. Mention it with your order.</p><a class="btn btn-ghost" href="{D['store']}" target="_blank" rel="noopener">Buy a license</a></div>
  </div>
</section>

<section id="watch">
  <div class="wrap">
    <div class="head reveal"><span class="eyebrow">Watch</span><h2>Behind the <span class="grad-text">sound</span></h2></div>
    <div class="watch">
      <a class="video reveal" href="{E(yt)}" target="_blank" rel="noopener" aria-label="Watch on YouTube"><img src="assets/img/hero.webp" alt="" loading="lazy"><span class="big"><span>{PLAY}</span></span></a>
      <div class="panel reveal"><h3>Videos, previews &amp; studio sessions</h3><p>Watch new beat previews, music videos and studio clips from Sweet Galaxy Productions. Subscribe so you never miss a drop.</p><a class="btn btn-primary" href="{E(yt)}" target="_blank" rel="noopener" style="align-self:flex-start">{svg('youtube')} Open YouTube</a></div>
    </div>
  </div>
</section>

<section class="alt" id="about">
  <div class="wrap about">
    <div class="pic reveal"><img src="assets/img/drop.webp" alt="S.G.P logo in a water drop" loading="lazy"></div>
    <div class="reveal">
      <span class="eyebrow">About us</span>
      <h2>Sweet Galaxy <span class="grad-text">Productions</span></h2>
      {''.join(f'<p>{E(p)}</p>' for p in D['about'])}
      <div class="pills">{''.join(f'<span>{E(g)}</span>' for g in genres)}<span>Zaandam, NL</span></div>
    </div>
  </div>
</section>

<section id="social">
  <div class="wrap">
    <div class="head reveal"><span class="eyebrow">Social media</span><h2>Follow the <span class="grad-text">galaxy</span></h2><p>New beats, previews and behind-the-scenes.</p></div>
    <div class="socials">
{soc_cards}
      <a class="soc reveal" style="--c:#c7900c" href="mailto:{D['email']}"><span class="ic">{svg('mail')}</span><b>E-mail</b><span>{E(D['email'])}</span></a>
    </div>
  </div>
</section>

<section class="alt" id="contact">
  <div class="wrap">
    <div class="head reveal"><span class="eyebrow">Contact</span><h2>Let&#39;s make <span class="grad-text">music together</span></h2><p>Custom beats, bookings or questions about a license? Send a message.</p></div>
    <div class="contact">
      <div class="panel reveal">
        <h3>Sweet Galaxy Productions</h3>
        <a class="mail" href="mailto:{D['email']}">{E(D['email'])}</a>
        <p>Zaandam, The Netherlands<br>KvK {D['kvk']}</p>
        <a class="btn btn-ghost" href="{D['store']}" target="_blank" rel="noopener" style="align-self:flex-start">Beat store: mrgental.com</a>
      </div>
      <form class="panel reveal" id="contact-form" data-to="{D['email']}">
        <label>Name<input name="name" required autocomplete="name"></label>
        <label>E-mail<input name="email" type="email" required autocomplete="email"></label>
        <label>Topic<select name="topic"><option>Beat license</option><option>Custom beat</option><option>Booking</option><option>Other</option></select></label>
        <label>Message<textarea name="message" required></textarea></label>
        <button class="btn btn-primary" type="submit">Send message</button>
      </form>
    </div>
  </div>
</section>
</main>
<footer>
  <div class="wrap">
    <div>&copy; <span id="year">2026</span> Sweet Galaxy Productions &middot; KvK {D['kvk']}</div>
    <nav>{foot_soc} <a href="{D['store']}" target="_blank" rel="noopener">Beat store</a></nav>
  </div>
</footer>
<script src="assets/main.js?v={D['version']}" defer></script>
</body>
</html>
'''
(ROOT / "site" / "index.html").write_text(page, encoding="utf8")
print("built", len(page), "bytes,", len(beats), "beats")
