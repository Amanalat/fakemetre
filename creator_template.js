// ── FakeMètre Creator — Excel template download & import ──
// Requires SheetJS (XLSX) already loaded on the page.

// ── Download ──

function downloadTemplate(lang) {
  const isFr = lang !== 'en';
  const wb = isFr ? _buildWorkbookFR() : _buildWorkbookEN();
  const filename = isFr ? 'fakemetre_modele.xlsx' : 'fakemeter_template.xlsx';
  const wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });
  const blob = new Blob([wbout], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

// ── Import trigger ──

function importTemplate() {
  document.getElementById('import-file-template').click();
}

// ── Template info modal ──

function openTemplateInfo() {
  document.getElementById('template-info-modal').style.display = 'flex';
}
function closeTemplateInfo() {
  document.getElementById('template-info-modal').style.display = 'none';
}

// ── File handlers ──

function handleImportTemplate(event)   { _doImportTemplate(event, 'fr'); }
function handleImportTemplateEN(event) { _doImportTemplate(event, 'en'); }

function _doImportTemplate(event, lang) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function(e) {
    try {
      const wb = XLSX.read(new Uint8Array(e.target.result), { type: 'array' });
      const ws = wb.Sheets[wb.SheetNames[0]];
      const rows = XLSX.utils.sheet_to_json(ws, { header: 1, defval: '' });
      const questions = _parseExcelRows(rows);
      _finishImport(questions, lang);
    } catch(err) {
      const prefix = lang === 'en' ? '❌ Error reading file: ' : '❌ Erreur lors de la lecture du fichier : ';
      alert(prefix + err.message);
    }
  };
  reader.readAsArrayBuffer(file);
  event.target.value = '';
}

function _finishImport(questions, lang) {
  if (questions.length === 0) {
    alert(lang === 'en'
      ? '❌ No valid questions found.\nCheck that each row has a Statement and at least 2 sources with a Name.'
      : '❌ Aucune question valide trouvée.\nVérifie que chaque ligne a une Affirmation et au moins 2 sources avec un Nom.');
    return;
  }
  const ok = confirm(lang === 'en'
    ? 'Import ' + questions.length + ' question(s)? (Existing questions will be kept)'
    : 'Importer ' + questions.length + ' question(s) ? (Les questions existantes seront conservées)');
  if (!ok) return;
  customQuestions = [...customQuestions, ...questions];
  saveToStorage();
  updateQuestionCount();
  renderQuestionsList();
  alert(lang === 'en'
    ? '✅ ' + questions.length + ' question(s) imported successfully!'
    : '✅ ' + questions.length + ' question(s) importée(s) avec succès !');
}

// ── Parser ──
// Reads header row to locate columns by name (partial, case-insensitive match).
// Supports both FR and EN headers so a template from either language can be imported anywhere.

function _findCol(header, ...terms) {
  return header.findIndex(h =>
    terms.some(t => String(h).toLowerCase().includes(t.toLowerCase()))
  );
}

function _findSrcCol(header, srcNum, ...terms) {
  const prefix = 'src' + srcNum;
  return header.findIndex(h => {
    const low = String(h).toLowerCase();
    return low.includes(prefix) && terms.some(t => low.includes(t.toLowerCase()));
  });
}

function _parseExcelRows(rows) {
  if (rows.length < 2) return [];
  const header = rows[0];

  const COL_AFF  = _findCol(header, 'affirmation', 'statement');
  const COL_VF   = _findCol(header, 'vrai ou faux', 'true or false');
  const COL_EXP  = _findCol(header, 'explication', 'explanation');
  const COL_NUA  = _findCol(header, 'nuancé', 'nuanced');
  const COL_ENUA = _findCol(header, 'explication nuance', 'nuance explanation');

  // Source groups — one entry per source slot (1-4)
  const srcCols = [1, 2, 3, 4].map(i => ({
    emoji   : _findSrcCol(header, i, 'emoji'),
    nom     : _findSrcCol(header, i, 'nom', 'name'),
    desc    : _findSrcCol(header, i, 'description'),
    citation: _findSrcCol(header, i, 'citation', 'quote'),
    fiable  : _findSrcCol(header, i, 'fiable', 'reliable'),
    bon     : _findSrcCol(header, i, 'bon choix', 'correct'),
    mauvais : _findSrcCol(header, i, 'mauvais choix', 'wrong'),
  }));

  const questions = [];

  for (let r = 1; r < rows.length; r++) {
    const row = rows[r];
    const affirmation = String(row[COL_AFF] || '').trim();
    if (!affirmation) continue;

    const vfRaw = String(row[COL_VF] || '').trim().toUpperCase();
    const nuaRaw = String(row[COL_NUA] || '').trim().toUpperCase();

    const q = {
      s     : affirmation,
      t     : vfRaw === 'VRAI' || vfRaw === 'TRUE',
      e     : String(row[COL_EXP]  || '').trim(),
      nuance: nuaRaw === 'OUI' || nuaRaw === 'YES',
      enuan : COL_ENUA >= 0 ? String(row[COL_ENUA] || '').trim() : '',
      src   : [],
    };

    for (const sc of srcCols) {
      const name = sc.nom >= 0 ? String(row[sc.nom] || '').trim() : '';
      if (!name) continue;

      const fiableRaw = sc.fiable >= 0 ? String(row[sc.fiable] || '').trim().toUpperCase() : '';
      const isGood    = fiableRaw === 'OUI' || fiableRaw === 'YES';
      const bon       = sc.bon     >= 0 ? String(row[sc.bon]     || '').trim() : '';
      const mauvais   = sc.mauvais >= 0 ? String(row[sc.mauvais] || '').trim() : '';

      q.src.push({
        em  : sc.emoji >= 0 ? (String(row[sc.emoji] || '').trim() || '📄') : '📄',
        n   : name,
        d   : sc.desc     >= 0 ? String(row[sc.desc]     || '').trim() : '',
        say : sc.citation >= 0 ? String(row[sc.citation] || '').trim() : '',
        g   : isGood,
        fb  : isGood ? { tg: bon, dg: mauvais } : { tb: mauvais, db: bon },
      });
    }

    if (q.src.length >= 2) questions.push(q);
  }

  return questions;
}

// ── Workbook builders ──

function _buildWorkbookFR() {
  const wb = XLSX.utils.book_new();

  const headers = [
    'Affirmation',
    'Vrai ou Faux',
    'Explication',
    'Sujet nuancé ?',
    'Explication nuance (si OUI ci-dessus)',
    'Src1 Emoji (optionnel)', 'Src1 Nom', 'Src1 Description', 'Src1 Citation', 'Src1 Fiable ?', 'Src1 Feedback bon choix', 'Src1 Feedback mauvais choix',
    'Src2 Emoji (optionnel)', 'Src2 Nom', 'Src2 Description', 'Src2 Citation', 'Src2 Fiable ?', 'Src2 Feedback bon choix', 'Src2 Feedback mauvais choix',
    'Src3 Emoji (optionnel)', 'Src3 Nom', 'Src3 Description', 'Src3 Citation', 'Src3 Fiable ?', 'Src3 Feedback bon choix', 'Src3 Feedback mauvais choix',
    'Src4 Emoji (optionnel)', 'Src4 Nom', 'Src4 Description', 'Src4 Citation', 'Src4 Fiable ?', 'Src4 Feedback bon choix', 'Src4 Feedback mauvais choix',
  ];

  const example = [
    "On avale en moyenne 8 araignées par an pendant qu'on dort",
    'FAUX',
    "C'est un mythe ! Les araignées fuient les vibrations des ronflements.",
    'NON', '',
    '🔬', 'Revue scientifique', 'Article dans une revue à comité de lecture',
    "Nos recherches n'ont trouvé aucune preuve que les araignées s'approchent des bouches.",
    'OUI', "Super ! Une revue à comité de lecture, c'est parmi les meilleures sources.", 'Dommage ! Une revue scientifique est très fiable.',
    '👍', 'Post TikTok avec 2 millions de likes', 'Vidéo virale sans source citée',
    'CHOQUANT : on avale 8 araignées par nuit !',
    'NON', "Bien joué ! Tu t'es méfié d'une vidéo TikTok sans source.", 'Attention ! Les likes ne prouvent rien.',
    '', '', '', '', '', '', '',
    '', '', '', '', '', '', '',
  ];

  // Empty template rows — pre-fill OUI/NON defaults to guide the user
  const empty = () => ['', 'VRAI', '', 'NON', '',  '', '', '', '', 'OUI', '', '',  '', '', '', '', 'NON', '', '',  '', '', '', '', '', '', '',  '', '', '', '', '', '', ''];

  const ws = XLSX.utils.aoa_to_sheet([headers, example, empty(), empty(), empty(), empty()]);

  ws['!cols'] = [
    {wch:50},{wch:13},{wch:50},{wch:14},{wch:35},
    {wch:8},{wch:25},{wch:30},{wch:40},{wch:10},{wch:40},{wch:40},
    {wch:8},{wch:25},{wch:30},{wch:40},{wch:10},{wch:40},{wch:40},
    {wch:8},{wch:25},{wch:30},{wch:40},{wch:10},{wch:40},{wch:40},
    {wch:8},{wch:25},{wch:30},{wch:40},{wch:10},{wch:40},{wch:40},
  ];

  // Freeze header row
  ws['!views'] = [{ state: 'frozen', ySplit: 1 }];

  // Dropdowns
  ws['!dataValidations'] = [
    { sqref: 'B2:B200', type: 'list', formula1: '"VRAI,FAUX"'  },
    { sqref: 'D2:D200', type: 'list', formula1: '"OUI,NON"'    },
    { sqref: 'J2:J200', type: 'list', formula1: '"OUI,NON"'    },
    { sqref: 'Q2:Q200', type: 'list', formula1: '"OUI,NON"'    },
    { sqref: 'X2:X200', type: 'list', formula1: '"OUI,NON"'    },
    { sqref: 'AE2:AE200', type: 'list', formula1: '"OUI,NON"'  },
  ];

  XLSX.utils.book_append_sheet(wb, ws, 'Questions');

  // Instructions sheet
  const instr = [
    ['FAKEMETRE — Modèle de questions personnalisées'],
    [''],
    ['COMMENT UTILISER CE FICHIER :'],
    ['  1. Va dans l\'onglet "Questions" — une ligne = une question.'],
    ['  2. Vrai ou Faux    : utilise le menu déroulant ou tape VRAI / FAUX.'],
    ['  3. Sujet nuancé ?  : OUI si le sujet est controversé/débattu, NON sinon.'],
    ['  4. Fiable ?        : OUI = source fiable, NON = source peu fiable.'],
    ['  5. Emoji           : OPTIONNEL — un seul emoji pour représenter la source.'],
    ['                       Laisse la case vide si tu ne veux pas en mettre.'],
    ['  6. Chaque question doit avoir au minimum 2 sources (Src1 et Src2 obligatoires).'],
    ['  7. Src3 et Src4 sont facultatives — laisse-les vides si tu n\'en as pas.'],
    [''],
    ['FEEDBACK :'],
    ['  Feedback bon choix    = message affiché quand le joueur identifie correctement'],
    ['                          la fiabilité de cette source.'],
    ['  Feedback mauvais choix = message affiché quand le joueur se trompe.'],
    ['  Ces deux champs sont optionnels mais recommandés pour une meilleure expérience.'],
    [''],
    ['EXPLICATION NUANCE :'],
    ['  À remplir uniquement si "Sujet nuancé ?" = OUI.'],
    ['  Explique pourquoi le sujet est débattu ou sans consensus clair.'],
    [''],
    ['Une fois rempli, sauvegarde le fichier et importe-le dans FakeMètre.'],
  ];
  const wsI = XLSX.utils.aoa_to_sheet(instr);
  wsI['!cols'] = [{wch:72}];
  XLSX.utils.book_append_sheet(wb, wsI, "Mode d'emploi");

  return wb;
}

function _buildWorkbookEN() {
  const wb = XLSX.utils.book_new();

  const headers = [
    'Statement',
    'True or False',
    'Explanation',
    'Nuanced topic ?',
    'Nuance explanation (if YES above)',
    'Src1 Emoji (optional)', 'Src1 Name', 'Src1 Description', 'Src1 Quote', 'Src1 Reliable ?', 'Src1 Feedback correct', 'Src1 Feedback wrong',
    'Src2 Emoji (optional)', 'Src2 Name', 'Src2 Description', 'Src2 Quote', 'Src2 Reliable ?', 'Src2 Feedback correct', 'Src2 Feedback wrong',
    'Src3 Emoji (optional)', 'Src3 Name', 'Src3 Description', 'Src3 Quote', 'Src3 Reliable ?', 'Src3 Feedback correct', 'Src3 Feedback wrong',
    'Src4 Emoji (optional)', 'Src4 Name', 'Src4 Description', 'Src4 Quote', 'Src4 Reliable ?', 'Src4 Feedback correct', 'Src4 Feedback wrong',
  ];

  const example = [
    'We swallow an average of 8 spiders a year while sleeping',
    'FALSE',
    "It's a myth! Spiders flee the vibrations of snoring.",
    'NO', '',
    '🔬', 'Scientific journal', 'Peer-reviewed research article',
    'Our research found no evidence that spiders approach mouths at night.',
    'YES', 'Great! A peer-reviewed journal is among the most reliable sources.', 'Too bad! A scientific journal is very reliable.',
    '👍', 'TikTok post with 2 million likes', 'Viral video with no sources cited',
    'SHOCKING: we swallow 8 spiders a night!',
    'NO', 'Well done! You were skeptical of a TikTok video with no source.', 'Watch out! Likes prove nothing.',
    '', '', '', '', '', '', '',
    '', '', '', '', '', '', '',
  ];

  const empty = () => ['', 'TRUE', '', 'NO', '',  '', '', '', '', 'YES', '', '',  '', '', '', '', 'NO', '', '',  '', '', '', '', '', '', '',  '', '', '', '', '', '', ''];

  const ws = XLSX.utils.aoa_to_sheet([headers, example, empty(), empty(), empty(), empty()]);

  ws['!cols'] = [
    {wch:50},{wch:14},{wch:50},{wch:16},{wch:35},
    {wch:8},{wch:25},{wch:30},{wch:40},{wch:12},{wch:40},{wch:40},
    {wch:8},{wch:25},{wch:30},{wch:40},{wch:12},{wch:40},{wch:40},
    {wch:8},{wch:25},{wch:30},{wch:40},{wch:12},{wch:40},{wch:40},
    {wch:8},{wch:25},{wch:30},{wch:40},{wch:12},{wch:40},{wch:40},
  ];

  ws['!views'] = [{ state: 'frozen', ySplit: 1 }];

  ws['!dataValidations'] = [
    { sqref: 'B2:B200', type: 'list', formula1: '"TRUE,FALSE"' },
    { sqref: 'D2:D200', type: 'list', formula1: '"YES,NO"'     },
    { sqref: 'J2:J200', type: 'list', formula1: '"YES,NO"'     },
    { sqref: 'Q2:Q200', type: 'list', formula1: '"YES,NO"'     },
    { sqref: 'X2:X200', type: 'list', formula1: '"YES,NO"'     },
    { sqref: 'AE2:AE200', type: 'list', formula1: '"YES,NO"'   },
  ];

  XLSX.utils.book_append_sheet(wb, ws, 'Questions');

  const instr = [
    ['FAKEMETER — Custom questions template'],
    [''],
    ['HOW TO USE THIS FILE:'],
    ['  1. Go to the "Questions" tab — one row = one question.'],
    ['  2. True or False   : use the dropdown or type TRUE / FALSE.'],
    ['  3. Nuanced topic ? : YES if the topic is controversial/debated, NO otherwise.'],
    ['  4. Reliable ?      : YES = reliable source, NO = unreliable source.'],
    ['  5. Emoji           : OPTIONAL — one single emoji to represent the source.'],
    ['                       Leave the cell empty if you don\'t want one.'],
    ['  6. Each question needs at least 2 sources (Src1 and Src2 are required).'],
    ['  7. Src3 and Src4 are optional — leave them empty if you don\'t need them.'],
    [''],
    ['FEEDBACK:'],
    ['  Feedback correct = message shown when the player correctly identifies'],
    ['                     the reliability of this source.'],
    ['  Feedback wrong   = message shown when the player misjudges the source.'],
    ['  Both fields are optional but recommended for a better experience.'],
    [''],
    ['NUANCE EXPLANATION:'],
    ['  Fill in only if "Nuanced topic?" = YES.'],
    ['  Explain why the topic is debated or has no clear consensus.'],
    [''],
    ['Once filled in, save the file and import it into FakeMeter.'],
  ];
  const wsI = XLSX.utils.aoa_to_sheet(instr);
  wsI['!cols'] = [{wch:72}];
  XLSX.utils.book_append_sheet(wb, wsI, 'Instructions');

  return wb;
}
