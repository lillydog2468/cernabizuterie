/**
 * Černá bižuterie — test order form (Google Apps Script web app).
 *
 * Deploy: see README-cs-en.md in this folder.
 * Script Properties (Project settings → Script properties):
 *   OWNER_EMAIL     where the Czech shop notice is sent.
 *                   If unset, mail goes to bananas4beading@icloud.com (Keith, test mode).
 *   ACCOUNT_NAME    bank account name. Leave empty until the real details exist.
 *   ACCOUNT_NUMBER  bank account number. Leave empty until the real details exist.
 *   IBAN            IBAN. Leave empty until the real details exist.
 *   SHEET_ID        optional Google Sheet id. If empty, orders are not written to a sheet.
 *
 * The script never fills in sample account numbers. Missing bank fields are
 * replaced with the sentence "TEST – bankovní údaje doplníme".
 */

var TEST_BANK_LINE = 'TEST – bankovní údaje doplníme';
var TEST_OWNER_EMAIL = 'bananas4beading@icloud.com';
var TIMEZONE = 'Europe/Prague';

/** Same ten products as paypal-test.html / the start of cs/vyrobky.html, in page order. */
var CATALOG = {
  '965': { label: 'vzor 965', price: '370,- Kč' },
  '1358': { label: 'vzor 1358', price: '420,- Kč' },
  '968': { label: 'vzor 968', price: '350,- Kč' },
  '995': { label: 'vzor 995', price: '300,- Kč' },
  '1038': { label: 'vzor 1038', price: '300,- Kč' },
  '998': { label: 'vzor 998', price: '300,- Kč' },
  '1034': { label: 'vzor 1034', price: '350,- Kč' },
  '723': { label: 'vzor 723', price: '300,- Kč' },
  '540': { label: 'vzor 540', price: '200,- Kč' },
  '1087': { label: 'vzor 1087', price: '550,- Kč' }
};

function doGet() {
  return json_({
    ok: true,
    service: 'cernabizuterie-order-test',
    connected: true
  });
}

function doPost(e) {
  try {
    var data = readBody_(e);
    var result = handleOrder_(data);
    return json_(result);
  } catch (err) {
    return json_({ ok: false, error: 'server' });
  }
}

function handleOrder_(data) {
  data = data || {};

  if (String(data.company_website || '').trim()) {
    return { ok: true, ignored: true, orderNumber: 'TEST-NOT-SENT' };
  }

  var email = String(data.email || '').trim();
  var item = String(data.item || '').trim();
  var name = String(data.name || '').trim();
  var message = String(data.message || '').trim();

  if (!isEmail_(email)) return { ok: false, error: 'email' };
  if (!CATALOG[item] && item !== 'other') return { ok: false, error: 'item' };
  if (name.length > 200) return { ok: false, error: 'name' };
  if (message.length > 4000) return { ok: false, error: 'message' };
  if (!allow_(email)) return { ok: false, error: 'rate' };

  var product = CATALOG[item] || { label: 'jiné / other', price: 'dle dohody' };
  var issued = nextOrderNumber_();
  var messageCs = translateToCzech_(message);
  var bank = bankDetails_();

  var customerBody = customerMail_(issued, product, bank);
  var ownerBody = ownerMail_(issued, product, email, name, message, messageCs);

  var props = PropertiesService.getScriptProperties();
  var owner = String(props.getProperty('OWNER_EMAIL') || '').trim() || TEST_OWNER_EMAIL;

  MailApp.sendEmail(email, 'Order ' + issued.orderNumber + ' — Černá bižuterie', customerBody);
  MailApp.sendEmail(owner, 'Nová objednávka ' + issued.orderNumber, ownerBody);
  appendSheet_(props, issued, product, email, name, message, messageCs);

  return {
    ok: true,
    orderNumber: issued.orderNumber,
    variableSymbol: issued.variableSymbol,
    bankReady: bank.ready
  };
}

function readBody_(e) {
  if (e && e.postData && e.postData.contents) {
    try {
      return JSON.parse(e.postData.contents);
    } catch (ignore) {}
  }
  return (e && e.parameter) || {};
}

function isEmail_(value) {
  if (!value || value.length > 200) return false;
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

/** At most 5 orders per email address per hour, and 30 orders per hour in total. */
function allow_(email) {
  var cache = CacheService.getScriptCache();
  var globalKey = 'rl_global';
  var emailKey = 'rl_' + email.toLowerCase();
  var globalCount = Number(cache.get(globalKey) || '0');
  var emailCount = Number(cache.get(emailKey) || '0');
  if (globalCount >= 30 || emailCount >= 5) return false;
  cache.put(globalKey, String(globalCount + 1), 3600);
  cache.put(emailKey, String(emailCount + 1), 3600);
  return true;
}

function nextOrderNumber_() {
  var lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    var props = PropertiesService.getScriptProperties();
    var day = Utilities.formatDate(new Date(), TIMEZONE, 'yyyyMMdd');
    var key = 'SEQ_' + day;
    var n = Number(props.getProperty(key) || '0') + 1;
    props.setProperty(key, String(n));
    var seq = ('000' + n).slice(-3);
    var orderNumber = 'CB-' + day + '-' + seq;
    return {
      orderNumber: orderNumber,
      variableSymbol: orderNumber.replace(/\D/g, '')
    };
  } finally {
    lock.releaseLock();
  }
}

function bankDetails_() {
  var props = PropertiesService.getScriptProperties();
  var name = String(props.getProperty('ACCOUNT_NAME') || '').trim();
  var number = String(props.getProperty('ACCOUNT_NUMBER') || '').trim();
  var iban = String(props.getProperty('IBAN') || '').trim();
  return {
    ready: !!(name && number && iban),
    name: name,
    number: number,
    iban: iban
  };
}

function bankValue_(value) {
  return value ? value : TEST_BANK_LINE;
}

function translateToCzech_(message) {
  if (!message) return '';
  try {
    return LanguageApp.translate(message, 'en', 'cs');
  } catch (ignore) {
    return '(překlad se nepodařil)';
  }
}

function customerMail_(issued, product, bank) {
  var lines = [
    'Thank you for your order from Černá bižuterie.',
    'Děkujeme za objednávku.',
    '',
    'Order number / Číslo objednávky: ' + issued.orderNumber,
    'Item / Výrobek: ' + product.label,
    'Amount / Částka: ' + product.price,
    '',
    'Please pay by bank transfer.',
    'Account name: ' + bankValue_(bank.name),
    'Account number: ' + bankValue_(bank.number),
    'IBAN: ' + bankValue_(bank.iban),
    'Variable symbol / Variabilní symbol: ' + issued.variableSymbol,
    'Amount / Částka: ' + product.price,
    'Please put the order number in the payment message.',
    'Do zprávy pro příjemce uveďte číslo objednávky.',
    '',
    'This message was sent automatically. / Tato zpráva byla odeslána automaticky.'
  ];
  return lines.join('\n');
}

function ownerMail_(issued, product, email, name, message, messageCs) {
  var lines = [
    'Nová objednávka (zkouška formuláře).',
    '',
    'Číslo objednávky: ' + issued.orderNumber,
    'Variabilní symbol: ' + issued.variableSymbol,
    'Výrobek: ' + product.label,
    'Cena: ' + product.price,
    'E-mail zákazníka: ' + email,
    'Jméno: ' + (name || '—'),
    '',
    'Zpráva zákazníka (překlad do češtiny):',
    messageCs || '—',
    '',
    'Původní zpráva (anglicky):',
    message || '—'
  ];
  return lines.join('\n');
}

function appendSheet_(props, issued, product, email, name, message, messageCs) {
  var sheetId = String(props.getProperty('SHEET_ID') || '').trim();
  if (!sheetId) return;
  try {
    var sheet = SpreadsheetApp.openById(sheetId).getSheets()[0];
    sheet.appendRow([
      Utilities.formatDate(new Date(), TIMEZONE, 'yyyy-MM-dd HH:mm:ss'),
      issued.orderNumber,
      issued.variableSymbol,
      product.label,
      product.price,
      email,
      name,
      message,
      messageCs
    ]);
  } catch (ignore) {}
}

function json_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
