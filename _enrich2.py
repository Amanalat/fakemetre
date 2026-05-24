"""
Enrichissement des sources non-augmentées dans questions_fr.js et questions_en.js.
Ajoute les champs: mediaType/Title/Year/Director/Platform, bookType/Title/Author/Year,
quoteType/Origin, adType/Brand/Slogan, expertTitle/Institution,
forumUser/Name, redditSub/User/Upvotes, linkedinUser/Title/Likes
"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

# ─────────────────────────────────────────────────────────────────
# Dictionnaire d'enrichissement: clé = (n_contains, d_contains) ou juste n_contains
# valeur = dict de champs à ajouter
# ─────────────────────────────────────────────────────────────────

FR_ENRICHMENTS = [
    # ── MEDIA ──────────────────────────────────────────────────────
    (("Scène de film d'aventure hollywoodien", None),
     {'mediaType':'film','mediaTitle':"Film de survie hollywoodien"}),

    (("Film biographique hollywoodien", "Edison"),
     {'mediaType':'film','mediaTitle':'Edison — Le génie','mediaYear':'2017'}),

    (("Film historique hollywoodien sur Christophe Colomb", None),
     {'mediaType':'film','mediaTitle':'Colomb — La Découverte','mediaYear':'1992'}),

    (("Film 'Les Dents de la Mer' — Making-of officiel", None),
     {'mediaType':'making-of','mediaTitle':'Les Dents de la Mer','mediaYear':'1975','mediaDirector':'S. Spielberg'}),

    (("Documentaire Netflix sur la pollution plastique", None),
     {'mediaType':'docu','mediaTitle':'Plastique — La grande vague','mediaPlatform':'Netflix'}),

    (("Documentaire 'Vaxxed' (2016)", None),
     {'mediaType':'docu','mediaTitle':'Vaxxed','mediaYear':'2016','mediaDirector':'A. Wakefield'}),

    (("Documentaire Netflix 'Ce que le sucre vous fait'", None),
     {'mediaType':'docu','mediaTitle':'Ce que le sucre vous fait','mediaPlatform':'Netflix'}),

    (("Émission de vulgarisation TV des années 1980", None),
     {'mediaType':'tv','mediaTitle':'Le Monde des Animaux','mediaYear':'1983'}),

    (("Opéra de Wagner (XIXe siècle)", None),
     {'mediaType':'opera','mediaTitle':'Lohengrin','mediaDirector':'R. Wagner','mediaYear':'1850'}),

    (("Jeu vidéo de combat médiéval", None),
     {'mediaType':'game','mediaTitle':'Age of Vikings II'}),

    (("TED Talk de Jill Bolte Taylor", None),
     {'mediaType':'ted','mediaTitle':"Mon coup de foudre cérébral",'mediaDirector':'Jill Bolte Taylor','mediaYear':'2008'}),

    (("Chaîne YouTube d'un influenceur gaming", None),
     {'mediaType':'youtube','mediaTitle':"Les jeux vidéo c'est que du bon !",'mediaPlatform':'YouTube'}),

    (("Caricatures de James Gillray (1803)", None),
     {'mediaType':'art','mediaTitle':'Bonaparte — Caricatures satiriques','mediaDirector':'James Gillray','mediaYear':'1803'}),

    # ── LIVRES / MANUELS ───────────────────────────────────────────
    (("Manuel scolaire de géographie", None),
     {'bookType':'manuel','bookTitle':'Géographie — Cycle 3'}),

    (("Encyclopédie Larousse en ligne", None),
     {'bookType':'encyclopédie','bookTitle':'Larousse.fr — Encyclopédie en ligne'}),

    (("Encyclopédie Larousse pour enfants", None),
     {'bookType':'encyclopédie','bookTitle':'Larousse Junior','bookYear':'1993'}),

    (("Manuel scolaire des années 1950", None),
     {'bookType':'manuel','bookTitle':'Sciences Naturelles','bookYear':'1952'}),

    (("Manuel scouting vintage réédité", None),
     {'bookType':'guide','bookTitle':'Le Guide du Scout'}),

    (("Manuel de psychologie des années 1970", None),
     {'bookType':'manuel','bookTitle':'Psychologie Pratique','bookYear':'1973'}),

    (("Encyclopédie Britannica", None),
     {'bookType':'encyclopédie','bookTitle':'Encyclopaedia Britannica'}),

    (("Livre illustré pour enfants", None),
     {'bookType':'livre','bookTitle':'La Nature en images'}),

    (("Livre de développement personnel", "confiance"),
     {'bookType':'livre','bookTitle':'Libérez votre potentiel'}),

    (("Livre 'Les 1000 choses à savoir absolument'", None),
     {'bookType':'livre','bookTitle':'Les 1000 choses à savoir absolument'}),

    (("Roman macabre — best-seller populaire", None),
     {'bookType':'roman','bookTitle':'Les Ombres du Caveau'}),

    (("Best-seller 'Wheat Belly'", None),
     {'bookType':'livre','bookTitle':'Wheat Belly','bookAuthor':'Dr William Davis'}),

    (("Biographie populaire de Napoléon (best-seller)", None),
     {'bookType':'livre','bookTitle':'Napoléon Bonaparte — La légende'}),

    (("'La fabrique du crétin digital'", None),
     {'bookType':'livre','bookTitle':'La fabrique du crétin digital','bookAuthor':'Michel Desmurget','bookYear':'2019'}),

    (("Dictionnaire des proverbes et expressions", None),
     {'bookType':'livre','bookTitle':'Dictionnaire des proverbes et expressions françaises'}),

    (("Archives du lycée d'Einstein à Aarau", None),
     {'bookType':'guide','bookTitle':"Bulletins scolaires d'Albert Einstein",'bookYear':'1895'}),

    # ── PROVERBES / CROYANCES ─────────────────────────────────────
    (("Proverbe populaire", None),
     {'quoteType':'proverbe'}),

    (("Dicton de grand-père", None),
     {'quoteType':'dicton','quoteOrigin':'Tradition familiale'}),

    (("Dicton populaire de montagne", None),
     {'quoteType':'dicton','quoteOrigin':'Tradition montagnarde'}),

    (("Expression populaire", None),
     {'quoteType':'expression'}),

    (("Croyance populaire répandue", None),
     {'quoteType':'croyance'}),

    (("Croyance populaire", None),
     {'quoteType':'croyance'}),

    (("Le bon sens", None),
     {'quoteType':'intuition'}),

    (("Mon intuition", None),
     {'quoteType':'intuition'}),

    (("Mon coiffeur", None),
     {'quoteType':'croyance','quoteOrigin':'Conversation chez le coiffeur'}),

    (("Les copains", "cour"),
     {'quoteType':'croyance','quoteOrigin':'Cour de récréation'}),

    (("Idée reçue très répandue", None),
     {'quoteType':'croyance'}),

    (("Blague populaire sur Internet", None),
     {'quoteType':'expression','quoteOrigin':'Humour viral'}),

    (("Citation attribuée à Voltaire", None),
     {'quoteType':'expression','quoteOrigin':'Attribuée à Voltaire (non vérifiée)'}),

    # ── PUBLICITÉS ─────────────────────────────────────────────────
    (("Emballage d'un paquet de carottes bio", None),
     {'adType':'packaging','adBrand':'Bio Jardin','adSlogan':'Naturellement bon pour vos yeux !'}),

    (("Publicité pour une marque d'eau en bouteille", None),
     {'adType':'tv','adBrand':'AquaVita','adSlogan':"L'eau pure pour une vie pure"}),

    (("Site d'une grande enseigne bio", None),
     {'adType':'store','adBrand':'Bio & Nature','adSlogan':'100% naturel, 100% vrai'}),

    (("Rayon 'Sans gluten' d'un supermarché", None),
     {'adType':'packaging','adBrand':'GlutenFree Pro','adSlogan':'Votre santé mérite le meilleur'}),

    (("Étiquette d'un produit alimentaire bio en supermarché", None),
     {'adType':'packaging','adBrand':'TerreBio','adSlogan':'Sans gluten · Bio · 100% naturel'}),

    (("Cabinet de recrutement RH — plaquette commerciale", None),
     {'adType':'print','adBrand':'HR Stratégie Conseil'}),

    # ── EXPERTS ───────────────────────────────────────────────────
    (("Témoignage de l'astronaute Yang Liwei", None),
     {'expertTitle':'Premier spationaute chinois','expertInstitution':'Programme spatial national (2003)'}),

    (("Ophtalmologiste (médecin des yeux)", None),
     {'expertTitle':'Ophtalmologiste','expertInstitution':"Cabinet d'ophtalmologie"}),

    (("Entomologiste du Muséum d'Histoire Naturelle", None),
     {'expertTitle':'Entomologiste, chercheur','expertInstitution':'Muséum National d\'Histoire Naturelle'}),

    (("Chimiste alimentaire de l'INRAE", None),
     {'expertTitle':'Chimiste alimentaire','expertInstitution':'INRAE — Institut National de Recherche pour l\'Agriculture'}),

    (("Archéologues de fouilles en Égypte", None),
     {'expertTitle':'Archéologues','expertInstitution':'Mission archéologique franco-égyptienne'}),

    (("Neurologue de l'hôpital universitaire", None),
     {'expertTitle':'Neurologue, spécialiste du cerveau','expertInstitution':'Hôpital universitaire'}),

    (("Coach en développement personnel", "Conférence en ligne"),
     {'expertTitle':'Coach en développement personnel (non certifié)','expertInstitution':'Conférence en ligne'}),

    (("Météorologiste de Météo-France", None),
     {'expertTitle':'Météorologiste','expertInstitution':'Météo-France'}),

    (("Ingénieur de la Tour Eiffel", None),
     {'expertTitle':'Ingénieur responsable technique','expertInstitution':'Tour Eiffel — SETE'}),

    (("Médecin généraliste", "Praticien de santé"),
     {'expertTitle':'Médecin généraliste','expertInstitution':'Cabinet médical'}),

    (("Médecin généraliste", "Docteur en médecine"),
     {'expertTitle':'Médecin généraliste','expertInstitution':'Cabinet médical'}),

    (("École Nationale Vétérinaire d'Alfort", None),
     {'expertTitle':'Experts vétérinaires','expertInstitution':"École Nationale Vétérinaire d'Alfort (ENVA)"}),

    (("Gastro-entérologue, CHU de Lyon", None),
     {'expertTitle':'Gastro-entérologue','expertInstitution':'CHU de Lyon'}),

    (("Historien spécialiste des Vikings", None),
     {'expertTitle':'Historien médiéviste, spécialiste des Vikings','expertInstitution':'Université de recherche'}),

    (("Sage-femme à la retraite", None),
     {'expertTitle':'Sage-femme (retraitée)','expertInstitution':'30 ans d\'expérience clinique'}),

    (("Nutritionniste influenceur", None),
     {'expertTitle':'Nutritionniste (influenceur)','expertInstitution':'Sans affiliation académique'}),

    (("Prof de chimie au lycée", None),
     {'expertTitle':'Professeur de chimie','expertInstitution':'Lycée (hors de sa spécialité)'}),

    (("Vétérinaire — Clinique vétérinaire", None),
     {'expertTitle':'Vétérinaire','expertInstitution':'Clinique vétérinaire'}),

    (("Médecin urgentiste", "urgences humaines"),
     {'expertTitle':'Médecin urgentiste','expertInstitution':'Service des urgences'}),

    (("Médecin urgentiste publiant dans un journal local", None),
     {'expertTitle':'Médecin urgentiste','expertInstitution':'Hôpital régional — journal local'}),

    (("Médecin hématologue", None),
     {'expertTitle':'Hématologue, spécialiste du sang','expertInstitution':'CHU'}),

    (("Pédiatre — Hôpital Necker", None),
     {'expertTitle':'Pédiatre','expertInstitution':'Hôpital Necker, Paris'}),

    (("Professeur de mathématiques", None),
     {'expertTitle':'Professeur de mathématiques','expertInstitution':'Lycée (hors de sa spécialité)'}),

    (("Chef cuisinier spécialisé en fruits de mer", None),
     {'expertTitle':'Chef cuisinier, spécialiste fruits de mer','expertInstitution':'Restaurant gastronomique'}),

    (("Médecin homéopathe, Faculté de médecine de Paris", None),
     {'expertTitle':'Médecin homéopathe','expertInstitution':'Faculté de médecine de Paris'}),

    (("Directeur IA d'une grande entreprise tech", None),
     {'expertTitle':'Directeur IA','expertInstitution':'Grande entreprise technologique'}),

    (("Futurologue indépendant", None),
     {'expertTitle':'Futurologue indépendant','expertInstitution':'Conférence TED'}),

    (("Policier retraité interviewé dans un documentaire", None),
     {'expertTitle':'Policier retraité','expertInstitution':'30 ans de patrouilles de nuit'}),

    (("William Happer, physicien émérite de Princeton", None),
     {'expertTitle':'Physicien émérite','expertInstitution':'Université de Princeton — CO2 Coalition'}),

    (("Andrew Wakefield, ex-gastro-entérologue", None),
     {'expertTitle':'Ex-gastro-entérologue (radié du registre médical)','expertInstitution':'Royal Free Hospital (ex)'}),

    (("Dr Nicole Avena, Columbia University", None),
     {'expertTitle':'Neuroscientifique, chercheuse','expertInstitution':'Université Columbia — New York'}),

    # ── FORUMS / REDDIT / LINKEDIN ─────────────────────────────────
    (("Forum de cuisine en ligne", None),
     {'forumUser':'gastronome42','forumName':'CuisinePassion.fr','forumDate':'il y a 2 ans','forumLikes':'34'}),

    (("Forum de pêche", None),
     {'forumUser':'CapitaineMerlu','forumName':'LaPêche.net','forumDate':'il y a 3 ans','forumLikes':'12'}),

    (("Forum 'Curiosités et mystères'", None),
     {'forumUser':'CurioMax77','forumName':'Curiosités & Mystères','forumDate':'il y a 1 an','forumLikes':'89'}),

    (("Forum de parents 'Mamanpourlavie.fr'", None),
     {'forumUser':'MamanInquiète91','forumName':'MamanPourLaVie.fr','forumDate':'il y a 8 mois','forumLikes':'27'}),

    (("Maman sur un forum de parents", None),
     {'forumUser':'Delphine_M','forumName':'ParentsConnectés.fr','forumDate':'il y a 1 an','forumLikes':'15'}),

    (("Thread Reddit 'Faits insolites'", None),
     {'redditSub':'r/FaitsInsolites','redditUser':'u/faits_cool_77','redditUpvotes':'3.4k','redditComments':'128',
      'redditTitle':'Savez-vous que les poissons ont UNE MÉMOIRE DE 3 SECONDES ?? 🐟'}),

    (("Post LinkedIn viral d'un coach en développement personnel", None),
     {'linkedinUser':'Jean-Pierre Martin','linkedinTitle':'Coach Développement Personnel | 50k abonnés',
      'linkedinLikes':'12 483','linkedinDate':'Il y a 5 jours'}),

    (("Discussion sur un forum écologie", None),
     {'forumUser':'EcoActif42','forumName':'PlanetVerte.org','forumDate':'il y a 4 mois','forumLikes':'61'}),

    (("Commentaire sous une vidéo d'aquariophilie", None),
     {'forumUser':'AquaMaster99','forumName':'YouTube · Commentaires','forumDate':'il y a 2 ans','forumLikes':'23'}),
]

EN_ENRICHMENTS = [
    # ── MEDIA ──────────────────────────────────────────────────────
    (("Hollywood adventure film scene", None),
     {'mediaType':'film','mediaTitle':'Hollywood Survival Movie'}),

    (("Hollywood biopic", "Edison"),
     {'mediaType':'film','mediaTitle':'Edison — The Genius','mediaYear':'2017'}),

    (("Hollywood historical film about Christopher Columbus", None),
     {'mediaType':'film','mediaTitle':'Columbus — The Discovery','mediaYear':'1992'}),

    (("Film 'Jaws' — official making-of", None),
     {'mediaType':'making-of','mediaTitle':'Jaws','mediaYear':'1975','mediaDirector':'S. Spielberg'}),

    (("Netflix documentary on plastic pollution", None),
     {'mediaType':'docu','mediaTitle':'Plastic — The Great Wave','mediaPlatform':'Netflix'}),

    (("Documentary 'Vaxxed' (2016)", None),
     {'mediaType':'docu','mediaTitle':'Vaxxed','mediaYear':'2016','mediaDirector':'A. Wakefield'}),

    (("Netflix documentary 'What Sugar Does to You'", None),
     {'mediaType':'docu','mediaTitle':'What Sugar Does to You','mediaPlatform':'Netflix'}),

    (("1980s science TV show", None),
     {'mediaType':'tv','mediaTitle':'The Animal Kingdom','mediaYear':'1983'}),

    (("Wagner opera (19th century)", None),
     {'mediaType':'opera','mediaTitle':'Lohengrin','mediaDirector':'R. Wagner','mediaYear':'1850'}),

    (("Medieval combat video game", None),
     {'mediaType':'game','mediaTitle':'Age of Vikings II'}),

    (("Jill Bolte Taylor TED Talk", None),
     {'mediaType':'ted','mediaTitle':'My Stroke of Insight','mediaDirector':'Jill Bolte Taylor','mediaYear':'2008'}),

    (("YouTube channel", "gaming"),
     {'mediaType':'youtube','mediaTitle':'Gaming is Only Good! — 2.3M views','mediaPlatform':'YouTube'}),

    (("James Gillray caricatures (1803)", None),
     {'mediaType':'art','mediaTitle':'Bonaparte — Satirical Caricatures','mediaDirector':'James Gillray','mediaYear':'1803'}),

    # ── BOOKS ──────────────────────────────────────────────────────
    (("Geography textbook", None),
     {'bookType':'textbook','bookTitle':'Geography — Secondary Level'}),

    (("Larousse online encyclopedia", None),
     {'bookType':'encyclopedia','bookTitle':'Larousse.fr — Online Encyclopaedia'}),

    (("Larousse Encyclopedia for Children", None),
     {'bookType':'encyclopedia','bookTitle':'Larousse Junior','bookYear':'1993'}),

    (("1950s school textbook", None),
     {'bookType':'textbook','bookTitle':'Natural Sciences','bookYear':'1952'}),

    (("Reissued vintage scouting manual", None),
     {'bookType':'guide','bookTitle':'The Scout Guide'}),

    (("1970s psychology textbook", None),
     {'bookType':'textbook','bookTitle':'Practical Psychology','bookYear':'1973'}),

    (("Encyclopaedia Britannica", None),
     {'bookType':'encyclopedia','bookTitle':'Encyclopaedia Britannica'}),

    (("Illustrated children's book", None),
     {'bookType':'book','bookTitle':'Nature in Pictures'}),

    (("Personal development book", "self-confidence"),
     {'bookType':'book','bookTitle':'Unlock Your Potential'}),

    (("Book 'The 1000 Things You Absolutely Need to Know'", None),
     {'bookType':'book','bookTitle':'The 1000 Things You Absolutely Need to Know'}),

    (("Macabre novel — popular bestseller", None),
     {'bookType':'novel','bookTitle':'Shadows of the Vault'}),

    (("Best-seller 'Wheat Belly'", None),
     {'bookType':'book','bookTitle':'Wheat Belly','bookAuthor':'Dr William Davis'}),

    (("Popular biography of Napoleon (bestseller)", None),
     {'bookType':'book','bookTitle':'Napoleon Bonaparte — The Legend'}),

    (("'The Digital Idiot Factory'", None),
     {'bookType':'book','bookTitle':'The Digital Idiot Factory','bookAuthor':'Michel Desmurget','bookYear':'2019'}),

    (("Dictionary of proverbs and expressions", None),
     {'bookType':'book','bookTitle':'Dictionary of Popular French Proverbs and Expressions'}),

    (("Archives of Einstein's high school in Aarau", None),
     {'bookType':'guide','bookTitle':"Albert Einstein's School Report Cards",'bookYear':'1895'}),

    # ── QUOTES ─────────────────────────────────────────────────────
    (("Popular proverb", None),
     {'quoteType':'proverbe'}),

    (("Grandfather's saying", None),
     {'quoteType':'dicton','quoteOrigin':'Family oral tradition'}),

    (("Dicton populaire de montagne", None),
     {'quoteType':'dicton','quoteOrigin':'Mountain hiking tradition'}),

    (("Popular expression", None),
     {'quoteType':'expression'}),

    (("Widespread popular belief", None),
     {'quoteType':'croyance'}),

    (("Popular belief", None),
     {'quoteType':'croyance'}),

    (("Common sense", None),
     {'quoteType':'intuition'}),

    (("Very widespread misconception", None),
     {'quoteType':'croyance'}),

    (("Popular internet joke", None),
     {'quoteType':'expression','quoteOrigin':'Viral humour'}),

    (("Quote attributed to Voltaire", None),
     {'quoteType':'expression','quoteOrigin':'Attributed to Voltaire (unverified)'}),

    # ── ADS ────────────────────────────────────────────────────────
    (("Organic carrot pack", "Label"),
     {'adType':'packaging','adBrand':'Bio Garden','adSlogan':'Naturally good for your eyes!'}),

    (("Organic carrot juice packaging", None),
     {'adType':'packaging','adBrand':'Bio Garden Juice','adSlogan':'Pure carrot, pure vision'}),

    (("Advertisement for a bottled water brand", None),
     {'adType':'tv','adBrand':'AquaVita','adSlogan':'Pure water for a pure life'}),

    (("Website of a major organic retailer", None),
     {'adType':'store','adBrand':'Bio & Nature','adSlogan':'100% natural, 100% true'}),

    (("\"Gluten-free\" aisle in a supermarket", None),
     {'adType':'packaging','adBrand':'GlutenFree Pro','adSlogan':'Your health deserves the best'}),

    (("Label on an organic food product in a supermarket", None),
     {'adType':'packaging','adBrand':'TerreBio','adSlogan':'Gluten-free · Organic · 100% natural'}),

    (("HR recruitment firm — sales brochure", None),
     {'adType':'print','adBrand':'HR Strategy Consulting'}),

    # ── EXPERTS ────────────────────────────────────────────────────
    (("Testimony of astronaut Yang Liwei", None),
     {'expertTitle':'First Chinese astronaut in space','expertInstitution':'Chinese National Space Programme (2003)'}),

    (("Ophthalmologist (eye doctor)", None),
     {'expertTitle':'Ophthalmologist','expertInstitution':'Medical clinic'}),

    (("Entomologist from the Natural History Museum", None),
     {'expertTitle':'Entomologist, researcher','expertInstitution':'Natural History Museum'}),

    (("Food chemist at INRAE", None),
     {'expertTitle':'Food chemist','expertInstitution':'INRAE — National Institute for Agricultural Research'}),

    (("Archaeologists from excavations in Egypt", None),
     {'expertTitle':'Archaeologists','expertInstitution':'Franco-Egyptian Archaeological Mission'}),

    (("Neurologist at a university hospital", None),
     {'expertTitle':'Neurologist, brain specialist','expertInstitution':'University hospital'}),

    (("Personal development coach", "Unverified"),
     {'expertTitle':'Personal development coach (uncertified)','expertInstitution':'Unverified online conference'}),

    (("Meteorologist from Météo-France", None),
     {'expertTitle':'Meteorologist','expertInstitution':'Météo-France'}),

    (("Eiffel Tower engineer", None),
     {'expertTitle':'Technical manager, engineer','expertInstitution':'Eiffel Tower — SETE'}),

    (("General practitioner", "Healthcare"),
     {'expertTitle':'General practitioner','expertInstitution':'Medical practice'}),

    (("General practitioner", "Doctor of human"),
     {'expertTitle':'General practitioner','expertInstitution':'Medical practice'}),

    (("National Veterinary School of Alfort", None),
     {'expertTitle':'Veterinary experts','expertInstitution':'National Veterinary School of Alfort (ENVA)'}),

    (("Gastroenterologist, Lyon University Hospital", None),
     {'expertTitle':'Gastroenterologist','expertInstitution':'Lyon University Hospital'}),

    (("Historian specialized in Vikings", None),
     {'expertTitle':'Medieval historian, Viking specialist','expertInstitution':'Research university'}),

    (("Retired midwife", None),
     {'expertTitle':'Retired midwife','expertInstitution':'30 years of clinical practice'}),

    (("Nutrition influencer", None),
     {'expertTitle':'Nutritionist (influencer)','expertInstitution':'No academic affiliation'}),

    (("High school chemistry teacher", None),
     {'expertTitle':'High school chemistry teacher','expertInstitution':'High school (outside specialty)'}),

    (("Veterinarian — veterinary clinic", None),
     {'expertTitle':'Veterinarian','expertInstitution':'Veterinary clinic'}),

    (("Emergency physician", "human emergencies"),
     {'expertTitle':'Emergency physician','expertInstitution':'Emergency department'}),

    (("Emergency physician publiant", None),
     {'expertTitle':'Emergency physician','expertInstitution':'Regional hospital — local newspaper'}),

    (("Hematologist", None),
     {'expertTitle':'Hematologist, blood specialist','expertInstitution':'University hospital'}),

    (("Pediatrician — Necker Hospital", None),
     {'expertTitle':'Paediatrician','expertInstitution':'Necker Hospital, Paris'}),

    (("Mathematics teacher", None),
     {'expertTitle':'Mathematics teacher','expertInstitution':'High school (outside specialty)'}),

    (("Chef specialized in seafood", None),
     {'expertTitle':'Chef, seafood specialist','expertInstitution':'Gastronomic restaurant'}),

    (("Homeopathic doctor, Paris Faculty of Medicine", None),
     {'expertTitle':'Homeopathic doctor','expertInstitution':'Paris Faculty of Medicine'}),

    (("AI director at a major tech company", None),
     {'expertTitle':'AI Director','expertInstitution':'Major technology company'}),

    (("Independent futurist", None),
     {'expertTitle':'Independent futurist','expertInstitution':'TED Conference'}),

    (("Retired police officer interviewed in a documentary", None),
     {'expertTitle':'Retired police officer','expertInstitution':'30 years of night patrols'}),

    (("William Happer, emeritus physicist at Princeton", None),
     {'expertTitle':'Emeritus physicist','expertInstitution':'Princeton University — CO2 Coalition'}),

    (("Andrew Wakefield, former gastroenterologist", None),
     {'expertTitle':'Former gastroenterologist (struck off medical register)','expertInstitution':'Royal Free Hospital (former)'}),

    (("Dr. Nicole Avena, Columbia University", None),
     {'expertTitle':'Neuroscientist, researcher','expertInstitution':'Columbia University — New York'}),

    # ── FORUMS / REDDIT / LINKEDIN ─────────────────────────────────
    (("Online cooking forum", None),
     {'forumUser':'gastronome42','forumName':'CookingPassion.com','forumDate':'2 years ago','forumLikes':'34'}),

    (("Fishing forum", None),
     {'forumUser':'CaptainCod','forumName':'SeaFishing.net','forumDate':'3 years ago','forumLikes':'12'}),

    (("'Curiosities and Mysteries' forum", None),
     {'forumUser':'CurioMax77','forumName':'Curiosities & Mysteries','forumDate':'1 year ago','forumLikes':'89'}),

    (("Parent forum 'Mamanpourlavie.fr'", None),
     {'forumUser':'WorriedMum91','forumName':'MamanPourLaVie.fr','forumDate':'8 months ago','forumLikes':'27'}),

    (("Mom on a parenting forum", None),
     {'forumUser':'Delphine_M','forumName':'ConnectedParents.com','forumDate':'1 year ago','forumLikes':'15'}),

    (("Thread Reddit", None),
     {'redditSub':'r/WeirdFacts','redditUser':'u/facts_cool_77','redditUpvotes':'3.4k','redditComments':'128',
      'redditTitle':'Did you know fish have a memory of only 3 SECONDS?? 🐟'}),

    (("Post LinkedIn viral", None),
     {'linkedinUser':'Jean-Pierre Martin','linkedinTitle':'Personal Development Coach | 50k followers',
      'linkedinLikes':'12,483','linkedinDate':'5 days ago'}),

    (("Online ecology forum", None),
     {'forumUser':'EcoActif42','forumName':'GreenPlanet.org','forumDate':'4 months ago','forumLikes':'61'}),

    (("Comment under an aquarium-keeping video", None),
     {'forumUser':'AquaMaster99','forumName':'YouTube · Comments','forumDate':'2 years ago','forumLikes':'23'}),
]

# ─────────────────────────────────────────────────────────────────
# Core injection function
# ─────────────────────────────────────────────────────────────────

def inject_fields_in_source(src_block, fields):
    """Inject fields into a JS source object block. Skips fields already present."""
    # Find the last '}' in the block
    last_brace = src_block.rfind('}')
    if last_brace == -1:
        return src_block, False

    # Find the last meaningful content before closing brace
    before = src_block[:last_brace]
    after  = src_block[last_brace:]

    new_fields = []
    for k, v in fields.items():
        if k not in src_block:  # only inject if field doesn't exist
            if isinstance(v, str):
                escaped = v.replace('\\', '\\\\').replace("'", "\\'")
                new_fields.append(f"{k}:'{escaped}'")
            elif isinstance(v, int):
                new_fields.append(f"{k}:{v}")
            elif isinstance(v, bool):
                new_fields.append(f"{k}:{'true' if v else 'false'}")

    if not new_fields:
        return src_block, False

    injection = ',\n     ' + ','.join(new_fields)
    return before + injection + after, True


def enrich_js_file(filepath, enrichments):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    total_injected = 0

    for (n_contains, d_contains), fields in enrichments:
        # Find all source objects matching this n: value
        # Pattern: find {em:"...", n:"...<n_contains>..."...}

        # Find positions of n:"<match>"
        pattern = 'n:"' + n_contains.replace('(', '\\(').replace(')', '\\)').replace('[', '\\[').replace(']', '\\]').replace("'", "\\'").replace("'", "\\'")

        # Simple substring search
        search_str = 'n:"' + n_contains

        start = 0
        while True:
            idx = content.find(search_str, start)
            if idx == -1:
                break

            # Find the start of the enclosing source object (look backwards for '{em:')
            obj_start = content.rfind('{em:', 0, idx)
            if obj_start == -1:
                obj_start = content.rfind('{', 0, idx)

            # Find the end (matching closing brace)
            depth = 0
            pos = obj_start
            in_str = False
            str_char = None
            while pos < len(content):
                c = content[pos]
                if in_str:
                    if c == str_char and (pos == 0 or content[pos-1] != '\\'):
                        in_str = False
                elif c in ('"', "'"):
                    in_str = True
                    str_char = c
                elif c == '{':
                    depth += 1
                elif c == '}':
                    depth -= 1
                    if depth == 0:
                        obj_end = pos + 1
                        break
                pos += 1
            else:
                start = idx + 1
                continue

            src_block = content[obj_start:obj_end]

            # Check d_contains filter
            if d_contains and d_contains not in src_block:
                start = idx + 1
                continue

            # Check that this source doesn't already have the first field
            first_field = list(fields.keys())[0]
            if first_field in src_block:
                start = idx + 1
                continue  # already enriched

            new_block, injected = inject_fields_in_source(src_block, fields)
            if injected:
                content = content[:obj_start] + new_block + content[obj_end:]
                total_injected += 1
                print(f"  + Enriched: {n_contains[:50]}")

            start = obj_start + len(new_block)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return total_injected


# ─────────────────────────────────────────────────────────────────
print("=== Enriching questions_fr.js ===")
n_fr = enrich_js_file(
    r'C:\Users\ASUS\Documents\Web apps\Jeux\fakemetre\questions_fr.js',
    FR_ENRICHMENTS
)
print(f"Total injections FR: {n_fr}")

print("\n=== Enriching questions_en.js ===")
n_en = enrich_js_file(
    r'C:\Users\ASUS\Documents\Web apps\Jeux\fakemetre\questions_en.js',
    EN_ENRICHMENTS
)
print(f"Total injections EN: {n_en}")

print(f"\nDone. Total: {n_fr + n_en} source objects enriched.")
