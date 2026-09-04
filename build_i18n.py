#!/usr/bin/env python3
"""Generate multilingual Černá bižuterie site + redesigned shared CSS."""
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parent
PAGES = ["index.html", "vyrobky.html", "sklo.html", "ceny.html", "historie.html", "oceneni.html", "kontakt.html"]
LANGS = ["cs", "en", "fr", "de"]

# --- Product gallery data extracted from Czech vyrobky.html ---
# (section, list of (full, thumb, pattern, price))
def parse_vyrobky(html: str):
    sections = []
    parts = re.split(r"<h2>(.*?)</h2>", html)
    # parts[0]=preamble, then pairs of (title, body)
    for i in range(1, len(parts), 2):
        title = parts[i]
        body = parts[i + 1]
        items = []
        for m in re.finditer(
            r'href="(images/bizu/[^"]+)"\s+data-lightbox\s+data-caption="vzor:\s*([^,]+),\s*cena:\s*([^"]+)"[^>]*>\s*<img\s+src="(images/bizu/[^"]+)"',
            body,
        ):
            items.append({
                "full": m.group(1),
                "pattern": m.group(2).strip(),
                "price": m.group(3).strip(),
                "thumb": m.group(4),
            })
        sections.append((title, items))
    return sections

VYROBKY_SECTIONS = parse_vyrobky((ROOT / "vyrobky.html").read_text(encoding="utf-8"))

BETLEMY = [
    ("Minimalistický betlém. 3 figurky, 400,- Kč.", "images/bet/3.jpg", "images/bet/3_t.jpg", "Betlém 3", "400,- Kč"),
    ("Malý betlém. 5 figurek, 630,- Kč.", "images/bet/5.jpg", "images/bet/5_t.jpg", "Betlém 5", "630,- Kč"),
    ("Menší betlém. 7 figurek, 860,- Kč.", "images/bet/7.jpg", "images/bet/7_t.jpg", "Betlém 7", "860,- Kč"),
    ("Základní betlém. 12 figurek, 1380,- Kč.", "images/bet/12.jpg", "images/bet/12_t.jpg", "Betlém 12", "1380,- Kč"),
    ("Ideální betlém. 15 figurek, 1670,- Kč.", "images/bet/15.jpg", "images/bet/15_t.jpg", "Betlém 15", "1670,- Kč"),
]

# --- Translations ---
T = {
    "cs": {
        "lang": "cs",
        "lang_label": "CS",
        "brand_sub": "Stanislav Jiroš",
        "tagline": "Tradiční jablonecký skleněný šperk od roku 1882",
        "nav": {
            "index.html": "Úvod",
            "vyrobky.html": "Výrobky",
            "sklo.html": "Sklo",
            "ceny.html": "Ceny",
            "historie.html": "Historie",
            "oceneni.html": "Ocenění",
            "kontakt.html": "Kontakt",
        },
        "meta_desc": "Stanislav Jiroš — Černá bižuterie. Tradiční jablonecká černá bižuterie.",
        "menu": "Menu",
        "close": "Zavřít",
        "pattern": "vzor",
        "price": "cena",
        "footer_h": "Obchodní, platební a dodací podmínky",
        "footer_p1": 'Objednávky telefonicky na čísle <a href="tel:+420723335058">723&nbsp;335&nbsp;058</a> nebo e-mailem na adrese <a href="mailto:blackjet@centrum.cz">blackjet@centrum.cz</a>.',
        "footer_p2": "Veškeré zboží je baleno jednotlivě v papírových krabičkách s průhledem.",
        "footer_p3": 'Platba na dobírku při zaslání zboží (poštovné a balné <strong>115,- Kč</strong>, při odběru nad <strong>3&nbsp;450,- Kč</strong> zdarma) nebo hotově při osobním odběru (po telefonické domluvě předem).',
        "home_title": "Úvod — Černá bižuterie",
        "home_h1": "Černá bižuterie",
        "home_lede": "Černá bižuterie patřila od roku 1882 k významnému odvětví jabloneckého průmyslu. Její obliba vyvrcholila v době smrti anglické královny Viktorie (1901), kdy se z této ozdoby stal smuteční šperk pro země britského impéria. Tento skleněný šperk byl zhotoven v Jablonci nad Nisou z původní suroviny.",
        "home_img_alt": "Černá bižuterie — ukázka šperku",
        "home_cta": "Prohlédnout výrobky",
        "vyrobky_title": "Výrobky — Černá bižuterie",
        "vyrobky_h1": "Výrobky",
        "vyrobky_intro": "Galerie černé bižuterie. Kliknutím na náhled zobrazíte větší fotografii.",
        "sections": {
            "Přívěsy": "Přívěsy",
            "Náušnice": "Náušnice",
            "Sametky": "Sametky",
            "Brože": "Brože",
            "Soupravy": "Soupravy",
        },
        "sklo_title": "Sklo / Betlémy — Černá bižuterie",
        "sklo_h1": "Sklo / Betlémy",
        "sklo_p1": "Jedná se o skleněné figurky, které dohromady tvoří BETLÉM. Sady jsou přesně podle fotografií, v každé sadě se mohou postavy mírně lišit v detailech a barvách, každá postava je originál. Velikost postav 7–8&nbsp;cm.",
        "sklo_p2": "Vše dokonale zabaleno k přepravě. Případně lze dohodnout jiné sestavy (počet a složení).",
        "betlemy": [
            "Minimalistický betlém. 3 figurky, 400,- Kč.",
            "Malý betlém. 5 figurek, 630,- Kč.",
            "Menší betlém. 7 figurek, 860,- Kč.",
            "Základní betlém. 12 figurek, 1380,- Kč.",
            "Ideální betlém. 15 figurek, 1670,- Kč.",
        ],
        "bet_label": "Betlém",
        "ceny_title": "Ceny — Černá bižuterie",
        "ceny_h1": "Ceny a dodací podmínky",
        "ceny_p": 'Aktuální ceny výrobků najdete přímo u fotografií na stránkách <a href="vyrobky.html">Výrobky</a> a <a href="sklo.html">Sklo / Betlémy</a>.',
        "ceny_li": [
            'Poštovné a balné: <strong>115,- Kč</strong>',
            'Doprava zdarma při odběru nad <strong>3&nbsp;450,- Kč</strong>',
            "Veškeré zboží je baleno jednotlivě v papírových krabičkách s průhledem",
            "Platba na dobírku při zaslání, nebo hotově při osobním odběru (po telefonické domluvě)",
        ],
        "ceny_orders": 'Objednávky: <a href="tel:+420723335058">+420&nbsp;723&nbsp;335&nbsp;058</a> · <a href="mailto:blackjet@centrum.cz">blackjet@centrum.cz</a>',
        "hist_title": "Historie — Černá bižuterie",
        "hist_h1": "Historie černé bižuterie",
        "hist_html": None,  # filled below from original for CS
        "ocen_title": "Ocenění — Černá bižuterie",
        "ocen_h1": "Ocenění",
        "ocen_cap": "Pořad Toulavá kamera České televize ze dne 19.&nbsp;4.&nbsp;2015. Reportáž o černé bižuterii.",
        "ocen_alt": "Toulavá kamera — Černá bižuterie",
        "ocen_img_alt": "Ocenění",
        "kon_title": "Kontakt — Černá bižuterie",
        "kon_h1": "Kontakt",
        "kon_phone": "Telefon",
        "kon_email": "E-mail",
        "kon_ico": "IČO",
        "kon_img_alt": "Ukázka bižuterie",
    },
    "en": {
        "lang": "en",
        "lang_label": "EN",
        "brand_sub": "Black jewellery · Stanislav Jiroš",
        "tagline": "Traditional Jablonec glass jewellery since 1882",
        "nav": {
            "index.html": "Home",
            "vyrobky.html": "Products",
            "sklo.html": "Glass",
            "ceny.html": "Prices",
            "historie.html": "History",
            "oceneni.html": "Awards",
            "kontakt.html": "Contact",
        },
        "meta_desc": "Stanislav Jiroš — Černá bižuterie. Traditional Jablonec black glass jewellery.",
        "menu": "Menu",
        "close": "Close",
        "pattern": "pattern",
        "price": "price",
        "footer_h": "Terms of sale, payment and delivery",
        "footer_p1": 'Orders by phone at <a href="tel:+420723335058">723&nbsp;335&nbsp;058</a> or by e-mail at <a href="mailto:blackjet@centrum.cz">blackjet@centrum.cz</a>.',
        "footer_p2": "All goods are packed individually in paper boxes with a viewing window.",
        "footer_p3": 'Cash on delivery when goods are shipped (postage and packing <strong>115,- Kč</strong>, free for orders over <strong>3&nbsp;450,- Kč</strong>) or cash on personal collection (by prior phone arrangement).',
        "home_title": "Home — Černá bižuterie",
        "home_h1": "Černá bižuterie",
        "home_lede": "Black jewellery has been an important part of Jablonec industry since 1882. Its popularity peaked around the death of Queen Victoria (1901), when this ornament became mourning jewellery for the countries of the British Empire. This glass jewellery is made in Jablonec nad Nisou from the original material.",
        "home_img_alt": "Černá bižuterie — jewellery sample",
        "home_cta": "Browse products",
        "vyrobky_title": "Products — Černá bižuterie",
        "vyrobky_h1": "Products",
        "vyrobky_intro": "Gallery of black jewellery. Click a thumbnail to view a larger photo.",
        "sections": {
            "Přívěsy": "Pendants",
            "Náušnice": "Earrings",
            "Sametky": "Velvet chokers",
            "Brože": "Brooches",
            "Soupravy": "Sets",
        },
        "sklo_title": "Glass / Nativity sets — Černá bižuterie",
        "sklo_h1": "Glass / Nativity sets",
        "sklo_p1": "These are glass figurines that together form a NATIVITY set. Sets match the photographs; within each set the figures may differ slightly in detail and colour — each figure is an original. Figure height 7–8&nbsp;cm.",
        "sklo_p2": "Everything is carefully packed for shipping. Other combinations (number and composition) can be arranged on request.",
        "betlemy": [
            "Minimalist nativity. 3 figures, 400,- Kč.",
            "Small nativity. 5 figures, 630,- Kč.",
            "Smaller nativity. 7 figures, 860,- Kč.",
            "Basic nativity. 12 figures, 1380,- Kč.",
            "Ideal nativity. 15 figures, 1670,- Kč.",
        ],
        "bet_label": "Nativity",
        "ceny_title": "Prices — Černá bižuterie",
        "ceny_h1": "Prices and delivery terms",
        "ceny_p": 'Current product prices are shown next to the photographs on the <a href="vyrobky.html">Products</a> and <a href="sklo.html">Glass / Nativity sets</a> pages.',
        "ceny_li": [
            'Postage and packing: <strong>115,- Kč</strong>',
            'Free shipping on orders over <strong>3&nbsp;450,- Kč</strong>',
            "All goods are packed individually in paper boxes with a viewing window",
            "Cash on delivery when shipped, or cash on personal collection (by prior phone arrangement)",
        ],
        "ceny_orders": 'Orders: <a href="tel:+420723335058">+420&nbsp;723&nbsp;335&nbsp;058</a> · <a href="mailto:blackjet@centrum.cz">blackjet@centrum.cz</a>',
        "hist_title": "History — Černá bižuterie",
        "hist_h1": "History of black jewellery",
        "ocen_title": "Awards — Černá bižuterie",
        "ocen_h1": "Awards",
        "ocen_cap": "Czech Television’s Toulavá kamera programme from 19&nbsp;April&nbsp;2015. A report on black jewellery.",
        "ocen_alt": "Toulavá kamera — Černá bižuterie",
        "ocen_img_alt": "Awards",
        "kon_title": "Contact — Černá bižuterie",
        "kon_h1": "Contact",
        "kon_phone": "Phone",
        "kon_email": "E-mail",
        "kon_ico": "Company ID (IČO)",
        "kon_img_alt": "Jewellery sample",
    },
    "fr": {
        "lang": "fr",
        "lang_label": "FR",
        "brand_sub": "Bijouterie noire · Stanislav Jiroš",
        "tagline": "Bijouterie en verre traditionnelle de Jablonec depuis 1882",
        "nav": {
            "index.html": "Accueil",
            "vyrobky.html": "Produits",
            "sklo.html": "Verre",
            "ceny.html": "Prix",
            "historie.html": "Histoire",
            "oceneni.html": "Récompenses",
            "kontakt.html": "Contact",
        },
        "meta_desc": "Stanislav Jiroš — Černá bižuterie. Bijouterie noire traditionnelle de Jablonec.",
        "menu": "Menu",
        "close": "Fermer",
        "pattern": "modèle",
        "price": "prix",
        "footer_h": "Conditions commerciales, de paiement et de livraison",
        "footer_p1": 'Commandes par téléphone au <a href="tel:+420723335058">723&nbsp;335&nbsp;058</a> ou par e-mail à <a href="mailto:blackjet@centrum.cz">blackjet@centrum.cz</a>.',
        "footer_p2": "Tous les articles sont emballés individuellement dans des boîtes en papier avec fenêtre.",
        "footer_p3": 'Paiement contre remboursement à l’envoi (frais de port et d’emballage <strong>115,- Kč</strong>, gratuits au-delà de <strong>3&nbsp;450,- Kč</strong>) ou en espèces lors d’un retrait en personne (après accord téléphonique préalable).',
        "home_title": "Accueil — Černá bižuterie",
        "home_h1": "Černá bižuterie",
        "home_lede": "La bijouterie noire fait partie des branches importantes de l’industrie de Jablonec depuis 1882. Sa popularité culmina à la mort de la reine Victoria d’Angleterre (1901), lorsque cet ornement devint un bijou de deuil pour les pays de l’Empire britannique. Ce bijou en verre est fabriqué à Jablonec nad Nisou à partir de la matière d’origine.",
        "home_img_alt": "Černá bižuterie — exemple de bijou",
        "home_cta": "Voir les produits",
        "vyrobky_title": "Produits — Černá bižuterie",
        "vyrobky_h1": "Produits",
        "vyrobky_intro": "Galerie de bijouterie noire. Cliquez sur une vignette pour agrandir la photo.",
        "sections": {
            "Přívěsy": "Pendentifs",
            "Náušnice": "Boucles d’oreilles",
            "Sametky": "Colliers de velours",
            "Brože": "Broches",
            "Soupravy": "Parures",
        },
        "sklo_title": "Verre / Crèches — Černá bižuterie",
        "sklo_h1": "Verre / Crèches",
        "sklo_p1": "Il s’agit de figurines en verre qui forment ensemble une CRÈCHE. Les ensembles correspondent aux photographies ; dans chaque ensemble, les personnages peuvent différer légèrement dans les détails et les couleurs — chaque figurine est un original. Hauteur des personnages : 7–8&nbsp;cm.",
        "sklo_p2": "Le tout est soigneusement emballé pour le transport. D’autres compositions (nombre et assortiment) peuvent être convenues.",
        "betlemy": [
            "Crèche minimaliste. 3 figurines, 400,- Kč.",
            "Petite crèche. 5 figurines, 630,- Kč.",
            "Crèche plus petite. 7 figurines, 860,- Kč.",
            "Crèche de base. 12 figurines, 1380,- Kč.",
            "Crèche idéale. 15 figurines, 1670,- Kč.",
        ],
        "bet_label": "Crèche",
        "ceny_title": "Prix — Černá bižuterie",
        "ceny_h1": "Prix et conditions de livraison",
        "ceny_p": 'Les prix actuels figurent à côté des photographies sur les pages <a href="vyrobky.html">Produits</a> et <a href="sklo.html">Verre / Crèches</a>.',
        "ceny_li": [
            'Frais de port et d’emballage : <strong>115,- Kč</strong>',
            'Livraison gratuite pour les commandes de plus de <strong>3&nbsp;450,- Kč</strong>',
            "Tous les articles sont emballés individuellement dans des boîtes en papier avec fenêtre",
            "Paiement contre remboursement à l’envoi, ou en espèces lors d’un retrait en personne (après accord téléphonique)",
        ],
        "ceny_orders": 'Commandes : <a href="tel:+420723335058">+420&nbsp;723&nbsp;335&nbsp;058</a> · <a href="mailto:blackjet@centrum.cz">blackjet@centrum.cz</a>',
        "hist_title": "Histoire — Černá bižuterie",
        "hist_h1": "Histoire de la bijouterie noire",
        "ocen_title": "Récompenses — Černá bižuterie",
        "ocen_h1": "Récompenses",
        "ocen_cap": "Émission Toulavá kamera de la Télévision tchèque du 19&nbsp;avril&nbsp;2015. Reportage sur la bijouterie noire.",
        "ocen_alt": "Toulavá kamera — Černá bižuterie",
        "ocen_img_alt": "Récompenses",
        "kon_title": "Contact — Černá bižuterie",
        "kon_h1": "Contact",
        "kon_phone": "Téléphone",
        "kon_email": "E-mail",
        "kon_ico": "N° d’entreprise (IČO)",
        "kon_img_alt": "Exemple de bijou",
    },
    "de": {
        "lang": "de",
        "lang_label": "DE",
        "brand_sub": "Schwarzer Schmuck · Stanislav Jiroš",
        "tagline": "Traditioneller Gablonzer Glasschmuck seit 1882",
        "nav": {
            "index.html": "Start",
            "vyrobky.html": "Produkte",
            "sklo.html": "Glas",
            "ceny.html": "Preise",
            "historie.html": "Geschichte",
            "oceneni.html": "Auszeichnungen",
            "kontakt.html": "Kontakt",
        },
        "meta_desc": "Stanislav Jiroš — Černá bižuterie. Traditioneller Gablonzer schwarzer Glasschmuck.",
        "menu": "Menü",
        "close": "Schließen",
        "pattern": "Muster",
        "price": "Preis",
        "footer_h": "Geschäfts-, Zahlungs- und Lieferbedingungen",
        "footer_p1": 'Bestellungen telefonisch unter <a href="tel:+420723335058">723&nbsp;335&nbsp;058</a> oder per E-Mail an <a href="mailto:blackjet@centrum.cz">blackjet@centrum.cz</a>.',
        "footer_p2": "Alle Waren werden einzeln in Pappschachteln mit Sichtfenster verpackt.",
        "footer_p3": 'Zahlung per Nachnahme bei Versand (Porto und Verpackung <strong>115,- Kč</strong>, ab <strong>3&nbsp;450,- Kč</strong> kostenlos) oder bar bei persönlicher Abholung (nach vorheriger telefonischer Absprache).',
        "home_title": "Start — Černá bižuterie",
        "home_h1": "Černá bižuterie",
        "home_lede": "Schwarzer Schmuck gehört seit 1882 zu einem bedeutenden Zweig der Gablonzer Industrie. Seine Beliebtheit gipfelte um den Tod der englischen Königin Victoria (1901), als dieser Schmuck zum Trauerschmuck für die Länder des Britischen Empire wurde. Dieser Glasschmuck wird in Jablonec nad Nisou aus dem ursprünglichen Material gefertigt.",
        "home_img_alt": "Černá bižuterie — Schmuckbeispiel",
        "home_cta": "Produkte ansehen",
        "vyrobky_title": "Produkte — Černá bižuterie",
        "vyrobky_h1": "Produkte",
        "vyrobky_intro": "Galerie des schwarzen Schmucks. Klicken Sie auf ein Vorschaubild für ein größeres Foto.",
        "sections": {
            "Přívěsy": "Anhänger",
            "Náušnice": "Ohrringe",
            "Sametky": "Samtbänder",
            "Brože": "Broschen",
            "Soupravy": "Garnituren",
        },
        "sklo_title": "Glas / Krippen — Černá bižuterie",
        "sklo_h1": "Glas / Krippen",
        "sklo_p1": "Es handelt sich um Glasfiguren, die zusammen eine KRIPPE bilden. Die Sets entsprechen den Fotografien; innerhalb jedes Sets können die Figuren in Details und Farben leicht abweichen — jede Figur ist ein Original. Figurenhöhe 7–8&nbsp;cm.",
        "sklo_p2": "Alles wird sorgfältig für den Versand verpackt. Andere Zusammenstellungen (Anzahl und Zusammensetzung) sind nach Absprache möglich.",
        "betlemy": [
            "Minimalistische Krippe. 3 Figuren, 400,- Kč.",
            "Kleine Krippe. 5 Figuren, 630,- Kč.",
            "Kleinere Krippe. 7 Figuren, 860,- Kč.",
            "Basis-Krippe. 12 Figuren, 1380,- Kč.",
            "Ideale Krippe. 15 Figuren, 1670,- Kč.",
        ],
        "bet_label": "Krippe",
        "ceny_title": "Preise — Černá bižuterie",
        "ceny_h1": "Preise und Lieferbedingungen",
        "ceny_p": 'Aktuelle Produktpreise finden Sie direkt bei den Fotografien auf den Seiten <a href="vyrobky.html">Produkte</a> und <a href="sklo.html">Glas / Krippen</a>.',
        "ceny_li": [
            'Porto und Verpackung: <strong>115,- Kč</strong>',
            'Kostenloser Versand ab <strong>3&nbsp;450,- Kč</strong>',
            "Alle Waren werden einzeln in Pappschachteln mit Sichtfenster verpackt",
            "Zahlung per Nachnahme bei Versand oder bar bei persönlicher Abholung (nach telefonischer Absprache)",
        ],
        "ceny_orders": 'Bestellungen: <a href="tel:+420723335058">+420&nbsp;723&nbsp;335&nbsp;058</a> · <a href="mailto:blackjet@centrum.cz">blackjet@centrum.cz</a>',
        "hist_title": "Geschichte — Černá bižuterie",
        "hist_h1": "Geschichte des schwarzen Schmucks",
        "ocen_title": "Auszeichnungen — Černá bižuterie",
        "ocen_h1": "Auszeichnungen",
        "ocen_cap": "Sendung Toulavá kamera des Tschechischen Fernsehens vom 19.&nbsp;April&nbsp;2015. Reportage über schwarzen Schmuck.",
        "ocen_alt": "Toulavá kamera — Černá bižuterie",
        "ocen_img_alt": "Auszeichnungen",
        "kon_title": "Kontakt — Černá bižuterie",
        "kon_h1": "Kontakt",
        "kon_phone": "Telefon",
        "kon_email": "E-Mail",
        "kon_ico": "IČO (Firmen-ID)",
        "kon_img_alt": "Schmuckbeispiel",
    },
}

# History prose translations (professional, faithful)
HIST = {
    "cs": None,  # use original extract
    "en": """<p>By the 1860s, Jablonec costume-jewellery production already had a hundred years of development behind it. It had firmly established itself not only in domestic awareness, but was also taken seriously abroad, and growing orders arrived in Jablonec for goods now demonstrably <span style="font-style: italic;">“Jablonec”</span>.</p>

<p style="text-align: center;"><a href="../images/bizu/892.jpg" data-lightbox data-caption=""><img src="../images/bizu/892_t.jpg" width="160" /></a></p>

<p>The favour of the age, emphasising glass ornament on dress, brought in the 1860s a boom such as the foothills of the Jizera Mountains had not yet seen. Demands from foreign — often exotic — markets, and the formal and functional peculiarity of jewellery meant for the most varied peoples of every continent, took their toll. Unusual stimuli, often ready-made patterns from outside, increasingly limited the independent creative work of jewellery makers. The pressure of an impersonal foreign market quickly led to mass imitation and alteration of foreign, predominantly French, formal innovations.</p>

<p>In this boom of mediocrity, only the glass button retained a special position; after 1864 it held world primacy in fashion. From its technological gains there then emerged, at the same time, another article that built on the best of costume-jewellery creation, returned wholly to the primacy of glass, and raised the Jablonec product to jewellery that was entirely distinctive, original and independent. At the close of the 1860s this became <span style="font-weight: bold;">black jewellery</span>.</p>

<p style="text-align: center;"><a href="../images/bizu/925.jpg" data-lightbox data-caption=""><img src="../images/bizu/925_t.jpg" width="160" /></a></p>

<p>In its beginnings it responded to strengthening demand — mainly from the European market — for light and valuable dress and hat ornament. Besides proven brooches and buttons, hair clasps, combs and pins were most often made. The true flowering of black jewellery, however, still lay ahead.</p>
<p>Transferring the novelty — the technique of soldering with tin, which the small Tanvald maker Karel Fischer had learned at the firm Naudascher et Kahn in Stuttgart — to black jewellery was only a matter of time, suitable paraffin soldering lamps, and experience. The result was revolutionary and, in its later economic consequences, more significant than riveting.</p>
<p>The same stones were used; only the fused rivets were replaced by pressing in a brass hollow tube, often of tiny dimensions. A designed pattern of black jewellery — for example a clasp, pin, brooch, dress ornament or hair comb — was cast in plaster; the cast then served as a matrix for serial production. Individual glass stones were soldered onto wire. The wire construction thus replaced a heavy metal backing; riveting was succeeded by soft soldering. The result was maximally light jewellery: the metal base was reduced to a minimum, and the pure cut of the black stone dominated the piece.</p>

<p style="text-align: center;"><a href="../images/bizu/937.jpg" data-lightbox data-caption=""><img src="../images/bizu/937_t.jpg" width="160" /></a></p>

<p>The new technique multiplied the formal possibilities of black jewellery to the very limits of the designer’s imagination. Moreover it required no special prior craft skills, nor capital investment in expensive foreign metal stampings still imported from France. It was what the Jizera landscape needed most — typical home work. Soft soldering with tin suited both the character of the jewellery and its domestic production base, the dispersed manufactory cottage industry around Smržovka.</p>
<p>Enormous demand for jewellery made this way brought jet jewellery in the 1890s to a high degree of perfection. With the death of Queen Victoria (1901), black jewellery became mourning jewellery for the countries of the British Empire. It became a world fashion. Its production and formal purity reached a peak never afterwards surpassed.</p>

<p style="text-align: center;"><a href="../images/bizu/943.jpg" data-lightbox data-caption=""><img src="../images/bizu/943_t.jpg" width="160" /></a></p>

<p>The Balkan Wars and rapidly changing fashion shifts led to more frequent and ever longer crises. Quality goods were replaced by devalued products. Strong competition from metal costume jewellery forced makers of glass goods to work in black jewellery. There was less bread for all.</p>
<p>The world economic crisis gradually struck every branch of Jablonec enterprise. Black jewellery, which for eighty years had successfully resisted fashion swings and crises, no longer had the strength to stand firm.</p>
<p>After the Second World War an attempt was made to revive it at the place of its origin. In the workshops of the once-famous Feix firm in Jiřetín it enjoyed two or three more years of renaissance. Then that too ended.</p>
<p>It fell into oblivion, like so many once-famous branches of Jablonec industry. Its production process and technological peculiarities were forgotten. Only somewhere in attic spaces stores of noble semi-finished goods survived — cut glass stones of every size and shape, those with tiny fused links meant for riveting, and the later ones for soldering — together with pliers, old plaster casts, metal backings, wires, galleries, cutting tools and matrices. And with them, rare old patterns.</p>""",
    "fr": """<p>Dans les années 1860, la fabrication de bijouterie de fantaisie à Jablonec avait déjà derrière elle cent ans de développement. Elle s’était durablement imposée non seulement dans les esprits du pays, mais était aussi prise au sérieux à l’étranger, et des commandes croissantes arrivaient à Jablonec pour des marchandises désormais clairement <span style="font-style: italic;">« de Jablonec »</span>.</p>

<p style="text-align: center;"><a href="../images/bizu/892.jpg" data-lightbox data-caption=""><img src="../images/bizu/892_t.jpg" width="160" /></a></p>

<p>La faveur de l’époque, qui mettait en avant l’ornement de verre sur les habits, apporta dans les années 1860 une conjoncture telle que le piémont des monts Jizera n’en avait pas encore connue. Les exigences des marchés étrangers, souvent exotiques, et le caractère formel et fonctionnel particulier de ces bijoux destinés aux peuples les plus divers de tous les continents firent leur œuvre. Des stimulants inhabituels, souvent des modèles tout prêts venus de l’extérieur, limitaient de plus en plus le travail créatif autonome des fabricants. La pression d’un marché étranger impersonnel mena rapidement à l’imitation et à la modification en masse d’innovations formelles étrangères, surtout françaises.</p>

<p>Dans cette conjoncture de médiocrité, seul le bouton de verre conserva une place particulière ; après 1864, il occupa la première place mondiale dans la mode. De ses acquis technologiques naquit alors, à la même époque, un autre article qui se rattacha au meilleur de la création bijoutière, revint entièrement à la prédominance du verre et éleva le produit de Jablonec au rang de bijou pleinement original, autonome et distinct. À la fin des années 1860, ce fut la <span style="font-weight: bold;">bijouterie noire</span>.</p>

<p style="text-align: center;"><a href="../images/bizu/925.jpg" data-lightbox data-caption=""><img src="../images/bizu/925_t.jpg" width="160" /></a></p>

<p>À ses débuts, elle répondit à une demande croissante — surtout du marché européen — d’ornements légers et de valeur pour habits et chapeaux. Outre les broches et boutons éprouvés, on fabriquait le plus souvent des épingles à cheveux, des peignes et des épingles. Le véritable essor de la bijouterie noire était encore à venir.</p>
<p>Transposer la nouveauté — la technique du soudage à l’étain, que le petit fabricant de Tanvald Karel Fischer avait découverte chez Naudascher et Kahn à Stuttgart — à la bijouterie noire n’était qu’une question de temps, de lampes à pétrole adaptées et d’expérience. Le résultat fut révolutionnaire et, dans ses conséquences économiques ultérieures, plus important que le rivetage.</p>
<p>On utilisa les mêmes pierres ; seuls les rivets fondus furent remplacés par l’enfoncement d’un tube creux de laiton, souvent de dimensions infimes. Un modèle dessiné de bijouterie noire — par exemple une agrafe, une épingle, une broche, un ornement de robe ou un peigne — était coulé en plâtre ; le moulage servait ensuite de matrice pour la production en série. Les pierres de verre individuelles étaient soudées sur du fil. La construction en fil remplaçait ainsi un support métallique lourd ; le rivetage cédait la place au soudage tendre. Il en résultait un bijou allégé au maximum : le support métallique était réduit au minimum, et la taille pure de la pierre noire dominait le bijou.</p>

<p style="text-align: center;"><a href="../images/bizu/937.jpg" data-lightbox data-caption=""><img src="../images/bizu/937_t.jpg" width="160" /></a></p>

<p>La nouvelle technique multiplia les possibilités formelles de la bijouterie noire jusqu’aux limites mêmes de l’imagination du dessinateur. De plus, elle n’exigeait ni savoir-faire artisanal préalable particulier, ni investissements en coûteux emboutis métalliques étrangers encore importés de France. C’était ce dont le paysage des Jizera avait le plus besoin — un travail domestique typique. Le soudage tendre à l’étain convenait parfaitement au caractère du bijou et à sa base de production domestique, l’industrie manufacturière dispersée autour de Smržovka.</p>
<p>L’énorme demande pour cette bijouterie porta dans les années 1890 le bijou de jais à un haut degré de perfection. À la mort de la reine Victoria (1901), la bijouterie noire devint le bijou de deuil des pays de l’Empire britannique. Elle devint une mode mondiale. Sa fabrication et sa pureté formelle atteignirent un sommet jamais dépassé depuis.</p>

<p style="text-align: center;"><a href="../images/bizu/943.jpg" data-lightbox data-caption=""><img src="../images/bizu/943_t.jpg" width="160" /></a></p>

<p>Les guerres balkaniques et les retournements de mode rapides entraînèrent des crises plus fréquentes et de plus en plus durables. Les marchandises de qualité furent remplacées par des produits dévalorisés. La forte concurrence de la bijouterie métallique força les fabricants de verre à travailler dans le bijou noir. Le pain se raréfia pour tous.</p>
<p>La crise économique mondiale toucha progressivement toutes les branches de l’entreprise de Jablonec. La bijouterie noire, qui avait pendant quatre-vingts ans résisté avec succès aux fluctuations de la mode et aux crises, n’avait plus la force de tenir.</p>
<p>Après la Seconde Guerre mondiale, on tenta de la faire revivre sur le lieu de sa naissance. Dans les ateliers de l’ancienne et célèbre firme Feix à Jiřetín, elle connut encore deux ou trois années de renaissance. Puis cela aussi prit fin.</p>
<p>Elle tomba dans l’oubli, comme tant de branches autrefois illustres de l’industrie de Jablonec. On oublia son procédé de fabrication et ses particularités technologiques. Ce n’est que quelque part dans des greniers que survécurent des stocks de semi-produits nobles — pierres de verre taillées de toutes tailles et formes, celles à petits maillons fondus destinées au rivetage, et les plus récentes pour le soudage — avec pinces, vieux moulages de plâtre, supports métalliques, fils, galeries, outils de coupe et matrices. Et avec eux, de rares anciens modèles.</p>""",
    "de": """<p>In den 1860er Jahren hatte die Gablonzer Bijouterieproduktion bereits hundert Jahre Entwicklung hinter sich. Sie hatte sich nicht nur im heimischen Bewusstsein dauerhaft durchgesetzt; auch im Ausland wurde sie ernst genommen, und nach Jablonec kamen wachsende Bestellungen auf nachweislich <span style="font-style: italic;">„Gablonzer“</span> Ware.</p>

<p style="text-align: center;"><a href="../images/bizu/892.jpg" data-lightbox data-caption=""><img src="../images/bizu/892_t.jpg" width="160" /></a></p>

<p>Die Gunst der Zeit, die am Kleid den Glaszierrat betonte, brachte in den 1860er Jahren eine Konjunktur, wie sie das Isergebirgsvorland bis dahin nicht gekannt hatte. Die Anforderungen ausländischer, oft exotischer Märkte und die formale wie funktionale Eigenart dieses Schmucks für die verschiedensten Völker aller Erdteile taten das Ihre. Ungewohnte Anregungen, oft fertige Muster von außen, schränkten die eigenständige schöpferische Arbeit der Bijouteriehersteller immer mehr ein. Der Druck des unpersönlichen fremden Marktes führte rasch zur Massenimitation und Abwandlung fremder, vorwiegend französischer Forminnovationen.</p>

<p>In dieser Konjunktur der Mittelmäßigkeit behielt nur der Glasknopf eine besondere Stellung; nach 1864 nahm er in der Mode den Weltvorrang ein. Aus seinen technologischen Gewinnen ging zur gleichen Zeit noch ein weiterer Artikel hervor, der an das Beste der Bijouterieschöpfung anknüpfte, ganz zur Vorherrschaft des Glases zurückkehrte und das Gablonzer Erzeugnis zu einem völlig eigenständigen, ursprünglichen Schmuck erhob. Ende der 1860er Jahre wurde daraus die <span style="font-weight: bold;">schwarze Bijouterie</span>.</p>

<p style="text-align: center;"><a href="../images/bizu/925.jpg" data-lightbox data-caption=""><img src="../images/bizu/925_t.jpg" width="160" /></a></p>

<p>In ihren Anfängen entsprang sie der erstarkenden Nachfrage — vor allem des europäischen Marktes — nach leichtem und wertvollem Kleid- und Hutzierrat. Neben bewährten Broschen und Knöpfen fertigte man am häufigsten Haarspangen, Kämme und Nadeln. Der eigentliche Aufschwung der schwarzen Bijouterie stand jedoch erst noch bevor.</p>
<p>Die Neuheit — die Technik des Lötens mit Zinn, die der kleine Tanwalder Hersteller Karel Fischer bei der Firma Naudascher et Kahn in Stuttgart kennengelernt hatte — auf die schwarze Bijouterie zu übertragen, war nur eine Frage der Zeit, geeigneter Petroleum-Lötlampen und der Erfahrung. Das Ergebnis war revolutionär und in seinen späteren wirtschaftlichen Folgen bedeutsamer als das Nieten.</p>
<p>Es wurden dieselben Steine verwendet; nur die eingeschmolzenen Nieten wurden durch das Eindrücken eines messingenen Hohlröhrchens oft winziger Abmessungen ersetzt. Ein entworfenes Muster schwarzer Bijouterie — etwa Spange, Nadel, Brosche, Kleidschmuck oder Haarkamm — wurde in Gips gegossen; der Abguss diente dann als Matrize für die Serienfertigung. Die einzelnen Glassteine wurden auf Draht gelötet. Die Drahtkonstruktion ersetzte so eine schwere Metallunterlage; das Nieten wurde durch Weichlöten abgelöst. Es entstand maximal erleichterter Schmuck: der Metalluntergrund war auf das Mindeste beschränkt, der reine Schliff des schwarzen Steins beherrschte das Stück.</p>

<p style="text-align: center;"><a href="../images/bizu/937.jpg" data-lightbox data-caption=""><img src="../images/bizu/937_t.jpg" width="160" /></a></p>

<p>Die neue Technik vervielfachte die Formmöglichkeiten der schwarzen Bijouterie bis an die Grenzen der Entwerferfantasie. Zudem verlangte sie weder besondere vorausgehende handwerkliche Fertigkeiten noch Kapitalinvestitionen in teure ausländische Metallpresslinge, die noch immer aus Frankreich eingeführt wurden. Sie war das, was die Iserlandschaft am meisten brauchte — typische Heimarbeit. Das Weichlöten mit Zinn entsprach am besten dem Charakter des Schmucks und seiner heimischen Produktionsbasis, der verstreuten manufakturellen Hausindustrie um Smržovka.</p>
<p>Die enorme Nachfrage nach so hergestellter Bijouterie brachte in den 1890er Jahren den Jettenschmuck zu einem hohen Grad der Vollkommenheit. Mit dem Tod der englischen Königin Victoria (1901) wurde aus der schwarzen Bijouterie der Trauerschmuck der Länder des Britischen Empire. Er wurde Weltmode. Seine Herstellung und formale Reinheit erreichten einen Gipfel, der nie wieder übertroffen wurde.</p>

<p style="text-align: center;"><a href="../images/bizu/943.jpg" data-lightbox data-caption=""><img src="../images/bizu/943_t.jpg" width="160" /></a></p>

<p>Die Balkankriege und rasch wechselnde Modeschwankungen führten zu häufigeren und immer länger andauernden Krisen. Qualitätsware wurde durch entwertete Erzeugnisse ersetzt. Die starke Konkurrenz der Metallbijouterie zwang die Hersteller von Glaswaren, im schwarzen Schmuck zu arbeiten. Das Brot wurde knapper für alle.</p>
<p>Die Weltwirtschaftskrise erfasste allmählich alle Zweige des Gablonzer Unternehmertums. Die schwarze Bijouterie, die achtzig Jahre lang Modeschwankungen und Krisen erfolgreich widerstanden hatte, hatte keine Kraft mehr zum Widerstand.</p>
<p>Nach dem Zweiten Weltkrieg wurde versucht, sie am Ort ihrer Entstehung wiederzubeleben. In den Betrieben der einst berühmten Firma Feix in Jiřetín erlebte sie noch zwei oder drei Jahre ihrer Renaissance. Dann endete auch das.</p>
<p>Sie geriet in Vergessenheit wie so viele einst berühmte Zweige der Gablonzer Industrie. Vergessen wurden ihr Herstellungsverfahren und ihre technologischen Besonderheiten. Nur irgendwo auf Dachböden überdauerten Lager edler Halbfabrikate — geschliffene Glassteine aller Größen und Formen, jene mit kleinen eingeschmolzenen Gliedern für das Nieten und die jüngeren für das Löten — zusammen mit Zangen, alten Gipsabgüssen, Metallunterlagen, Drähten, Galerien, Schneidwerkzeugen und Matrizen. Und mit ihnen seltene alte Muster.</p>""",
}

def extract_cs_history():
    html = (ROOT / "historie.html").read_text(encoding="utf-8")
    m = re.search(r'<div class="prose">(.*?)</div>\s*</main>', html, re.S)
    prose = m.group(1)
    # fix image paths
    prose = prose.replace('href="images/', 'href="../images/')
    prose = prose.replace('src="images/', 'src="../images/')
    return prose

T["cs"]["hist_html"] = extract_cs_history()
for lang in ("en", "fr", "de"):
    T[lang]["hist_html"] = HIST[lang]


def lang_switch(current: str, page: str) -> str:
    parts = []
    for i, code in enumerate(LANGS):
        label = code.upper()
        cls = ' class="active"' if code == current else ""
        href = f"../{code}/{page}"
        parts.append(f'<a href="{href}" data-lang="{code}"{cls}>{label}</a>')
        if i < len(LANGS) - 1:
            parts.append('<span class="sep" aria-hidden="true">·</span>')
    return '<nav class="lang-switch" aria-label="Language">' + "".join(parts) + "</nav>"


def header(t: dict, page: str) -> str:
    nav_links = []
    for p in PAGES:
        active = ' class="active"' if p == page else ""
        nav_links.append(f'<a href="{p}"{active}>{t["nav"][p]}</a>')
    return f'''<header class="site-header">
  <div class="brand">
    <a href="index.html">
      <span class="brand-title">Černá bižuterie</span>
      <span class="brand-sub">{t["brand_sub"]}</span>
    </a>
  </div>
  <div class="header-right">
    {lang_switch(t["lang"], page)}
    <button type="button" class="nav-toggle" aria-label="{t["menu"]}" aria-expanded="false">☰</button>
  </div>
  <nav class="site-nav" id="site-nav">
{chr(10).join(nav_links)}
  </nav>
</header>'''


def footer(t: dict) -> str:
    return f'''<footer class="site-footer">
  <h3>{t["footer_h"]}</h3>
  <p>{t["footer_p1"]}</p>
  <p>{t["footer_p2"]}</p>
  <p>{t["footer_p3"]}</p>
</footer>

<dialog id="lightbox" class="lightbox">
  <form method="dialog"><button class="lb-close" aria-label="{t["close"]}">×</button></form>
  <img id="lb-img" alt="" />
  <p id="lb-cap"></p>
</dialog>
<script src="../lang.js"></script>
<script src="../script.js"></script>'''


def page_shell(t: dict, page: str, title: str, main: str) -> str:
    return f'''<!DOCTYPE html>
<html lang="{t["lang"]}">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="description" content="{t["meta_desc"]}" />
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="../styles.css" />
</head>
<body>
{header(t, page)}
<main class="page">
{main}
</main>

{footer(t)}
</body>
</html>
'''


def build_index(t):
    main = f'''<section class="hero">
  <p class="hero-tagline">{t["tagline"]}</p>
  <h1>{t["home_h1"]}</h1>
  <p class="lede">{t["home_lede"]}</p>
  <p class="hero-actions"><a class="btn" href="vyrobky.html">{t["home_cta"]}</a></p>
  <figure class="hero-fig">
    <img src="../images/nejfoto.jpg" alt="{t["home_img_alt"]}" width="720" />
  </figure>
</section>'''
    return page_shell(t, "index.html", t["home_title"], main)


def build_vyrobky(t):
    blocks = [f'<h1>{t["vyrobky_h1"]}</h1>', f'<p class="intro">{t["vyrobky_intro"]}</p>']
    for cs_title, items in VYROBKY_SECTIONS:
        title = t["sections"].get(cs_title, cs_title)
        blocks.append(f"<h2>{title}</h2>")
        blocks.append('<div class="gallery">')
        for it in items:
            cap = f'{t["pattern"]} {it["pattern"]}'
            caption = f'{t["pattern"]}: {it["pattern"]}, {t["price"]}: {it["price"]}'
            full = "../" + it["full"]
            thumb = "../" + it["thumb"]
            blocks.append(
                f'<a class="card" href="{full}" data-lightbox data-caption="{caption}">'
                f'<img src="{thumb}" alt="{t["pattern"]} {it["pattern"]}" loading="lazy" />'
                f'<span class="cap"><span class="pattern-label">{cap}</span>'
                f'<span class="price-badge">{it["price"]}</span></span></a>'
            )
        blocks.append("</div>")
    return page_shell(t, "vyrobky.html", t["vyrobky_title"], "\n".join(blocks))


def build_sklo(t):
    blocks = [
        f'<h1>{t["sklo_h1"]}</h1>',
        f'<p>{t["sklo_p1"]}</p>',
        f'<p>{t["sklo_p2"]}</p>',
    ]
    for i, (cs_h, full, thumb, label, price) in enumerate(BETLEMY):
        h = t["betlemy"][i]
        num = label.split()[-1]
        bet_name = f'{t["bet_label"]} {num}'
        caption = f'{t["pattern"]}: {bet_name}, {t["price"]}: {price}'
        blocks.append(f"<h2>{h}</h2>")
        blocks.append(
            f'<div class="gallery bet-gallery">'
            f'<a class="card" href="../{full}" data-lightbox data-caption="{caption}">'
            f'<img src="../{thumb}" alt="{bet_name}" loading="lazy" />'
            f'<span class="cap"><span class="price-badge">{price}</span></span></a></div>'
        )
    return page_shell(t, "sklo.html", t["sklo_title"], "\n".join(blocks))


def build_ceny(t):
    lis = "\n".join(f"  <li>{li}</li>" for li in t["ceny_li"])
    main = f'''<h1>{t["ceny_h1"]}</h1>
<p>{t["ceny_p"]}</p>
<ul class="terms">
{lis}
</ul>
<p>{t["ceny_orders"]}</p>'''
    return page_shell(t, "ceny.html", t["ceny_title"], main)


def build_historie(t):
    main = f'<h1>{t["hist_h1"]}</h1>\n<div class="prose">{t["hist_html"]}</div>'
    return page_shell(t, "historie.html", t["hist_title"], main)


def build_oceneni(t):
    main = f'''<h1>{t["ocen_h1"]}</h1>
<figure class="hero-fig">
  <a href="https://www.ceskatelevize.cz/ivysilani/1126666764-toulava-kamera/215562221500016/obsah/394995-cerna-bizuterie" target="_blank" rel="noopener">
    <img src="../images/toulavakamera.jpg" alt="{t["ocen_alt"]}" width="720" />
  </a>
  <figcaption>{t["ocen_cap"]}</figcaption>
</figure>
<figure class="hero-fig">
  <img src="../images/oceneni.jpg" alt="{t["ocen_img_alt"]}" width="720" />
</figure>'''
    return page_shell(t, "oceneni.html", t["ocen_title"], main)


def build_kontakt(t):
    main = f'''<h1>{t["kon_h1"]}</h1>
<div class="contact">
  <div>
    <h2>Stanislav Jiroš</h2>
    <p>Trpasličí 8<br>
    Jablonec nad Nisou<br>
    466&nbsp;04</p>
    <p>{t["kon_phone"]}: <a href="tel:+420723335058">+420&nbsp;723&nbsp;335&nbsp;058</a><br>
    {t["kon_email"]}: <a href="mailto:blackjet@centrum.cz">blackjet@centrum.cz</a><br>
    {t["kon_ico"]}: 14829550</p>
  </div>
  <div>
    <a href="../images/bizu/923.jpg" data-lightbox data-caption="{t["pattern"]}: 929">
      <img src="../images/bizu/923_t.jpg" alt="{t["kon_img_alt"]}" width="240" />
    </a>
  </div>
</div>'''
    return page_shell(t, "kontakt.html", t["kon_title"], main)


BUILDERS = {
    "index.html": build_index,
    "vyrobky.html": build_vyrobky,
    "sklo.html": build_sklo,
    "ceny.html": build_ceny,
    "historie.html": build_historie,
    "oceneni.html": build_oceneni,
    "kontakt.html": build_kontakt,
}

STYLES = r'''
:root {
  --bg: #080706;
  --bg-elev: #14110e;
  --bg-card: #1a1612;
  --cream: #f5ecd8;
  --cream-dim: #c9b896;
  --gold: #c2b280;
  --gold-bright: #e0d0a0;
  --gold-soft: #a8945c;
  --ink: #120f0c;
  --line: rgba(194, 178, 128, 0.32);
  --line-strong: rgba(194, 178, 128, 0.55);
  --shadow: 0 18px 50px rgba(0, 0, 0, 0.55);
  --radius: 12px;
  --max: 1040px;
  --serif: "Cormorant Garamond", "Palatino Linotype", Palatino, Georgia, serif;
  --sans: "Source Sans 3", "Segoe UI", system-ui, -apple-system, sans-serif;
}

*, *::before, *::after { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: var(--sans);
  background:
    radial-gradient(ellipse 120% 70% at 50% -10%, rgba(194, 178, 128, 0.09), transparent 55%),
    radial-gradient(ellipse at bottom, #12100c 0%, var(--bg) 60%);
  color: var(--cream);
  line-height: 1.6;
  min-height: 100vh;
  font-size: 1.02rem;
}
a { color: var(--gold); text-decoration-thickness: 1px; text-underline-offset: 3px; }
a:hover { color: var(--gold-bright); }
img { max-width: 100%; height: auto; display: block; }

/* —— Header / brand (large, dominant) —— */
.site-header {
  position: sticky; top: 0; z-index: 30;
  background: rgba(8, 7, 6, 0.94);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--line);
  display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between;
  gap: 0.65rem 1rem; padding: 0.85rem 1.25rem 0.95rem;
  box-shadow: 0 8px 28px rgba(0,0,0,0.35);
}
.brand a { text-decoration: none; color: inherit; display: flex; flex-direction: column; gap: 0.12rem; }
.brand-title {
  font-family: var(--serif);
  font-size: clamp(1.85rem, 4.2vw, 2.75rem);
  line-height: 1.05;
  letter-spacing: 0.06em;
  text-transform: none;
  color: var(--cream);
  font-weight: 600;
  text-shadow: 0 2px 18px rgba(194, 178, 128, 0.18);
}
.brand-sub {
  font-family: var(--sans);
  font-size: clamp(0.78rem, 1.6vw, 0.95rem);
  color: var(--gold);
  letter-spacing: 0.14em;
  text-transform: uppercase;
  font-weight: 500;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-left: auto;
}
.nav-toggle {
  display: none; background: transparent; border: 1px solid var(--line);
  color: var(--cream); font-size: 1.25rem; padding: 0.35rem 0.6rem; border-radius: 6px;
  cursor: pointer;
}
.site-nav { display: flex; flex-wrap: wrap; gap: 0.2rem 1rem; width: 100%; }
.site-nav a {
  color: var(--cream-dim); text-decoration: none; font-size: 0.95rem;
  padding: 0.2rem 0; border-bottom: 2px solid transparent;
  letter-spacing: 0.02em;
}
.site-nav a:hover, .site-nav a.active {
  color: var(--cream); border-bottom-color: var(--gold);
}

/* Language switcher */
.lang-switch {
  display: flex;
  align-items: center;
  gap: 0.1rem;
  font-size: 0.78rem;
  letter-spacing: 0.08em;
  flex-shrink: 0;
  padding: 0.2rem 0.35rem;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: rgba(26, 22, 18, 0.7);
}
.lang-switch a {
  color: var(--cream-dim);
  text-decoration: none;
  padding: 0.22rem 0.42rem;
  border-radius: 999px;
  font-weight: 700;
}
.lang-switch a:hover { color: var(--cream); }
.lang-switch a.active {
  color: var(--ink);
  background: var(--gold);
}
.lang-switch .sep {
  color: var(--line-strong);
  user-select: none;
  padding: 0 0.02rem;
  font-weight: 400;
}

.page {
  max-width: var(--max); margin: 0 auto; padding: 1.75rem 1.15rem 3rem;
}
h1 {
  font-family: var(--serif);
  font-weight: 600;
  font-size: clamp(1.85rem, 4vw, 2.55rem);
  letter-spacing: 0.03em;
  margin: 0 0 1rem;
  color: var(--cream);
  border-bottom: 1px solid var(--line);
  padding-bottom: 0.55rem;
  line-height: 1.15;
}
h2 {
  font-family: var(--serif);
  font-size: 1.45rem; font-weight: 600; color: var(--gold);
  margin: 2rem 0 1rem; letter-spacing: 0.03em;
}
.lede, .intro, .prose p { color: var(--cream-dim); }
.lede { font-size: 1.12rem; max-width: 40rem; line-height: 1.65; }

/* Hero */
.hero { text-align: center; padding-top: 0.5rem; }
.hero-tagline {
  font-family: var(--sans);
  font-size: 0.82rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--gold);
  margin: 0 0 0.75rem;
}
.hero h1 {
  border: none;
  font-size: clamp(2.4rem, 6vw, 3.6rem);
  margin-bottom: 0.85rem;
  text-shadow: 0 4px 30px rgba(0,0,0,0.45);
}
.hero .lede { margin: 0 auto 1.25rem; text-align: center; }
.hero-actions { margin: 0 0 1.75rem; }
.btn {
  display: inline-block;
  font-family: var(--sans);
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-size: 0.82rem;
  text-decoration: none;
  color: var(--ink) !important;
  background: linear-gradient(180deg, var(--gold-bright), var(--gold));
  padding: 0.75rem 1.5rem;
  border-radius: 999px;
  border: 1px solid var(--gold-soft);
  box-shadow: 0 8px 24px rgba(194, 178, 128, 0.25);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(194, 178, 128, 0.35);
  color: var(--ink) !important;
}
.hero-fig { margin: 1.5rem auto; text-align: center; max-width: 720px; }
.hero-fig img {
  margin: 0 auto; border-radius: var(--radius);
  box-shadow: var(--shadow);
  border: 1px solid var(--line-strong);
}
.hero-fig figcaption { color: var(--cream-dim); margin-top: 0.85rem; font-size: 0.98rem; }

/* Gallery cards */
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(168px, 1fr));
  gap: 1.15rem;
}
.card {
  background: var(--bg-card);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  overflow: hidden;
  text-decoration: none;
  color: inherit;
  display: flex; flex-direction: column;
  transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
  box-shadow: 0 8px 22px rgba(0,0,0,0.28);
}
.card:hover {
  transform: translateY(-4px);
  border-color: var(--gold);
  box-shadow: 0 16px 36px rgba(0,0,0,0.45), 0 0 0 1px rgba(194,178,128,0.2);
  color: inherit;
}
.card img {
  width: 100%; aspect-ratio: 1; object-fit: cover; background: #000;
  transition: transform 0.35s ease;
}
.card:hover img { transform: scale(1.04); }
.card .cap {
  display: flex; flex-direction: column; align-items: center; gap: 0.35rem;
  padding: 0.7rem 0.65rem 0.85rem; font-size: 0.84rem;
  color: var(--cream-dim); text-align: center; line-height: 1.35;
}
.pattern-label { letter-spacing: 0.02em; }
.price-badge {
  display: inline-block;
  font-weight: 700;
  color: var(--ink);
  background: linear-gradient(180deg, var(--gold-bright), var(--gold));
  padding: 0.22rem 0.65rem;
  border-radius: 999px;
  font-size: 0.88rem;
  letter-spacing: 0.02em;
  box-shadow: 0 2px 8px rgba(0,0,0,0.25);
}
.bet-gallery { max-width: 300px; }

.prose { color: var(--cream-dim); max-width: 42rem; margin: 0 auto; }
.prose p { margin: 1rem 0; }
.prose p[style*="center"] { text-align: center; }
.prose img {
  margin: 0.5rem auto; border-radius: 8px; border: 1px solid var(--line);
  box-shadow: 0 8px 24px rgba(0,0,0,0.35);
}

.terms { color: var(--cream-dim); padding-left: 1.2rem; }
.terms li { margin: 0.55rem 0; }
.terms strong { color: var(--cream); }

.contact {
  display: grid; gap: 1.75rem;
  grid-template-columns: 1fr;
  align-items: start;
}
@media (min-width: 560px) {
  .contact { grid-template-columns: 1fr auto; }
}
.contact h2 {
  margin-top: 0; color: var(--cream);
  font-family: var(--serif); font-size: 1.6rem;
}
.contact img {
  border-radius: var(--radius); border: 1px solid var(--line);
  box-shadow: var(--shadow);
}

.site-footer {
  max-width: var(--max); margin: 0 auto 2.5rem; padding: 1.5rem 1.15rem;
  border-top: 1px solid var(--line); color: var(--cream-dim); font-size: 0.92rem;
}
.site-footer h3 {
  margin: 0 0 0.7rem; font-size: 1rem; color: var(--gold);
  font-weight: 600; letter-spacing: 0.04em;
  font-family: var(--serif);
}
.site-footer p { margin: 0.45rem 0; }

.lightbox {
  border: 1px solid var(--line-strong);
  border-radius: 14px;
  padding: 1.15rem;
  background: #0a0908;
  color: var(--cream);
  max-width: min(94vw, 820px);
  box-shadow: 0 30px 80px rgba(0,0,0,0.7);
}
.lightbox::backdrop { background: rgba(0,0,0,0.82); }
.lightbox img { max-height: 78vh; margin: 0 auto; border-radius: 6px; }
.lightbox p { text-align: center; margin: 0.85rem 0 0; color: var(--cream-dim); }
.lb-close {
  position: absolute; top: 0.4rem; right: 0.6rem;
  background: transparent; border: none; color: var(--cream);
  font-size: 1.7rem; cursor: pointer; line-height: 1;
}
.lightbox { position: relative; }

@media (max-width: 720px) {
  .site-header { padding: 0.7rem 0.9rem 0.8rem; }
  .brand-title { font-size: clamp(1.55rem, 7vw, 2.1rem); }
  .nav-toggle { display: inline-block; }
  .site-nav {
    display: none; width: 100%; flex-direction: column; gap: 0.4rem;
    padding: 0.55rem 0 0.35rem;
  }
  .site-nav.open { display: flex; }
  .gallery { grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 0.85rem; }
  .header-right { order: 2; }
  .nav-toggle { order: 3; }
  .site-nav { order: 4; }
  .lang-switch { font-size: 0.72rem; }
}
'''

ROOT_INDEX = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="description" content="Stanislav Jiroš — Černá bižuterie. Traditional Jablonec black glass jewellery." />
<title>Černá bižuterie</title>
<script>document.documentElement.setAttribute('data-cerna-redirect','1');</script>
<script src="lang.js"></script>
<style>
  body{margin:0;background:#080706;color:#f5ecd8;font-family:system-ui,sans-serif;display:flex;min-height:100vh;align-items:center;justify-content:center}
  a{color:#c2b280}
  .box{text-align:center;padding:2rem}
</style>
</head>
<body>
<div class="box">
  <p>Černá bižuterie</p>
  <p>
    <a href="cs/index.html">Česky</a> ·
    <a href="en/index.html">English</a> ·
    <a href="fr/index.html">Français</a> ·
    <a href="de/index.html">Deutsch</a>
  </p>
</div>
</body>
</html>
'''

README = '''# Černá bižuterie — Stanislav Jiroš

Multilingual static remake of [cernabizuterie.cz](http://www.cernabizuterie.cz) for Keith Dudman.

- Languages: Czech (cs), English (en), French (fr), German (de)
- Browser-language auto-detect + `localStorage` preference (`cerna-lang`)
- Shared design: black / gold Victorian-glass heritage look
- Product prices +15 %, rounded to 10 Kč (unchanged in this update)

Live: https://lillydog2468.github.io/cernabizuterie/
'''


def main():
    # Write shared assets
    (ROOT / "styles.css").write_text(STYLES.lstrip("\n"), encoding="utf-8")
    (ROOT / "index.html").write_text(ROOT_INDEX, encoding="utf-8")
    (ROOT / "README.md").write_text(README, encoding="utf-8")

    for lang in LANGS:
        d = ROOT / lang
        d.mkdir(exist_ok=True)
        t = T[lang]
        for page, builder in BUILDERS.items():
            html = builder(t)
            (d / page).write_text(html, encoding="utf-8")
            print(f"wrote {lang}/{page}")

    # Remove old root-level page copies (now live under /cs/ etc.)
    for name in PAGES:
        if name == "index.html":
            continue  # root redirector stays
        p = ROOT / name
        if p.exists():
            p.unlink()
            print(f"removed root {name}")

    print("done")


if __name__ == "__main__":
    main()
