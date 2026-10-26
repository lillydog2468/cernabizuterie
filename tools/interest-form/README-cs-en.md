# Zájem o šperky — nasazení / Interest form — deploy

Stránky `cs/zajem.html`, `en/interest.html`, `fr/interet.html` a `de/interesse.html` jen sbírají zájem. Dokud v nich není adresa webové aplikace, **nic se neposílá**. Zákazníkovi se e-mail neposílá nikdy.

The pages `cs/zajem.html`, `en/interest.html`, `fr/interet.html` and `de/interesse.html` only collect interest. Until they contain the web-app address, **nothing is sent**. The visitor is never emailed.

Když je vlastnost `OWNER_EMAILS` prázdná, pošta jde na `bananas4beading@icloud.com,blackjet@centrum.cz`. Odeslání s `test` rovno `keith` jde jen Keithovi a předmět začíná `[TEST]`.

If `OWNER_EMAILS` is empty, mail goes to `bananas4beading@icloud.com,blackjet@centrum.cz`. A post whose `test` field is `keith` goes only to Keith and the subject starts with `[TEST]`.

---

## Česky — krok za krokem

1. Otevřete [https://script.google.com](https://script.google.com) a přihlaste se účtem Google, ze kterého mají odcházet e-maily.
2. **Nový projekt**. Nepoužívejte projekt objednávkového formuláře — toto je samostatný skript.
3. Smažte ukázkový kód. Vložte celý soubor `tools/interest-form/Code.gs`. Uložte.
4. **Nastavení projektu** (ozubené kolo) → **Vlastnosti skriptu**:
   - `OWNER_EMAILS` — nechte prázdné, pokud mají chodit oba výchozí příjemci. Jinak napište adresy oddělené čárkou.
   - `SHEET_ID` — volitelné. ID tabulky z adresy `https://docs.google.com/spreadsheets/d/TOTO-ID/edit`. Když je prázdné, tabulka se nepoužije.
5. **Nasadit → Nové nasazení**. Typ: **Webová aplikace**.
6. **Spouštět jako: Já**. **Kdo má přístup: Kdokoli**.
7. **Nasadit** a povolte odesílání e-mailu (a tabulku, pokud jste vyplnili `SHEET_ID`).
8. Zkopírujte adresu, která končí na `/exec`.
9. Ve všech čtyřech stránkách najděte `var INTEREST_ENDPOINT = "";` a vložte stejnou adresu mezi uvozovky. Uložte a publikujte web (větev `main`).
10. Pozdější úprava skriptu: **Nasadit → Spravovat nasazení → tužka → Nová verze → Nasadit**. Adresa zůstane stejná.

E-mail majitelům je česky a pod ním anglicky. Je v něm jméno, e-mail, jazyk formuláře, země, město nebo region, zvolené vzory s cenou a zpráva přeložená do češtiny i v originále. Předmět: `Zájem o šperky – [země] – [jméno]`.

## English — step by step

1. Open [https://script.google.com](https://script.google.com) and sign in with the Google account that should send the mail.
2. Choose **New project**. Do not reuse the order-form project — this script is separate.
3. Delete the sample function. Paste the whole file `tools/interest-form/Code.gs`. Save.
4. **Project settings** (gear) → **Script properties**:
   - `OWNER_EMAILS` — leave empty to use both default recipients. Otherwise type addresses separated by commas.
   - `SHEET_ID` — optional. The id in `https://docs.google.com/spreadsheets/d/THIS-ID/edit`. If empty, no spreadsheet is used.
5. **Deploy → New deployment**. Type: **Web app**.
6. **Execute as: Me**. **Who has access: Anyone**.
7. **Deploy** and approve sending email (and spreadsheets if you set `SHEET_ID`).
8. Copy the URL that ends in `/exec`.
9. In all four pages, find `var INTEREST_ENDPOINT = "";` and paste the same URL between the quotes. Save and publish the site (the `main` branch).
10. After later edits: **Deploy → Manage deployments → pencil → New version → Deploy**. The URL stays the same.

The owners’ email is Czech, with English underneath. It includes the name, email, which language the visitor used, country, town or region, the chosen pattern numbers and prices, and the message translated into Czech plus the original. Subject: `Zájem o šperky – [country] – [name]`.
