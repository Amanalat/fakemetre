import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\ASUS\Documents\Web apps\Jeux\fakemetre\index.html', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')

# ── Boundaries ──────────────────────────────────────────────────────────────
style_open  = content.index('<style>') + len('<style>')
style_close = content.index('</style>')
css_orig    = content[style_open:style_close]

builder_start = None
revealSay_ln  = None
for i, line in enumerate(lines):
    if 'function buildInstaPost' in line and builder_start is None:
        builder_start = i
    if 'function revealSay' in line and revealSay_ln is None:
        revealSay_ln = i
        break
builders_orig = '\n'.join(lines[builder_start:revealSay_ln])

# ── New CSS ──────────────────────────────────────────────────────────────────
NEW_CSS = """
/* ── Fake Media ── */
.fake-media{background:#0f0f0f;border-radius:12px;overflow:hidden;font-style:normal;color:#fff;border:1px solid #2a2a2a;}
.fake-media-banner{background:linear-gradient(160deg,#1a0d00 0%,#0a0a1a 100%);padding:14px 14px 10px;min-height:72px;position:relative;display:flex;flex-direction:column;justify-content:flex-end;}
.fake-media-bg-icon{position:absolute;right:12px;top:50%;transform:translateY(-50%);font-size:3.5rem;opacity:.12;}
.fake-media-type-badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:.58rem;font-weight:900;letter-spacing:.6px;text-transform:uppercase;margin-bottom:7px;width:fit-content;}
.fake-media-type-badge.film,.fake-media-type-badge.making-of{background:#e50914;color:#fff;}
.fake-media-type-badge.docu{background:#0071eb;color:#fff;}
.fake-media-type-badge.tv{background:#f7c948;color:#1a0a00;}
.fake-media-type-badge.youtube{background:#ff0000;color:#fff;}
.fake-media-type-badge.ted{background:#e62b1e;color:#fff;}
.fake-media-type-badge.game{background:#107c10;color:#fff;}
.fake-media-type-badge.opera,.fake-media-type-badge.art{background:#7b2d8b;color:#fff;}
.fake-media-title{font-size:1.05rem;font-weight:900;color:#fff;font-family:Georgia,serif;line-height:1.25;}
.fake-media-meta{font-size:.68rem;color:#888;margin-top:4px;}
.fake-media-body{padding:10px 14px 14px;font-size:.84rem;line-height:1.55;color:#ccc;margin:0;border-top:1px solid #222;}
/* ── Fake Book ── */
.fake-book{background:#fff;border-radius:12px;overflow:hidden;font-style:normal;color:#1a1a1a;border:1px solid #ddd;display:flex;}
.fake-book-spine{width:12px;flex-shrink:0;}
.fake-book-content{flex:1;padding:13px 13px 13px 11px;}
.fake-book-type{font-size:.58rem;font-weight:900;letter-spacing:1px;text-transform:uppercase;color:#888;margin-bottom:5px;}
.fake-book-title{font-size:.96rem;font-weight:800;line-height:1.3;color:#1a1a1a;font-family:Georgia,serif;margin-bottom:3px;}
.fake-book-author{font-size:.7rem;color:#555;font-style:italic;margin-bottom:9px;}
.fake-book-excerpt{font-size:.82rem;line-height:1.55;color:#444;font-style:italic;border-left:3px solid #ddd;padding-left:9px;}
.fake-book-foot{margin-top:9px;font-size:.67rem;color:#aaa;border-top:1px solid #eee;padding-top:7px;display:flex;gap:8px;flex-wrap:wrap;}
/* ── Fake Quote ── */
.fake-quote{background:#faf7f0;border-radius:12px;font-style:normal;color:#2a1a0a;border:1px solid #ddd3bf;padding:16px 16px 14px;}
.fake-quote-type{font-size:.58rem;font-weight:900;letter-spacing:1px;text-transform:uppercase;color:#a08060;margin-bottom:8px;}
.fake-quote-mark{font-size:3rem;font-family:Georgia,serif;color:#d4c4a0;line-height:.8;display:block;margin-bottom:4px;}
.fake-quote-text{font-family:Georgia,'Times New Roman',serif;font-size:.93rem;line-height:1.65;color:#2a1a0a;font-style:italic;padding:0 0 0 10px;border-left:3px solid #d4c4a0;margin:0;}
.fake-quote-origin{font-size:.67rem;color:#a08060;text-align:right;margin-top:8px;}
/* ── Fake Ad ── */
.fake-ad{background:#fff;border-radius:12px;overflow:hidden;font-style:normal;color:#1a1a1a;border:2px solid #eee;}
.fake-ad-header{display:flex;justify-content:space-between;align-items:center;padding:4px 10px;background:#f0f0f0;border-bottom:1px solid #e0e0e0;}
.fake-ad-label{font-size:.55rem;font-weight:900;letter-spacing:1.5px;color:#aaa;text-transform:uppercase;}
.fake-ad-brand{font-weight:900;font-size:.78rem;color:#1a1a1a;}
.fake-ad-visual{padding:16px 14px 10px;text-align:center;font-size:2.2rem;}
.fake-ad-slogan{font-size:.98rem;font-weight:900;color:#1a1a1a;padding:0 14px 4px;text-align:center;font-family:Arial,sans-serif;line-height:1.3;}
.fake-ad-body{font-size:.82rem;color:#444;padding:6px 14px 12px;line-height:1.5;text-align:center;}
.fake-ad-foot{background:#f8f8f8;padding:5px 14px;font-size:.6rem;color:#bbb;border-top:1px solid #eee;text-align:center;}
/* ── Fake Expert ── */
.fake-expert{background:#f7fafd;border-radius:12px;overflow:hidden;font-style:normal;color:#1a2733;border:1px solid #c8d8e8;}
.fake-expert-hd{background:#1e3a5f;padding:11px 14px;color:#fff;display:flex;align-items:center;gap:11px;}
.fake-expert-av{width:38px;height:38px;border-radius:50%;background:rgba(255,255,255,.12);display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0;}
.fake-expert-info{flex:1;}
.fake-expert-name{font-weight:800;font-size:.86rem;line-height:1.2;}
.fake-expert-cred{font-size:.66rem;color:#8bb8d8;margin-top:2px;}
.fake-expert-inst{font-size:.62rem;color:#6698b8;margin-top:1px;}
.fake-expert-body{padding:12px 14px;font-size:.84rem;line-height:1.55;color:#2a3a4a;font-style:italic;}
/* ── Fake Reddit ── */
.fake-reddit{background:#fff;border-radius:12px;overflow:hidden;font-style:normal;color:#1c1c1c;border:1px solid #ededed;}
.fake-reddit-bar{background:#ff4500;padding:6px 12px;display:flex;align-items:center;gap:7px;color:#fff;}
.fake-reddit-logo{font-weight:900;font-size:.78rem;}
.fake-reddit-sub{font-weight:800;font-size:.8rem;color:#ffe0d6;}
.fake-reddit-inner{display:flex;}
.fake-reddit-vote{display:flex;flex-direction:column;align-items:center;padding:10px 8px;background:#f8f9fa;min-width:40px;font-size:.65rem;font-weight:900;color:#ff4500;gap:3px;border-right:1px solid #ededed;flex-shrink:0;}
.fake-reddit-main{padding:10px 12px;flex:1;}
.fake-reddit-title{font-size:.86rem;font-weight:700;line-height:1.35;color:#1c1c1c;margin-bottom:5px;}
.fake-reddit-meta{font-size:.63rem;color:#878a8c;margin-bottom:7px;}
.fake-reddit-excerpt{font-size:.82rem;line-height:1.5;color:#333;background:#f8f9fa;padding:7px 9px;border-radius:5px;border-left:2px solid #ff4500;}
.fake-reddit-foot{padding:5px 12px;font-size:.66rem;color:#878a8c;border-top:1px solid #ededed;display:flex;gap:10px;}
/* ── Fake LinkedIn ── */
.fake-linkedin{background:#fff;border-radius:12px;overflow:hidden;font-style:normal;color:#1a1a1a;border:1px solid #e0e0e0;}
.fake-linkedin-hd{padding:12px 14px 8px;display:flex;gap:10px;align-items:flex-start;}
.fake-linkedin-av{width:42px;height:42px;border-radius:50%;background:linear-gradient(135deg,#0a66c2,#004182);display:flex;align-items:center;justify-content:center;font-size:1rem;flex-shrink:0;color:#fff;font-weight:900;}
.fake-linkedin-meta{flex:1;}
.fake-linkedin-name{font-weight:700;font-size:.86rem;color:#1a1a1a;line-height:1.2;}
.fake-linkedin-jobtitle{font-size:.7rem;color:#666;margin-top:1px;}
.fake-linkedin-date{font-size:.63rem;color:#888;margin-top:1px;}
.fake-linkedin-li-logo{width:20px;height:20px;background:#0a66c2;border-radius:3px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:.62rem;flex-shrink:0;}
.fake-linkedin-body{padding:0 14px 10px;font-size:.83rem;line-height:1.55;color:#333;}
.fake-linkedin-foot{border-top:1px solid #e0e0e0;padding:7px 14px;display:flex;gap:12px;font-size:.7rem;color:#555;align-items:center;}
/* ── Medium badge extensions ── */
.medium-badge.media{background:rgba(229,9,20,.18);color:#ff8080;}
.medium-badge.book{background:rgba(26,58,110,.22);color:#7bb0f0;}
.medium-badge.quote{background:rgba(160,128,96,.2);color:#c4a06a;}
.medium-badge.ad{background:rgba(255,107,53,.18);color:#ff9966;}
.medium-badge.expert{background:rgba(30,58,95,.22);color:#7bb8e8;}
"""

# ── New JS builders ──────────────────────────────────────────────────────────
NEW_BUILDERS = r"""
function buildMedia(src){
  const isEn=lang==='en';
  const type=(src.mediaType||'film').toLowerCase();
  const title=escH(src.mediaTitle||src.n);
  const year=escH(src.mediaYear||'');
  const director=escH(src.mediaDirector||'');
  const studio=escH(src.mediaStudio||src.mediaPlatform||'');
  const body=escH(src.say);
  const icons={film:'🎬',docu:'🎥','making-of':'🎬',tv:'📺',youtube:'▶️',ted:'💡',game:'🎮',opera:'🎭',art:'🖼️'};
  const labels={film:{fr:'FILM',en:'FILM'},'making-of':{fr:'MAKING-OF',en:'MAKING-OF'},docu:{fr:'DOCUMENTAIRE',en:'DOCUMENTARY'},tv:{fr:'ÉMISSION TV',en:'TV SHOW'},youtube:{fr:'VIDÉO YOUTUBE',en:'YOUTUBE VIDEO'},ted:{fr:'CONFÉRENCE TED',en:'TED TALK'},game:{fr:'JEU VIDÉO',en:'VIDEO GAME'},opera:{fr:'OPÉRA',en:'OPERA'},art:{fr:"ŒUVRE D'ART",en:'ARTWORK'}};
  const icon=icons[type]||'🎬';
  const label=(labels[type]||{fr:'MÉDIA',en:'MEDIA'})[isEn?'en':'fr'];
  const meta=[year,director,studio].filter(Boolean).join(' · ');
  return `<div class="fake-media"><div class="fake-media-banner"><div class="fake-media-bg-icon">${icon}</div><span class="fake-media-type-badge ${type}">${icon} ${label}</span><div class="fake-media-title">${title}</div>${meta?`<div class="fake-media-meta">${meta}</div>`:''}</div><p class="fake-media-body">${body}</p></div>`;
}
function buildBook(src){
  const isEn=lang==='en';
  const btype=(src.bookType||'livre').toLowerCase();
  const title=escH(src.bookTitle||src.n);
  const author=escH(src.bookAuthor||'');
  const year=escH(src.bookYear||'');
  const publisher=escH(src.bookPublisher||'');
  const body=escH(src.say);
  const spineColors={livre:'#1a3a6e',manuel:'#2a5a2a','encyclopédie':'#6a1a1a',roman:'#4a1a5a',guide:'#4a3a1a',encyclopedia:'#6a1a1a',textbook:'#2a5a2a',novel:'#4a1a5a',book:'#1a3a6e'};
  const typeLabels={livre:{fr:'LIVRE',en:'BOOK'},manuel:{fr:'MANUEL',en:'TEXTBOOK'},'encyclopédie':{fr:'ENCYCLOPÉDIE',en:'ENCYCLOPAEDIA'},roman:{fr:'ROMAN',en:'NOVEL'},guide:{fr:'GUIDE',en:'GUIDE'},encyclopedia:{fr:'ENCYCLOPÉDIE',en:'ENCYCLOPAEDIA'},textbook:{fr:'MANUEL',en:'TEXTBOOK'},novel:{fr:'ROMAN',en:'NOVEL'},book:{fr:'LIVRE',en:'BOOK'}};
  const spineColor=spineColors[btype]||'#1a3a6e';
  const typeLabel=(typeLabels[btype]||{fr:'LIVRE',en:'BOOK'})[isEn?'en':'fr'];
  const foot=[author?'✍️ '+author:'',year?'📅 '+year:'',publisher?'🏢 '+publisher:''].filter(Boolean).join(' · ');
  return `<div class="fake-book"><div class="fake-book-spine" style="background:${spineColor}"></div><div class="fake-book-content"><div class="fake-book-type">📖 ${typeLabel}</div><div class="fake-book-title">${title}</div>${author?`<div class="fake-book-author">${author}</div>`:''}<div class="fake-book-excerpt">${body}</div>${foot?`<div class="fake-book-foot">${foot}</div>`:''}</div></div>`;
}
function buildQuote(src){
  const isEn=lang==='en';
  const qtype=(src.quoteType||'proverbe').toLowerCase();
  const origin=escH(src.quoteOrigin||'');
  const body=escH(src.say);
  const typeLabels={proverbe:{fr:'PROVERBE',en:'PROVERB'},dicton:{fr:'DICTON',en:'SAYING'},expression:{fr:'EXPRESSION POPULAIRE',en:'POPULAR EXPRESSION'},croyance:{fr:'CROYANCE POPULAIRE',en:'POPULAR BELIEF'},intuition:{fr:'INTUITION PERSONNELLE',en:'PERSONAL INTUITION'}};
  const typeLabel=(typeLabels[qtype]||{fr:'SAGESSE POPULAIRE',en:'FOLK WISDOM'})[isEn?'en':'fr'];
  return `<div class="fake-quote"><div class="fake-quote-type">💬 ${typeLabel}</div><span class="fake-quote-mark">❝</span><p class="fake-quote-text">${body}</p>${origin?`<div class="fake-quote-origin">— ${origin}</div>`:''}</div>`;
}
function buildAd(src){
  const isEn=lang==='en';
  const atype=(src.adType||'tv').toLowerCase();
  const brand=escH(src.adBrand||src.n);
  const slogan=escH(src.adSlogan||'');
  const body=escH(src.say);
  const typeLabels={tv:{fr:'PUBLICITÉ TÉLÉVISÉE',en:'TV ADVERTISEMENT'},packaging:{fr:'EMBALLAGE PRODUIT',en:'PRODUCT PACKAGING'},store:{fr:'COMMUNICATION COMMERCIALE',en:'COMMERCIAL COMMUNICATION'},web:{fr:'PUBLICITÉ EN LIGNE',en:'ONLINE ADVERTISEMENT'},print:{fr:'PUBLICITÉ PRESSE',en:'PRINT ADVERTISEMENT'}};
  const emojis={tv:'📺',packaging:'🛒',store:'🏪',web:'💻',print:'📄'};
  const typeLabel=(typeLabels[atype]||{fr:'PUBLICITÉ',en:'ADVERTISEMENT'})[isEn?'en':'fr'];
  const emoji=emojis[atype]||'📢';
  return `<div class="fake-ad"><div class="fake-ad-header"><span class="fake-ad-label">📢 ${isEn?'Advertisement':'Publicité'}</span><span class="fake-ad-brand">${brand}</span></div><div class="fake-ad-visual">${emoji}</div>${slogan?`<div class="fake-ad-slogan">&ldquo;${slogan}&rdquo;</div>`:''}<p class="fake-ad-body">${body}</p><div class="fake-ad-foot">${typeLabel}</div></div>`;
}
function buildExpert(src){
  const isEn=lang==='en';
  const name=escH(src.expertName||src.n);
  const cred=escH(src.expertTitle||src.d||'');
  const inst=escH(src.expertInstitution||'');
  const body=escH(src.say);
  const lc=(cred+name).toLowerCase();
  const av=lc.includes('vétér')||lc.includes('veter')?'🐾':lc.includes('astronaute')||lc.includes('astronaut')?'🚀':lc.includes('botanist')||lc.includes('botaniste')?'🌿':lc.includes('météo')||lc.includes('weather')?'🌤️':lc.includes('archéo')||lc.includes('archeo')?'🏺':lc.includes('ingénieur')||lc.includes('engineer')?'⚙️':lc.includes('historien')||lc.includes('historian')?'📜':lc.includes('coach')?'🎯':lc.includes('nutritio')?'🥗':lc.includes('neurolog')?'🧠':lc.includes('pédiatr')||lc.includes('pediatr')?'👶':lc.includes('sage-femme')||lc.includes('midwife')?'🤱':lc.includes('chimiste')||lc.includes('chemist')?'⚗️':lc.includes('policier')||lc.includes('police')?'👮':lc.includes('entomolog')?'🦋':'🧑‍⚕️';
  return `<div class="fake-expert"><div class="fake-expert-hd"><div class="fake-expert-av">${av}</div><div class="fake-expert-info"><div class="fake-expert-name">${name}</div>${cred?`<div class="fake-expert-cred">🎓 ${cred}</div>`:''}${inst?`<div class="fake-expert-inst">🏥 ${inst}</div>`:''}</div></div><div class="fake-expert-body">${body}</div></div>`;
}
function buildReddit(src){
  const isEn=lang==='en';
  const sub=escH(src.redditSub||'r/discussion');
  const user=escH(src.redditUser||'u/anonyme');
  const upvotes=escH(String(src.redditUpvotes||'1.2k'));
  const comments=escH(String(src.redditComments||'47'));
  const title=escH(src.redditTitle||src.d||src.n);
  const body=escH(src.say);
  return `<div class="fake-reddit"><div class="fake-reddit-bar"><span class="fake-reddit-logo">Reddit</span><span class="fake-reddit-sub">${sub}</span></div><div class="fake-reddit-inner"><div class="fake-reddit-vote">▲<br>${upvotes}<br>▼</div><div class="fake-reddit-main"><div class="fake-reddit-title">${title}</div><div class="fake-reddit-meta">👤 ${user}</div><div class="fake-reddit-excerpt">${body}</div></div></div><div class="fake-reddit-foot"><span>💬 ${comments} ${isEn?'comments':'commentaires'}</span><span>🔗 ${isEn?'Share':'Partager'}</span></div></div>`;
}
function buildLinkedIn(src){
  const isEn=lang==='en';
  const user=escH(src.linkedinUser||src.n);
  const jobtitle=escH(src.linkedinTitle||src.d||'');
  const likes=escH(String(src.linkedinLikes||'8 742'));
  const date=escH(src.linkedinDate||(isEn?'3 days ago':'Il y a 3 jours'));
  const body=escH(src.say);
  const ini=user.split(/\s+/).slice(0,2).map(w=>w[0]||'').join('').toUpperCase()||'?';
  return `<div class="fake-linkedin"><div class="fake-linkedin-hd"><div class="fake-linkedin-av">${ini}</div><div class="fake-linkedin-meta"><div class="fake-linkedin-name">${user}</div>${jobtitle?`<div class="fake-linkedin-jobtitle">${jobtitle}</div>`:''}<div class="fake-linkedin-date">${date} · 🌐</div></div><div class="fake-linkedin-li-logo">in</div></div><div class="fake-linkedin-body">${body}</div><div class="fake-linkedin-foot"><span>👍 ${likes}</span><span>💬 ${isEn?'Comments':'Commentaires'}</span><span>↗️ ${isEn?'Repost':'Repartager'}</span></div></div>`;
}
function srcMedium(src){
  const isEn=lang==='en';
  if(src.studyJournal)            return {ic:'🔬',lab:isEn?'Scientific study':'Étude scientifique',cls:'sci'};
  if(src.govSite)                 return {ic:'🏛️',lab:isEn?'Official site':'Site officiel',cls:'gov'};
  if(src.pressOutlet)             return {ic:'📰',lab:isEn?'Press · Fact-check':'Presse · Fact-check',cls:'press'};
  if(src.mediaTitle||src.mediaType){const t=src.mediaType||'film';const m={film:'🎬',docu:'🎥','making-of':'🎬',tv:'📺',youtube:'▶️',ted:'💡',game:'🎮',opera:'🎭',art:'🖼️'};return {ic:m[t]||'🎬',lab:isEn?'Media':'Média',cls:'media'};}
  if(src.bookTitle||src.bookType) return {ic:'📖',lab:isEn?'Book':'Livre',cls:'book'};
  if(src.quoteType)               return {ic:'💬',lab:isEn?'Proverb / Belief':'Proverbe / Croyance',cls:'quote'};
  if(src.adType)                  return {ic:'📢',lab:isEn?'Advertisement':'Publicité',cls:'ad'};
  if(src.expertTitle)             return {ic:'🧑‍⚕️',lab:isEn?'Expert':'Expert',cls:'expert'};
  if(src.imgUser||src.tweetUser)  return {ic:'📱',lab:isEn?'Social media':'Réseau social',cls:'social'};
  if(src.forumUser)               return {ic:'💬',lab:isEn?'Forum':'Forum',cls:'social'};
  if(src.waForwarded)             return {ic:'💬',lab:isEn?'Private message':'Message privé',cls:'social'};
  if(src.gmapsUser)               return {ic:'⭐',lab:isEn?'Online review':'Avis en ligne',cls:'social'};
  if(src.blogTitle)               return {ic:'✏️',lab:isEn?'Blog':'Blog',cls:'blog'};
  if(src.redditSub)               return {ic:'🔴',lab:'Reddit',cls:'social'};
  if(src.linkedinUser)            return {ic:'💼',lab:'LinkedIn',cls:'social'};
  return {ic:'🗣️',lab:isEn?'Testimony':'Témoignage',cls:'testi'};
}
"""

# ── Write fakemetre.css ──────────────────────────────────────────────────────
css_full = css_orig + NEW_CSS
with open(r'C:\Users\ASUS\Documents\Web apps\Jeux\fakemetre\fakemetre.css', 'w', encoding='utf-8') as f:
    f.write(css_full)
print(f'fakemetre.css: {len(css_full)} chars')

# ── Write fakemetre-cards.js ─────────────────────────────────────────────────
# Remove srcMedium from builders_orig (it ends the extracted block)
sm_idx = builders_orig.index('\nfunction srcMedium')
builders_without_srm = builders_orig[:sm_idx]
cards_js = builders_without_srm + '\n' + NEW_BUILDERS.strip() + '\n'
with open(r'C:\Users\ASUS\Documents\Web apps\Jeux\fakemetre\fakemetre-cards.js', 'w', encoding='utf-8') as f:
    f.write(cards_js)
print(f'fakemetre-cards.js: {len(cards_js)} chars')

# ── Patch index.html ─────────────────────────────────────────────────────────
new_html = content

# 1. Replace <style>...</style> with <link>
new_html = (new_html[:new_html.index('<style>')] +
            '<link rel="stylesheet" href="fakemetre.css">' +
            new_html[new_html.index('</style>') + len('</style>'):])

# 2. Remove builders block + add reference comment
bstart2 = new_html.index('function buildInstaPost')
rend2   = new_html.index('function revealSay')
new_html = new_html[:bstart2] + '// Card builders -> fakemetre-cards.js\n' + new_html[rend2:]

# 3. Add <script src="fakemetre-cards.js"> just before the inline <script> block
cf_marker = '</script><script>'
cf_idx = new_html.index(cf_marker)
new_html = (new_html[:cf_idx + len('</script>')] +
            '<script src="fakemetre-cards.js"></script><script>' +
            new_html[cf_idx + len(cf_marker):])

# 4. Patch openSrc dispatch
OLD_DISPATCH = "  } else if(src.govSite){\n    sayEl.className='';sayEl.style.cssText='margin-bottom:16px;';\n    sayEl.innerHTML=buildGov(src);\n  } else {"
NEW_DISPATCH = """  } else if(src.govSite){
    sayEl.className='';sayEl.style.cssText='margin-bottom:16px;';
    sayEl.innerHTML=buildGov(src);
  } else if(src.mediaTitle||src.mediaType){
    sayEl.className='';sayEl.style.cssText='margin-bottom:16px;';
    sayEl.innerHTML=buildMedia(src);
  } else if(src.bookTitle||src.bookType){
    sayEl.className='';sayEl.style.cssText='margin-bottom:16px;';
    sayEl.innerHTML=buildBook(src);
  } else if(src.quoteType){
    sayEl.className='';sayEl.style.cssText='margin-bottom:16px;';
    sayEl.innerHTML=buildQuote(src);
  } else if(src.adType){
    sayEl.className='';sayEl.style.cssText='margin-bottom:16px;';
    sayEl.innerHTML=buildAd(src);
  } else if(src.expertTitle){
    sayEl.className='';sayEl.style.cssText='margin-bottom:16px;';
    sayEl.innerHTML=buildExpert(src);
  } else if(src.redditSub){
    sayEl.className='';sayEl.style.cssText='margin-bottom:16px;';
    sayEl.innerHTML=buildReddit(src);
  } else if(src.linkedinUser){
    sayEl.className='';sayEl.style.cssText='margin-bottom:16px;';
    sayEl.innerHTML=buildLinkedIn(src);
  } else {"""

if OLD_DISPATCH in new_html:
    new_html = new_html.replace(OLD_DISPATCH, NEW_DISPATCH, 1)
    print('openSrc dispatch patched OK')
else:
    # Try to find it
    idx = new_html.find('buildGov(src);\n  } else {')
    print(f'Dispatch not found exactly. buildGov+else at: {idx}')
    if idx > 0:
        print(repr(new_html[idx-200:idx+50]))

with open(r'C:\Users\ASUS\Documents\Web apps\Jeux\fakemetre\index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

sz = len(new_html)
ln = new_html.count('\n')
print(f'index.html: {sz} chars ({round(sz/1024,1)} KB), {ln} lines')
