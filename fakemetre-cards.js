function buildInstaPost(src){
  const cap=escH(src.say);
  const img=escH(src.img);
  const user=escH(src.imgUser||'nature_facts_viral');
  const loc=escH(src.imgLoc||'');
  const likes=escH(src.imgLikes||'47 382');
  const ago=escH(src.imgAgo||'2 days ago');
  return `<div class="fake-insta">
    <div class="fake-insta-hd">
      <div class="fake-insta-av">📱</div>
      <div class="fake-insta-info">
        <div class="fake-insta-uname">${user}</div>
        ${loc?`<div class="fake-insta-loc">${loc}</div>`:''}
      </div>
      <div class="fake-insta-dots">···</div>
    </div>
    <img class="fake-insta-img" src="${img}" alt="">
    <div class="fake-insta-acts">❤️ 💬 ✈️ &nbsp;&nbsp;&nbsp; 🔖</div>
    <div class="fake-insta-likes">❤️ ${likes} likes</div>
    <div class="fake-insta-cap"><b>${user}</b> ${cap}</div>
    <div class="fake-insta-date">${ago}</div>
  </div>`;
}
function buildForum(src){
  const isEn=lang==='en';
  const user=escH(src.forumUser||'Utilisateur42');
  const fname=escH(src.forumName||'forum.fr');
  const date=escH(src.forumDate||(isEn?'1 year ago':'il y a 1 an'));
  const body=escH(src.say);
  const ini=user.replace(/^u\//,'').substring(0,2).toUpperCase();
  return `<div class="fake-forum">
    <div class="fake-forum-hd">💬 <a>${fname}</a></div>
    <div class="fake-forum-post">
      <div class="fake-forum-meta">
        <div class="fake-forum-av">${ini}</div>
        <div>
          <div class="fake-forum-user">${user}</div>
          <div class="fake-forum-date">${date} · ${isEn?'Member':'Membre'}</div>
        </div>
      </div>
      <div class="fake-forum-body">${body}</div>
      <div class="fake-forum-foot">
        <span>👍 ${src.forumLikes||'12'}</span>
        <span>💬 ${isEn?'Reply':'Répondre'}</span>
        <span>🚩 ${isEn?'Report':'Signaler'}</span>
      </div>
    </div>
  </div>`;
}
function buildWhatsApp(src){
  const isEn=lang==='en';
  const sender=escH(src.waSender||'Contact');
  const time=escH(src.waTime||'12:47');
  const text=escH(src.say);
  const ini=sender.substring(0,1).toUpperCase();
  return `<div class="fake-wa">
    <div class="fake-wa-hd">
      <div class="fake-wa-av">${ini}</div>
      <div>
        <div class="fake-wa-name">${sender}</div>
        <div class="fake-wa-status">${isEn?'Online':'En ligne'}</div>
      </div>
    </div>
    <div class="fake-wa-body">
      <div class="fake-wa-fwd">↩ ${isEn?'Forwarded':'Transféré'}</div>
      <div class="fake-wa-bubble">
        <div class="fake-wa-text">${text}</div>
        <div class="fake-wa-time">${time} ✓✓</div>
      </div>
    </div>
  </div>`;
}
function buildGMaps(src){
  const isEn=lang==='en';
  const user=escH(src.gmapsUser||'Visiteur anonyme');
  const rating=src.gmapsRating||5;
  const place=escH(src.gmapsPlace||'');
  const date=escH(src.gmapsDate||(isEn?'3 months ago':'Il y a 3 mois'));
  const body=escH(src.say);
  const stars='★'.repeat(rating)+'☆'.repeat(5-rating);
  const ini=user.substring(0,2).toUpperCase();
  return `<div class="fake-gmaps">
    <div class="fake-gmaps-hd">
      <div class="fake-gmaps-av">${ini}</div>
      <div>
        <div class="fake-gmaps-user">${user}</div>
        <div class="fake-gmaps-date">${date}</div>
      </div>
    </div>
    <div class="fake-gmaps-stars">${stars}</div>
    ${place?`<div class="fake-gmaps-place">📍 ${place}</div>`:''}
    <div class="fake-gmaps-body">${body}</div>
    <div class="fake-gmaps-foot">
      <span>👍 ${isEn?'Helpful':'Utile'}</span>
      <span>🚩 ${isEn?'Report':'Signaler'}</span>
    </div>
  </div>`;
}
function buildTweet(src){
  const user=escH(src.tweetUser||'Utilisateur');
  const handle=escH(src.tweetHandle||'user');
  const likes=escH(src.tweetLikes||'1 204');
  const reposts=escH(src.tweetReposts||'387');
  const date=escH(src.tweetDate||(lang==='en'?'2h ago':'il y a 2 h'));
  const body=escH(src.say);
  return `<div class="fake-tweet">
    <div class="fake-tweet-hd">
      <div class="fake-tweet-av">🐦</div>
      <div class="fake-tweet-names">
        <div class="fake-tweet-name">${user}</div>
        <div class="fake-tweet-handle">@${handle}</div>
      </div>
      <div class="fake-tweet-x">𝕏</div>
    </div>
    <div class="fake-tweet-body">${body}</div>
    <div class="fake-tweet-foot">
      <span>💬 ${reposts}</span>
      <span>🔁 ${reposts}</span>
      <span>❤️ ${likes}</span>
      <span class="fake-tweet-date">${date}</span>
    </div>
  </div>`;
}
function buildBlog(src){
  const isEn=lang==='en';
  const title=escH(src.blogTitle||src.n);
  const author=escH(src.blogAuthor||(isEn?'Anonymous':'Anonyme'));
  const date=escH(src.blogDate||'');
  const readtime=escH(src.blogReadTime||'3');
  const site=escH(src.blogSite||src.n);
  const body=escH(src.say);
  return `<div class="fake-blog">
    <div class="fake-blog-hd">
      <div class="fake-blog-site">✏️ ${site}</div>
      <div class="fake-blog-title">${title}</div>
      <div class="fake-blog-meta">
        <span>👤 ${isEn?'by':'par'} ${author}</span>
        ${date?`<span>📅 ${date}</span>`:''}
        <span>⏱ ${readtime} ${isEn?'min read':'min de lecture'}</span>
      </div>
    </div>
    <div class="fake-blog-body">${body} <span class="fake-blog-more">${isEn?'Read more →':'Lire la suite →'}</span></div>
  </div>`;
}

function buildPress(src){
  const isEn=lang==='en';
  const outlet=escH(src.pressOutlet||src.n);
  const headline=escH(src.pressTitle||src.d||src.n);
  const author=escH(src.pressAuthor||(isEn?'Editorial staff':'Rédaction'));
  const date=escH(src.pressDate||'');
  const domain=escH(src.pressDomain||'');
  const body=escH(src.say);
  return `<div class="fake-press">
    <div class="fake-press-masthead">
      <span class="fake-press-outlet">📰 ${outlet}</span>
      ${domain?`<span class="fake-press-domain">🔒 ${domain}</span>`:''}
    </div>
    <div class="fake-press-kicker">${isEn?'FACT-CHECK':'VÉRIFICATION'}</div>
    <div class="fake-press-headline">${headline}</div>
    <div class="fake-press-byline">${isEn?'By':'Par'} ${author}${date?` · ${date}`:''}</div>
    <p class="fake-press-body">${body}</p>
  </div>`;
}
function buildStudy(src){
  const isEn=lang==='en';
  const journal=escH(src.studyJournal||src.n);
  const year=escH(src.studyYear||'');
  const authors=escH(src.studyAuthors||'et al.');
  const body=escH(src.say);
  return `<div class="fake-study">
    <div class="fake-study-hd">
      <span class="fake-study-badge">🔬 ${isEn?'PEER-REVIEWED':'REVUE À COMITÉ DE LECTURE'}</span>
    </div>
    <div class="fake-study-journal">${journal}${year?` (${year})`:''}</div>
    <div class="fake-study-authors">${authors}</div>
    <p class="fake-study-abstract"><span class="fake-study-abstract-tag">${isEn?'Abstract':'Résumé'}</span> ${body}</p>
    <div class="fake-study-foot">📄 ${isEn?'Peer-reviewed article':'Article évalué par des pairs'}</div>
  </div>`;
}
function buildGov(src){
  const isEn=lang==='en';
  const site=escH(src.govSite||src.n);
  const domain=escH(src.govDomain||'');
  const body=escH(src.say);
  const desc=escH(src.d||'');
  return `<div class="fake-gov">
    <div class="fake-gov-bar">
      <span>🏛️</span>
      <span class="fake-gov-site">${site}</span>
      ${domain?`<a href="https://${escH(src.govDomain)}" target="_blank" rel="noopener" class="fake-gov-domain">🔒 ${domain}</a>`:''}
      ${desc?`<span class="fake-gov-info" data-tooltip="${desc}">i</span>`:''}
    </div>
    <p class="fake-gov-body">${body}</p>
  </div>`;
}
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
function buildVideo(src){
  const isEn=lang==='en';
  const title=escH(src.videoTitle||src.n);
  const channel=escH(src.videoChannel||'');
  const views=escH(src.videoViews||'');
  const date=escH(src.videoDate||'');
  const vsrc=escH(src.videoSrc||'');
  const body=escH(src.say);
  const ini=channel.replace(/[^A-Za-z0-9]/g,'').substring(0,2).toUpperCase()||'YT';
  const meta=[views?`👁 ${views}`:'',date?`📅 ${date}`:''].filter(Boolean).join(' · ');
  return `<div class="fake-video"><div class="fake-video-player"><video controls preload="metadata" playsinline><source src="${vsrc}" type="video/mp4"></video></div><div class="fake-video-info"><div class="fake-video-title">${title}</div>${channel?`<div class="fake-video-channel"><div class="fake-video-channel-av">${ini}</div>${channel}</div>`:''} ${meta?`<div class="fake-video-meta">${meta}</div>`:''}<div class="fake-video-desc">${body}</div></div></div>`;
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
  if(src.videoSrc)                return {ic:'▶️',lab:isEn?'Viral video':'Vidéo virale',cls:'media'};
  return {ic:'🗣️',lab:isEn?'Testimony':'Témoignage',cls:'testi'};
}
