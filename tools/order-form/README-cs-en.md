# Objednávkový formulář — nasazení / Order form — deploy

Stránka `objednavka-test.html` je jen ukázka. Dokud v ní není adresa webové aplikace, **nic se neposílá**. E-maily začnou chodit až po krocích níže.

The page `objednavka-test.html` is only a demonstration. Until it contains the web-app address, **nothing is sent**. Mail starts only after the steps below.

Údaje o účtu (jméno, číslo, IBAN) se **nikde nepíšou do kódu**. Doplní se jen jako vlastnosti skriptu. Když chybí, v e-mailu je věta „TEST – bankovní údaje doplníme“.

Bank details are **not written in the code**. They are Script Properties only. If they are missing, the email says “TEST – bankovní údaje doplníme”.

Zkušební oznámení pro obchod jde na `bananas4beading@icloud.com` (Keith), ne na adresu majitelů. To se změní až vlastností `OWNER_EMAIL`.

Shop notices go to `bananas4beading@icloud.com` (Keith), not to the owners, until `OWNER_EMAIL` is changed.

---

## Česky — krok za krokem

1. Otevřete [https://script.google.com](https://script.google.com) a přihlaste se účtem Google, ze kterého mají odcházet e-maily. To je účet „já“ při nasazení.
2. **Nový projekt** (New project).
3. Smažte ukázkový kód v editoru. Vložte celý soubor `tools/order-form/Code.gs` z tohoto repozitáře. Uložte (ikona disku). Soubor se může jmenovat `Code.gs`.
4. Vlevo **Nastavení projektu** (ozubené kolo) → **Vlastnosti skriptu** (Script properties) → **Přidat vlastnost**:
   - `OWNER_EMAIL` — nechte prázdné pro zkoušku (pošta jde Keithovi), nebo později napište adresu majitelů.
   - `ACCOUNT_NAME` — jméno účtu. Pro zkoušku nechte prázdné. Nevymýšlejte číslo.
   - `ACCOUNT_NUMBER` — číslo účtu. Pro zkoušku nechte prázdné.
   - `IBAN` — IBAN. Pro zkoušku nechte prázdné.
   - `SHEET_ID` — volitelné. ID tabulky Google z adresy `https://docs.google.com/spreadsheets/d/TOTO-ID/edit`. Když je prázdné, tabulka se nepoužije.
5. Vpravo nahoře **Nasadit** (Deploy) → **Nové nasazení** (New deployment).
6. Typ: **Webová aplikace** (Web app). Ozubené kolo vedle „Vyberte typ“.
7. **Spouštět jako** (Execute as): **Já** (Me).
8. **Kdo má přístup** (Who has access): **Kdokoli** (Anyone).
9. **Nasadit**. Google se zeptá na oprávnění (odesílat e-mail, a tabulku, pokud jste vyplnili `SHEET_ID`). Povolte je.
10. Zkopírujte adresu webové aplikace. Končí na `/exec`.
11. V souboru `objednavka-test.html` na webu najděte řádek `var ORDER_ENDPOINT = "";` a vložte adresu mezi uvozovky. Uložte a publikujte web (tento řádek musí být na větvi, ze které GitHub Pages staví stránku — `main`).
12. Když skript později změníte: **Nasadit → Spravovat nasazení → tužka → Nová verze → Nasadit**. Adresa `/exec` zůstane stejná, stránku znovu měnit nemusíte.

Číslo objednávky má tvar `CB-RRRRMMDD-NNN` (datum v Praze). Variabilní symbol jsou jen číslice z tohoto čísla, například `CB-20261026-001` → `20261026001`. Zákazník ho dostane v e-mailu a má ho uvést do zprávy k platbě.

## English — step by step

1. Open [https://script.google.com](https://script.google.com) and sign in with the Google account that should send the mail. That account is “Me” when you deploy.
2. Choose **New project**.
3. Delete the sample function. Paste the whole file `tools/order-form/Code.gs` from this repository. Save (disk icon). The file can stay named `Code.gs`.
4. Open **Project settings** (gear) → **Script properties** → **Add script property**:
   - `OWNER_EMAIL` — leave empty during the test (mail goes to Keith), or later set the owners’ address.
   - `ACCOUNT_NAME` — account name. Leave empty for the test. Do not type a made-up number.
   - `ACCOUNT_NUMBER` — account number. Leave empty for the test.
   - `IBAN` — IBAN. Leave empty for the test.
   - `SHEET_ID` — optional. The id in `https://docs.google.com/spreadsheets/d/THIS-ID/edit`. If empty, no spreadsheet is used.
5. **Deploy → New deployment**.
6. Type: **Web app** (gear icon next to “Select type”).
7. **Execute as: Me**.
8. **Who has access: Anyone**.
9. **Deploy**. Approve the permission prompt (send email, and spreadsheets if you set `SHEET_ID`).
10. Copy the web app URL. It ends in `/exec`.
11. In `objednavka-test.html`, find `var ORDER_ENDPOINT = "";` and paste the URL between the quotes. Save and publish the site (that line has to be on the branch GitHub Pages publishes, which is `main`).
12. After later edits to the script: **Deploy → Manage deployments → pencil → New version → Deploy**. The `/exec` URL stays the same, so the web page does not need another change.

The order number looks like `CB-YYYYMMDD-NNN` (Prague date). The variable symbol is only the digits, so `CB-20261026-001` becomes `20261026001`. The customer email asks them to put the order number in the payment message.
