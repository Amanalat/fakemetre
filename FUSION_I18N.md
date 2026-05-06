# Fusion FR/EN — Progression

## Objectif
Remplacer `index.html` + `index_en.html` par un seul `index.html` avec un système i18n minimal.
La langue est détectée via `?lang=en` dans l'URL ou le bouton de bascule existant.

## Stratégie
- `questions_en.js` : constantes renommées `QUESTIONS_JUNIOR_EN` etc.
- Un objet `I18N = { fr: {...}, en: {...} }` dans le JS de index.html
- `const lang` détecté depuis `?lang=en` (URLSearchParams)
- `function t(key)` pour les chaînes JS
- `function applyI18n()` pour les éléments HTML via `data-i18n="key"`
- Pour HTML complexe (innerHTML) : attribut `data-i18n-html="key"`
- `renderHelpSections()` pour les sections d'aide HTML complexes
- Charger les 2 fichiers questions, sélectionner au moment du startGame()

## Phases

### Phase 1 — Renommer constantes dans questions_en.js [FAIT ✅]
- [x] QUESTIONS_JUNIOR → QUESTIONS_JUNIOR_EN
- [x] QUESTIONS_INTER → QUESTIONS_INTER_EN
- [x] QUESTIONS_PRO → QUESTIONS_PRO_EN

### Phase 2 — Infrastructure I18N dans index.html [FAIT ✅]
- [x] Charger questions_en.js dans les scripts
- [x] Détecter lang depuis URLSearchParams
- [x] Écrire I18N dict (toutes les chaînes FR/EN) — ~100 clés
- [x] Écrire t(), applyI18n()
- [x] Appel applyI18n() + renderHelpSections() au chargement

### Phase 3 — HTML statique : data-i18n [FAIT ✅]
- [x] <html lang="..."> dynamique
- [x] <title>
- [x] Header (h1, p.sub, lang-switch)
- [x] Level cards (6 cartes × title + desc)
- [x] Mode screen (bouton, h2, p, 2 cartes)
- [x] Creator screen : onglets, labels, boutons, placeholders
- [x] Community screen : boutons, filtres, grille
- [x] Cursor hint modal
- [x] Fullscreen button
- [x] Help sections → IDs + renderHelpSections()
- [x] Community howto → renderHelpSections()

### Phase 4 — JS dynamique : t() [FAIT ✅]
- [x] chooseLevel() : textContent modescreen-title
- [x] backToMenu() : confirm
- [x] startGame() : pool de questions EN/FR
- [x] updMeter() / updMiniMeter() : Plutôt FAUX / VRAI / Incertain
- [x] updCounter() : messages de compteur
- [x] loadPacks() : messages communauté
- [x] renderPacks() : packBy, packAnon, dateLocale, levelLabels, packPlays, boutons
- [x] loadComments() / submitComment()
- [x] playCommunityPack() : alertInvalidPack
- [x] openPublishModal() : titres, boutons, hints
- [x] submitPublish() : tous les alert/confirm + authorDefault
- [x] showShareModal() : titre, desc, boutons
- [x] copyShareUrl() : Copié / Copier
- [x] deleteMyPack() : alerts/confirm
- [x] editPack() : prompt, alerts, lang default
- [x] adminMode / adminDeletePack() : prompt, alerts
- [x] deep link : alerts
- [x] toggleFS / _updFsBtn()

### Phase 5 — Cas spéciaux [FAIT ✅]
- [x] CSV headers → t('csvHeaders')
- [x] 'VRAI'/'FAUX' export → t('csvTrueWord'/'csvFalseWord')
- [x] 'VRAI'/'FAUX' import parsing → accepter VRAI et TRUE
- [x] Feedbacks par défaut → t('fbSrcDefaultGood') etc.
- [x] Upload alerts → t('uploadTooBig/Progress/Error')
- [x] CSV/template import alerts → t() partout
- [x] Date locale → t('dateLocale')
- [x] downloadTemplate() → t('templateLang')
- [x] handleImportTemplate / handleImportTemplateEN → unifié (même fonction)
- [x] editingPackData.lang → lang variable
- [x] pub-lang default → lang variable
- [x] renderHelpSections() pour sections complexes

### Phase 5b — Éléments manquants [FAIT ✅]
- [x] Game area : stag, mlabels (Faux/Vrai), meter-hint, sectitle
- [x] Vote zone : p, vhint, 3 boutons (FAUX/consensus/VRAI)
- [x] Source modal junior : msq, btnTrustYes, btnTrustNo
- [x] Source modal pro : msq, likert min/mid/max, likertConfirmBtn, researchBtn
- [x] Cursor prompt : p, btnNo, btnYes
- [x] Mini meter modal : title, labels, hint, confirm btn
- [x] mvr modal : Continuer →
- [x] Saved indicator
- [x] Scorebar : Score/pts/Enquête wrappés en spans
- [x] Template info modal : h3 + renderTemplateInfoModal()
- [x] Community welcome modal : title, body, btn
- [x] Publish modal : tous les labels, placeholders, options, charter

### Phase 6 — Validation et nettoyage [EN COURS]
- [x] Tester FR : charger index.html → comportement identique
- [x] Tester EN : charger index.html?lang=en → comportement identique
- [x] Vérifier bouton lang-switch fonctionne dans les deux sens
- [x] Supprimer index_en.html
- [x] Commit

## Journal
- [2026-05-06] Début analyse diff — ~150 chaînes, 2 diff logiques, 1 diff structurelle publish flow
- [2026-05-06] Phase 1 : renommage constantes EN
- [2026-05-06] Phase 2 : infrastructure I18N (dict ~100 clés, t(), applyI18n())
- [2026-05-06] Phase 3 : HTML statique — 79 attributs data-i18n posés
- [2026-05-06] Phase 4 : JS dynamique — ~265 appels t() dans le code
- [2026-05-07] Phase 5 : cas spéciaux (CSV, VRAI/TRUE, feedbacks, upload, dates)
- [2026-05-07] Vérification : 3184 lignes, applyI18n ✅, renderHelpSections ✅, questions_en.js ✅
- [2026-05-07] Phase 5b : 60+ nouveaux data-i18n, 60+ nouvelles clés I18N, renderTemplateInfoModal()

## À tester avant de supprimer index_en.html
1. FR : toutes les écrans s'affichent en français
2. EN : charger ?lang=en → toutes les écrans en anglais
3. Mode créateur : import/export CSV fonctionne dans les deux langues
4. Communauté : chargement, vote, commentaires, publication
5. Jeu : 5 questions EN avec ?lang=en, 5 questions FR sans paramètre
