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

## 4. État des images déjà intégrées

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
