#!/usr/bin/env python3
"""Refresh WxCareers data from public sources -> data/jobs.json and site/jobs.json"""
import json, re, html, datetime, urllib.request, concurrent.futures as cf
UA={"User-Agent":"Mozilla/5.0 (WxCareers updater)"}
TODAY=datetime.date.today()
def get(url,data=None,hdr=None):
    r=urllib.request.Request(url,data=data,headers={**UA,**(hdr or {})})
    return urllib.request.urlopen(r,timeout=30).read().decode('utf-8','ignore')
STATES=dict(AL='Alabama',AK='Alaska',AZ='Arizona',AR='Arkansas',CA='California',CO='Colorado',CT='Connecticut',DE='Delaware',DC='District of Columbia',FL='Florida',GA='Georgia',HI='Hawaii',ID='Idaho',IL='Illinois',IN='Indiana',IA='Iowa',KS='Kansas',KY='Kentucky',LA='Louisiana',ME='Maine',MD='Maryland',MA='Massachusetts',MI='Michigan',MN='Minnesota',MS='Mississippi',MO='Missouri',MT='Montana',NE='Nebraska',NV='Nevada',NH='New Hampshire',NJ='New Jersey',NM='New Mexico',NY='New York',NC='North Carolina',ND='North Dakota',OH='Ohio',OK='Oklahoma',OR='Oregon',PA='Pennsylvania',RI='Rhode Island',SC='South Carolina',SD='South Dakota',TN='Tennessee',TX='Texas',UT='Utah',VT='Vermont',VA='Virginia',WA='Washington',WV='West Virginia',WI='Wisconsin',WY='Wyoming')
def state_of(loc):
    m=re.search(r',\s*([A-Z]{2})\b',loc)
    if m and m.group(1) in STATES: return m.group(1)
    for k,v in STATES.items():
        if v in loc: return k
    if re.search(r'remote',loc,re.I): return 'Remote'
    return 'Other'
def sector(title,emp):
    t=(title+' '+emp).lower()
    if re.search(r'air force|air national guard|national guard|army|navy|usafa|military',t): return 'military'
    if re.search(r'aviation|airline|faa|airport',t): return 'aviation'
    if re.search(r'university|college|institute',t): return 'academic'
    if re.search(r'energy|power|utility|wind farm|solar',t): return 'energy'
    if re.search(r'noaa|oceanic|national weather service|department of|federal',t): return 'federal'
    if re.search(r'\b[kw][a-z]{2,3}\b|tv|television|broadcast|news|media|gray|sinclair|nexstar|scripps|tegna|hearst|graham|telemundo|wtvd|cbs|nbc|abc|fox|reporter|forum communications',t): return 'TV'
    return 'private'
WX=re.compile(r'meteorolog|forecast|weather|atmospher|lightning|climat|hydrolog',re.I)
def rel(s):
    m=re.search(r'(\d+)\s+(hour|day)',s)
    if not m: return TODAY.isoformat()
    n=int(m.group(1)); return (TODAY-datetime.timedelta(days=n if m.group(2)=='day' else 0)).isoformat()
def ihire():
    out=[]
    for p in range(1,6):
        h=get(f"https://www.ihirebroadcasting.com/t-meteorologist-jobs.html?page={p}")
        cards=re.split(r'<div id="job-\d+" class="job-list-item',h)[1:]
        if not cards: break
        for c in cards:
            u=re.search(r'href="(/jobs/view/\d+)"',c); t=re.search(r'browse-jobs-jobclick">(.*?)</a>',c,re.S)
            e=re.search(r'title="View Company Profile">\s*<a[^>]*>(.*?)</a>',c,re.S) or re.search(r'fa-mountain-city[^>]*></i>\s*([^<]+?)\s*<',c,re.S)
            l=re.search(r'fa-location-dot[^>]*></i>(.*?)<',c,re.S); d=re.search(r'fa-calendar-clock[^>]*></i>(.*?)<',c,re.S)
            if not (u and t): continue
            title=html.unescape(re.sub('<.*?>','',t.group(1))).strip(); emp=html.unescape(e.group(1)).strip() if e else 'Confidential'
            if not WX.search(title): continue
            loc=l.group(1).strip() if l else ''
            out.append(dict(title=title,employer=emp,location=loc,salary=None,date_posted=rel(d.group(1) if d else ''),source='iHireBroadcasting',url="https://www.ihirebroadcasting.com"+u.group(1)))
    return out
def usajobs():
    out=[]
    for body in ({"JobCategoryCode":["1340"],"Page":1},{"Keyword":"meteorologist","Page":1},{"Keyword":"meteorological technician","Page":1}):
        d=json.loads(get("https://www.usajobs.gov/Search/ExecuteSearch",json.dumps(body).encode(),{"Content-Type":"application/json"}))
        for j in d.get('Jobs',[]):
            if not (WX.search(j['Title']) or any(c['Code']=='1340' for c in j.get('JobCategoryCode',[]))): continue
            m=re.search(r'Open (\d\d)/(\d\d)/(\d{4})',j.get('DateDisplay',''))
            out.append(dict(title=j['Title'],employer=j['Agency'],location=j['LocationDisplay'],salary=j.get('SalaryDisplay') or None,
              date_posted=f"{m.group(3)}-{m.group(1)}-{m.group(2)}" if m else None,source='USAJOBS',url=j['PositionURI'].replace(':443','')))
    return out
GH={'tomorrow':'Tomorrow.io','accuweather':'AccuWeather','spire':'Spire Global','theweathercompany':'The Weather Company'}
def greenhouse():
    out=[]
    for slug,name in GH.items():
        for j in json.loads(get(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"))['jobs']:
            if WX.search(j['title']):
                out.append(dict(title=j['title'].strip(),employer=name,location=j['location']['name'],salary=None,date_posted=j['updated_at'][:10],source='Greenhouse (employer careers page)',url=j['absolute_url']))
    return out
def alive(j):
    try: urllib.request.urlopen(urllib.request.Request(j['url'],headers=UA),timeout=20); return True
    except Exception: return False
EXCLUDE_TITLES=re.compile(r'funny weather reporter',re.I)   # curation: drop non-meteorology postings
SECTOR_OVERRIDES=[(re.compile(r'spire',re.I),re.compile(r'engineer|sales',re.I),'private')]  # (employer, title, sector)
def main():
    jobs=[]
    for f in (ihire,usajobs,greenhouse):
        try: r=f(); print(f.__name__,len(r)); jobs+=r
        except Exception as e: print(f.__name__,'FAILED',e)
    try: jobs=json.load(open('data/manual.json'))+jobs  # hand-collected employer pages
    except FileNotFoundError: pass
    seen=set(); uniq=[]
    for j in jobs:
        k2=(re.sub(r'\W','',j['title'].lower())[:20],j['location'][:6].lower())
        if j['url'] in seen or k2 in seen: continue
        seen.add(j['url']); seen.add(k2); uniq.append(j)
    with cf.ThreadPoolExecutor(12) as ex: ok=list(ex.map(alive,uniq))
    live=[j for j,o in zip(uniq,ok) if o]; print('dead dropped:',len(uniq)-len(live))
    live=[j for j in live if not EXCLUDE_TITLES.search(j['title'])]
    for j in live:
        j.setdefault('sector',sector(j['title'],j['employer']))
        for e,t,sec in SECTOR_OVERRIDES:
            if e.search(j['employer']) and t.search(j['title']): j['sector']=sec; j['state']=state_of(j['location'])
    live.sort(key=lambda j:j['date_posted'] or '',reverse=True)
    out=dict(updated=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='minutes'),count=len(live),jobs=live)
    import os
    for p in ['data/jobs.json','site/jobs.json']:
        json.dump(out,open(p,'w'),indent=1)
    print('saved',len(live))
if __name__=='__main__': main()
