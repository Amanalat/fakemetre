# TODO — FakeMètre : Images à générer

## 1. Images en français → traduire en anglais

Ces 4 images existent en FR mais contiennent du texte français. Il faut générer une version EN avec le même visuel mais le texte en anglais. Les prompts EN sont dans `PROMPTS_IMAGES.md`.

| Image FR existante | Fichier EN à créer | Prompt dans PROMPTS_IMAGES.md |
|--------------------|-------------------|-------------------------------|
| `images/tiktok_araignees.png` | `images/tiktok_araignees_en.png` | Section 1 — EN |
| `images/tiktok_chat_ronron.png` | `images/tiktok_chat_ronron_en.png` | Section 2 — EN |
| `images/facebook_napoleon_cochon.png` | `images/facebook_napoleon_cochon_en.png` | Section 3 — EN |
| `images/magazine_carottes_vue.png` | `images/magazine_carottes_vue_en.png` | Section 9 — EN |

> Une fois générées : les déposer ici et demander à Claude de les intégrer dans `questions_en.js`.

---

## 2. Images pas encore générées (ni FR ni EN)

Ces images n'existent pas encore. Générer les deux versions FR et EN. Les prompts sont dans `PROMPTS_IMAGES.md`.

| # | Sujet | Fichier FR à créer | Fichier EN à créer | Section dans PROMPTS_IMAGES.md |
|---|-------|-------------------|-------------------|-------------------------------|
| 4 | Blog apiculteur — miel | `images/blog_miel_apiculteur.png` | `images/blog_miel_apiculteur_en.png` | Section 4 |
| 5 | Affiche film 10% cerveau | `images/affiche_film_cerveau.png` | `images/affiche_film_cerveau_en.png` | Section 5 |
| 6 | Pub TV paracétamol | `images/pub_tv_paracetamol.png` | `images/pub_tv_paracetamol_en.png` | Section 6 |
| 7 | Cartoon carotte nuit | `images/cartoon_carotte_nuit.png` | `images/cartoon_carotte_nuit_en.png` | Section 7 |
| 8 | Propagande WWII carottes | `images/propagande_wwii_carottes.png` | `images/propagande_wwii_carottes_en.png` | Section 8 |

> Note : les images 7 et 8 illustrent la même question ("Manger des carottes améliore la vue dans le noir") — deux sources différentes.

---

## 3. Supabase Storage — images des séries communauté

### Pourquoi c'est nécessaire

Quand un créateur ajoute une image à une source dans le Mode Créateur, elle est stockée en **base64** (une longue chaîne de texte encodée) dans localStorage, puis envoyée telle quelle dans le champ `questions` de la table Supabase lors de la publication.

**Problème :** une image de 500 Ko devient ~670 Ko en base64. Une série avec 3 images = ~2 Mo dans une seule row Supabase. Sur plusieurs séries, les performances se dégradent et on peut atteindre les limites de taille de row Supabase.

**Solution :** utiliser Supabase Storage (un bucket de fichiers) pour héberger les images séparément, et ne stocker que leur URL dans le JSON de la série.

### Ce qu'il faut faire

**Étape 1 — Côté Supabase (5 min, dans le dashboard)**
1. Aller dans ton projet Supabase → Storage → "New bucket"
2. Nommer le bucket `series-images`
3. Le mettre en **Public** (pour que les URLs soient accessibles sans auth)
4. Dans "Policies", autoriser l'upload anonyme (INSERT pour `anon`)

**Étape 2 — Côté code (dans `index.html`, fonction `submitPublish()`)**

Avant d'envoyer les données à Supabase, parcourir toutes les sources de `customQuestions` et, pour chaque `src.img` qui commence par `data:` (= base64) :
1. Convertir la base64 en blob binaire
2. Uploader le blob dans le bucket `series-images` via l'API Storage Supabase
3. Remplacer la base64 par l'URL publique retournée
4. Envoyer le JSON allégé dans la table `packs`

```js
// Pseudo-code de la logique à ajouter dans submitPublish()
async function uploadImagesAndClean(questions) {
  const clean = JSON.parse(JSON.stringify(questions)); // copie profonde
  for(const q of clean) {
    for(const src of q.sources||[]) {
      if(src.img && src.img.startsWith('data:')) {
        const blob = dataURLtoBlob(src.img);
        const filename = crypto.randomUUID() + '.webp';
        const url = await uploadToSupabaseStorage(blob, filename);
        src.img = url; // remplace la base64 par l'URL
      }
    }
  }
  return clean;
}
```

**Fonctions utilitaires à écrire :**
- `dataURLtoBlob(dataURL)` — convertit une data URL en Blob
- `uploadToSupabaseStorage(blob, filename)` — appelle `SB_URL + '/storage/v1/object/series-images/' + filename` avec `method: 'POST'` et la clé API

**Étape 3 — Affichage côté joueur**
Rien à changer : `src.img` contiendra une URL https:// au lieu d'une base64, le `<img src="...">` fonctionne pareil.

---

## 4. Sources non visuelles → à rendre visuelles ou interactives

Ces formats existent dans les questions mais s'affichent aujourd'hui en texte brut (pas d'image). L'objectif est de créer des **classes CSS réutilisables** (sur le modèle de `.fake-insta` existant) et d'ajouter les champs correspondants dans les objets source des questions.

---

### 🥇 Priorité haute

#### `.fake-forum` — Fil de forum internet
- **Sources concernées (8+) :** forum de cuisine (miel), forum de parents (fièvre, chewing-gum, sucre hyperactif), forum de pêche (dauphin), forum "Curiosités et mystères" (foudre), forum santé, forum écologie, commentaire sous vidéo d'aquariophilie (poisson rouge), forum aquariophilie
- **Format visuel :** avatar générique gris + pseudonyme aléatoire + date + texte + barre "👍 12 · 💬 Répondre"
- **Champs à ajouter dans les objets source :** `forumName` (nom du forum), `forumUser` (pseudo), `forumDate`
- **CSS estimé :** ~30 lignes

#### `.fake-whatsapp` — Message transmis / chaîne de messages
- **Sources concernées (5+) :** "Mon tonton", "Voisin qui l'a lu quelque part", "Mamie sur un forum de parents", "Copains dans la cour", "Bouche à oreille voisine"
- **Format visuel :** bulle verte/grise + bannière "⟩ Transféré" au-dessus + texte + heure
- **Champs à ajouter :** `waForwarded: true`, `waSender` (ex : "Tonton Michel")
- **CSS estimé :** ~20 lignes
- **Note pédagogique :** format n°1 de désinformation quotidienne pour les jeunes

---

### 🥈 Priorité moyenne

#### `.fake-gmaps` — Avis Google Maps / TripAdvisor
- **Sources concernées (1–2) :** "Commentaire d'un touriste sur Google Maps" (Grande Muraille), guide touristique Tour Eiffel (possible)
- **Format visuel :** avatar initiales coloré + nom + ⭐⭐⭐⭐⭐ + texte + "Lieu : [nom]"
- **Champs à ajouter :** `gmapsUser`, `gmapsRating` (1–5), `gmapsPlace`
- **CSS estimé :** ~15 lignes

#### `.fake-tweet` — Carte tweet / post X
- **Sources concernées (3–4) :** "Quiz tourisme TikTok" (Tour Eiffel), posts viraux sans image, quelques "Le saviez-vous" en mode texte
- **Format visuel :** @pseudo, texte court, barre 💬 ❤️ 🔁, date
- **Champs à ajouter :** `tweetUser`, `tweetHandle`, `tweetLikes`, `tweetDate`
- **CSS estimé :** ~25 lignes

#### `.fake-blog` — Header d'article de blog
- **Sources concernées (5+) :** Blog "Amoureux des chats", Blog survivaliste "Techniques de survie", Blog "Vivre Naturellement", Blog "La cuisine sans chimie", Blog amateur sur Napoléon
- **Format visuel :** titre H2 + meta (auteur anonyme, date, "🕐 3 min de lecture"), corps tronqué avec "Lire la suite…"
- **Champs à ajouter :** `blogTitle`, `blogAuthor`, `blogDate`, `blogReadTime`
- **CSS estimé :** ~35 lignes

---

### 🎁 Bonus — format interactif

#### Fil de commentaires YouTube empilés
- **Source concernée (1) :** "Commentaire sous une vidéo d'aquariophilie" (poisson rouge mémoire 3s)
- **Format visuel :** plusieurs commentaires empilés (avatar rond + nom + texte), dont un qui dit "scientifiquement prouvé" sans lien
- **Interactivité :** le joueur voit plusieurs commentaires contradictoires et doit évaluer la source globale
- **Champs à ajouter :** `ytComments: [{user, text, likes}]`
- **CSS estimé :** ~40 lignes
- **Note :** nécessite une adaptation JS pour le rendu (pas juste CSS)

---

### Tableau récapitulatif

| Format | Sources concernées | CSS estimé | Impact péda |
|---|---|---|---|
| `.fake-forum` | 8+ sources | ~30 lignes | ⭐⭐⭐ |
| `.fake-whatsapp` | 5+ sources | ~20 lignes | ⭐⭐⭐ |
| `.fake-gmaps` | 1–2 sources | ~15 lignes | ⭐⭐ |
| `.fake-tweet` | 3–4 sources | ~25 lignes | ⭐⭐ |
| `.fake-blog` | 5+ sources | ~35 lignes | ⭐⭐ |
| YouTube commentaires | 1 source (interactif) | ~40 lignes | ⭐⭐⭐ |

---

## 5. État des images déjà intégrées

### Version FR ✅ complète
| Image | Source dans le jeu |
|-------|--------------------|
| `ostrich.webp` | Post Instagram viral — autruche |
| `poisson_3s_memoire_fr.png` | Mème Instagram viral — mémoire des poissons |
| `flamant_rose_fr.png` | Quiz Instagram — couleur des flamants roses |
| `tournesols_soleil_fr.png` | Vidéo Instagram — tournesols et soleil |
| `edison_ampoule_fr.png` | Post "Le saviez-vous ?" — Edison et l'ampoule |
| `influenceur_nutrition_fr.png` | Influenceur nutrition — produits chimiques |
| `militant_vegan_fr.png` | Militant vegan — émissions de l'élevage |
| `jus_carotte_bio.png` | Emballage jus de carotte bio |
| `tiktok_araignees.png` | Post TikTok — araignées avalées |
| `tiktok_chat_ronron.png` | Vidéo TikTok — chat ronron |
| `facebook_napoleon_cochon.png` | Message viral Facebook — cochon Napoléon |
| `magazine_carottes_vue.png` | Article magazine bien-être — carottes et vue |

### Version EN ✅ intégrée
| Image | Source dans le jeu |
|-------|--------------------|
| `ostrich.webp` | Viral Instagram post — ostrich |
| `fish-meme.png` | Viral Instagram meme — fish memory |
| `flamingo-pink.png` | Instagram quiz — flamingo color |
| `sunflowers-sun.png` | Instagram video — sunflowers and sun |
| `edison-lightbulb.png` | "Did you know?" post — Edison |
| `nutrition-chemicals.png` | Nutrition influencer — chemicals |
| `vegan-activist.png` | Vegan activist — livestock emissions |

### EN : pas encore intégrée (en attente des images traduites)
- TikTok araignées EN
- TikTok chat ronron EN
- Facebook cochon Napoléon EN
- Magazine carottes vue EN

---

## 6. Sources texte seul → à rendre visuelles (inventaire complet)

Audit du 24/05/2026 — 155 sources FR + 153 sources EN sont encore en texte brut.
Classées par format visuel applicable. Les composants CSS/JS marqués ✅ **existent déjà** dans `index.html` (`.fake-blog`, `.fake-tweet`, etc.) — il suffit d'ajouter les champs correspondants dans l'objet source. Les composants ❌ **restent à créer**.

---

### 🟢 Composant existant `.fake-blog` ✅ — ajouter `blogTitle`, `blogName`, `blogAuthor`, `blogDate`

| Source FR | Source EN | Ligne FR | Ligne EN |
|---|---|---|---|
| 🪓 Site survivaliste 'Techniques de survie' | 🪓 Survival techniques blog | L257 | L254 |
| 📲 Blog bien-être 'Vivre Naturellement' | 📲 Wellness blog 'Living Naturally' | L515 | L515 |
| 📱 Blog 'La cuisine sans chimie' | 📱 Blog 'Cooking Without Chemicals' | L593 | — |
| 📝 Blog amateur sur l'histoire de Napoléon | 📝 Amateur blog on Napoleon's history | L808 | L808 |

---

### 🟢 Composant existant `.fake-tweet` ✅ — ajouter `tweetUser`, `tweetHandle`, `tweetLikes`, `tweetDate`

| Source FR | Source EN | Ligne FR | Ligne EN |
|---|---|---|---|
| 📱 Quiz tourisme sur TikTok (Tour Eiffel) | 📱 TikTok tourism quiz (Eiffel Tower) | L548 | L545 |
| 📺 Chaîne YouTube influenceur gaming | 📺 Gaming influencer YouTube channel | L848 | L848 |
| 📱 Coach nutrition — YouTube 800k abonnés | 📱 Nutrition coach — YouTube 800k subscribers | L970 | L970 |
| 💻 Post LinkedIn viral — coach développement perso | 💻 Viral LinkedIn post — personal development coach | L1021 | L1021 |
| 💬 Citation attribuée à Voltaire (photo N&B) | 💬 Quote attributed to Voltaire (B&W photo) | L956 | L956 |
| 🌻 Pétition en ligne d'une ONG environnementale | 🌻 Online petition from an environmental NGO | L919 | L919 |
| 🌍 Infographie virale d'une ONG environnementale | 🌍 Viral infographic from an environmental NGO | L834 | L834 |

---

### 🔴 Nouveau composant `.fake-article` à créer — presse écrite / magazine ❌

Format : une à deux colonnes, titre accrocheur en gras, sous-titre, auteur + journal + date, chapeau tronqué avec "Lire la suite…".

| Source FR | Source EN | Ligne FR | Ligne EN |
|---|---|---|---|
| 📰 Titre de presse généraliste | 📰 Mainstream press headline | L852 | L852 |
| 📰 Article magazine famille | 📰 Family magazine article | L532 | L532 |
| 📰 Magazine bien-être | 📰 Wellness magazine | L953 | L953 |
| 📰 Article 'Le bio c'est du marketing' | 📰 Article "Organic is just marketing" | L886 | L886 |
| 📰 Article d'un syndicat agricole | 📰 Article from a farmers' union | L922 | L922 |
| 📰 Article 'Le jeûne, c'est de la torture inutile' | 📰 Article "Fasting is useless torture" | L973 | L973 |
| 📰 Mainstream press headline (lune de pleine lune) | 📰 Mainstream press headline (full moon) | L902 | L902 |

---

### 🔴 Nouveau composant `.fake-paper` à créer — revue scientifique / rapport ❌

Format : header DOI + journal + auteurs, résumé court, indicateurs (n participants, date, impact factor), bouton "Accéder à l'article →".

| Source FR | Source EN | Ligne FR | Ligne EN |
|---|---|---|---|
| 🔬 Revue Science — Université de Cambridge | 🔬 Science journal — University of Cambridge | L186 | L186 |
| 🔬 Journal of Feline Medicine and Surgery | 🔬 Journal of Feline Medicine and Surgery | L202 | L202 |
| 🔬 Revue Zoo Biology | 🔬 Zoo Biology journal | L218 | L218 |
| 🔬 Université de Plymouth — étude comportementale | 🔬 University of Plymouth — behavioral study | L268 | L268 |
| 📚 Revue Animal Cognition | 📚 Animal Cognition journal | L271 | L271 |
| 🔬 Revue de biologie marine | 🔬 Marine biology journal | L409 | L409 |
| 📊 JAMA — méta-analyse 23 études | 📊 JAMA — meta-analysis of 23 studies | L523 | L523 |
| 🔬 Dr William Morden — Journal of Forensic Sciences | 🔬 Dr William Morden — Journal of Forensic Sciences | L640 | L640 |
| 🔬 INSERM — Physiologie de l'alcool | 🔬 INSERM — Physiology of alcohol | L658 | L658 |
| 📈 Étude corrélant temps d'écran et résultats | 📈 Study correlating screen time and results | L735 | L735 |
| 📊 Étude publiée dans Scientific Reports | 📊 Study published in Scientific Reports | L831 | L831 |
| 🎓 Université d'Oxford — étude bien-être joueurs | 🎓 University of Oxford — gamers well-being study | L842 | L842 |
| 📊 Méta-analyse 37 études (Psychological Bulletin) | 📊 Meta-analysis of 37 studies (Psychological Bulletin) | L860 | L860 |
| 📈 Étude 150 000 admissions aux urgences | 📈 Study analyzing 150,000 ER admissions | L866 | L866 |
| 📊 INSERM — Étude NutriNet (2018, 70 000 participants) | 📊 INSERM — NutriNet study (70,000 participants) | L877 | L877 |
| 🔬 EFSA — Rapport sur les pollinisateurs (2023) | 🔬 EFSA — Pollinators report (2023) | L913 | L913 |
| 🌍 IPBES — Rapport mondial sur la biodiversité | 🌍 IPBES — Global biodiversity report | L916 | L916 |
| 📊 Étude Monash — double aveugle (2013) | 📊 Double-blind study — Monash University (2013) | L930 | L930 |
| 📊 Cohorte Oxford (2016, 700 000 femmes) | 📊 Cohort study — Oxford (2016, 700,000 women) | L947 | L947 |
| 🔬 Psychological Science — méta-analyse (2011) | 🔬 Psychological Science — meta-analysis (2011) | L950 | L950 |
| 📊 New England Journal of Medicine (2019) | 📊 New England Journal of Medicine (2019) | L964 | L964 |
| 📚 Annual Review of Nutrition (2022) | 📚 Annual Review of Nutrition (2022) | L967 | L967 |
| 📊 Revue Cochrane — 225 études | 📊 Cochrane Review — 225 studies | L983 | L983 |
| 📊 Neuroscience & Biobehavioral Reviews (2016) | 📊 Neuroscience & Biobehavioral Reviews (2016) | L996 | L996 |
| 🎓 Dr Nicole Avena, Columbia University | 🎓 Dr Nicole Avena, Columbia University | L999 | L999 |
| 📊 Personality and Individual Differences | 📊 Personality and Individual Differences | L1012 | L1012 |
| 🎓 British Journal of Medical Psychology | 🎓 British Journal of Medical Psychology | L1015 | L1015 |
| 📊 Rapport McKinsey Global Institute (2023) | 📊 McKinsey Global Institute report (2023) | L1029 | L1029 |
| 🏦 Rapport du FMI — IA et marché du travail | 🏦 IMF report — AI and the labor market | L1032 | L1032 |

---

### 🔴 Nouveau composant `.fake-book` à créer — couverture de livre ❌

Format : visuel couverture stylisée (couleur générée depuis le titre), titre, auteur, éditeur, nombre d'étoiles Amazon, mention "best-seller" ou "N exemplaires vendus".

| Source FR | Source EN | Ligne FR | Ligne EN |
|---|---|---|---|
| 📕 Livre 'Les 1000 choses à savoir absolument' | 📕 'The 1000 Things You Absolutely Need to Know' | L330 | L330 |
| 📖 Livre de développement personnel (sans sources) | 📖 Personal development book (no cited sources) | L346 | L346 |
| 📖 Best-seller 'Wheat Belly' — Dr William Davis | 📖 Best-seller 'Wheat Belly' — Dr William Davis | L936 | L936 |
| 📕 Livre best-seller 'Zéro sucre en 30 jours' | 📕 Best-seller 'Zero Sugar in 30 Days' | L1005 | L1005 |
| 📕 Biographie populaire de Napoléon | 📕 Popular biography of Napoleon | L816 | L816 |
| 📚 Manuel scolaire des années 1950 | 📚 1950s school textbook | L244 | L244 |
| 📖 Manuel scouting vintage réédité | 📖 Reissued vintage scouting manual | L261 | L261 |
| 📖 Manuel de psychologie des années 1970 | 📖 1970s psychology textbook | L788 | L788 |

---

### 🔴 Nouveau composant `.fake-documentary` à créer — affiche film/docu Netflix ❌

Format : bannière sombre style Netflix/cinéma, logo plateforme, titre en grand, sous-titre, note spectateurs, "▶ Disponible sur…".

| Source FR | Source EN | Ligne FR | Ligne EN |
|---|---|---|---|
| 🎬 Documentaire Netflix sur la pollution plastique | 🎬 Netflix documentary on plastic pollution | L828 | L828 |
| 🎬 Documentaire Netflix 'Ce que le sucre vous fait' | 🎬 Netflix documentary 'What Sugar Does to You' | L1002 | L1002 |
| 🎬 Film biographique hollywoodien (Edison) | 🎬 Hollywood biopic (Edison) | L379 | L379 |
| 🎬 Film historique hollywoodien (Christophe Colomb) | 🎬 Hollywood historical film (Christopher Columbus) | L577 | L577 |
| 🎬 Film 'Les Dents de la Mer' — Making-of | 🎬 Film 'Jaws' — official making-of | L561 | L561 |
| 🎬 Scène de film d'aventure hollywoodien | 🎬 Hollywood adventure film scene | L668 | L668 |
| 📺 Dessin animé avec une chauve-souris aveugle | 📺 Cartoon featuring a blind bat | L402 | L402 |
| 📺 Émission de vulgarisation TV des années 1980 | 📺 1980s science TV show | L195 | L195 |

---

### ⚪ Naturellement texte seul — faible priorité visuelle

Ces sources représentent de l'oral, du ressenti ou du savoir diffus : les rendre "visuelles" n'apporterait pas grand-chose pédagogiquement.

| Source FR | Source EN |
|---|---|
| 🤔 Mon intuition | 🤔 My intuition |
| ✂️ Mon coiffeur | ✂️ My hairdresser |
| 💡 Le bon sens | 💡 Common sense |
| 👴 Proverbe / Dicton populaire | 👴 Popular proverb / Saying |
| 🗣️ Croyance populaire / Expression populaire | 🗣️ Popular belief / expression |
| 🏔️ Dicton populaire de montagne | 🏔️ Mountain folk saying |
| 🗣️ Idée reçue très répandue | 🗣️ Widespread misconception |
| 🗣️ Guide touristique (oral) | 🗣️ Tour guide (oral) |

---

### Résumé priorités

| Format | Composant | Sources FR+EN | Effort |
|---|---|---|---|
| `.fake-blog` | ✅ Existe | 4+4 | 🟢 Faible — juste ajouter les champs |
| `.fake-tweet` | ✅ Existe | 7+7 | 🟢 Faible — juste ajouter les champs |
| `.fake-article` | ❌ À créer | 7+7 | 🟡 Moyen — ~30 lignes CSS + buildArticle() |
| `.fake-paper` | ❌ À créer | 30+30 | 🟡 Moyen — ~35 lignes CSS + buildPaper() |
| `.fake-book` | ❌ À créer | 8+8 | 🟡 Moyen — ~25 lignes CSS + buildBook() |
| `.fake-documentary` | ❌ À créer | 8+8 | 🟡 Moyen — ~30 lignes CSS + buildDoc() |
