/**
 * Černá bižuterie — expression of interest (Google Apps Script web app).
 *
 * Deploy: see README-cs-en.md in this folder.
 * Script Properties (Project settings → Script properties):
 *   OWNER_EMAILS  comma-separated recipients. If unset, mail goes to
 *                 bananas4beading@icloud.com,blackjet@centrum.cz
 *   SHEET_ID      optional Google Sheet id. If empty, nothing is written to a sheet.
 *
 * A post with test === "keith" is sent only to bananas4beading@icloud.com
 * and the subject starts with [TEST]. The visitor is never emailed.
 */

var DEFAULT_OWNERS = 'bananas4beading@icloud.com,blackjet@centrum.cz';
var TEST_ONLY = 'bananas4beading@icloud.com';

var CATALOG = [
  { id: "965", price: "370,- Kč", sectionCs: "Přívěsy", sectionEn: "Pendants" },
  { id: "1358", price: "420,- Kč", sectionCs: "Přívěsy", sectionEn: "Pendants" },
  { id: "968", price: "350,- Kč", sectionCs: "Přívěsy", sectionEn: "Pendants" },
  { id: "995", price: "300,- Kč", sectionCs: "Přívěsy", sectionEn: "Pendants" },
  { id: "1038", price: "300,- Kč", sectionCs: "Přívěsy", sectionEn: "Pendants" },
  { id: "998", price: "300,- Kč", sectionCs: "Přívěsy", sectionEn: "Pendants" },
  { id: "1034", price: "350,- Kč", sectionCs: "Přívěsy", sectionEn: "Pendants" },
  { id: "723", price: "300,- Kč", sectionCs: "Přívěsy", sectionEn: "Pendants" },
  { id: "540", price: "200,- Kč", sectionCs: "Přívěsy", sectionEn: "Pendants" },
  { id: "1087", price: "550,- Kč", sectionCs: "Přívěsy", sectionEn: "Pendants" },
  { id: "1082", price: "310,- Kč", sectionCs: "Přívěsy", sectionEn: "Pendants" },
  { id: "1336", price: "400,- Kč", sectionCs: "Přívěsy", sectionEn: "Pendants" },
  { id: "1357", price: "600,- Kč", sectionCs: "Přívěsy", sectionEn: "Pendants" },
  { id: "1320", price: "500,- Kč", sectionCs: "Přívěsy", sectionEn: "Pendants" },
  { id: "1157", price: "600,- Kč", sectionCs: "Přívěsy", sectionEn: "Pendants" },
  { id: "470", price: "200,- Kč", sectionCs: "Přívěsy", sectionEn: "Pendants" },
  { id: "1326", price: "500,- Kč", sectionCs: "Přívěsy", sectionEn: "Pendants" },
  { id: "817", price: "200,- Kč", sectionCs: "Náušnice", sectionEn: "Earrings" },
  { id: "1054", price: "300,- Kč", sectionCs: "Náušnice", sectionEn: "Earrings" },
  { id: "850", price: "400,- Kč", sectionCs: "Náušnice", sectionEn: "Earrings" },
  { id: "1006", price: "200,- Kč", sectionCs: "Náušnice", sectionEn: "Earrings" },
  { id: "897", price: "250,- Kč", sectionCs: "Náušnice", sectionEn: "Earrings" },
  { id: "887", price: "250,- Kč", sectionCs: "Náušnice", sectionEn: "Earrings" },
  { id: "1051", price: "400,- Kč", sectionCs: "Náušnice", sectionEn: "Earrings" },
  { id: "286", price: "250,- Kč", sectionCs: "Náušnice", sectionEn: "Earrings" },
  { id: "706", price: "250,- Kč", sectionCs: "Náušnice", sectionEn: "Earrings" },
  { id: "1047", price: "400,- Kč", sectionCs: "Náušnice", sectionEn: "Earrings" },
  { id: "929", price: "350,- Kč", sectionCs: "Náušnice", sectionEn: "Earrings" },
  { id: "892", price: "380,- Kč", sectionCs: "Náušnice", sectionEn: "Earrings" },
  { id: "848", price: "290,- Kč", sectionCs: "Náušnice", sectionEn: "Earrings" },
  { id: "813", price: "350,- Kč", sectionCs: "Náušnice", sectionEn: "Earrings" },
  { id: "883", price: "500,- Kč", sectionCs: "Náušnice", sectionEn: "Earrings" },
  { id: "1026", price: "500,- Kč", sectionCs: "Sametky", sectionEn: "Velvet chokers" },
  { id: "1096", price: "450,- Kč", sectionCs: "Sametky", sectionEn: "Velvet chokers" },
  { id: "1089", price: "500,- Kč", sectionCs: "Sametky", sectionEn: "Velvet chokers" },
  { id: "1090", price: "500,- Kč", sectionCs: "Sametky", sectionEn: "Velvet chokers" },
  { id: "1074", price: "800,- Kč", sectionCs: "Brože", sectionEn: "Brooches" },
  { id: "1073", price: "450,- Kč", sectionCs: "Brože", sectionEn: "Brooches" },
  { id: "518", price: "250,- Kč", sectionCs: "Brože", sectionEn: "Brooches" },
  { id: "776", price: "350,- Kč", sectionCs: "Brože", sectionEn: "Brooches" },
  { id: "662", price: "400,- Kč", sectionCs: "Brože", sectionEn: "Brooches" },
  { id: "512", price: "290,- Kč", sectionCs: "Brože", sectionEn: "Brooches" },
  { id: "1067", price: "400,- Kč", sectionCs: "Brože", sectionEn: "Brooches" },
  { id: "710", price: "350,- Kč", sectionCs: "Brože", sectionEn: "Brooches" },
  { id: "1188", price: "450,- Kč", sectionCs: "Brože", sectionEn: "Brooches" },
  { id: "1291", price: "700,- Kč", sectionCs: "Brože", sectionEn: "Brooches" },
  { id: "1321", price: "750,- Kč", sectionCs: "Brože", sectionEn: "Brooches" },
  { id: "1336 B", price: "400,- Kč", sectionCs: "Brože", sectionEn: "Brooches" },
  { id: "1344", price: "350,- Kč", sectionCs: "Brože", sectionEn: "Brooches" },
  { id: "926", price: "700,- Kč", sectionCs: "Spony", sectionEn: "Clasps" },
  { id: "1331", price: "800,- Kč", sectionCs: "Spony", sectionEn: "Clasps" },
  { id: "1131", price: "450,- Kč", sectionCs: "Spony", sectionEn: "Clasps" },
  { id: "1130", price: "550,- Kč", sectionCs: "Spony", sectionEn: "Clasps" },
  { id: "680", price: "800,- Kč", sectionCs: "Spony", sectionEn: "Clasps" },
  { id: "962", price: "1000,- Kč", sectionCs: "Soupravy", sectionEn: "Sets" },
  { id: "411", price: "400,- Kč", sectionCs: "Soupravy", sectionEn: "Sets" },
  { id: "352", price: "1500,- Kč", sectionCs: "Soupravy", sectionEn: "Sets" },
  { id: "882", price: "1000,- Kč", sectionCs: "Soupravy", sectionEn: "Sets" }
];

var COUNTRIES = {
  "CZ": { cs: "Česko", en: "Czechia" },
  "SK": { cs: "Slovensko", en: "Slovakia" },
  "PL": { cs: "Polsko", en: "Poland" },
  "DE": { cs: "Německo", en: "Germany" },
  "AT": { cs: "Rakousko", en: "Austria" },
  "HU": { cs: "Maďarsko", en: "Hungary" },
  "GB": { cs: "Spojené království", en: "United Kingdom" },
  "IE": { cs: "Irsko", en: "Ireland" },
  "FR": { cs: "Francie", en: "France" },
  "BE": { cs: "Belgie", en: "Belgium" },
  "NL": { cs: "Nizozemsko", en: "Netherlands" },
  "LU": { cs: "Lucembursko", en: "Luxembourg" },
  "CH": { cs: "Švýcarsko", en: "Switzerland" },
  "IT": { cs: "Itálie", en: "Italy" },
  "ES": { cs: "Španělsko", en: "Spain" },
  "PT": { cs: "Portugalsko", en: "Portugal" },
  "DK": { cs: "Dánsko", en: "Denmark" },
  "SE": { cs: "Švédsko", en: "Sweden" },
  "NO": { cs: "Norsko", en: "Norway" },
  "FI": { cs: "Finsko", en: "Finland" },
  "IS": { cs: "Island", en: "Iceland" },
  "EE": { cs: "Estonsko", en: "Estonia" },
  "LV": { cs: "Lotyšsko", en: "Latvia" },
  "LT": { cs: "Litva", en: "Lithuania" },
  "SI": { cs: "Slovinsko", en: "Slovenia" },
  "HR": { cs: "Chorvatsko", en: "Croatia" },
  "RO": { cs: "Rumunsko", en: "Romania" },
  "BG": { cs: "Bulharsko", en: "Bulgaria" },
  "GR": { cs: "Řecko", en: "Greece" },
  "CY": { cs: "Kypr", en: "Cyprus" },
  "MT": { cs: "Malta", en: "Malta" },
  "UA": { cs: "Ukrajina", en: "Ukraine" },
  "RS": { cs: "Srbsko", en: "Serbia" },
  "BA": { cs: "Bosna a Hercegovina", en: "Bosnia and Herzegovina" },
  "US": { cs: "Spojené státy", en: "United States" },
  "CA": { cs: "Kanada", en: "Canada" },
  "MX": { cs: "Mexiko", en: "Mexico" },
  "BR": { cs: "Brazílie", en: "Brazil" },
  "AR": { cs: "Argentina", en: "Argentina" },
  "CL": { cs: "Chile", en: "Chile" },
  "AU": { cs: "Austrálie", en: "Australia" },
  "NZ": { cs: "Nový Zéland", en: "New Zealand" },
  "JP": { cs: "Japonsko", en: "Japan" },
  "KR": { cs: "Jižní Korea", en: "South Korea" },
  "CN": { cs: "Čína", en: "China" },
  "TW": { cs: "Tchaj-wan", en: "Taiwan" },
  "HK": { cs: "Hongkong", en: "Hong Kong" },
  "SG": { cs: "Singapur", en: "Singapore" },
  "IN": { cs: "Indie", en: "India" },
  "AE": { cs: "Spojené arabské emiráty", en: "United Arab Emirates" },
  "IL": { cs: "Izrael", en: "Israel" },
  "ZA": { cs: "Jihoafrická republika", en: "South Africa" },
  "TR": { cs: "Turecko", en: "Turkey" },
  "OTHER": { cs: "Jiná země", en: "Other country" }
};

var LANG_NAMES = {
  cs: { cs: 'čeština', en: 'Czech' },
  en: { cs: 'angličtina', en: 'English' },
  fr: { cs: 'francouzština', en: 'French' },
  de: { cs: 'němčina', en: 'German' }
};

function doGet() {
  return json_({ ok: true, service: 'cernabizuterie-interest', connected: true });
}

function doPost(e) {
  try {
    return json_(handle_(readBody_(e)));
  } catch (err) {
    return json_({ ok: false, error: 'server' });
  }
}

function handle_(data) {
  data = data || {};
  if (String(data.company_website || '').trim()) {
    return { ok: true, ignored: true };
  }

  var name = oneLine_(data.name);
  var email = String(data.email || '').trim();
  var country = String(data.country || '').trim();
  var region = oneLine_(data.region);
  var message = String(data.message || '').replace(/\r\n/g, '\n').trim();
  var language = String(data.language || '').trim();
  var testKeith = String(data.test || '') === 'keith';
  var ids = productIds_(data.products);

  if (!name || name.length > 200) return { ok: false, error: 'name' };
  if (!isEmail_(email)) return { ok: false, error: 'email' };
  if (!COUNTRIES[country]) return { ok: false, error: 'country' };
  if (!region || region.length > 200) return { ok: false, error: 'region' };
  if (message.length > 4000) return { ok: false, error: 'message' };
  if (language !== 'cs' && language !== 'en' && language !== 'fr' && language !== 'de') {
    return { ok: false, error: 'language' };
  }

  var chosen = resolveProducts_(ids);
  if (!chosen.length) return { ok: false, error: 'products' };
  if (!allow_(email)) return { ok: false, error: 'rate' };

  var messageCs = translateToCzech_(message, language);
  var props = PropertiesService.getScriptProperties();
  var owners = String(props.getProperty('OWNER_EMAILS') || '').trim() || DEFAULT_OWNERS;
  if (testKeith) owners = TEST_ONLY;

  var subject = 'Zájem o šperky – ' + COUNTRIES[country].cs + ' – ' + name;
  if (testKeith) subject = '[TEST] ' + subject;

  MailApp.sendEmail({
    to: owners,
    replyTo: email,
    subject: subject,
    body: mailBody_(name, email, country, region, language, chosen, message, messageCs)
  });
  appendSheet_(props, name, email, country, region, language, chosen, message, messageCs, testKeith);
  return { ok: true };
}

function readBody_(e) {
  if (e && e.postData && e.postData.contents) {
    try { return JSON.parse(e.postData.contents); } catch (ignore) {}
  }
  return (e && e.parameter) || {};
}

function productIds_(raw) {
  if (Object.prototype.toString.call(raw) === '[object Array]') return raw;
  if (typeof raw === 'string') return raw.split(',');
  return [];
}

function resolveProducts_(ids) {
  var byId = {};
  for (var i = 0; i < CATALOG.length; i++) byId[CATALOG[i].id] = CATALOG[i];
  var seen = {};
  var chosen = [];
  for (var j = 0; j < ids.length && chosen.length < 80; j++) {
    var id = String(ids[j] || '').trim();
    if (!id || seen[id]) continue;
    seen[id] = true;
    if (id === 'general') {
      chosen.push({ id: 'general' });
    } else if (byId[id]) {
      chosen.push(byId[id]);
    }
  }
  return chosen;
}

function isEmail_(value) {
  if (!value || value.length > 200) return false;
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

function allow_(email) {
  var cache = CacheService.getScriptCache();
  var globalKey = 'interest_rl_global';
  var emailKey = 'interest_rl_' + email.toLowerCase();
  var globalCount = Number(cache.get(globalKey) || '0');
  var emailCount = Number(cache.get(emailKey) || '0');
  if (globalCount >= 30 || emailCount >= 5) return false;
  cache.put(globalKey, String(globalCount + 1), 3600);
  cache.put(emailKey, String(emailCount + 1), 3600);
  return true;
}

function translateToCzech_(message, language) {
  if (!message) return '';
  if (language === 'cs') return message;
  var source = { en: 'en', fr: 'fr', de: 'de' }[language] || 'en';
  try {
    return LanguageApp.translate(message, source, 'cs');
  } catch (ignore) {
    return '(překlad se nepodařil)';
  }
}

function linesFor_(chosen, word) {
  var lines = [];
  for (var i = 0; i < chosen.length; i++) {
    var item = chosen[i];
    if (item.id === 'general') {
      lines.push(word === 'vzor'
        ? '- obecný zájem / vše'
        : '- general interest / everything');
    } else {
      lines.push('- ' + word + ' ' + item.id + ', ' + item.price);
    }
  }
  return lines.join('\n');
}

function mailBody_(name, email, country, region, language, chosen, message, messageCs) {
  var place = COUNTRIES[country];
  var lang = LANG_NAMES[language];
  var cs = [
    'Nový zájem o zasílání šperků.',
    '',
    'Jméno: ' + name,
    'E-mail: ' + email,
    'Jazyk formuláře: ' + lang.cs + ' (' + language + ')',
    'Země: ' + place.cs,
    'Město / region: ' + region,
    'Výrobky:',
    linesFor_(chosen, 'vzor'),
    '',
    'Zpráva (překlad do češtiny):',
    messageCs || '—',
    '',
    'Původní zpráva:',
    message || '—'
  ];
  var en = [
    'New interest in jewellery by post.',
    '',
    'Name: ' + name,
    'Email: ' + email,
    'Form language: ' + lang.en + ' (' + language + ')',
    'Country: ' + place.en,
    'Town / region: ' + region,
    'Products:',
    linesFor_(chosen, 'pattern'),
    '',
    'Message (original):',
    message || '—'
  ];
  return cs.join('\n') + '\n\n---\n\n' + en.join('\n');
}

function appendSheet_(props, name, email, country, region, language, chosen, message, messageCs, testKeith) {
  var sheetId = String(props.getProperty('SHEET_ID') || '').trim();
  if (!sheetId) return;
  try {
    var sheet = SpreadsheetApp.openById(sheetId).getSheets()[0];
    var list = [];
    for (var i = 0; i < chosen.length; i++) {
      list.push(chosen[i].id === 'general' ? 'general' : chosen[i].id + ' ' + chosen[i].price);
    }
    sheet.appendRow([
      Utilities.formatDate(new Date(), 'Europe/Prague', 'yyyy-MM-dd HH:mm:ss'),
      language,
      name,
      email,
      COUNTRIES[country].cs,
      region,
      list.join('; '),
      message,
      messageCs,
      testKeith ? 'keith' : ''
    ]);
  } catch (ignore) {}
}

function oneLine_(value) {
  return String(value || '').replace(/[\r\n]+/g, ' ').trim();
}

function json_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
