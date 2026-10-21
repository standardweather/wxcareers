#!/usr/bin/env python3
"""Build the WxCareers blog: blog-src/*.md -> site/blog/, site/blog/feed.xml, site/sitemap.xml.
No dependencies. Front matter: title, date (YYYY-MM-DD), description, optional slug, optional draft: true.
Files starting with '_' and README.md are ignored."""
import re, html, datetime, pathlib, email.utils
ROOT=pathlib.Path(__file__).resolve().parent.parent
SRC=ROOT/'blog-src'; SITE=ROOT/'site'; OUT=SITE/'blog'; BASE='https://wxcareers.com'
esc=lambda s: html.escape(str(s), quote=True)

def inline(t):
    t=html.escape(t, quote=False)
    t=re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t=re.sub(r'!\[([^\]]*)\]\(([^)\s]+)\)', r'<img src="\2" alt="\1" loading="lazy">', t)
    t=re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', r'<a href="\2">\1</a>', t)
    t=re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t=re.sub(r'(?<![*\w])\*([^*]+)\*(?!\w)', r'<em>\1</em>', t)
    return t

def md(src):
    out=[]; para=[]; lst=None; code=None
    def flush():
        nonlocal para, lst
        if para: out.append('<p>'+inline(' '.join(para))+'</p>'); para=[]
        if lst: out.append(f'<{lst[0]}>'+''.join(f'<li>{inline(i)}</li>' for i in lst[1])+f'</{lst[0]}>'); lst=None
    for line in src.splitlines():
        if code is not None:
            if line.startswith('```'): out.append('<pre><code>'+html.escape('\n'.join(code))+'</code></pre>'); code=None
            else: code.append(line)
            continue
        if line.startswith('```'): flush(); code=[]; continue
        s=line.strip()
        if not s: flush(); continue
        m=re.match(r'(#{1,4})\s+(.*)', s)
        if m: flush(); n=min(max(len(m.group(1)),2),4); out.append(f'<h{n}>{inline(m.group(2))}</h{n}>'); continue
        if s.startswith('>'): flush(); out.append('<blockquote><p>'+inline(s.lstrip('> '))+'</p></blockquote>'); continue
        m=re.match(r'([-*]|\d+\.)\s+(.*)', s)
        if m:
            kind='ol' if m.group(1)[0].isdigit() else 'ul'
            if para: flush()
            if lst and lst[0]!=kind: flush()
            lst=lst or (kind, []); lst[1].append(m.group(2)); continue
        if lst: flush()
        para.append(s)
    flush(); return '\n'.join(out)

def parse(p):
    t=p.read_text(encoding='utf-8'); meta={}
    m=re.match(r'---\s*\n(.*?)\n---\s*\n', t, re.S)
    if m:
        for l in m.group(1).splitlines():
            if ':' in l: k,v=l.split(':',1); meta[k.strip().lower()]=v.strip().strip('"\'')
        t=t[m.end():]
    if meta.get('draft','').lower()=='true': return None
    for k in ('title','date','description'):
        if not meta.get(k): raise SystemExit(f'{p.name}: missing front matter "{k}"')
    d=datetime.date.fromisoformat(meta['date'])
    slug=meta.get('slug') or re.sub(r'^\d{4}-\d\d-\d\d-','',p.stem)
    slug=re.sub(r'[^a-z0-9-]+','-',slug.lower()).strip('-')
    return dict(title=meta['title'], date=d, description=meta['description'], slug=slug, body=md(t))

def chrome():
    """Reuse the live site's header/footer from site/index.html so the blog always matches the design."""
    s=(SITE/'index.html').read_text(encoding='utf-8')
    head_links=re.search(r'<meta name=theme-color.*?</head>', s, re.S).group(0).replace('</head>','')
    top=re.search(r'<a class=skip.*?</header>', s, re.S).group(0)
    foot=re.search(r'<footer class=site-footer>.*?</footer>', s, re.S).group(0)
    navjs=re.search(r'<script>\(function\(\)\{var b=.*?</script>', s, re.S).group(0)
    def rel(x, depth):
        pre='../'*depth
        x=re.sub(r'(href|src)=("?)(?!https?:|#|mailto:|/|\.\./)([^"\s>]+)', lambda m: f'{m.group(1)}={m.group(2)}{pre}{m.group(3)}', x)
        return x
    def page(depth, title, desc, url, body, kind='website', extra=''):
        t=re.sub(r' class=on aria-current=page','',top)
        t=t.replace('<li><a href=blog/>Blog</a>','<li><a href=blog/ class=on aria-current=page>Blog</a>')
        return ('<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">'
          f'<title>{esc(title)}</title><link rel=canonical href="{url}"><meta name=description content="{esc(desc)}">'
          f'<meta property=og:title content="{esc(title)}"><meta property=og:description content="{esc(desc)}"><meta property=og:type content={kind}>'
          f'<meta property=og:site_name content=WxCareers><meta property=og:url content="{url}">{extra}'
          + rel(head_links, depth) + '</head><body>\n' + rel(t, depth) + '\n<main id=main>' + body + '</main>' + rel(foot, depth) + navjs + '</body></html>\n')
    return page

def human(d): return d.strftime('%b ') + str(d.day) + d.strftime(', %Y')

def main():
    page=chrome()
    posts=[p for p in (parse(f) for f in sorted(SRC.glob('*.md')) if not f.name.startswith('_') and f.name.lower()!='readme.md') if p]
    posts.sort(key=lambda p:(p['date'],p['title']), reverse=True)
    if len({p['slug'] for p in posts})!=len(posts): raise SystemExit('duplicate slugs')
    OUT.mkdir(parents=True, exist_ok=True)
    keep={'index.html','feed.xml'}|{p['slug'] for p in posts}
    for old in OUT.iterdir():   # remove pages for deleted/drafted posts
        if old.name not in keep and old.is_dir() and (old/'index.html').exists():
            (old/'index.html').unlink(); old.rmdir()
    for p in posts:
        url=f"{BASE}/blog/{p['slug']}/"
        ld=f'<meta property=article:published_time content="{p["date"].isoformat()}">'
        body=(f'<section class="hero hero-sm"><div class=wrap><p class=post-date><time datetime="{p["date"].isoformat()}">{human(p["date"])}</time></p>'
              f'<h1>{esc(p["title"])}</h1><p class=hero-lede>{esc(p["description"])}</p></div></section>'
              f'<section class="wrap content"><article class=article>{p["body"]}<p><a class=back href="../">← All posts</a></p></article></section>')
        d=OUT/p['slug']; d.mkdir(exist_ok=True)
        (d/'index.html').write_text(page(2, f"{p['title']} | WxCareers Blog", p['description'], url, body, 'article', ld), encoding='utf-8')
    if posts:
        lst='<div class=post-list>'+''.join(f'<article class=post-card><p class=post-date><time datetime="{p["date"].isoformat()}">{human(p["date"])}</time></p><h2><a href="{p["slug"]}/">{esc(p["title"])}</a></h2><p>{esc(p["description"])}</p></article>' for p in posts)+'</div>'
    else:
        lst=('<div class=coming-soon><svg viewBox="0 0 32 32" width=40 height=40 aria-hidden=true><circle cx=12 cy=12 r=6 fill="#F5A524"/><path d="M10 27h14a5 5 0 0 0 .6-9.96A7 7 0 0 0 11.3 19 4 4 0 0 0 10 27z" fill="#fff" stroke="#0B5FD9" stroke-width=2 /></svg>'
             '<h2>First post coming soon</h2><p>Notes on meteorology hiring, pay, and careers, written by a meteorologist. Get it in The WxCareers Weekly, every Tuesday morning.</p>'
             '<div class=cta-row style="justify-content:center"><a class="btn btn-primary" href="../newsletter.html">Get The WxCareers Weekly</a><a class="btn btn-secondary" href="../index.html">Browse jobs</a></div></div>')
    body=('<section class="hero hero-sm"><div class=wrap><h1>The WxCareers Blog</h1><p class=hero-lede>Notes on meteorology jobs, pay, and careers across broadcast, NWS and federal, private, aviation, military, and academic work.</p></div></section>'
          f'<section class="wrap content">{lst}<p class=meta><a href="feed.xml">RSS feed</a></p></section>')
    (OUT/'index.html').write_text(page(1,'Blog | WxCareers','Notes on meteorology jobs, pay, and careers from WxCareers.',f'{BASE}/blog/',body), encoding='utf-8')
    now=email.utils.format_datetime(datetime.datetime.now(datetime.timezone.utc))
    items=''.join(f'<item><title>{esc(p["title"])}</title><link>{BASE}/blog/{p["slug"]}/</link><guid isPermaLink="true">{BASE}/blog/{p["slug"]}/</guid>'
        f'<pubDate>{email.utils.format_datetime(datetime.datetime.combine(p["date"],datetime.time(10),datetime.timezone.utc))}</pubDate><description>{esc(p["description"])}</description></item>' for p in posts)
    (OUT/'feed.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>'
        f'<title>WxCareers Blog</title><link>{BASE}/blog/</link><description>Notes on meteorology jobs, pay, and careers.</description><language>en-us</language>'
        f'<atom:link href="{BASE}/blog/feed.xml" rel="self" type="application/rss+xml"/><lastBuildDate>{now}</lastBuildDate>{items}</channel></rss>\n', encoding='utf-8')
    urls=[f'{BASE}/',f'{BASE}/salaries.html',f'{BASE}/post.html',f'{BASE}/newsletter.html',f'{BASE}/blog/']
    sm=''.join(f'<url><loc>{u}</loc></url>' for u in urls)+''.join(f'<url><loc>{BASE}/blog/{p["slug"]}/</loc><lastmod>{p["date"].isoformat()}</lastmod></url>' for p in posts)
    (SITE/'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n', encoding='utf-8')
    (SITE/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n')
    print(f'built {len(posts)} post(s), blog index, feed.xml, sitemap.xml ({len(urls)+len(posts)} urls)')
if __name__=='__main__': main()
