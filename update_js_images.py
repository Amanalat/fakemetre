"""Mise a jour des references images dans questions_fr.js et questions_en.js"""
import sys, re
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path

BASE = Path(__file__).parent

# Images qui restent en .png (non converties)
KEEP_PNG = {
    "ostrich.webp", "fish-meme.png", "flamingo-pink.png",
    "sunflowers-sun.png", "vegan-activist.png", "nutrition-chemicals.png",
    "edison-lightbulb.png",
}

def replace_png_to_jpg(content, skip_names):
    """Remplace images/XXX.png -> images/XXX.jpg sauf pour les fichiers skip."""
    def replacer(m):
        name = m.group(1)
        if name in skip_names:
            return m.group(0)
        return f'images/{name[:-4]}.jpg'
    return re.sub(r'images/([^\'"]+\.png)', replacer, content)

def add_img_before(content, search_str, img_path):
    """Ajoute img:"images/XXX" juste avant search_str si pas deja present."""
    if f'img:"images/{img_path}"' in content:
        print(f"  [DEJA PRESENT] {img_path}")
        return content
    # Cherche la position du patron
    idx = content.find(search_str)
    if idx == -1:
        print(f"  [PATRON INTROUVABLE] pour {img_path}: {search_str[:60]}")
        return content
    # Trouve le debut de la ligne contenant search_str
    # On insere img: juste avant le patron
    insert = f'img:"images/{img_path}",'
    new_content = content[:idx] + insert + content[idx:]
    print(f"  [AJOUTE] {img_path}")
    return new_content

# ──────────────────────────────────────────
# QUESTIONS_FR.JS
# ──────────────────────────────────────────
print("=== questions_fr.js ===")
fr_path = BASE / "questions_fr.js"
fr = fr_path.read_text(encoding="utf-8")

# 1. PNG -> JPG global
fr = replace_png_to_jpg(fr, KEEP_PNG)

# 2. Remplacer caricature_gillray par caricature_napoleon
fr = fr.replace('img:"images/caricature_gillray.jpg"', 'img:"images/caricature_napoleon.jpg"')
print("  [REMPLACE] caricature_gillray -> caricature_napoleon")

# 3. Ajouter les images manquantes — on insere juste avant le champ distinctif

# emballage_carottes_bio — Junior, carotte vue
fr = add_img_before(fr, "adType:'packaging',adBrand:'Bio Jardin'", "emballage_carottes_bio.jpg")

# opera_wagner_vikings
fr = add_img_before(fr, "mediaType:'opera',mediaTitle:'Lohengrin'", "opera_wagner_vikings.jpg")

# jeu_video_vikings
fr = add_img_before(fr, "mediaType:'game',mediaTitle:'Age of Vikings II'", "jeu_video_vikings.jpg")

# pub_tv_eau_bouteille
fr = add_img_before(fr, "adType:'tv',adBrand:'AquaVita'", "pub_tv_eau_bouteille.jpg")

# emission_tv_annees80
fr = add_img_before(fr, "mediaType:'tv',mediaTitle:'Le Monde des Animaux'", "emission_tv_annees80.jpg")

# ted_conference
fr = add_img_before(fr, "mediaType:'ted',mediaTitle:'Mon coup de foudre", "ted_conference.jpg")

# youtube_gaming_thumbnail
fr = add_img_before(fr, "mediaType:'youtube',mediaTitle:'Les jeux vid", "youtube_gaming_thumbnail.jpg")

# livre_larousse_junior — autruche question
fr = add_img_before(fr, "bookType:'encyclopedie',bookTitle:'Larousse Junior'",
                    "livre_larousse_junior.jpg")
# Si encode different
fr = add_img_before(fr, "bookType:'encyclopédie',bookTitle:'Larousse Junior'",
                    "livre_larousse_junior.jpg")

# manuel_sciences_1950
fr = add_img_before(fr, "bookType:'manuel',bookTitle:'Sciences Naturelles',bookYear:'1952'",
                    "manuel_sciences_1950.jpg")

# magazine_clim_pollution — source magazine clim
fr = add_img_before(fr, 'pressOutlet:"Magazine grand public",pressDomain:""',
                    "magazine_clim_pollution.jpg")

# livre_wheat_belly — gluten question
fr = add_img_before(fr, "bookType:'livre',bookTitle:'Wheat Belly'", "livre_wheat_belly.jpg")

# livre_fabriquecretin — ecrans question
fr = add_img_before(fr, "bookTitle:'La fabrique du crétin digital'", "livre_fabriquecretin.jpg")

# blog_survivaliste_mousse — mousse question
fr = add_img_before(fr, 'blogSite:"techniques-de-survie.fr"', "blog_survivaliste_mousse.jpg")

# pub_sans_gluten — gluten-free products
fr = add_img_before(fr, "adType:'store',adBrand:'Bio & Nature'", "pub_sans_gluten.jpg")

fr_path.write_text(fr, encoding="utf-8")
print("  -> Fichier sauvegarde\n")

# ──────────────────────────────────────────
# QUESTIONS_EN.JS
# ──────────────────────────────────────────
print("=== questions_en.js ===")
en_path = BASE / "questions_en.js"
en = en_path.read_text(encoding="utf-8")

# 1. PNG -> JPG global
en = replace_png_to_jpg(en, KEEP_PNG)

# 2. Corrections des versions EN specifiques
en = en.replace('img:"images/caricature_gillray.jpg"', 'img:"images/caricature_napoleon_en.jpg"')
print("  [REMPLACE] caricature_gillray -> caricature_napoleon_en")

en = en.replace('img:"images/etude_desert_cactus.jpg"', 'img:"images/etude_desert_cactus_en.jpg"')
print("  [REMPLACE] etude_desert_cactus -> etude_desert_cactus_en")

en = en.replace('img:"images/guide_wms_survie.jpg"', 'img:"images/guide_wms_survie_en.jpg"')
print("  [REMPLACE] guide_wms_survie -> guide_wms_survie_en")

en = en.replace('img:"images/livre_survie_cactus.jpg"', 'img:"images/livre_survie_cactus_en.jpg"')
print("  [REMPLACE] livre_survie_cactus -> livre_survie_cactus_en")

# 3. Ajouter images manquantes EN
# On cherche les patrons equivalents en anglais

# emballage_carottes_bio_en — "Bio Garden" packaging
en = add_img_before(en, "adBrand:'Bio Garden'", "emballage_carottes_bio_en.jpg")

# opera_wagner_vikings_en
en = add_img_before(en, "mediaType:'opera',mediaTitle:'Lohengrin'", "opera_wagner_vikings_en.jpg")

# jeu_video_vikings_en
en = add_img_before(en, "mediaType:'game',mediaTitle:'Age of Vikings II'", "jeu_video_vikings_en.jpg")

# pub_tv_eau_bouteille_en
en = add_img_before(en, "adType:'tv',adBrand:'AquaVita'", "pub_tv_eau_bouteille_en.jpg")

# emission_tv_annees80_en
en = add_img_before(en, "mediaType:'tv',mediaTitle:'Le Monde des Animaux'", "emission_tv_annees80_en.jpg")

# ted_conference_en
en = add_img_before(en, "mediaType:'ted',mediaTitle:", "ted_conference_en.jpg")

# youtube_gaming_thumbnail_en
en = add_img_before(en, "mediaType:'youtube',mediaTitle:", "youtube_gaming_thumbnail_en.jpg")

# livre_larousse_junior_en — "Britannica Junior"
en = add_img_before(en, "bookTitle:'Britannica Junior'", "livre_larousse_junior_en.jpg")

# manuel_sciences_1950_en
en = add_img_before(en, "bookYear:'1952'", "manuel_sciences_1950_en.jpg")

# magazine_clim_pollution_en
en = add_img_before(en, 'pressOutlet:"Magazine grand public",pressDomain:""',
                    "magazine_clim_pollution_en.jpg")

# livre_wheat_belly_en
en = add_img_before(en, "bookTitle:'Wheat Belly'", "livre_wheat_belly_en.jpg")

# livre_fabriquecretin_en — "The Digital Moron Factory" or similar
en = add_img_before(en, "bookTitle:'The Digital Moron Factory'", "livre_fabriquecretin_en.jpg")

# blog_survivaliste_mousse_en
en = add_img_before(en, 'blogSite:"techniques-de-survie.fr"', "blog_survivaliste_mousse_en.jpg")

# pub_sans_gluten_en
en = add_img_before(en, "adType:'store',adBrand:'Bio & Nature'", "pub_sans_gluten_en.jpg")

en_path.write_text(en, encoding="utf-8")
print("  -> Fichier sauvegarde\n")

# ──────────────────────────────────────────
# VERIFICATION FINALE
# ──────────────────────────────────────────
fr2 = (BASE / "questions_fr.js").read_text(encoding="utf-8")
en2 = (BASE / "questions_en.js").read_text(encoding="utf-8")

fr_imgs = re.findall(r'img\s*:\s*"images/([^"]+)"', fr2)
en_imgs = re.findall(r'img\s*:\s*"images/([^"]+)"', en2)

print(f"FR : {len(fr_imgs)} img references")
print(f"EN : {len(en_imgs)} img references")

# Check remaining PNG refs (hors keep_png)
fr_pngs = [i for i in fr_imgs if i.endswith('.png') and i not in KEEP_PNG]
en_pngs = [i for i in en_imgs if i.endswith('.png') and i not in KEEP_PNG]
if fr_pngs: print(f"  FR refs .png restantes: {fr_pngs}")
if en_pngs: print(f"  EN refs .png restantes: {en_pngs}")
if not fr_pngs and not en_pngs:
    print("  OK - Plus de refs .png (hors fichiers legacy)")
