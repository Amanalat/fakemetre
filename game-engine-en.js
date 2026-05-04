
// ═══════════════════════════════════════════════
// GAME STATE
// ═══════════════════════════════════════════════
let QS=[], qi=0, score=0, meter=50, uc=0, sh=[], um={}, pend=null, gameMode=5, currentLevel='junior';
let dragging=false, miniDragging=false, tempMeter=50;
let playingCustom=false;
let playingCommunity=false;
let cursorTutorialSeen=false; // Show the slider tutorial only once

// Detailed history for the personalized report
let gameHistory = [];
// Structure: { question, userVote, correctAnswer, hasNuance, sourceEvals: [{src, likertScore, isGoodSource}] }

// Load tutorial state from localStorage
try {
  cursorTutorialSeen = localStorage.getItem('fakemetre_cursor_tutorial_seen') === 'true';
} catch(e) {}

const $=id=>document.getElementById(id);
function show(id){$('ov').classList.add('show');$(id).classList.add('show');}
function hide(id){$(id).classList.remove('show');if(!['msrc','mfb','mvr','mfb-meter','mhint-cursor'].some(m=>$(m).classList.contains('show')))$('ov').classList.remove('show');}
function shuf(a){return[...a].sort(()=>Math.random()-.5);}

// ── Navigation niveaux/modes ──
function chooseLevel(level){
  currentLevel=level;
  $('levelscreen').style.display='none';
  $('modescreen').style.display='block';
  if(level==='junior'){
    $('modescreen-title').textContent = '🔎 Apprentice Detective — Choose your mode';
  } else if(level==='inter'){
    $('modescreen-title').textContent = '🕵️ Junior Investigator — Choose your mode';
  } else {
    $('modescreen-title').textContent = '⚡ Advanced Fact-Checker — Choose your mode';
  }
}

function backToLevel(){
  $('modescreen').style.display='none';
  $('levelscreen').style.display='block';
}

function chooseMode(){
  $('final').style.display='none';
  if(playingCommunity){
    playingCommunity=false;
    playingCustom=false;
    $('communityscreen').style.display='block';
  } else if(playingCustom){
    playingCustom=false;
    $('creatorscreen').style.display='block';
    switchCreatorTab('play');
  } else {
    $('levelscreen').style.display='block';
  }
}

function backToMenu(){
  if(confirm('⚠️ Leave the current game? Your progress will be lost.')){
    $('game').style.display='none';
    $('scorebar').style.display='none';
    $('dots').style.display='none';
    $('final').style.display='none';
    if(playingCommunity){
      playingCommunity=false;
      playingCustom=false;
      $('communityscreen').style.display='block';
    } else if(playingCustom){
      playingCustom=false;
      $('creatorscreen').style.display='block';
    } else {
      $('levelscreen').style.display='block';
    }
  }
}

// ── Start the game ──
function startGame(mode){
  gameMode=mode;
  playingCustom=false;
  let pool;
  if(currentLevel==='pro') pool=QUESTIONS_PRO;
  else if(currentLevel==='inter') pool=QUESTIONS_INTER;
  else pool=QUESTIONS_JUNIOR;
  const all=[...pool];
  QS = mode===5 ? shuf(all).slice(0,5) : shuf(all).slice(0,10);
  qi=0;score=0;meter=50;
  gameHistory=[]; // Reset history for the report
  $('modescreen').style.display='none';
  $('scorebar').style.display='flex';
  $('dots').style.display='flex';
  $('game').style.display='block';
  $('qtotal').textContent=QS.length;
  initMeterDrag();
  renderQ();
}

function restart(){
  $('final').style.display='none';
  gameHistory=[]; // Reset history
  if(playingCustom){
    // Replay custom questions
    QS = shuf([...customQuestions]);
    qi = 0; score = 0; meter = 50;
    $('scorebar').style.display = 'flex';
    $('dots').style.display = 'flex';
    $('game').style.display = 'block';
    $('qtotal').textContent = QS.length;
    initMeterDrag();
    renderQ();
  } else {
    startGame(gameMode);
  }
}

// ── Meter drag ──
function initMeterDrag(){
  const bg=$('mbg');
  function getPos(e){
    const rect=bg.getBoundingClientRect();
    const clientX=e.touches?e.touches[0].clientX:e.clientX;
    return Math.max(3,Math.min(97,(clientX-rect.left)/rect.width*100));
  }
  function onMove(e){if(!dragging)return;e.preventDefault();meter=getPos(e);updMeter();}
  function onDown(e){dragging=true;meter=getPos(e);updMeter();}
  function onUp(){dragging=false;}
  bg.addEventListener('mousedown',onDown);
  window.addEventListener('mousemove',onMove);
  window.addEventListener('mouseup',onUp);
  bg.addEventListener('touchstart',onDown,{passive:true});
  window.addEventListener('touchmove',onMove,{passive:false});
  window.addEventListener('touchend',onUp);
}

function openMeterAdjust(){
  hide('mfb');
  tempMeter=meter;
  updMiniMeter(tempMeter);
  show('mfb-meter');
  initMiniMeterDrag();
}

function confirmMeterAdjust(){
  meter=tempMeter;
  updMeter();
  hide('mfb-meter');
}

function updMiniMeter(p){
  p=Math.max(3,Math.min(97,p));
  $('mini-mfill').style.width=p+'%';
  $('mini-mcursor').style.left=p+'%';
  const s=$('mini-mstatus');
  if(p<33){$('mini-mfill').style.background='linear-gradient(90deg,#f75f5f,#f7a548)';s.textContent='⬅️ Rather FALSE';s.style.color='#f75f5f';}
  else if(p>66){$('mini-mfill').style.background='linear-gradient(90deg,#3ecf8e,#4fa3f7)';s.textContent='Rather TRUE ➡️';s.style.color='#3ecf8e';}
  else{$('mini-mfill').style.background='linear-gradient(90deg,#f7c948,#4fa3f7)';s.textContent='🤔 Unsure...';s.style.color='#f7c948';}
}

let miniListenersAdded=false;
function initMiniMeterDrag(){
  if(miniListenersAdded)return;
  miniListenersAdded=true;
  const bg=$('mini-mbg');
  function getPos(e){
    const rect=bg.getBoundingClientRect();
    const clientX=e.touches?e.touches[0].clientX:e.clientX;
    return Math.max(3,Math.min(97,(clientX-rect.left)/rect.width*100));
  }
  function onMove(e){if(!miniDragging)return;e.preventDefault();tempMeter=getPos(e);updMiniMeter(tempMeter);}
  function onDown(e){miniDragging=true;tempMeter=getPos(e);updMiniMeter(tempMeter);}
  function onUp(){miniDragging=false;}
  bg.addEventListener('mousedown',onDown);
  window.addEventListener('mousemove',onMove);
  window.addEventListener('mouseup',onUp);
  bg.addEventListener('touchstart',onDown,{passive:true});
  window.addEventListener('touchmove',onMove,{passive:false});
  window.addEventListener('touchend',onUp);
}

function updMeter(){
  const p=Math.max(3,Math.min(97,meter));
  $('mfill').style.width=p+'%';
  $('mcursor').style.left=p+'%';
  const s=$('mstatus');
  if(p<33){$('mfill').style.background='linear-gradient(90deg,#f75f5f,#f7a548)';s.textContent='⬅️ Rather FALSE';s.style.color='#f75f5f';}
  else if(p>66){$('mfill').style.background='linear-gradient(90deg,#3ecf8e,#4fa3f7)';s.textContent='Rather TRUE ➡️';s.style.color='#3ecf8e';}
  else{$('mfill').style.background='linear-gradient(90deg,#f7c948,#4fa3f7)';s.textContent='🤔 Unsure...';s.style.color='#f7c948';}
}

function updDots(){
  const w=$('dots');w.innerHTML='';
  QS.forEach((_,i)=>{const d=document.createElement('div');d.className='dot'+(i<qi?' done':i===qi?' active':'');w.appendChild(d);});
}

function updCounter(){
  const total=sh.length;
  const remaining=total-uc;
  if(uc===0) $('counter').textContent=`Check at least 1 source before voting (${total} disponibles)`;
  else if(remaining>0) $('counter').textContent=`✅ You can vote or check ${remaining} more source${remaining>1?'s':''}!`;
  else $('counter').textContent=`✅ You have evaluated all the sources. It’s up to you to decide!`;
}

function renderQ(){
  const q=QS[qi];
  meter=50;uc=0;um={};
  $('stxt').textContent=q.s;
  $('qn').textContent=qi+1;
  $('sc').textContent=score;
  $('vzone').style.display='none';
  updMeter();updDots();updCounter();
  // Show the "No consensus" button on ALL questions in pro level
  const btnConsensus = $('btn-consensus');
  if(btnConsensus){
    btnConsensus.style.display = (currentLevel==='pro') ? 'block' : 'none';
  }
  // Show slider tutorial only if not already seen AND on the first question of the game
  if((currentLevel==='pro'||currentLevel==='inter')&&qi===0&&!cursorTutorialSeen){
    setTimeout(()=>show('mhint-cursor'),200);
  }
  sh=shuf(q.src);
  const g=$('sgrid');g.innerHTML='';
  sh.forEach((src,i)=>{
    const b=document.createElement('button');
    b.className='sbtn';b.id='sb'+i;
    b.innerHTML=`<span class="semoji">${src.em}</span><div><div class="sname">${src.n}</div><div class="sdesc">${src.d}</div></div>`;
    b.onclick=()=>openSrc(src,i,b);
    g.appendChild(b);
  });
}

function closeCursorHint(){
  hide('mhint-cursor');
  // Marquer le tutoriel comme vu et sauvegarder
  cursorTutorialSeen=true;
  try {
    localStorage.setItem('fakemetre_cursor_tutorial_seen', 'true');
  } catch(e) {}
}

function openSrc(src,idx,btn){
  const isEdit=um[idx]!==undefined;
  pend={src,idx,btn,isEdit};
  $('msname').textContent=src.em+'  '+src.n;
  $('msdesc').textContent=src.d;
  $('mssays').textContent=src.say;

  if(currentLevel==='pro'||currentLevel==='inter'||src.g==='free'){
    $('msrc-junior').style.display='none';
    $('msrc-pro').style.display='block';
    initLikert(isEdit ? (src._likertScore||0) : 0);
  } else {
    $('msrc-junior').style.display='block';
    $('msrc-pro').style.display='none';
  }
  show('msrc');
}

let likertVal=0;
const LIKERT_LABELS=['','Absolutely not reliable','Very unreliable','Somewhat unreliable','Neutral — hard to tell','Somewhat reliable','Very reliable','Totally reliable'];

function initLikert(preVal=0){
  likertVal=0;
  const container=$('likert-btns');
  container.innerHTML='';
  for(let v=1;v<=7;v++){
    const b=document.createElement('button');
    b.className='lbtn';b.dataset.v=v;b.textContent=v;
    b.onclick=()=>selectLikert(v);
    container.appendChild(b);
  }
  $('likert-label').textContent='';
  $('likert-confirm').style.opacity='.4';
  $('likert-confirm').style.pointerEvents='none';
  if(preVal>0) selectLikert(preVal);
}

function selectLikert(v){
  likertVal=v;
  document.querySelectorAll('.lbtn').forEach(b=>{
    b.classList.toggle('selected',parseInt(b.dataset.v)===v);
  });
  $('likert-label').textContent=LIKERT_LABELS[v];
  $('likert-confirm').style.opacity='1';
  $('likert-confirm').style.pointerEvents='auto';
}

function confirmLikert(){
  const{src,idx,btn,isEdit}=pend;
  src._likertScore = likertVal;
  um[idx] = likertVal >= 5 ? 'ug' : (likertVal <= 3 ? 'ub' : 'neutral');
  if(!isEdit) uc++;
  btn.classList.remove('ug','ub');
  btn.classList.add('ug');
  // Update the tag (create or reuse)
  let tag=btn.querySelector('.utag');
  if(!tag){tag=document.createElement('div');btn.querySelector('div').appendChild(tag);}
  tag.className='utag g';
  tag.textContent='⭐ '+likertVal+'/7';
  updCounter();
  $('fbemoji').textContent='🎚️';
  $('fbtitle').textContent=isEdit?'Rating changed!':'Source evaluated!';
  $('fbexpl').textContent='You rated this source '+likertVal+'/7. You can check other sources or vote directly.';
  $('fbpts').textContent='';$('fbpts').className='fbpts';
  // Atomic swap: show mfb before hiding msrc to avoid a gap without overlay
  show('mfb');
  setTimeout(()=>$('msrc').classList.remove('show'),50);
  setTimeout(()=>{$('vzone').style.display='block';},600);
}

function searchSource(){
  // Open a Google search for the current source
  if(!pend) return;
  const src = pend.src;
  
  // If the source has a direct URL, open it
  if(src.url) {
    window.open(src.url, '_blank');
    return;
  }
  
  // If the source is fictional/generic, show a message
  if(src.noSearch) {
    alert("🔍 Impossible to find this source online!\n\nIt is a fictional or too-generic source to verify. In real life, this is a warning sign: a source that cannot be found is suspicious!");
    return;
  }
  
  // Sinon, recherche Google classique
  const sourceName = src.n;
  const sourceDesc = src.d;
  const query = encodeURIComponent(sourceName + ' ' + sourceDesc);
  window.open('https://www.google.com/search?q=' + query, '_blank');
}

function trust(trusts){
  const{src,idx,btn,isEdit}=pend;
  let emoji,title,expl,oc;
  if(src.g===true&&trusts)  {oc='ug';emoji='🎉';title='Excellent choice!';expl=src.fb.tg||'';}
  else if(src.g===true)     {oc='ub';emoji='😬';title='Too bad...';       expl=src.fb.dg||'';}
  else if(trusts)            {oc='ub';emoji='😬';title='Careful!';        expl=src.fb.tb||'';}
  else                       {oc='ug';emoji='👏';title='Well done!';      expl=src.fb.db||'';}
  if(!isEdit) uc++;
  um[idx]=oc;
  btn.classList.remove('ug','ub');
  btn.classList.add(oc);
  // Update the tag (create or reuse)
  let tag=btn.querySelector('.utag');
  if(!tag){tag=document.createElement('div');btn.querySelector('div').appendChild(tag);}
  tag.className='utag '+(oc==='ug'?'g':'b');
  tag.textContent=trusts?'✅ Trusted':'🙅 Ignored';
  updCounter();
  $('fbemoji').textContent=emoji;$('fbtitle').textContent=title;$('fbexpl').textContent=expl;
  $('fbpts').textContent='';$('fbpts').className='fbpts';
  // Atomic swap: show mfb before hiding msrc to avoid a gap without overlay
  show('mfb');
  setTimeout(()=>$('msrc').classList.remove('show'),50);
  setTimeout(()=>{$('vzone').style.display='block';},600);
}

function submitV(v){
  const q=QS[qi];$('vzone').style.display='none';
  
  // Calculate whether the answer is correct
  let ok, emoji, title, expl;

  if(v === 'nuance' && q.nuance){
    ok = true;
    emoji = '🧠';
    title = "Excellent critical thinking!";
    expl = q.enuan || q.e;
  } else if(v === 'nuance' && !q.nuance){
    ok = false;
    emoji = '🤔';
    title = "Hmm, there is actually a clear consensus here...";
    expl = q.e;
  } else {
    ok = v === q.t;
    emoji = ok ? '🎉' : '😬';
    title = ok ? (q.t ? "✅ Yes, it is TRUE!" : "✅ Yes, it is FALSE!") : (q.t ? "❌ No, it was TRUE!" : "❌ No, it was FALSE!");
    expl = q.e;
  }

  if(ok) score++;
  $('sc').textContent = score;
  $('vremoji').textContent = emoji;
  $('vrtitle').textContent = title;
  $('vrexpl').textContent = expl;
  $('vrpts').textContent = '';
  $('vrpts').className = 'fbpts';
  
  // Enregistrer dans l'historique pour le bilan
  const currentQHistory = {
    question: q.s,
    userVote: v,
    correctAnswer: q.t,
    hasNuance: q.nuance || false,
    wasCorrect: ok,
    sourceEvals: []
  };
  // Retrieve source evaluations
  sh.forEach((src, i) => {
    if(um[i] !== undefined){
      currentQHistory.sourceEvals.push({
        sourceName: src.n,
        isGoodSource: src.g,
        userTrusted: um[i] === 'ug', // ug = user trusted good, ub = user trusted bad
        likertScore: src._likertScore || null
      });
    }
  });
  gameHistory.push(currentQHistory);
  
  show('mvr');
}

function closeV(){
  hide('mvr');
  setTimeout(()=>{
    if(qi+1<QS.length){nextQ();}else{showFinal();}
  },400);
}

function nextQ(){
  qi++;
  if(qi>=QS.length)showFinal();else renderQ();
}

function showFinal(){
  $('game').style.display='none';$('scorebar').style.display='none';$('dots').style.display='none';
  const pct=score/QS.length;
  let m,c;
  if(pct>=.8){m='🥇';c="Incredible! You are a real information detective!";}
  else if(pct>=.5){m='🥈';c="Well done! You have good verification reflexes!";}
  else if(pct>=.25){m='🥉';c="Not bad! Keep practicing how to verify information!";}
  else{m='📚';c="The fake news really got you... but now you know how to react!";}
  
  // Generate the personalized report
  const bilan = generateBilan();
  
  const tips=[['✅','Consult an expert or specialist on the topic'],['✅','Use official sources (.gov, scientific agencies)'],['✅','Check on a fact-checking website (Hoaxbuster, AFP Factuel, etc.)'],['✅','Read encyclopedias or scientific books'],['❌','Likes and shares prove nothing'],['❌','“Everyone says so” proves nothing'],['❌','Funny or shocking information needs even more verification']];
  $('final').style.display='block';
  $('final').innerHTML=`
    <span class="fmedal">${m}</span>
    <h2 class="fh2">Investigation complete!</h2>
    <p style="color:var(--mu);font-weight:700;margin-bottom:8px">${c}</p>
    <div class="fscore">${score} / ${QS.length}</div>
    ${bilan ? `<div class="bilan-perso">${bilan}</div>` : ''}
    <div class="ftips"><h3>📋 Good habits to remember</h3>${tips.map(t=>`<div class="tip"><span>${t[0]}</span><span>${t[1]}</span></div>`).join('')}</div>
    <button id="rbtn" onclick="restart()">🔄 Replay</button>
    <button id="mbtn" onclick="chooseMode()">🏠 Menu</button>`;
}

function generateBilan(){
  if(gameHistory.length === 0) return '';
  
  let insights = [];
  let trustedBadSources = [];
  let distrustedGoodSources = [];
  let absoluteTrust = []; // Sources rated 7/7
  let wrongVotes = [];
  let missedNuances = [];
  
  gameHistory.forEach(h => {
    // Analyze TRUE/FALSE votes
    if(!h.wasCorrect){
      if(h.hasNuance && h.userVote !== 'nuance'){
        missedNuances.push(h.question.slice(0,50)+'...');
      } else {
        wrongVotes.push({q: h.question.slice(0,50)+'...', voted: h.userVote, correct: h.correctAnswer});
      }
    }
    
    // Analyze source evaluations
    h.sourceEvals.forEach(se => {
      if(se.likertScore === 7){
        absoluteTrust.push(se.sourceName);
      }
      if(se.likertScore >= 5 && !se.isGoodSource){
        trustedBadSources.push(se.sourceName);
      }
      if(se.likertScore <= 3 && se.isGoodSource){
        distrustedGoodSources.push(se.sourceName);
      }
      // Mode junior: userTrusted
      if(se.likertScore === null){
        if(se.userTrusted && !se.isGoodSource){
          trustedBadSources.push(se.sourceName);
        }
        if(!se.userTrusted && se.isGoodSource){
          distrustedGoodSources.push(se.sourceName);
        }
      }
    });
  });
  
  // Build insights
  if(trustedBadSources.length > 0){
    insights.push(`<div class="bilan-item bad">
      <span class="bilan-icon">⚠️</span>
      <div>
        <strong>You trusted unreliable sources :</strong><br>
        <em>${trustedBadSources.slice(0,3).join(', ')}</em><br>
        <span class="bilan-tip">→ Be wary of sources that look serious but do not cite their own sources, or that have an interest in convincing you.</span>
      </div>
    </div>`);
  }
  
  if(distrustedGoodSources.length > 0){
    insights.push(`<div class="bilan-item warn">
      <span class="bilan-icon">🤔</span>
      <div>
        <strong>You distrusted sources that were actually reliable :</strong><br>
        <em>${distrustedGoodSources.slice(0,3).join(', ')}</em><br>
        <span class="bilan-tip">→ Institutional, scientific, or fact-checking sources are generally reliable, even if they seem less “fun” than others.</span>
      </div>
    </div>`);
  }
  
  if(absoluteTrust.length > 0){
    insights.push(`<div class="bilan-item info">
      <span class="bilan-icon">💡</span>
      <div>
        <strong>You rated some sources 7/7 (absolute trust)</strong><br>
        <span class="bilan-tip">→ Even the best sources can be wrong! Keep a little doubt and cross-check several reliable sources.</span>
      </div>
    </div>`);
  }
  
  if(missedNuances.length > 0){
    insights.push(`<div class="bilan-item info">
      <span class="bilan-icon">⚖️</span>
      <div>
        <strong>You missed some nuances :</strong><br>
        <em>${missedNuances.slice(0,2).join(', ')}</em><br>
        <span class="bilan-tip">→ Some topics do not have a clear TRUE/FALSE answer. Spotting scientific debates is also part of fact-checking!</span>
      </div>
    </div>`);
  }
  
  if(wrongVotes.length > 0 && insights.length < 3){
    insights.push(`<div class="bilan-item bad">
      <span class="bilan-icon">❌</span>
      <div>
        <strong>Errors on the final verdict :</strong><br>
        <span class="bilan-tip">→ Keep checking sources before voting. The more you check, the more you refine your judgment!</span>
      </div>
    </div>`);
  }
  
  // Si tout est bon
  if(insights.length === 0){
    insights.push(`<div class="bilan-item good">
      <span class="bilan-icon">🌟</span>
      <div>
        <strong>Excellent travail !</strong><br>
        <span class="bilan-tip">You evaluated the sources well and voted correctly. Keep it up!</span>
      </div>
    </div>`);
  }
  
  return `<h3 style="margin-bottom:12px;">📊 Your personalized report</h3>${insights.join('')}`;
}

// ═══════════════════════════════════════════════
// CREATOR MODE
// ═══════════════════════════════════════════════
let customQuestions = [];
let editingIndex = -1;
let currentSources = [];
let currentTruth = true;
let currentNuance = false;

// Load from localStorage on startup
function loadCustomQuestions(){
  try {
    const saved = localStorage.getItem('fakemetre_custom_questions');
    if(saved) customQuestions = JSON.parse(saved);
  } catch(e){ console.log('Loading error:', e); }
  updateQuestionCount();
}

function saveToStorage(){
  try {
    localStorage.setItem('fakemetre_custom_questions', JSON.stringify(customQuestions));
    showSavedIndicator();
  } catch(e){ console.log('Save error:', e); }
}

function showSavedIndicator(){
  const ind = $('saved-indicator');
  ind.classList.add('show');
  setTimeout(()=> ind.classList.remove('show'), 2000);
}

function updateQuestionCount(){
  $('q-count').textContent = customQuestions.length;
  if(customQuestions.length > 0){
    $('play-empty').style.display = 'none';
    $('play-ready').style.display = 'block';
    $('play-count').textContent = customQuestions.length;
    $('export-empty').style.display = 'none';
    $('export-ready').style.display = 'block';
  } else {
    $('play-empty').style.display = 'block';
    $('play-ready').style.display = 'none';
    $('export-empty').style.display = 'block';
    $('export-ready').style.display = 'none';
  }
  // The import section is always visible (managed directly in the HTML)
}

function openCreator(){
  $('levelscreen').style.display = 'none';
  $('creatorscreen').style.display = 'block';
  loadCustomQuestions();
  resetForm();
  renderQuestionsList();
}

function closeCreator(){
  $('creatorscreen').style.display = 'none';
  $('levelscreen').style.display = 'block';
}

function switchCreatorTab(tab){
  document.querySelectorAll('.creator-tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.creator-panel').forEach(p => p.classList.remove('active'));
  document.querySelector(`.creator-tab[onclick*="${tab}"]`).classList.add('active');
  $('panel-' + tab).classList.add('active');
  if(tab === 'list') renderQuestionsList();
}

function setTruth(val){
  currentTruth = val;
  $('tog-true').classList.toggle('active', val);
  $('tog-false').classList.toggle('active', !val);
}

function toggleNuance(){
  currentNuance = !currentNuance;
  $('tog-nuance').classList.toggle('active', currentNuance);
  $('enuan-group').style.display = currentNuance ? 'block' : 'none';
}

function addSource(){
  const id = Date.now();
  currentSources.push({
    id, em:'📄', n:'', d:'', say:'', g:true, url:'', noSearch:false,
    fb:{tg:'', dg:'', tb:'', db:'', gen:''}
  });
  renderSources();
}

function removeSource(id){
  currentSources = currentSources.filter(s => s.id !== id);
  renderSources();
}

function srcTypeKey(g){
  if(g===true)   return 'reliable';
  if(g==='free') return 'free';
  return 'unreliable';
}

function setSourceType(id, type){
  const src = currentSources.find(s => s.id === id);
  if(!src) return;
  if(type==='reliable')  src.g = true;
  else if(type==='free') src.g = 'free';
  else                   src.g = false;
  src.fb = {tg:'', dg:'', tb:'', db:'', gen:''};
  renderSources();
}

function renderSources(){
  const container = $('sources-list');
  if(currentSources.length === 0){
    container.innerHTML = '<p style="color:var(--mu);font-size:.85rem;text-align:center;padding:20px;">Click "Add a source" to get started.</p>';
    return;
  }
  container.innerHTML = currentSources.map((src, i) => {
    const typeKey = srcTypeKey(src.g);
    const typeInfo = {
      reliable:   {icon:'✅', label:'Reliable',           desc:'The player should trust it'},
      unreliable: {icon:'❌', label:'Non reliable',        desc:'The player should not trust it'},
      free:       {icon:'🎚️', label:'Player evaluates',    desc:'The player uses the Likert scale — no imposed correct answer'},
    }[typeKey];

    let feedbackHTML = '';
    if(typeKey === 'free'){
      feedbackHTML = `
        <div class="form-group">
          <label>💬 General feedback after evaluation (optionnel)</label>
          <input type="text" value="${src.fb.gen||''}" onchange="updateSourceFb(${src.id},'gen',this.value)" placeholder="Example: This source is complex — here is why...">
        </div>`;
    } else if(typeKey === 'reliable'){
      feedbackHTML = `
        <div class="form-group">
          <label>✅ If the player trusts it (correct answer)</label>
          <input type="text" value="${src.fb.tg||''}" onchange="updateSourceFb(${src.id},'tg',this.value)" placeholder="Well done! This source is reliable because...">
        </div>
        <div class="form-group">
          <label>❌ If the player ignores it (wrong answer)</label>
          <input type="text" value="${src.fb.dg||''}" onchange="updateSourceFb(${src.id},'dg',this.value)" placeholder="Too bad! This source was reliable because...">
        </div>`;
    } else {
      feedbackHTML = `
        <div class="form-group">
          <label>❌ If the player trusts it (wrong answer)</label>
          <input type="text" value="${src.fb.tb||''}" onchange="updateSourceFb(${src.id},'tb',this.value)" placeholder="Careful! This source is not reliable because...">
        </div>
        <div class="form-group">
          <label>✅ If the player ignores it (correct answer)</label>
          <input type="text" value="${src.fb.db||''}" onchange="updateSourceFb(${src.id},'db',this.value)" placeholder="Well done! You were right to be skeptical because...">
        </div>`;
    }

    return `
    <div class="source-card ${typeKey}" id="src-${src.id}">
      <div class="source-header">
        <span class="source-num">${typeInfo.icon} Source ${i+1} — <span style="font-family:'Nunito',sans-serif;font-size:.85rem;">${typeInfo.label}</span></span>
        <button class="source-action-btn delete" onclick="removeSource(${src.id})">🗑️</button>
      </div>

      <label style="display:block;font-weight:700;font-size:.8rem;color:var(--mu);margin-bottom:6px;">Source type</label>
      <div class="stype-btns">
        <button class="stype-btn ${typeKey==='reliable'?'active-reliable':''}" onclick="setSourceType(${src.id},'reliable')">✅ Fiable</button>
        <button class="stype-btn ${typeKey==='unreliable'?'active-unreliable':''}" onclick="setSourceType(${src.id},'unreliable')">❌ Non reliable</button>
        <button class="stype-btn ${typeKey==='free'?'active-free':''}" onclick="setSourceType(${src.id},'free')">🎚️ Player evaluates</button>
      </div>
      <p style="color:var(--mu);font-size:.73rem;font-weight:700;margin-bottom:12px;margin-top:-6px;">${typeInfo.desc}</p>

      <div class="form-row three">
        <div class="form-group">
          <label>Emoji</label>
          <input type="text" value="${src.em}" onchange="updateSource(${src.id},'em',this.value)" placeholder="📄" maxlength="4">
        </div>
        <div class="form-group">
          <label>Source name</label>
          <input type="text" value="${src.n}" onchange="updateSource(${src.id},'n',this.value)" placeholder="Ex: Site Hoaxbuster">
        </div>
        <div class="form-group">
          <label>Short description</label>
          <input type="text" value="${src.d}" onchange="updateSource(${src.id},'d',this.value)" placeholder="Ex: Site de fact-checking">
        </div>
      </div>
      <div class="form-group">
        <label>What the source says (quote)</label>
        <textarea onchange="updateSource(${src.id},'say',this.value)" placeholder="Ex: « Nos recherches montrent que... »">${src.say}</textarea>
      </div>
      <div class="form-group" style="margin-bottom:8px;">
        <label>🔍 Source link or file (optionnel, mode Fact-Checker)</label>
        <div style="display:flex;gap:8px;align-items:center;">
          <input type="url" id="src-url-${src.id}" value="${escH(src.url||'')}" onchange="updateSource(${src.id},'url',this.value)" placeholder="https://..." style="flex:1;${src.noSearch?'opacity:.4;pointer-events:none;':''}">
          <button type="button" onclick="triggerFileUpload(${src.id})" class="creator-btn secondary" style="padding:8px 14px;font-size:.8rem;white-space:nowrap;flex-shrink:0;" ${src.noSearch?'disabled':''}>📎 File</button>
          <input type="file" id="file-input-${src.id}" accept="image/jpeg,image/png,image/gif,image/webp,application/pdf" style="display:none;" onchange="uploadSourceFile(${src.id},this)">
        </div>
        ${src.url && src.url.match(/\.(jpg|jpeg|png|gif|webp)(\?|$)/i) ? `<img src="${escH(src.url)}" style="max-width:100%;max-height:120px;margin-top:8px;border-radius:8px;object-fit:contain;" onerror="this.style.display='none'">` : ''}
        ${src.url && src.url.match(/\.pdf(\?|$)/i) ? `<div style="margin-top:6px;font-size:.78rem;color:var(--bl);font-weight:700;">📄 PDF joint — <a href="${escH(src.url)}" target="_blank" style="color:var(--bl);">Preview</a></div>` : ''}
      </div>
      <div class="nosearch-row" style="margin-bottom:12px;">
        <input type="checkbox" id="nosearch-${src.id}" ${src.noSearch?'checked':''} onchange="updateSourceNoSearch(${src.id},this.checked)">
        <label for="nosearch-${src.id}">🚫 Fictional source / not found online</label>
      </div>
      <details style="margin-top:4px;">
        <summary style="cursor:pointer;color:var(--mu);font-size:.8rem;font-weight:700;">💬 Feedbacks (optionnel)</summary>
        <div style="margin-top:12px;">${feedbackHTML}</div>
      </details>
    </div>`;
  }).join('');
}

function updateSource(id, field, value){
  const src = currentSources.find(s => s.id === id);
  if(src) src[field] = value;
}

function updateSourceFb(id, field, value){
  const src = currentSources.find(s => s.id === id);
  if(src) src.fb[field] = value;
}

function updateSourceNoSearch(id, checked){
  const src = currentSources.find(s => s.id === id);
  if(src){
    src.noSearch = checked;
    // Visually disable the URL field when noSearch is checked
    const srcCard = document.getElementById('src-' + id);
    if(srcCard){
      const urlInput = srcCard.querySelector('input[type=url]');
      if(urlInput){
        urlInput.style.opacity = checked ? '.4' : '1';
        urlInput.style.pointerEvents = checked ? 'none' : 'auto';
      }
    }
  }
}

function resetForm(){
  editingIndex = -1;
  $('edit-title').textContent = '➕ New question';
  $('c-statement').value = '';
  $('c-explanation').value = '';
  $('c-enuan').value = '';
  currentNuance = false;
  $('tog-nuance').classList.remove('active');
  $('enuan-group').style.display = 'none';
  setTruth(true);
  currentSources = [];
  renderSources();
}

function validateQuestion(){
  const statement = $('c-statement').value.trim();
  const explanation = $('c-explanation').value.trim();
  
  if(!statement){
    alert('⚠️ Enter a statement to verify!');
    return false;
  }
  if(!explanation){
    alert('⚠️ Enter an explanation!');
    return false;
  }
  if(currentSources.length < 2){
    alert('⚠️ Add at least 2 sources!');
    return false;
  }
  // Check all sources have name and say
  for(let i=0; i<currentSources.length; i++){
    if(!currentSources[i].n.trim() || !currentSources[i].say.trim()){
      alert(`⚠️ Source ${i+1} must have a name and a quote!`);
      return false;
    }
  }
  return true;
}

function saveQuestion(){
  if(!validateQuestion()) return;
  
  const question = {
    s: $('c-statement').value.trim(),
    t: currentTruth,
    e: $('c-explanation').value.trim(),
    src: currentSources.map(s => {
      const tk = srcTypeKey(s.g);
      const srcObj = {
        em: s.em || '📄',
        n: s.n,
        d: s.d || '',
        say: s.say,
        g: s.g,
        fb: {
          tg: s.fb.tg || (tk==='reliable' ? 'Good source! You have bien fait de lui faire confiance.' : ''),
          dg: s.fb.dg || (tk==='reliable' ? 'This source was actually reliable.' : ''),
          tb: s.fb.tb || (tk==='unreliable'||tk==='weak' ? 'This source was not reliable!' : ''),
          db: s.fb.db || (tk==='unreliable'||tk==='weak' ? 'Well done for being skeptical!' : ''),
          gen: s.fb.gen || (tk==='free' ? 'Source evaluated! You can check other sources or vote.' : '')
        }
      };
      if(s.url && s.url.trim()) srcObj.url = s.url.trim();
      if(s.noSearch) srcObj.noSearch = true;
      return srcObj;
    })
  };
  
  if(currentNuance){
    question.nuance = true;
    const enuan = $('c-enuan').value.trim();
    if(enuan) question.enuan = enuan;
  }
  
  if(editingIndex >= 0){
    customQuestions[editingIndex] = question;
  } else {
    customQuestions.push(question);
  }
  
  saveToStorage();
  updateQuestionCount();
  resetForm();
  alert('✅ Question saved!');
}

function renderQuestionsList(){
  const container = $('questions-list');
  if(customQuestions.length === 0){
    container.innerHTML = `<div class="empty-state">
      <div class="empty-icon">📭</div>
      <p>No questions created yet.<br>Start by creating one!</p>
    </div>`;
    return;
  }
  container.innerHTML = customQuestions.map((q, i) => `
    <div class="question-card" onclick="editQuestion(${i})">
      <div class="q-statement">${q.s}</div>
      <div class="q-meta">
        <span class="q-badge ${q.t ? 'true' : 'false'}">${q.t ? 'TRUE' : 'FALSE'}</span>
        ${q.nuance ? '<span class="q-badge" style="background:rgba(247,201,72,.2);color:#f7c948;">⚖️ NUANCED</span>' : ''}
        <span>📚 ${q.src.length} sources</span>
        <span style="margin-left:auto;">✏️ Edit</span>
      </div>
    </div>
  `).join('') + `
    <div class="creator-actions" style="margin-top:16px;">
      <button class="creator-btn danger" onclick="clearAllQuestions()">🗑️ Delete all</button>
    </div>
  `;
}

function editQuestion(index){
  const q = customQuestions[index];
  editingIndex = index;
  $('edit-title').textContent = '✏️ Edit question';
  $('c-statement').value = q.s;
  $('c-explanation').value = q.e;
  
  // Restore nuance state
  currentNuance = q.nuance || false;
  $('tog-nuance').classList.toggle('active', currentNuance);
  $('enuan-group').style.display = currentNuance ? 'block' : 'none';
  $('c-enuan').value = q.enuan || '';
  
  setTruth(q.t);
  currentSources = q.src.map((s,i) => ({
    ...s,
    id: Date.now() + i,
    url: s.url || '',
    noSearch: s.noSearch || false
  }));
  renderSources();
  switchCreatorTab('edit');
}

function clearAllQuestions(){
  if(confirm('⚠️ Delete ALL questions? This action is irreversible!')){
    customQuestions = [];
    saveToStorage();
    updateQuestionCount();
    renderQuestionsList();
  }
}

function playCustomQuestions(){
  if(customQuestions.length === 0) return;
  
  playingCustom = true;
  const mode = $('play-mode-select').value;
  currentLevel = mode;
  
  // Use custom questions
  QS = shuf([...customQuestions]);
  qi = 0; score = 0; meter = 50;
  
  $('creatorscreen').style.display = 'none';
  $('scorebar').style.display = 'flex';
  $('dots').style.display = 'flex';
  $('game').style.display = 'block';
  $('qtotal').textContent = QS.length;
  initMeterDrag();
  renderQ();
}

function exportJSON(){
  if(customQuestions.length === 0) return;
  const data = JSON.stringify(customQuestions, null, 2);
  const blob = new Blob([data], {type: 'application/json'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'fakemetre_questions.json';
  a.click();
  URL.revokeObjectURL(url);
}

function importJSON(){
  $('import-file-json').click();
}

function handleImportJSON(event){
  const file = event.target.files[0];
  if(!file) return;
  const reader = new FileReader();
  reader.onload = function(e){
    try {
      const imported = JSON.parse(e.target.result);
      if(Array.isArray(imported)){
        if(confirm(`Import ${imported.length} question(s) ? (Existing questions will be kept)`)){
          customQuestions = [...customQuestions, ...imported];
          saveToStorage();
          updateQuestionCount();
          renderQuestionsList();
          alert('✅ Import successful!');
        }
      } else {
        alert('❌ Invalid file format');
      }
    } catch(err){
      alert('❌ Error during import : ' + err.message);
    }
  };
  reader.readAsText(file);
  event.target.value = '';
}

// ── Export CSV ──
function escapeCSV(str){
  if(!str) return '';
  str = String(str);
  if(str.includes('"') || str.includes(',') || str.includes('\n') || str.includes(';')){
    return '"' + str.replace(/"/g, '""') + '"';
  }
  return str;
}

function exportCSV(){
  if(customQuestions.length === 0) return;
  
  // Header — nuance + enuan added after explanation; per source: url + noSearch added
  let csv = 'Statement;True/False;Explanation;Nuance;ExplanationNuance;Source1_Emoji;Source1_Name;Source1_Description;Source1_Citation;Source1_Reliable;Source1_URL;Source1_Fictive;Source1_FB_Positif;Source1_FB_Negatif;Source2_Emoji;Source2_Name;Source2_Description;Source2_Citation;Source2_Reliable;Source2_URL;Source2_Fictive;Source2_FB_Positif;Source2_FB_Negatif;Source3_Emoji;Source3_Name;Source3_Description;Source3_Citation;Source3_Reliable;Source3_URL;Source3_Fictive;Source3_FB_Positif;Source3_FB_Negatif;Source4_Emoji;Source4_Name;Source4_Description;Source4_Citation;Source4_Reliable;Source4_URL;Source4_Fictive;Source4_FB_Positif;Source4_FB_Negatif\n';
  
  customQuestions.forEach(q => {
    let row = [
      escapeCSV(q.s),
      q.t ? 'TRUE' : 'FALSE',
      escapeCSV(q.e),
      q.nuance ? 'OUI' : 'NON',
      escapeCSV(q.enuan || '')
    ];
    
    // Add up to 4 sources — 9 columns each now (added url + noSearch)
    for(let i=0; i<4; i++){
      if(q.src[i]){
        const s = q.src[i];
        row.push(
          escapeCSV(s.em),
          escapeCSV(s.n),
          escapeCSV(s.d),
          escapeCSV(s.say),
          s.g ? 'OUI' : 'NON',
          escapeCSV(s.url || ''),
          s.noSearch ? 'OUI' : 'NON',
          escapeCSV(s.g ? s.fb.tg : s.fb.tb),
          escapeCSV(s.g ? s.fb.dg : s.fb.db)
        );
      } else {
        row.push('','','','','','','','','');
      }
    }
    csv += row.join(';') + '\n';
  });
  
  // Add BOM for Excel UTF-8 compatibility
  const blob = new Blob(['\ufeff' + csv], {type: 'text/csv;charset=utf-8'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'fakemetre_questions.csv';
  a.click();
  URL.revokeObjectURL(url);
}

function importCSV(){
  $('import-file-csv').click();
}

function parseCSVLine(line){
  const result = [];
  let current = '';
  let inQuotes = false;
  
  for(let i=0; i<line.length; i++){
    const char = line[i];
    if(char === '"'){
      if(inQuotes && line[i+1] === '"'){
        current += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if(char === ';' && !inQuotes){
      result.push(current);
      current = '';
    } else {
      current += char;
    }
  }
  result.push(current);
  return result;
}

function handleImportCSV(event){
  const file = event.target.files[0];
  if(!file) return;
  const reader = new FileReader();
  reader.onload = function(e){
    try {
      const lines = e.target.result.split('\n').filter(l => l.trim());
      if(lines.length < 2){
        alert('❌ The CSV file is empty or invalid');
        return;
      }
      
      // Detect format version by counting columns in header
      const headerCols = parseCSVLine(lines[0]);
      // New format has 5 base cols + 9 per source = 5+36 = 41
      // Old format has 3 base cols + 7 per source = 3+28 = 31
      const isNewFormat = headerCols.length >= 41 || headerCols[3] === 'Nuance';
      
      const imported = [];
      // Skip header (line 0)
      for(let i=1; i<lines.length; i++){
        const cols = parseCSVLine(lines[i]);
        if(cols.length < 3 || !cols[0].trim()) continue;
        
        const question = {
          s: cols[0],
          t: cols[1].toUpperCase() === 'TRUE',
          e: cols[2],
          src: []
        };
        
        let srcStart, srcStride;
        if(isNewFormat){
          // nuance at col 3, enuan at col 4, sources start at 5 with 9 cols each
          question.nuance = cols[3] && cols[3].toUpperCase() === 'OUI';
          question.enuan = cols[4] || '';
          srcStart = 5;
          srcStride = 9;
        } else {
          // Old format: sources start at 3 with 7 cols each
          srcStart = 3;
          srcStride = 7;
        }
        
        // Parse sources
        for(let j=0; j<4; j++){
          const base = srcStart + (j * srcStride);
          if(cols[base+1] && cols[base+1].trim()){ // If source name exists
            const isReliable = cols[base+4] && cols[base+4].toUpperCase() === 'OUI';
            const src = {
              em: cols[base] || '📄',
              n: cols[base+1],
              d: cols[base+2] || '',
              say: cols[base+3] || '',
              g: isReliable,
              fb: {}
            };
            if(isNewFormat){
              src.url = cols[base+5] || '';
              src.noSearch = cols[base+6] && cols[base+6].toUpperCase() === 'OUI';
              const fbPos = cols[base+7] || '';
              const fbNeg = cols[base+8] || '';
              if(isReliable){ src.fb.tg = fbPos; src.fb.dg = fbNeg; }
              else { src.fb.tb = fbPos; src.fb.db = fbNeg; }
            } else {
              const fbPos = cols[base+5] || '';
              const fbNeg = cols[base+6] || '';
              if(isReliable){ src.fb.tg = fbPos || 'Good source!'; src.fb.dg = fbNeg || 'This source was reliable.'; }
              else { src.fb.tb = fbPos || 'This source was not reliable!'; src.fb.db = fbNeg || 'Well done for being skeptical!'; }
            }
            question.src.push(src);
          }
        }
        
        if(question.src.length >= 1){
          imported.push(question);
        }
      }
      
      if(imported.length === 0){
        alert('❌ No valid question found in the CSV.\n\nCheck that your file matches the format exported by FakeMeter (identical columns).');
        return;
      }
      
      if(confirm(`Import ${imported.length} question(s) from the CSV? (Existing questions will be kept)`)){
        customQuestions = [...customQuestions, ...imported];
        saveToStorage();
        updateQuestionCount();
        renderQuestionsList();
        alert('✅ CSV import successful!');
      }
    } catch(err){
      alert('❌ Error during CSV import : ' + err.message + '\n\nMake sure the file is a FakeMeter export.');
    }
  };
  reader.readAsText(file);
  event.target.value = '';
}

function exportHTML(){
  if(customQuestions.length === 0) return;

  // Serialize custom questions into a self-contained HTML file
  const questionsJSON = JSON.stringify(customQuestions, null, 2);
  const currentHTML = document.documentElement.outerHTML;

  // Inject a bootstrap script right before </head>
  const bootstrap = `<script>
window.addEventListener('DOMContentLoaded', function(){
  try {
    var CUSTOM_EMBEDDED = ${questionsJSON};
    var existing = localStorage.getItem('fakemetre_custom_questions');
    if(!existing || JSON.parse(existing).length === 0){
      localStorage.setItem('fakemetre_custom_questions', JSON.stringify(CUSTOM_EMBEDDED));
    }
  } catch(e){}
});
<\/script>`;

  const exportedHTML = currentHTML.replace('</head>', bootstrap + '</head>');
  const blob = new Blob([exportedHTML], {type: 'text/html'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'fakemetre_export.html';
  a.click();
  URL.revokeObjectURL(url);
}


function importSpreadsheet(){
  $('import-file-spreadsheet').click();
}

function handleImportSpreadsheet(event){
  const file = event.target.files[0];
  if(!file) return;

  const isXLSX = file.name.endsWith('.xlsx') || file.name.endsWith('.xls');
  const reader = new FileReader();

  reader.onload = function(e){
    try {
      let rows;
      if(isXLSX){
        const wb = XLSX.read(e.target.result, {type: 'binary'});
        const ws = wb.Sheets[wb.SheetNames[0]];
        rows = XLSX.utils.sheet_to_csv(ws).split('\n').filter(l => l.trim());
      } else {
        rows = e.target.result.split('\n').filter(l => l.trim());
      }

      if(rows.length < 2){
        alert('❌ The file is empty or invalid.');
        return;
      }

      const headerCols = parseCSVLine(rows[0]);
      const isNewFormat = headerCols.length >= 41 || headerCols[3] === 'Nuance';

      const imported = [];
      for(let i = 1; i < rows.length; i++){
        const cols = parseCSVLine(rows[i]);
        if(cols.length < 3 || !cols[0].trim()) continue;

        const question = { s: cols[0], t: cols[1].toUpperCase() === 'TRUE', e: cols[2], src: [] };

        let srcStart, srcStride;
        if(isNewFormat){
          question.nuance = cols[3] && cols[3].toUpperCase() === 'OUI';
          question.enuan = cols[4] || '';
          srcStart = 5; srcStride = 9;
        } else {
          srcStart = 3; srcStride = 7;
        }

        for(let j = 0; j < 4; j++){
          const base = srcStart + (j * srcStride);
          if(cols[base+1] && cols[base+1].trim()){
            const isReliable = cols[base+4] && cols[base+4].toUpperCase() === 'OUI';
            const src = { em: cols[base] || '📄', n: cols[base+1], d: cols[base+2] || '', say: cols[base+3] || '', g: isReliable, fb: {} };
            if(isNewFormat){
              src.url = cols[base+5] || '';
              src.noSearch = cols[base+6] && cols[base+6].toUpperCase() === 'OUI';
              const fbPos = cols[base+7] || '', fbNeg = cols[base+8] || '';
              if(isReliable){ src.fb.tg = fbPos; src.fb.dg = fbNeg; }
              else { src.fb.tb = fbPos; src.fb.db = fbNeg; }
            } else {
              const fbPos = cols[base+5] || '', fbNeg = cols[base+6] || '';
              if(isReliable){ src.fb.tg = fbPos || 'Good source!'; src.fb.dg = fbNeg || 'This source was reliable.'; }
              else { src.fb.tb = fbPos || 'This source was not reliable!'; src.fb.db = fbNeg || 'Well done for being skeptical!'; }
            }
            question.src.push(src);
          }
        }
        if(question.src.length >= 1) imported.push(question);
      }

      if(imported.length === 0){
        alert('❌ No valid question found.\n\nMake sure the file was exported from FakeMeter (CSV or Excel).');
        return;
      }

      if(confirm(`Import ${imported.length} question(s) ? (Existing questions will be kept)`)){
        customQuestions = [...customQuestions, ...imported];
        saveToStorage();
        updateQuestionCount();
        renderQuestionsList();
        alert('✅ Import successful!');
      }
    } catch(err){
      alert('❌ Error during import : ' + err.message + '\n\nMake sure the file was exported from FakeMeter.');
    }
  };

  if(isXLSX){
    reader.readAsBinaryString(file);
  } else {
    reader.readAsText(file);
  }
  event.target.value = '';
}

loadCustomQuestions();

// ═══════════════════════════════════════════════
// FILE UPLOAD (creator sources)
// ═══════════════════════════════════════════════
function triggerFileUpload(srcId){
  document.getElementById('file-input-'+srcId).click();
}

async function uploadSourceFile(srcId, input){
  const file = input.files[0];
  if(!file) return;
  if(file.size > 5*1024*1024){ alert('File too large (max 5 Mo).'); input.value=''; return; }

  const ext = file.name.split('.').pop().toLowerCase();
  const filename = Date.now()+'_'+Math.random().toString(36).slice(2)+'.'+ext;

  const urlInput = document.getElementById('src-url-'+srcId);
  if(urlInput){ urlInput.value='⏳ Upload in progress...'; urlInput.disabled=true; }

  try {
    const res = await fetch(SB_URL+'/storage/v1/object/sources/'+filename, {
      method:'POST',
      headers:{
        'apikey': SB_KEY,
        'Authorization': 'Bearer '+SB_KEY,
        'Content-Type': file.type,
        'x-upsert': 'true'
      },
      body: file
    });
    if(!res.ok) throw new Error(await res.text());

    const publicUrl = SB_URL+'/storage/v1/object/public/sources/'+filename;
    updateSource(srcId, 'url', publicUrl);
    renderSources();
  } catch(e){
    alert('❌ Upload error : '+e.message);
    if(urlInput){ urlInput.value=''; urlInput.disabled=false; }
  }
  input.value='';
}

// ═══════════════════════════════════════════════
// SUPABASE — COMMUNITY
// Replace the two values below with those
// of your Supabase project (Settings → API)
// ═══════════════════════════════════════════════
const SB_URL = 'https://hkuwalmnvjeazsegdlgf.supabase.co';
const SB_KEY = 'sb_publishable_I58Oi2FVnQdyzhf9UGoywA_WrCDcuIj';

function sbFetch(path, opts={}){
  return fetch(SB_URL+'/rest/v1/'+path, {
    ...opts,
    headers:{
      'apikey': SB_KEY,
      'Authorization': 'Bearer '+SB_KEY,
      'Content-Type': 'application/json',
      'Prefer': opts.prefer||'',
      ...(opts.headers||{})
    }
  }).then(r=>{
    if(!r.ok) return r.text().then(t=>{throw new Error(t);});
    return r.text().then(t=>t?JSON.parse(t):null);
  });
}

let communityPacks=[];
let communityFilter='all';
let langFilter='all';

function showCommunityTab(tab, btn){
  $('community-browse').style.display = tab==='browse' ? 'block' : 'none';
  $('community-howto').style.display  = tab==='howto'  ? 'block' : 'none';
  document.querySelectorAll('.community-filters .cfbtn').forEach(b=>b.classList.remove('active'));
  if(btn) btn.classList.add('active');
}

function openCommunity(){
  $('levelscreen').style.display='none';
  $('communityscreen').style.display='block';
  if(!localStorage.getItem('community_welcome_seen')){
    $('community-welcome-modal').style.display='flex';
  }
  loadPacks();
}

function closeCommunityWelcome(){
  $('community-welcome-modal').style.display='none';
  localStorage.setItem('community_welcome_seen','true');
}

function closeCommunity(){
  $('communityscreen').style.display='none';
  $('levelscreen').style.display='block';
}

function filterPacks(level, btn){
  communityFilter=level;
  document.querySelectorAll('#community-browse .community-filters:first-child .cfbtn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  loadPacks();
}

function filterLang(lang, btn){
  langFilter=lang;
  document.querySelectorAll('.cfbtn-lang').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  loadPacks();
}

function loadPacks(){
  const grid=$('pack-grid');
  grid.innerHTML='<div class="comm-loading">⏳ Loading...</div>';
  if(SB_URL==='REMPLACER_PAR_TON_URL_SUPABASE'){
    grid.innerHTML='<div class="comm-error">⚙️ Supabase not configured.<br><small>Follow the instructions in the source code (SB_URL / SB_KEY).</small></div>';
    return;
  }
  let q='packs?select=id,title,description,author,level,lang,play_count,likes,created_at,questions&order=created_at.desc&limit=50';
  if(communityFilter!=='all') q+='&level=eq.'+communityFilter;
  if(langFilter!=='all') q+='&lang=eq.'+langFilter;
  sbFetch(q).then(data=>{
    communityPacks=data||[];
    renderPacks();
  }).catch(()=>{
    grid.innerHTML='<div class="comm-error">❌ Unable to load packs.<br><small>Check your internet connection.</small></div>';
  });
}

function escH(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}

const LEVEL_LABELS={junior:'Apprentice',inter:'Investigator',pro:'Fact-Checker',mixed:'Mixed'};
const LANG_FLAGS={fr:'🇫🇷',en:'🇬🇧',both:'🌍'};

function renderPacks(){
  const grid=$('pack-grid');
  if(!communityPacks.length){
    grid.innerHTML='<div class="comm-loading">No packs yet.<br>Be the first to publish!</div>';
    return;
  }
  const myTokens=getMyPackTokens();
  grid.innerHTML=communityPacks.map(p=>{
    const voted=localStorage.getItem('vote_'+p.id)||'';
    const dis=voted?'disabled':'';
    const isMine=!!myTokens[p.id];
    return `
    <div class="pack-card" id="pack-${p.id}">
      <div class="pack-title">${escH(p.title)}</div>
      <div class="pack-meta">By ${escH(p.author||'Anonymous')} · ${new Date(p.created_at).toLocaleDateString('en-GB')}</div>
      ${p.description?`<div class="pack-desc">${escH(p.description)}</div>`:''}
      <div class="pack-footer">
        <span class="pack-badge ${escH(p.level)}">${LEVEL_LABELS[p.level]||escH(p.level)}</span>
        ${p.lang?`<span class="pack-stat">${LANG_FLAGS[p.lang]||'🌍'}</span>`:''}
        <span class="pack-stat">📋 ${(p.questions||[]).length} question(s)</span>
        <span class="pack-stat">🎮 ${p.play_count||0} plays</span>
      </div>
      <div class="pack-actions">
        <button class="vote-btn up${voted==='up'?' voted':''}" onclick="votePack('${p.id}','up')" ${dis}>👍 ${p.likes||0}</button>
        <button class="vote-btn down${voted==='down'?' voted':''}" onclick="votePack('${p.id}','down')" ${dis}>👎 ${p.dislikes||0}</button>
        <button class="comment-btn" onclick="toggleComments('${p.id}')">💬 Comments</button>
        <button class="comment-btn" onclick="editPack('${p.id}')">✏️ Edit</button>
        ${isMine?`<button class="pack-delete-btn" onclick="deleteMyPack('${p.id}')">🗑️ Delete</button>`:''}
        ${adminMode?`<button class="pack-delete-btn" onclick="adminDeletePack('${p.id}')">🗑️ Admin</button>`:''}
        <button class="pack-play-btn" onclick="playCommunityPack('${p.id}')">Play ▶</button>
      </div>
      <div class="comments-section" id="comments-${p.id}" style="display:none;">
        <div id="comments-list-${p.id}" class="comments-list"></div>
        <div class="comment-form">
          <input type="text" id="comment-author-${p.id}" class="form-input" placeholder="Your nickname (optional)" maxlength="30">
          <textarea id="comment-content-${p.id}" class="form-input" placeholder="Write your opinion about this pack..." maxlength="500" rows="2" style="resize:none;"></textarea>
          <button id="comment-submit-${p.id}" class="creator-btn primary" style="padding:9px 20px;font-size:.9rem;" onclick="submitComment('${p.id}')">Send</button>
        </div>
      </div>
    </div>`;
  }).join('');
}

function votePack(id, type){
  const key='vote_'+id;
  if(localStorage.getItem(key)){return;}
  const pack=communityPacks.find(p=>p.id===id);
  if(!pack) return;
  const field=type==='up'?'likes':'dislikes';
  const newVal=(pack[field]||0)+1;
  sbFetch('packs?id=eq.'+id,{method:'PATCH',prefer:'return=minimal',body:JSON.stringify({[field]:newVal})})
    .then(()=>{
      pack[field]=newVal;
      localStorage.setItem(key,type);
      renderPacks();
    }).catch(()=>alert('Error while voting.'));
}

function toggleComments(id){
  const section=document.getElementById('comments-'+id);
  if(section.style.display==='none'){
    section.style.display='block';
    loadComments(id);
  } else {
    section.style.display='none';
  }
}

function loadComments(packId){
  const container=document.getElementById('comments-list-'+packId);
  container.innerHTML='<div style="color:var(--mu);font-size:.8rem;padding:8px 0;">Loading...</div>';
  sbFetch('comments?pack_id=eq.'+packId+'&order=created_at.asc&limit=50')
    .then(data=>{
      if(!data||!data.length){
        container.innerHTML='<div style="color:var(--mu);font-size:.8rem;text-align:center;padding:12px 0;">No comments. Be the first!</div>';
        return;
      }
      container.innerHTML=data.map(c=>`
        <div class="comment-item">
          <div class="comment-author">${escH(c.author||'Anonymous')}</div>
          <div class="comment-content">${escH(c.content)}</div>
          <div class="comment-date">${new Date(c.created_at).toLocaleDateString('fr-FR')}</div>
        </div>`).join('');
    }).catch(()=>{
      container.innerHTML='<div style="color:var(--rd);font-size:.8rem;">Loading error.</div>';
    });
}

function submitComment(packId){
  const content=document.getElementById('comment-content-'+packId).value.trim();
  const author=document.getElementById('comment-author-'+packId).value.trim()||'Anonymous';
  if(!content){alert('Write a comment before sending!');return;}
  const btn=document.getElementById('comment-submit-'+packId);
  btn.disabled=true;btn.textContent='Sending...';
  sbFetch('comments',{method:'POST',prefer:'return=minimal',body:JSON.stringify({pack_id:packId,author,content})})
    .then(()=>{
      document.getElementById('comment-content-'+packId).value='';
      loadComments(packId);
    }).catch(e=>alert('Error: '+e.message))
    .finally(()=>{btn.disabled=false;btn.textContent='Send';});
}

function playCommunityPack(id){
  const pack=communityPacks.find(p=>p.id===id);
  if(!pack||!pack.questions||!pack.questions.length){alert('Invalid or empty pack.');return;}

  sbFetch('packs?id=eq.'+id,{method:'PATCH',prefer:'return=minimal',body:JSON.stringify({play_count:(pack.play_count||0)+1})}).catch(()=>{});

  playingCustom=true;
  playingCommunity=true;
  currentLevel=pack.level==='mixed'?'inter':(pack.level||'inter');
  QS=shuf([...pack.questions]);
  qi=0;score=0;meter=50;gameHistory=[];

  $('communityscreen').style.display='none';
  $('scorebar').style.display='flex';
  $('dots').style.display='flex';
  $('game').style.display='block';
  $('qtotal').textContent=QS.length;
  initMeterDrag();
  renderQ();
}

function openPublishModal(){
  if(!customQuestions.length){alert('Create questions in Creator Mode first!');return;}
  $('pub-secret').value='';
  if(editingPackId&&editingPackData){
    $('pub-title').value=editingPackData.title;
    $('pub-desc').value=editingPackData.description;
    $('pub-author').value=editingPackData.author;
    $('pub-level').value=editingPackData.level;
    $('pub-lang').value=editingPackData.lang;
    $('edit-mode-banner').style.display='block';
    $('edit-pack-name').textContent=editingPackData.title;
    $('publish-modal-title').textContent='✏️ Update Pack';
    $('pub-submit-btn').textContent='💾 Update Pack';
    $('secret-hint-text').textContent='(enter your code to confirm)';
    $('pub-charter-section').style.display='none';
    $('pub-charter-label').style.display='none';
  } else {
    $('pub-title').value='';
    $('pub-desc').value='';
    $('pub-author').value='';
    $('pub-level').value='mixed';
    $('edit-mode-banner').style.display='none';
    $('publish-modal-title').textContent='🌍 Publish to the Community';
    $('pub-submit-btn').textContent='🚀 Publish!';
    $('secret-hint-text').textContent='(optional — needed to edit or delete later)';
    $('pub-charter-section').style.display='';
    $('pub-charter-label').style.display='flex';
    $('pub-charter-check').checked=false;
  }
  $('publish-modal').style.display='flex';
}

function closePublishModal(){
  $('publish-modal').style.display='none';
}

async function submitPublish(){
  const title=$('pub-title').value.trim();
  if(!title){alert('Give your pack a title!');$('pub-title').focus();return;}
  if(SB_URL==='REMPLACER_PAR_TON_URL_SUPABASE'){alert('Supabase not configured.');return;}
  const secretRaw=$('pub-secret').value.trim();
  const btn=$('pub-submit-btn');

  if(editingPackId){
    if(!secretRaw){alert('Enter your secret code to confirm the update.');return;}
    const hash=await sha256(secretRaw);
    if(hash!==editingPackSecret){alert('❌ Incorrect code.');return;}
    btn.textContent='Updating...';btn.disabled=true;
    sbFetch('packs?id=eq.'+editingPackId+'&secret_hash=eq.'+editingPackSecret,{
      method:'PATCH',
      prefer:'return=minimal',
      body:JSON.stringify({
        title,
        description:$('pub-desc').value.trim(),
        level:$('pub-level').value,
        lang:$('pub-lang').value,
        questions:customQuestions
      })
    }).then(()=>{
      closePublishModal();
      cancelEditPack();
      alert('✅ Pack updated successfully!');
      loadPacks();
    }).catch(e=>{
      alert('❌ Error during update.\n'+e.message);
    }).finally(()=>{
      btn.textContent='💾 Update Pack';btn.disabled=false;
    });
  } else {
    if(!$('pub-charter-check').checked){alert('You must accept the publication guidelines before continuing.');return;}
    const secret_hash=secretRaw?await sha256(secretRaw):null;
    btn.textContent='Publishing...';btn.disabled=true;
    sbFetch('packs',{
      method:'POST',
      headers:{'Prefer':'return=representation'},
      body:JSON.stringify({
        title,
        description:$('pub-desc').value.trim(),
        author:$('pub-author').value.trim()||'Anonymous',
        level:$('pub-level').value,
        lang:$('pub-lang').value,
        secret_hash,
        questions:customQuestions
      })
    }).then(data=>{
      closePublishModal();
      if(data&&data[0]&&data[0].id){
        if(secret_hash) saveMyPackToken(data[0].id, secret_hash);
        const url=window.location.origin+window.location.pathname+'?pack='+data[0].id;
        showShareModal(url);
      }
      loadPacks();
    }).catch(e=>{
      alert('❌ Error during publication.\n'+e.message);
    }).finally(()=>{
      btn.textContent='🚀 Publish!';btn.disabled=false;
    });
  }
}

function showShareModal(url){
  const existing=document.getElementById('share-modal');
  if(existing) existing.remove();
  const m=document.createElement('div');
  m.id='share-modal';
  m.className='modal-overlay';
  m.style.cssText='display:flex;';
  m.innerHTML=`
    <div class="modal-box" style="max-width:440px;text-align:center;">
      <div style="font-size:2rem;margin-bottom:8px;">🎉</div>
      <h3 style="margin-bottom:8px;">Pack published!</h3>
      <p style="color:var(--mu);font-size:.85rem;font-weight:600;margin-bottom:16px;">Share this link so players can access your pack directly:</p>
      <div style="display:flex;gap:8px;align-items:center;">
        <input id="share-url-input" type="text" value="${url}" readonly class="form-input" style="font-size:.78rem;flex:1;">
        <button onclick="copyShareUrl()" class="creator-btn primary" style="padding:10px 14px;white-space:nowrap;">Copy</button>
      </div>
      <button class="creator-btn" style="margin-top:14px;width:100%;" onclick="document.getElementById('share-modal').remove()">Close</button>
    </div>`;
  document.body.appendChild(m);
}

function copyShareUrl(){
  const input=document.getElementById('share-url-input');
  navigator.clipboard.writeText(input.value).then(()=>{
    const btn=input.nextElementSibling;
    btn.textContent='Copied!';
    setTimeout(()=>btn.textContent='Copy',2000);
  });
}

// ── My packs (localStorage ownership) ──
function getMyPackTokens(){
  try{return JSON.parse(localStorage.getItem('fakemetre_my_packs')||'{}');}catch(e){return {};}
}
function saveMyPackToken(id,hash){
  const t=getMyPackTokens();t[id]=hash;
  localStorage.setItem('fakemetre_my_packs',JSON.stringify(t));
}
async function deleteMyPack(id){
  const tokens=getMyPackTokens();
  const hash=tokens[id];
  if(!hash){alert('No secret code stored for this pack on this device.');return;}
  if(!confirm('Permanently delete your pack?')) return;
  sbFetch('packs?id=eq.'+id+'&secret_hash=eq.'+hash,{method:'DELETE',prefer:'return=minimal'})
    .then(()=>{delete tokens[id];localStorage.setItem('fakemetre_my_packs',JSON.stringify(tokens));alert('Pack deleted.');loadPacks();})
    .catch(e=>alert('❌ Error: '+e.message));
}

// ── Creator edit mode ──
let editingPackId=null;
let editingPackSecret=null;
let editingPackData=null;

async function editPack(id){
  const tokens=getMyPackTokens();
  let hash=tokens[id];
  if(!hash){
    const code=prompt('Enter the secret code for this pack:');
    if(code===null) return;
    if(!code.trim()){alert('Please enter a secret code.');return;}
    hash=await sha256(code.trim());
  }
  let data;
  try{
    data=await sbFetch('packs?id=eq.'+id+'&secret_hash=eq.'+hash+'&select=id,title,description,author,level,lang,questions');
  }catch(e){alert('❌ Connection error.');return;}
  if(!data||!data.length){alert('❌ Incorrect code.');return;}
  const pack=data[0];
  editingPackId=id;
  editingPackSecret=hash;
  editingPackData={title:pack.title,description:pack.description||'',author:pack.author||'',level:pack.level||'mixed',lang:pack.lang||'en'};
  customQuestions=[...(pack.questions||[])];
  saveCustomQuestions();
  updateQuestionCount();
  renderQuestionsList();
  closeCommunity();
  openCreator();
  switchCreatorTab('export');
  alert(`✅ Pack loaded (${customQuestions.length} question(s)). Edit your questions, then click "Update Pack" in this tab.`);
}

function cancelEditPack(){
  editingPackId=null;
  editingPackSecret=null;
  editingPackData=null;
}

// ── Admin mode (deletion) ──
let adminMode=false;
const ADMIN_HASH='a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3';

async function sha256(str){
  const buf=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(str));
  return Array.from(new Uint8Array(buf)).map(b=>b.toString(16).padStart(2,'0')).join('');
}

async function toggleAdminMode(){
  if(adminMode){
    adminMode=false;
    renderPacks();
    return;
  }
  const pw=prompt('Admin password:');
  if(!pw) return;
  const h=await sha256(pw);
  if(h===ADMIN_HASH){
    adminMode=true;
    renderPacks();
  } else {
    alert('Incorrect password.');
  }
}

function adminDeletePack(id){
  if(!adminMode) return;
  if(!confirm('Permanently delete this pack? (admin)')) return;
  sbFetch('packs?id=eq.'+id,{method:'DELETE',prefer:'return=minimal'})
    .then(()=>{ alert('Pack deleted.'); loadPacks(); })
    .catch(e=>alert('❌ Error: '+e.message));
}

// ── Deep link ?pack=ID ──
(function(){
  const params=new URLSearchParams(window.location.search);
  const packId=params.get('pack');
  if(!packId) return;
  window.addEventListener('load',function(){
    openCommunity();
    sbFetch('packs?id=eq.'+packId+'&select=id,title,description,author,level,play_count,likes,created_at,questions&limit=1')
      .then(data=>{
        if(!data||!data.length){alert('Pack not found.');return;}
        const p=data[0];
        communityPacks=[p,...communityPacks.filter(x=>x.id!==p.id)];
        renderPacks();
        setTimeout(()=>{
          const el=document.getElementById('pack-'+p.id);
          if(el){el.scrollIntoView({behavior:'smooth',block:'center'});el.style.outline='2px solid #f97316';}
        },300);
      }).catch(()=>alert('Unable to load this pack.'));
  });
})();

// ── Fullscreen (mobile) ──
function toggleFS(){
  const el=document.documentElement;
  const isCssFs=document.body.classList.contains('css-fs');
  const isNativeFs=document.fullscreenElement||document.webkitFullscreenElement;
  if(!isNativeFs&&!isCssFs){
    if(el.requestFullscreen) el.requestFullscreen();
    else if(el.webkitRequestFullscreen) el.webkitRequestFullscreen();
    else{ document.body.classList.add('css-fs'); window.scrollTo(0,1); _updFsBtn(); }
  } else {
    if(isNativeFs){
      if(document.exitFullscreen) document.exitFullscreen();
      else if(document.webkitExitFullscreen) document.webkitExitFullscreen();
    } else { document.body.classList.remove('css-fs'); _updFsBtn(); }
  }
}
function _updFsBtn(){
  const btn=document.getElementById('fs-btn');
  if(!btn) return;
  const isFs=document.fullscreenElement||document.webkitFullscreenElement||document.body.classList.contains('css-fs');
  btn.innerHTML=isFs?'✕ Exit':'⛶ Fullscreen';
}
document.addEventListener('fullscreenchange',_updFsBtn);
document.addEventListener('webkitfullscreenchange',_updFsBtn);
