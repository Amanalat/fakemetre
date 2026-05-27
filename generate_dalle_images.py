"""
generate_dalle_images.py — Génère les images manquantes pour FakeMètre avec DALL-E 3

Usage:
    python generate_dalle_images.py              # Génère toutes les images manquantes
    python generate_dalle_images.py --dry-run    # Liste ce qui serait généré (sans appel API)
    python generate_dalle_images.py --filter ted # Génère uniquement les images contenant "ted"
    python generate_dalle_images.py --list       # Liste toutes les images définies

API key : définir OPENAI_API_KEY en variable d'environnement
   ou créer un fichier .env avec OPENAI_API_KEY=sk-...
"""

import os
import sys
import time
import argparse
import base64
from pathlib import Path

# Encodage UTF-8 pour la console Windows
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────
IMAGES_DIR = Path(__file__).parent / "images"
RATE_LIMIT_DELAY = 8   # secondes entre appels
MODEL = "gpt-image-2"  # dall-e-3 est déprécié depuis 2025

# Tailles supportées par gpt-image-2
# (différentes de dall-e-3 : portrait = 1024x1536, paysage = 1536x1024)
SIZE_MAP = {
    "1024x1024": "1024x1024",   # carré → carré
    "1024x1792": "1024x1536",   # portrait → portrait
    "1792x1024": "1536x1024",   # paysage → paysage
}

# Coût gpt-image-2 standard (USD) — à titre indicatif
COST = {
    "1024x1024": 0.04,
    "1024x1792": 0.07,
    "1792x1024": 0.07,
}

# ─────────────────────────────────────────────
# Prompts — clé = nom de fichier sans extension ni _en
# Chaque entrée : size, fr (prompt FR → fichier.png), en (prompt EN → fichier_en.png)
# ─────────────────────────────────────────────
IMAGES = {

    # ══════════════════════════════════════════
    # FILMS ET DOCUMENTAIRES (manquants)
    # ══════════════════════════════════════════

    "emission_tv_annees80": {
        "size": "1024x1024",
        "fr": (
            "Capture d'ecran simulee d'une emission de vulgarisation scientifique francaise des annees 1980, "
            "format 4:3. Qualite video degradee authentique : grain VHS marque, legere distorsion de balayage "
            "CRT horizontale, couleurs legerement dessaturees tirant vers le jaune-orange. Bandeaux noirs haut "
            "et bas. Cadre legerement bombe comme un ecran CRT convexe. En bas, generique incrust blanc "
            "Helvetica : 'LE MONDE DES ANIMAUX' a gauche et 'Antenne 2 — 1983' a droite sur bande noire "
            "semi-transparente. Au centre : presentateur en costume marron/beige, cravate bordeaux, cheveux "
            "raie sur le cote, micro a main metallique gris. Il se tient devant un ecran de projection avec "
            "des images de chimpanzes en foret. Expression serieuse et pedagogique. Eclairage de studio cru, "
            "legerement sur-expose sur le visage."
        ),
        "en": (
            "Simulated screenshot of a French 1980s science TV show, 4:3 format. Authentic degraded video "
            "quality: heavy VHS grain, slight CRT horizontal scan distortion, slightly desaturated colors with "
            "yellow-orange cast. Black bars at top and bottom. Slightly convex frame like a real CRT screen. "
            "Bottom caption in white Helvetica: 'LE MONDE DES ANIMAUX' on left and 'Antenne 2 — 1983' on right "
            "on semi-transparent black bar. Center: male TV presenter in brown/beige suit with burgundy tie, "
            "hair parted on the side, holding a vintage grey metal hand microphone. He stands in front of a "
            "projection screen showing chimpanzees in a forest. Serious, pedagogical expression. Harsh studio "
            "lighting, slightly overexposed face."
        ),
    },

    "opera_wagner_vikings": {
        "size": "1024x1792",
        "fr": (
            "Illustration de style gravure victorienne XIXe siecle d'une scene d'opera romantique allemand, "
            "format portrait. Palette sepia chaude avec accents rouge sombre et or. Traits fins d'encre noire "
            "sur papier creme legerement jauni, hachures croisees pour les ombres, style gravure de livre "
            "d'epoque. Scene sur scene d'opera : personnage central masculin imposant, barbe longue broussailleuse, "
            "cape flottante, bras tendus en posture dramatique. Sur sa tete : un casque a cornes monumentales "
            "et recourbees, brillant, ornements metalliques graves. A cote, une valkyrie en robe longue avec "
            "un casque similaire. Decor de fond : colonnes nordiques stylisees, ciel nocturne nuages tourmentés. "
            "En bas cartouche calligraphie XIXe : 'LOHENGRIN — Drame lyrique de R. Wagner — 1850'. "
            "Lumiere theatrale dramatique venant d'en bas."
        ),
        "en": (
            "Victorian 19th-century engraving style illustration of a romantic German opera scene, portrait "
            "format. Warm sepia palette with dark red and gold accents. Fine black ink lines on slightly yellowed "
            "cream paper, cross-hatching for shadows, period book engraving style. Stage scene: imposing central "
            "male character, long bushy beard, flowing cape, arms outstretched in dramatic operatic posture. "
            "On his head: monumental curved horned helmet, gleaming, engraved metal ornaments. Beside him, a "
            "valkyrie in a long gown with a similar horned helmet. Background: stylized Nordic columns, stormy "
            "night sky with turbulent clouds. Bottom manuscript cartouche in 19th-century calligraphy: "
            "'LOHENGRIN — Lyric Drama by R. Wagner — 1850'. Dramatic theatrical lighting from below."
        ),
    },

    "jeu_video_vikings": {
        "size": "1792x1024",
        "fr": (
            "Capture d'ecran realiste d'un jeu video de combat medieval fictif, format 16:9. Style fantasy AAA "
            "annees 2010, rendu 3D realiste mais stylise, couleurs saturees. Scene de combat : guerrier viking "
            "jouable au premier plan vu de dos. Son casque : enorme, metal bruni avec motifs nordiques graves et "
            "deux cornes massives et recourbees brillantes, spectaculaires. Armure metal et fourrure animale, "
            "hache de combat a la main. Decor : village nordique en flammes, ciel rouge sang, fumee noire. "
            "Interface HUD : barre de vie rouge 'HP: 847/1200', barre rage bleue 'RAGE: 65%', minimap circulaire "
            "avec points ennemis, 3 icones de competences, inventaire. Coin inferieur droit : logo fictif "
            "'AGE OF VIKINGS II' en runes dorees. Effet profondeur de champ, lueur de feu sur le casque. "
            "Qualite graphique photoréaliste type Unreal Engine."
        ),
        "en": (
            "Realistic screenshot of a fictional medieval combat video game, 16:9 format. Fantasy AAA 2010s "
            "graphic style, realistic but stylized 3D rendering, saturated colors. Combat scene: playable Viking "
            "warrior in foreground seen from behind. His helmet: enormous, burnished metal with engraved Nordic "
            "motifs and two massive curved gleaming horns, spectacular. Metal and animal fur armor, battle axe "
            "in hand. Setting: burning Nordic village, blood-red sky, black smoke. HUD interface: red health "
            "bar 'HP: 847/1200', blue rage bar 'RAGE: 65%', circular minimap with red enemy dots, 3 skill icons "
            "with cooldowns, inventory. Lower right corner: fictional game logo 'AGE OF VIKINGS II' in gold "
            "runic letters. Depth of field effect, firelight glow on helmet. Photorealistic quality, Unreal "
            "Engine style."
        ),
    },

    "ted_conference": {
        "size": "1792x1024",
        "fr": (
            "Photo simulee d'une conference TED, format paysage 16:9, style photo de presse professionnelle. "
            "Eclairage de scene theatral sombre avec fond noir total. Plancher de scene rouge vif TED bien "
            "visible. A gauche de l'image, grand logo 'TED' blanc sur fond rouge dans le coin. Oratrice : "
            "femme d'une cinquantaine d'annees, cheveux courts, tailleur professionnel sombre, tenant un "
            "pointeur laser. Elle se tient a cour de la scene, bras leve vers l'ecran de projection. Ecran "
            "de projection derriere elle occupant la moitie droite : diapositive claire sur fond blanc montrant "
            "une illustration anatomique du cerveau vue de dessus, coupe en deux hemispheres bien separes. "
            "Hemisphere gauche en bleu : 'LOGIQUE · LANGAGE · ANALYSE'. Hemisphere droit en rouge-orange : "
            "'CREATIVITE · INTUITION · EMOTIONS'. Fleche blanche au centre. Titre de la diapo en gras : "
            "'MON COUP DE FOUDRE CEREBRAL — Jill Bolte Taylor · TED 2008'. Silhouettes du public visibles "
            "en bas dans l'ombre."
        ),
        "en": (
            "Simulated TED talk photo, landscape 16:9 format, professional press photo style. Dramatic dark "
            "stage lighting with total black background. Bright red TED stage floor clearly visible. Top left "
            "corner: large 'TED' white logo on red background. Speaker: a woman in her fifties, short hair, "
            "dark professional suit jacket, holding a laser pointer. She stands center stage, arm raised toward "
            "projection screen. Projection screen behind her occupying right half of image: clear slide on white "
            "background showing anatomical top-view illustration of the human brain, split into two clearly "
            "separated hemispheres. Left hemisphere colored blue: 'LOGIC · LANGUAGE · ANALYSIS'. Right "
            "hemisphere in red-orange: 'CREATIVITY · INTUITION · EMOTIONS'. White arrow in center. Slide "
            "title in bold: 'MY STROKE OF INSIGHT — Jill Bolte Taylor · TED 2008'. Audience silhouettes "
            "visible in the shadow of the front row."
        ),
    },

    "youtube_gaming_thumbnail": {
        "size": "1792x1024",
        "fr": (
            "Miniature YouTube fictive realiste, format 16:9 (1280x720). Style clickbait gaming ultra-flashy. "
            "Fond : degrade explosif violet-bleu electrique avec eclairs et particules flottantes. A droite : "
            "jeune homme d'une vingtaine d'annees, joie totale exageree, bouche grande ouverte, yeux ecarquilles. "
            "Il porte un casque gaming RGB avec leds bleues, t-shirt noir avec logo de manette fictive. Sa main "
            "fait un pouce en l'air enorme vers la camera. A gauche : tres grandes lettres grasses blanches avec "
            "contour noir epais et ombre portee rouge, sur 3 lignes : 'LES JEUX VIDEO' puis 'C EST QUE DU BON !!' "
            "puis 'C EST PROUVE !!'. Petite fleche jaune pointant vers le visage. Coin superieur gauche : avatar "
            "de chaine 'GamingAvecMax'. Coin inferieur droit : badge vues '2,3M vues'. Duree '18:42' en haut a "
            "droite. Couleurs : violet, bleu electrique, jaune flashy, rouge. Style miniature YouTube gaming "
            "ultra-sature annees 2020."
        ),
        "en": (
            "Realistic fictional YouTube thumbnail, 16:9 format (1280x720). Ultra-flashy gaming clickbait style. "
            "Background: explosive electric blue-purple gradient with lightning bolts and floating particles. "
            "Right side: young man in his twenties with exaggerated total joy expression — wide open mouth, eyes "
            "wide, eyebrows raised to the max. He wears an RGB gaming headset with lit blue LEDs, black t-shirt "
            "with fictional controller logo. His hand gives a huge thumbs up toward the camera. Left side: very "
            "large bold white text with thick black outline and red drop shadow, on 3 lines: 'VIDEO GAMES' then "
            "'ARE ONLY GOOD!!' then 'IT S PROVEN!!'. Small yellow arrow pointing at gamer's face. Top left: "
            "channel avatar 'GamingAvecMax'. Bottom right: yellow views badge '2.3M views'. Duration '18:42' "
            "top right. Colors: purple, electric blue, flashy yellow, red. Typical ultra-saturated 2020s YouTube "
            "gaming thumbnail style."
        ),
    },

    "caricature_napoleon": {
        "size": "1024x1792",
        "fr": (
            "Caricature politique de style gravure britannique authentique du debut XIXe siecle (circa 1803), "
            "format portrait. Technique : encre noire et lavis brun-sepia sur papier creme jauni, hachures "
            "croisees pour les volumes, style James Gillray tres reconnaissable. Scene principale : groupe de "
            "4 personnages en pied. Au centre a gauche : Napoleon Bonaparte represente comme un nain grotesque "
            "mesurant a peine jusqu'aux hanches des autres. Bicorne enorme plus grand que sa tete, redingote "
            "militaire verte avec medailles, bottes trop grandes. Expression colereuse et vantarde, poing leve. "
            "Face a lui : trois hommes d'Etat britanniques immenses et dignes, sourire moqueur et condescendant "
            "de haut. L'un se penche pour regarder Napoleon comme un insecte. Bulle de dialogue Napoleon : "
            "'Je suis le maitre de l Europe !' en francais. Bulle Britannique : 'Poor little Boney !' Decor : "
            "carte de l'Europe et drapeaux britanniques. En bas : titre manuscrit anglais 'Little Boney — A "
            "Political Satyr' et signature stylisee 'J. Gillray fecit, 1803'. Papier aux bords legerement "
            "irreguliers et brunis."
        ),
        "en": (
            "Authentic British political caricature engraving style from the early 19th century (circa 1803), "
            "portrait format. Technique: black ink and brown-sepia wash on yellowed cream paper, cross-hatching "
            "for volumes, very recognizable James Gillray style. Main scene: group of 4 full-length figures. "
            "Center-left: Napoleon Bonaparte depicted as a grotesque dwarf barely reaching the others' hips. "
            "Enormous bicorne hat bigger than his head, green military greatcoat with medals, oversized boots. "
            "Angry and boastful expression, fist raised. Facing him: three immense dignified British statesmen "
            "looking down at Napoleon with mocking condescending smiles. One leans over to look at Napoleon like "
            "an insect. Napoleon speech bubble: 'Je suis le maitre de l Europe!' Speech bubble from a Briton: "
            "'Poor little Boney!' Background: map of Europe and British flags. Bottom: handwritten title "
            "'Little Boney — A Political Satyr' and stylized signature 'J. Gillray fecit, 1803'. Paper with "
            "slightly irregular and browned edges."
        ),
    },

    # ══════════════════════════════════════════
    # LIVRES ET MANUELS (manquants)
    # ══════════════════════════════════════════

    "livre_larousse_junior": {
        "size": "1024x1024",
        "fr": (
            "Photo realiste d'une encyclopedie pour enfants fictive des annees 1990 posee ouverte sur une table. "
            "Couverture cartonnee usee, couleurs vives primaires annees 90 : fond rouge vif, bande jaune en haut, "
            "bande bleue en bas. Titre en grandes lettres blanches grasses : 'LAROUSSE JUNIOR' suivi de "
            "'L Encyclopedie des jeunes curieux'. Millésime en jaune : 'Edition 1993'. Illustration de couverture "
            "style dessin vectoriel annees 90 : enfants de differentes nationalites tenant les mains en cercle "
            "autour du globe terrestre. Le livre est ouvert sur une double page consacree aux animaux du desert. "
            "Page de gauche : illustration d'autruche en couleur style encyclopedie educative annees 90, style "
            "semi-realiste. La legende dit lisiblement : 'L autruche, comme tout le monde le sait, enfonce sa "
            "tete dans le sable pour se cacher du danger.' Page de droite : texte en deux colonnes, police "
            "Times New Roman, titre 'L AUTRUCHE' et petite carte de l'Afrique. Pages legerement jaunies."
        ),
        "en": (
            "Realistic photo of a fictional 1990s children's encyclopedia laid open on a table. Worn hardcover, "
            "typical 1990s bright primary colors: bright red background, yellow band at the top, blue band at "
            "the bottom. Title in large bold white letters: 'BRITANNICA JUNIOR' followed by 'The Encyclopedia "
            "for Young Minds'. Vintage year in yellow: 'Edition 1993'. Cover illustration in 90s vector drawing "
            "style: children of different nationalities holding hands in a circle around the globe. The book "
            "is open on a double-page spread about desert animals. Left page: a color ostrich illustration in "
            "1990s educational encyclopedia style, semi-realistic. The illustration caption reads clearly: "
            "'The ostrich, as everyone knows, buries its head in the sand when frightened by danger.' Right "
            "page: article text in two columns, Times New Roman font, header 'THE OSTRICH' and small map of "
            "Africa. Pages slightly yellowed."
        ),
    },

    "manuel_sciences_1950": {
        "size": "1024x1024",
        "fr": (
            "Photo realiste d'un vieux manuel scolaire fictif des annees 1950 pose ouvert sur un bureau en bois "
            "sombre, lumiere de bureau chaleureux. Couverture cartonnee epaisse, toile verte/marron usee, coins "
            "taches et ecrases. Etiquette de nom collée sur la couverture avec 'Jean-Pierre M.' inscrit a l'encre. "
            "Titre frappe en relief dore sur la couverture : 'SCIENCES NATURELLES — Cours elementaire CM1-CM2' "
            "editeur fictif 'Librairie Hachette — Paris, 1952'. Le livre est ouvert sur une double page concernant "
            "les animaux marins. Page de gauche : 4 illustrations scientifiques en noir et blanc style gravure "
            "educative annees 50 — trait propre, ombrage hachure. Les illustrations montrent : une baleine bleue "
            "etiquetee 'GRAND POISSON DES MERS', un dauphin etiquete 'POISSON DAUPHIN', un marsouin, et une "
            "sardine pour comparaison. Page de droite : texte en deux colonnes, police serife corps 9, papier "
            "tres jauni : 'Les baleines, dauphins et marsouins sont des poissons de grande taille. La baleine "
            "est le plus grand de tous les poissons connus.' Annotations manuscrites au crayon en marge. "
            "Une regle en bois posee en travers des pages."
        ),
        "en": (
            "Realistic photo of a fictional 1950s school science textbook laid open on a dark wooden desk, warm "
            "desk lamp light. Thick cardboard cover, worn green/brown cloth, stained and crushed corners. Label "
            "stuck on the cover with the name 'James P.' written in ink. Title embossed in slightly faded gold: "
            "'NATURAL SCIENCES — Elementary Course Grades 4-5' fictional publisher 'Oxford Educational Press — "
            "London, 1952'. The book is open on a double-page spread about marine animals. Left page: 4 black "
            "and white scientific illustrations in 1950s educational engraving style — clean lines, hatched "
            "shading. Illustrations show: a blue whale labeled 'GREAT FISH OF THE SEAS', a dolphin labeled "
            "'DOLPHIN FISH', a porpoise, and a sardine for comparison. Right page: text in two columns, serif "
            "size 9 font, very yellowed paper: 'Whales, dolphins and porpoises are large fish. The whale is "
            "the largest of all known fish.' Pencil annotations in the margin by a former student. "
            "A wooden ruler lying across the pages."
        ),
    },

    "livre_wheat_belly": {
        "size": "1024x1792",
        "fr": (
            "Photo realiste d'une couverture de livre de regime anti-gluten fictif style best-seller medical "
            "americain, format portrait, posee sur fond blanc neutre. Couverture brillante, qualite impression "
            "professionnelle. Palette : vert vif, blanc pur, rouge alerte. En haut de la couverture, bandeau "
            "rouge : 'VENDU A 3 MILLIONS D EXEMPLAIRES DANS LE MONDE'. Au centre, illustration principale : "
            "une baguette de pain doree avec un enorme pictogramme d'interdiction rouge (cercle barre) superpose. "
            "Titre en tres grandes lettres : 'WHEAT BELLY' sur deux lignes, police ultra-grasse condensee, "
            "couleur vert vif. Sous-titre en blanc plus petit : 'Comment le ble moderne empoisonne votre cerveau, "
            "votre poids et votre sante'. Bandeau vert en bas avec nom de l'auteur : 'Dr William Davis — "
            "Cardiologue'. Petit badge jaune en haut a droite : 'N 1 NEW YORK TIMES BESTSELLER'."
        ),
        "en": (
            "Realistic photo of a fictional American anti-gluten diet book cover in medical bestseller style, "
            "portrait format, placed on neutral white background. Glossy cover, professional print quality. "
            "Color palette: vivid green, pure white, alert red. Top: red banner with bold text: '3 MILLION "
            "COPIES SOLD WORLDWIDE'. Center: main illustration — a golden shiny baguette with a huge red "
            "prohibition symbol (crossed circle) superimposed, close-up. Title in very large letters: "
            "'WHEAT BELLY' on two lines, ultra-bold condensed font, vivid green color. White smaller subtitle: "
            "'How modern wheat destroys your brain, your weight and your health'. Green banner at the bottom "
            "with author name: 'Dr William Davis — Cardiologist'. Small yellow badge top right: "
            "'NUMBER 1 NEW YORK TIMES BESTSELLER'."
        ),
    },

    "livre_fabriquecretin": {
        "size": "1024x1792",
        "fr": (
            "Photo realiste d'une couverture de livre de neurosciences grand public fictif style essai francais, "
            "format portrait, sur fond blanc. Couverture brillante soignee, style editions Seuil ou Albin Michel. "
            "Palette : fond blanc pur, rouge vif pour les elements d'alerte, noir pour les textes. Composition "
            "epuree et graphique. En haut, nom de l'auteur en police serife noire : 'Michel Desmurget — Directeur "
            "de recherche au CNRS'. Au centre, illustration principale : un cerveau humain vu de profil, rendu "
            "semi-realiste, a l'interieur duquel est insere un smartphone allume dont l'ecran diffuse une lumiere "
            "bleue. Le cerveau presente des fissures/craquelures rouges irradiant depuis le smartphone, comme "
            "un verre casse, sur fond blanc pur. Titre en tres grandes lettres noires grasses sans serif : "
            "'LA FABRIQUE DU CRETIN DIGITAL' sur trois lignes, le mot 'CRETIN' le plus grand et en rouge. "
            "Sous-titre en italique noir : 'Les dangers des ecrans pour nos enfants'. Bande rouge en bas : "
            "'PRIX DU LIVRE POLITIQUE 2020 — Vendu a 400 000 exemplaires'."
        ),
        "en": (
            "Realistic photo of a fictional popular neuroscience book cover in French essay style, portrait "
            "format, on white background. Polished glossy cover, Seuil or Albin Michel publishing style. "
            "Color palette: pure white background, vivid red for alert elements, black for text. Clean graphic "
            "composition. Top: author name in black serif font: 'Michel Desmurget — Research Director, CNRS'. "
            "Center: main illustration — a human brain in profile, semi-realistic rendering, inside which a lit "
            "smartphone is inserted, screen emitting blue light. The brain shows red cracks/fractures radiating "
            "from the smartphone, like broken glass, all on pure white background. Title in very large bold "
            "black sans-serif letters: 'THE DIGITAL MORON FACTORY' on three lines, the word 'MORON' being the "
            "largest and in red. Black italic subtitle: 'The dangers of screens for our children'. Red band at "
            "the bottom: 'BEST POLITICAL BOOK AWARD 2020 — 400,000 copies sold'."
        ),
    },

    # ══════════════════════════════════════════
    # PUBLICITÉS (manquantes)
    # ══════════════════════════════════════════

    "pub_tv_eau_bouteille": {
        "size": "1792x1024",
        "fr": (
            "Capture d'ecran d'une publicite televisee fictive francaise pour eau en bouteille, format 16:9. "
            "Style pub TV grand public haut de gamme annees 2010, photographie professionnelle, lumiere naturelle "
            "doree de fin d'apres-midi. Scene principale : famille heureuse — pere, mere et deux jeunes enfants "
            "— autour d'une table de jardin en bois blanche. La mere verse de l'eau depuis une bouteille en verre "
            "elegant 'AquaVita' (bouteille transparente, etiquette bleu glacier avec sommet montagneux enneige). "
            "Les enfants sourient et tendent leur verre. Jardin verdoyant en arriere-plan flou, haie bien taillee, "
            "ciel bleu sans nuage. En surimpression en bas : slogan en police serife elegante bleu glacier : "
            "'AquaVita — L eau pure pour une vie pure.' Juste en dessous : 'Parce que votre famille merite mieux "
            "que l eau du robinet.' Logo fictif 'AquaVita' en haut a droite : cercle bleu avec flocon de neige "
            "stylise. Mise en scene publicitaire parfaitement composee, couleurs chaudes et lumiere golden hour."
        ),
        "en": (
            "Screenshot of a fictional French television advertisement for bottled water, 16:9 format. "
            "High-end French TV commercial style from the 2010s, professional photography, natural golden "
            "late-afternoon light. Main scene: a happy family — father, mother and two young children — around "
            "a white wooden garden table. The mother pours water from an elegant glass 'AquaVita' bottle "
            "(transparent bottle, glacier blue label with a snowy mountain peak). The children smile and hold "
            "out their glasses. Green garden in the blurred background, neatly trimmed hedge, clear blue sky. "
            "Bottom overlay: slogan in elegant spaced serif font in glacier blue: 'AquaVita — Pure water for "
            "a pure life.' Just below: 'Because your family deserves better than tap water.' Fictional 'AquaVita' "
            "logo top right: blue circle with stylized snowflake. Perfectly composed advertising staging, "
            "warm colors and golden hour light."
        ),
    },

    "emballage_carottes_bio": {
        "size": "1024x1792",
        "fr": (
            "Photo realiste d'un emballage de carottes bio fictif pose sur un fond blanc en rayon de supermarche, "
            "format portrait legerement incline. Sachet en filet ou barquette carton recyclé avec film "
            "transparent. Palette : orange vif pour la dominante, vert feuille, blanc creme, brun terre. En haut "
            "de l'emballage : logo de marque fictive 'Bio Jardin' en lettres rondes vertes avec une feuille "
            "stylisee. En tres grande police orange grasse : 'Carottes Biologiques — Sachet 500g'. Illustration "
            "centrale : photo appetissante de carottes entieres brillantes avec leurs fanes vertes fraiches. "
            "Sur l'image des carottes, etiquette adhesive en forme d'oeil stylise orange et vert : "
            "'Naturellement bon pour vos yeux !' En bas a gauche : grand logo rond officiel 'AB Agriculture "
            "Biologique' vert et blanc. En bas a droite : logo Euro Feuille. Au centre bas, texte marketing "
            "vert : 'Nos carottes sont riches en beta-carotene pour une bonne vision ! Mangez-en tous les jours !'. "
            "Code-barres fictif."
        ),
        "en": (
            "Realistic photo of a fictional organic carrot packaging placed on a white background or supermarket "
            "shelf, portrait format slightly tilted. Net bag or recycled cardboard tray with transparent film. "
            "Color palette: vivid orange as the dominant, leaf green, cream white, earth brown. Top of packaging: "
            "fictional brand logo 'Bio Garden' in rounded green letters with a stylized leaf. In very large bold "
            "orange font: 'Organic Carrots — 500g bag'. Central illustration: appetizing photo of whole shiny "
            "bright orange carrots with fresh green tops. On the carrot photo, a sticker in the shape of a "
            "stylized orange and green eye: 'Naturally good for your eyes!' Bottom left: large round official "
            "'Organic Certified' logo in green and white. Bottom right: Euro Leaf logo. Bottom center, green "
            "marketing text: 'Our carrots are rich in beta-carotene for better vision! Eat them every day!'. "
            "Fictional barcode."
        ),
    },

    "pub_sans_gluten": {
        "size": "1792x1024",
        "fr": (
            "Photo realiste d'un rayon de supermarche fictif dedie aux produits 'Sans gluten', format paysage "
            "16:9. Gondole de supermarche moderne, eclairage blanc froid de grande surface, sol carrelé blanc. "
            "Lineaire de 3 etages bien rempli de produits varies. Panneau de rayon en haut sur fond vert vif : "
            "'SANS GLUTEN — Votre sante, notre priorite'. Petite pancarte en dessous : 'Choisissez nos produits "
            "sans gluten pour une vie plus saine et legere !' Produits sur les etageres : emballages fictifs de "
            "pates sans gluten 'GlutenFree Pro' (jaune et vert), pain de mie sans gluten, biscuits 'NaturFree', "
            "barres cerealieres, farine de riz, crackers. Chaque emballage porte de gros badges visibles : "
            "'SANS GLUTEN', '100% NATUREL', 'HEALTHY', 'BON POUR VOUS'. Les emballages sont colores, positifs "
            "et rassurants. Un ecriteau orange sur l'etagere du milieu : 'NOS BEST-SELLERS SANTE'. Etiquettes "
            "de prix visibles : les produits sont nettement plus chers (4,99 EUR, 5,49 EUR, 6,20 EUR). Un ou "
            "deux clients dans l'allee en fond flou."
        ),
        "en": (
            "Realistic photo of a fictional supermarket aisle dedicated to 'Gluten-Free' products, landscape "
            "16:9 format. Modern supermarket gondola, cold white supermarket lighting, white tiled floor. "
            "A 3-shelf unit well stocked with varied products. Aisle sign at the top on vivid green background: "
            "'GLUTEN FREE — Your health, our priority'. Small placard below: 'Choose our gluten-free products "
            "for a healthier, lighter life!' Products on the shelves: fictional gluten-free pasta packaging "
            "'GlutenFree Pro' (yellow and green), gluten-free sandwich bread, 'NaturFree' cookies, cereal bars, "
            "rice flour, crackers. Each packaging carries large visible badges: 'GLUTEN FREE', '100% NATURAL', "
            "'HEALTHY', 'GOOD FOR YOU'. Colorful, positive and reassuring packaging. Orange sign on middle "
            "shelf: 'OUR HEALTH BEST-SELLERS'. Price tags visible: gluten-free products are significantly more "
            "expensive (EUR 4.99, EUR 5.49, EUR 6.20). One or two customers in the blurred aisle background."
        ),
    },

    # ══════════════════════════════════════════
    # BLOGS & BIEN-ÊTRE (manquants)
    # ══════════════════════════════════════════

    "blog_survivaliste_mousse": {
        "size": "1792x1024",
        "fr": (
            "Capture d'ecran realiste d'un blog survivaliste francais amateur, format paysage 16:9. Palette "
            "sombre : fond gris anthracite, accents kaki et marron foret. En-tete epais avec texture camouflage "
            "militaire (kaki, vert olive et marron). A gauche de l'en-tete : logo d'une hache plantee dans un "
            "tronc d'arbre, dessin simple en blanc. A droite du logo, en police Impact blanche majuscule : "
            "'TECHNIQUES DE SURVIE'. En dessous en gris : 'Preparons-nous. La nature n attend pas.' Barre de "
            "navigation noire avec onglets : 'Orientation | Feu & Eau | Nourriture | Abri | Kit de survie'. "
            "Page en deux colonnes. Colonne principale : grande photo d'un tronc d'arbre rugueux recouvert "
            "d'une epaisse mousse verte vif, lumiere sous-bois froide et filtree. Titre d'article en tres grande "
            "police condensee grasse blanche : 'S orienter avec la mousse : la regle infaillible de nos ancetres'. "
            "Premier paragraphe lisible : 'Depuis des siecles, nos ancetres utilisaient la mousse pour s orienter "
            "en foret. La regle est simple et absolue : la mousse pousse TOUJOURS du cote nord des arbres, la "
            "ou le soleil ne brille jamais. Apprenez-la par coeur.' Colonne de droite : encadre rouge "
            "'ARTICLES POPULAIRES' avec 3 entrees et encart publicitaire kaki 'SurvivalKit Pro — COMMANDER "
            "MAINTENANT'."
        ),
        "en": (
            "Realistic screenshot of an amateur French survivalist blog, landscape 16:9 format. Dark palette: "
            "charcoal background, khaki and forest brown accents. Thick header with military camouflage texture "
            "(khaki, olive green and brown patches). Left of header: logo of an axe planted in a tree trunk, "
            "simple white drawing. Right of logo, in white all-caps Impact font: 'SURVIVAL TECHNIQUES'. Below "
            "in smaller grey font: 'Be prepared. Nature doesn t wait.' Black navigation bar with white tabs: "
            "'Navigation | Fire & Water | Food | Shelter | Survival Kit'. Page in two columns. Left main "
            "column: large photo of a rough tree trunk covered in thick bright green moss, cold filtered forest "
            "light. Article title in very large bold condensed off-white font: 'Orienting with moss: the "
            "infallible rule of our ancestors'. First readable paragraph: 'For centuries, our ancestors used "
            "moss to navigate the forest. The rule is simple and absolute: moss ALWAYS grows on the north side "
            "of trees, where the sun never shines. Learn it by heart.' Right column: red box 'POPULAR ARTICLES' "
            "with 3 entries and khaki ad rectangle 'SurvivalKit Pro — ORDER NOW'."
        ),
    },

    # ══════════════════════════════════════════
    # QUESTION CACTUS (sources fiable ET non fiable)
    # ══════════════════════════════════════════

    "etude_desert_cactus": {
        "size": "1792x1024",
        "fr": (
            "Capture d'ecran realiste d'un article scientifique en ligne, format paysage 16:9. Interface de "
            "portail de revue academique sobre, fond blanc casse. En haut : barre de navigation avec logo fictif "
            "'JOURNAL OF ARID ENVIRONMENTS' en lettres noires serif a gauche, onglets bleu marine 'Home | Browse "
            "| Submit | About'. Corps de la page : titre de l'article en grand, police Georgia noire : 'Alkaloid "
            "Content and Water Availability in Sonoran Desert Cacti: Implications for Survival Use'. Auteurs en "
            "lien bleu : 'Gary P. Nabhan, Richard S. Felger, Wendy C. Hodgson'. Affiliation en gris italique : "
            "'Desert Botanical Laboratory, University of Arizona, Tucson'. Encadre gris clair 'ABSTRACT' en "
            "majuscules grasses : 'Sonoran cacti contain high concentrations of alkaloids and a thick mucilaginous "
            "gel that triggers severe gastrointestinal distress when ingested. Our field experiments demonstrate "
            "that cactus consumption increases dehydration rates in 100% of test subjects within 4 hours. Contrary "
            "to popular belief, no common cactus species provides safe hydration.' Meta-donnees a droite : "
            "'Volume 4 | Issue 2 | October 1982 | Pages 45-62 | DOI: 10.1016/jarid.1982.0012'. Bouton rouge "
            "'Download PDF'. Style interface Elsevier ou Nature, palette bleu marine et rouge brique."
        ),
        "en": (
            "Realistic screenshot of an online academic journal article, landscape 16:9 format. Clean academic "
            "portal interface, off-white background. Top: white navigation bar with fictional logo 'JOURNAL OF "
            "ARID ENVIRONMENTS' in serif black letters on the left, navy blue tabs 'Home | Browse | Submit | "
            "About'. Page body: article title in large Georgia font, black: 'Alkaloid Content and Water "
            "Availability in Sonoran Desert Cacti: Implications for Survival Use'. Authors as blue links: "
            "'Gary P. Nabhan, Richard S. Felger, Wendy C. Hodgson'. Grey italic affiliation: 'Desert Botanical "
            "Laboratory, University of Arizona, Tucson'. Light grey box labeled 'ABSTRACT' in bold capitals: "
            "'Sonoran cacti contain high concentrations of alkaloids and a thick mucilaginous gel that triggers "
            "severe gastrointestinal distress when ingested. Our field experiments demonstrate that cactus "
            "consumption increases dehydration rates in 100% of test subjects within 4 hours. Contrary to "
            "popular belief, no common cactus species provides safe hydration.' Right column metadata: "
            "'Volume 4 | Issue 2 | October 1982 | Pages 45-62 | DOI: 10.1016/jarid.1982.0012'. Red 'Download "
            "PDF' button. Elsevier or Nature portal interface style, navy blue and brick red palette."
        ),
    },

    "guide_wms_survie": {
        "size": "1024x1792",
        "fr": (
            "Couverture d'un guide medical officiel de survie en milieu sauvage, format portrait. Style couverture "
            "institutionnelle serieuse. Fond vert foret profond. En haut : logo fictif compose d'un caducee "
            "medical stylise encercle de branches vertes, texte blanc condensed gras en dessous : 'WILDERNESS "
            "MEDICAL SOCIETY'. Separation horizontale or. Grand titre central en lettres blanches condensees "
            "tres grasses : 'WILDERNESS MEDICINE GUIDELINES'. Sous-titre en jaune vif : 'Water, Hydration & "
            "Field Emergencies'. Image centrale : illustration vectorielle medicale sobre sur fond vert fonce — "
            "une bouteille d'eau propre avec coche verte a gauche, un cactus tonneau barre d'une croix rouge "
            "epaisse a droite, une fleche de comparaison entre les deux. Encadre blanc en bas de page : "
            "'6e Edition — Recommandations officielles — Approuve par le Board of Directors WMS 2022'. "
            "Style publication medicale professionnelle, sobre et autoritaire."
        ),
        "en": (
            "Cover of an official wilderness medical survival guide, portrait format. Serious, institutional "
            "cover style. Deep forest green background. Top: fictional logo composed of a stylized medical "
            "caduceus circled by green branches, bold condensed white text below: 'WILDERNESS MEDICAL SOCIETY'. "
            "Gold horizontal separator. Large central title in very bold condensed white letters: 'WILDERNESS "
            "MEDICINE GUIDELINES'. Subtitle in bright yellow: 'Water, Hydration & Field Emergencies'. Central "
            "image: clean medical vector illustration on dark green background — a clean water bottle with a "
            "green check mark on the left, a barrel cactus crossed out with a thick red X on the right, a "
            "comparison arrow between the two. White box at the bottom: '6th Edition — Official Recommendations "
            "— Approved by the WMS Board of Directors 2022'. Professional, austere, authoritative medical "
            "publication style."
        ),
    },

    "livre_survie_cactus": {
        "size": "1024x1792",
        "fr": (
            "Couverture de livre de survie grand public best-seller, format portrait. Photographie de couverture : "
            "homme muscle en veste tactique kaki dechirée, agenouillé dans un desert ocre sous un soleil rasant, "
            "regard determine fixe face camera, machoire carree, sueur visible. Ciel orange-rouge dramatique au "
            "coucher du soleil derriere lui. En haut de la couverture, bandeau rouge vif : 'N 1 DES VENTES | "
            "2 MILLIONS D EXEMPLAIRES VENDUS'. Nom d'auteur fictif en blanc : 'MAX LEBLANC'. Grand titre en "
            "tres grosses lettres ultra-condensees jaune vif avec fine bordure noire, deux lignes : 'SURVIVRE' "
            "sur la premiere ligne, 'PARTOUT' sur la deuxieme, encore plus grand. Sous-titre en orange vif : "
            "'LE GUIDE ULTIME'. Bande beige en bas : 'Desert, montagne, foret, mer — toutes les techniques pour "
            "rester en vie'. Logo editeur fictif 'TERRA SURVIVALIST EDITIONS' en bas a gauche. Style survival "
            "moderne agressif."
        ),
        "en": (
            "Bestselling popular survival book cover, portrait format. Cover photograph: muscular man in torn "
            "khaki tactical jacket, kneeling in an ochre desert under a harsh glaring sun, determined gaze "
            "fixed directly at the camera, square jaw, visible sweat. Dramatic orange-red sunset sky behind "
            "him. Top of cover, bright red band: 'NUMBER 1 BESTSELLER | 2 MILLION COPIES SOLD'. Fictional "
            "author name in white: 'MAX LEBLANC'. Large title in huge ultra-condensed bright yellow letters "
            "with thin black border, two lines: 'SURVIVE' on the first line, 'ANYWHERE' on the second line, "
            "even larger. Subtitle in bright orange: 'THE ULTIMATE GUIDE'. Beige band at the bottom: 'Desert, "
            "mountain, forest, sea — every technique to stay alive'. Fictional publisher logo 'TERRA SURVIVALIST "
            "EDITIONS' at the bottom left. Aggressive modern survival style."
        ),
    },

    # ══════════════════════════════════════════
    # QUESTION CLIM (source non fiable)
    # ══════════════════════════════════════════

    "magazine_clim_pollution": {
        "size": "1792x1024",
        "fr": (
            "Capture d'ecran realiste d'un article en ligne d'un grand magazine de vulgarisation scientifique "
            "francais, format paysage 16:9. Interface sobre et credible : fond blanc casse, police serife noire, "
            "style 'Sciences & Avenir' ou 'Le Monde'. En haut : bandeau rouge avec le nom fictif du magazine "
            "'PLANETE SCIENCES' et sous-titre gris : 'Environnement · Energie · Societe'. Titre de l'article "
            "en tres grande police noire grasse sur deux lignes : 'Climatisation : la bombe climatique' puis "
            "'que personne ne veut voir'. Sous-titre en italique gris : 'Les climatiseurs consomment autant "
            "d electricite que toute l Afrique et menacent directement nos objectifs climatiques.' Date et "
            "auteur : 'Par Marie Durand | 23 juin 2023 | 8 min de lecture'. Grande image d'illustration : "
            "vue aerienne dramatique d'une ville europeenne dense en plein ete, ciel bleu metallique brumeux "
            "de chaleur. En surimpression sur la photo : une grande icone de climatiseur stylisee en rouge "
            "avec des flammes qui en sortent. Encadre chiffre-cle dans l'article : fond rouge vif, texte blanc "
            "gras 'x10 : la clim pollue 10 fois plus que le chauffage a usage egal' — chiffre sans source. "
            "Debut de l'article lisible : 'Partout en Europe, les climatiseurs tournent a plein regime. Mais "
            "ce confort a un cout : a proportion egale d utilisation, la climatisation rejette bien plus de "
            "CO2 que n importe quel systeme de chauffage.'"
        ),
        "en": (
            "Realistic screenshot of an online article from a major French popular science magazine, landscape "
            "16:9 format. Clean, credible interface: off-white background, black serif font, 'Sciences & Avenir' "
            "or 'Le Monde' style. Top: red banner with the fictional magazine name 'PLANET SCIENCES' and grey "
            "subtitle: 'Environment · Energy · Society'. Article title in very large bold black font on two "
            "lines: 'Air conditioning: the climate bomb' then 'nobody wants to talk about'. Italic grey subtitle: "
            "'Air conditioners consume as much electricity as all of Africa and directly threaten our climate "
            "goals.' Date and author: 'By Marie Durand | June 23, 2023 | 8 min read'. Large illustration: "
            "dramatic aerial view of a dense European city in full summer heat, blue metallic hazy sky. "
            "Superimposed on the photo: a large stylized red air conditioner icon with flames coming out of "
            "it toward the sky. Key figure box in the article: vivid red background, bold white text 'x10: "
            "AC pollutes 10 times more than heating per equivalent use' — figure with no source cited. Start "
            "of article: 'All across Europe, air conditioners are running at full capacity. But this comfort "
            "comes at a cost: per unit of use, air conditioning releases far more CO2 than any heating system.'"
        ),
    },
}


# ─────────────────────────────────────────────
# Utilitaires
# ─────────────────────────────────────────────

def load_api_key() -> str:
    """Charge la clé API depuis l'environnement ou un fichier .env"""
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        env_file = Path(__file__).parent / ".env"
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                if line.startswith("OPENAI_API_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    return key


def get_output_path(name: str, lang: str) -> Path:
    """Retourne le chemin de sortie pour une image"""
    suffix = "" if lang == "fr" else "_en"
    return IMAGES_DIR / f"{name}{suffix}.png"


def image_exists(name: str, lang: str) -> bool:
    """Vérifie si l'image existe (PNG ou JPEG)"""
    suffix = "" if lang == "fr" else "_en"
    base = IMAGES_DIR / f"{name}{suffix}"
    return base.with_suffix(".png").exists() or base.with_suffix(".jpg").exists()


def list_missing() -> list[tuple[str, str]]:
    """Retourne la liste des (nom, lang) manquants"""
    missing = []
    for name in IMAGES:
        for lang in ("fr", "en"):
            if not image_exists(name, lang):
                missing.append((name, lang))
    return missing


def estimate_cost(items: list[tuple[str, str]]) -> float:
    """Estime le coût total en USD"""
    total = 0.0
    for name, _lang in items:
        size = IMAGES[name]["size"]
        total += COST[size]
    return total


def generate_image(client, name: str, lang: str, dry_run: bool = False) -> bool:
    """Génère une image via gpt-image-2 et la sauvegarde. Retourne True si succès."""
    prompt = IMAGES[name][lang]
    size_key = IMAGES[name]["size"]
    actual_size = SIZE_MAP[size_key]  # convertit vers les tailles de gpt-image-2
    output_path = get_output_path(name, lang)
    lang_label = "FR" if lang == "fr" else "EN"

    print(f"\n  [{lang_label}] {name}.png — {actual_size}")
    print(f"  Prompt : {prompt[:80]}...")

    if dry_run:
        print(f"  ➡  [DRY RUN] Serait sauvegardé dans : {output_path}")
        return True

    try:
        response = client.images.generate(
            model=MODEL,
            prompt=prompt,
            size=actual_size,
            n=1,
        )

        # gpt-image-2 retourne base64, pas une URL
        img_data = response.data[0].b64_json
        img_bytes = base64.b64decode(img_data)

        output_path.write_bytes(img_bytes)
        print(f"  ✅ Sauvegardé : {output_path.name} ({len(img_bytes) // 1024} Ko)")
        return True

    except Exception as e:
        error_msg = str(e)
        if "content_policy" in error_msg.lower() or "safety" in error_msg.lower():
            print(f"  ⚠️  Refusé par le filtre de contenu : {error_msg[:120]}")
        else:
            print(f"  ❌ Erreur : {error_msg[:200]}")
        return False


# ─────────────────────────────────────────────
# Point d'entrée
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Génère les images manquantes de FakeMètre via DALL-E 3"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Liste ce qui serait généré sans appel API"
    )
    parser.add_argument(
        "--filter", metavar="NOM",
        help="Génère seulement les images dont le nom contient NOM"
    )
    parser.add_argument(
        "--list", action="store_true",
        help="Liste toutes les images définies dans le script"
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Régénère même les images déjà existantes"
    )
    parser.add_argument(
        "--yes", "-y", action="store_true",
        help="Lance sans demander de confirmation"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  FakeMètre — Générateur d'images DALL-E 3")
    print("=" * 60)
    print(f"  Dossier images : {IMAGES_DIR}")
    print(f"  Images définies : {len(IMAGES)} × 2 langues = {len(IMAGES) * 2} images")

    # ── Mode --list
    if args.list:
        print("\n  Images définies :")
        for name, cfg in IMAGES.items():
            for lang in ("fr", "en"):
                exists = "✅" if image_exists(name, lang) else "❌"
                suffix = "" if lang == "fr" else "_en"
                print(f"    {exists} {name}{suffix}.png  ({cfg['size']})")
        return

    # ── Déterminer quelles images générer
    if args.force:
        items_to_generate = [(n, l) for n in IMAGES for l in ("fr", "en")]
    else:
        items_to_generate = list_missing()

    # Appliquer le filtre --filter
    if args.filter:
        items_to_generate = [(n, l) for n, l in items_to_generate if args.filter.lower() in n.lower()]
        print(f"\n  Filtre : '{args.filter}' → {len(items_to_generate)} images concernées")

    if not items_to_generate:
        print("\n  ✅ Toutes les images sont déjà présentes. Rien à générer.")
        return

    # ── Afficher le récapitulatif
    cost = estimate_cost(items_to_generate)
    print(f"\n  📋 Images à générer : {len(items_to_generate)}")
    for name, lang in items_to_generate:
        suffix = "" if lang == "fr" else "_en"
        size = IMAGES[name]["size"]
        print(f"     • {name}{suffix}.png  ({size})")
    print(f"\n  💰 Coût estimé DALL-E 3 standard : ~${cost:.2f} USD")
    print(f"  🤖 Modèle : {MODEL} (dall-e-3 est déprécié depuis 2025)")
    print(f"  ⏱  Durée estimée : ~{len(items_to_generate) * RATE_LIMIT_DELAY // 60} min")

    if args.dry_run:
        print("\n  [MODE DRY RUN — aucun appel API effectué]")
        return

    # ── Charger la clé API
    api_key = load_api_key()
    if not api_key:
        print("\n  ❌ OPENAI_API_KEY non trouvée !")
        print("     Option 1 : définir la variable d'environnement :")
        print("       $env:OPENAI_API_KEY = 'sk-...'")
        print("     Option 2 : créer un fichier .env dans le dossier du projet :")
        print("       OPENAI_API_KEY=sk-...")
        sys.exit(1)

    print(f"\n  🔑 Clé API : {api_key[:8]}...")

    # ── Confirmation (sautée avec --yes ou stdin non-TTY)
    if not args.yes and sys.stdin.isatty():
        print(f"\n  ⚠️  Appuyez sur ENTRÉE pour lancer la génération (ou Ctrl+C pour annuler)...")
        try:
            input()
        except KeyboardInterrupt:
            print("\n  Annulé.")
            return
    else:
        print(f"\n  🚀 Lancement automatique (--yes)...")

    # ── Génération
    from openai import OpenAI  # noqa
    client = OpenAI(api_key=api_key)

    success_count = 0
    fail_count = 0

    for i, (name, lang) in enumerate(items_to_generate, 1):
        print(f"\n{'─' * 60}")
        print(f"  [{i}/{len(items_to_generate)}] Génération en cours...")

        ok = generate_image(client, name, lang)
        if ok:
            success_count += 1
        else:
            fail_count += 1

        # Rate limiting (sauf pour la dernière image)
        if i < len(items_to_generate):
            print(f"  ⏳ Attente {RATE_LIMIT_DELAY}s (rate limit DALL-E 3)...")
            time.sleep(RATE_LIMIT_DELAY)

    # ── Bilan
    print(f"\n{'=' * 60}")
    print(f"  ✅ Succès : {success_count}/{len(items_to_generate)}")
    if fail_count > 0:
        print(f"  ❌ Échecs : {fail_count}/{len(items_to_generate)}")
    print(f"\n  N'oubliez pas de vérifier les images et de mettre à jour")
    print(f"  les fichiers JS (questions_fr.js / questions_en.js) avec")
    print(f"  img:\"images/NOM.png\" puis de lancer deploy.bat")
    print("=" * 60)


if __name__ == "__main__":
    main()
