/**
 * Hiroki Digital — website lead capture for Google Sheets
 * --------------------------------------------------------
 * Every form on the website (homepage, landing pages, service and area pages) posts here.
 * Each enquiry becomes one row in the "Leads" tab, with its ad attribution
 * (UTM tags, Google/Meta/Microsoft click IDs) so you can see which ads bring in leads.
 *
 * Setup (about 5 minutes) — full steps with screenshots-free detail in README.md:
 *   1. Create a new Google Sheet, e.g. "Hiroki Digital — Website Leads".
 *   2. Extensions → Apps Script. Delete the sample code, paste this whole file, click Save.
 *   3. In the toolbar choose the function "setup" and click Run. Approve the permissions.
 *      This builds and formats the Leads and Dashboard tabs.
 *   4. Deploy → New deployment → type "Web app".
 *        Execute as: Me      Who has access: Anyone
 *      Click Deploy and copy the Web app URL (it ends in /exec).
 *   5. Paste that URL into the website file assets/js/config.js → sheetEndpoint.
 *
 * Privacy: keep this spreadsheet private (never "Anyone with the link"), turn on 2-step
 * verification for the Google account, and only share it with people who need it.
 * setup() also installs a daily clean-up that deletes rows past the retention periods in
 * CONFIG, matching the website's privacy policy.
 *
 * After editing this script later, use Deploy → Manage deployments → Edit (pencil)
 * → Version: New version → Deploy, so the same URL keeps working.
 */

const CONFIG = {
  SHEET_NAME: 'Leads',
  DASHBOARD_NAME: 'Dashboard',
  // Who gets an email for each new lead. Leave '' to email the Google account that owns
  // this script, put an address (or several, comma-separated), or 'off' to disable.
  NOTIFY_EMAIL: '',
  TIMEZONE: 'Australia/Sydney',
  LOCALE: 'en_AU',
  // Data retention (matches the website privacy policy). A daily trigger deletes old rows.
  RETENTION_MONTHS: 24,        // enquiries that didn't go ahead
  SPAM_RETENTION_DAYS: 30,     // rows marked Spam
  CLIENT_RETENTION_YEARS: 7,   // rows marked Won (client records; tax law needs at least 5 years)
  // Abuse protection: maximum form submissions accepted per minute across the whole site.
  MAX_PER_MINUTE: 20,
};

// [Column header, form field name, column width in px]
// Field names must match the name="" attributes in the website forms.
const COLUMNS = [
  ['Received', '_timestamp', 170],
  ['Lead ID', '_id', 130],
  ['Status', '_status', 130],
  ['Service', 'service', 150],
  ['Name', 'name', 160],
  ['Email', 'email', 220],
  ['Phone', 'phone', 130],
  ['Business', 'business', 170],
  ['Website', 'website', 190],
  ['Budget', 'budget', 170],
  ['Message', 'message', 320],
  ['Form page', 'page', 170],
  ['Landing page', 'landing_page', 240],
  ['Referrer', 'referrer', 200],
  ['UTM source', 'utm_source', 120],
  ['UTM medium', 'utm_medium', 120],
  ['UTM campaign', 'utm_campaign', 170],
  ['UTM term', 'utm_term', 150],
  ['UTM content', 'utm_content', 140],
  ['GCLID', 'gclid', 150],
  ['FBCLID', 'fbclid', 150],
  ['MSCLKID', 'msclkid', 130],
  ['Follow up on', '_followup', 120],
  ['Notes', '_notes', 280],
];

// [Status, background, text colour] — used for the Status dropdown and its colours.
const STATUSES = [
  ['New', '#E5E8FC', '#2230B4'],
  ['Contacted', '#FFF3CF', '#7A5600'],
  ['Call booked', '#E3F0FF', '#1D4E9E'],
  ['Proposal sent', '#F1E8FF', '#5B2EA6'],
  ['Won', '#DDF4EC', '#0B6E50'],
  ['Lost', '#EEEFF3', '#62678A'],
  ['Spam', '#FDECE8', '#C23B26'],
];

const SERVICES = ['Website design', 'Marketing services', 'Google SEO', 'Not sure yet'];

const BRAND = { night: '#141A4D', indigo: '#2D3BD1', ink: '#0F1433', muted: '#62678A', paper: '#F4F5FA', band: '#F7F8FC', line: '#DCDFEC', saffron: '#FFC93C' };
const DATA_ROWS = 2000; // rows pre-formatted for data; extended automatically if you ever exceed it
// Longest value stored per field; anything longer is cut off.
const FIELD_MAX = { name: 80, email: 120, phone: 30, business: 100, website: 200, budget: 60, service: 60, message: 2000 };
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

/* ------------------------------------------------------------------ web endpoints */

function doPost(e) {
  const lock = LockService.getScriptLock();
  try {
    lock.waitLock(20000);
  } catch (err) {
    return json_({ ok: false, error: 'busy' });
  }
  try {
    const p = (e && e.parameter) || {};
    if (p.company_fax) return json_({ ok: true }); // honeypot field filled: a bot, drop silently
    if (!EMAIL_RE.test(String(p.email || '').trim())) return json_({ ok: false, error: 'a valid email is required' });
    if (!rateOk_()) return json_({ ok: false, error: 'too many submissions, try again in a minute' });

    const sheet = getLeadsSheet_();
    const now = new Date();
    const lead = { _timestamp: now, _id: makeId_(now), _status: 'New', _followup: '', _notes: '' };
    COLUMNS.forEach(function (c) {
      if (c[1].charAt(0) !== '_') lead[c[1]] = clean_(p[c[1]], FIELD_MAX[c[1]] || 300);
    });

    const row = COLUMNS.map(function (c) { return lead[c[1]]; });
    const target = sheet.getLastRow() + 1;
    if (target > sheet.getMaxRows()) sheet.insertRowsAfter(sheet.getMaxRows(), 500);
    sheet.getRange(target, 1, 1, row.length).setValues([row]);

    try { notify_(lead); } catch (mailErr) { console.warn('Lead saved, email not sent: ' + mailErr); }
    return json_({ ok: true, id: lead._id });
  } catch (err) {
    console.error(err);
    return json_({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

function doGet() {
  return json_({ ok: true, service: 'Hiroki Digital lead endpoint', time: new Date().toISOString() });
}

/* ------------------------------------------------------------------ setup & formatting */

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Hiroki leads')
    .addItem('Re-apply formatting', 'setup')
    .addItem('Add a test lead', 'addTestLead')
    .addItem('Run data clean-up now', 'purgeOldLeads')
    .addToUi();
}

function setup() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  ss.setSpreadsheetTimeZone(CONFIG.TIMEZONE);
  try { ss.setSpreadsheetLocale(CONFIG.LOCALE); } catch (e) { /* locale is optional */ }
  formatLeads_(getLeadsSheet_());
  buildDashboard_(ss);
  installRetention_();
  ss.setActiveSheet(ss.getSheetByName(CONFIG.SHEET_NAME));
  return 'Leads and Dashboard tabs are ready.';
}

function getLeadsSheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(CONFIG.SHEET_NAME);
  if (!sheet) {
    const sheets = ss.getSheets();
    const blank = sheets.length === 1 && sheets[0].getLastRow() === 0 ? sheets[0] : null;
    sheet = blank ? blank.setName(CONFIG.SHEET_NAME) : ss.insertSheet(CONFIG.SHEET_NAME, 0);
    formatLeads_(sheet);
  }
  return sheet;
}

function formatLeads_(sheet) {
  const n = COLUMNS.length;
  // size the grid
  if (sheet.getMaxColumns() < n) sheet.insertColumnsAfter(sheet.getMaxColumns(), n - sheet.getMaxColumns());
  if (sheet.getMaxColumns() > n) sheet.deleteColumns(n + 1, sheet.getMaxColumns() - n);
  const rows = Math.max(DATA_ROWS, sheet.getLastRow() + 200);
  if (sheet.getMaxRows() < rows + 1) sheet.insertRowsAfter(sheet.getMaxRows(), rows + 1 - sheet.getMaxRows());

  // header
  const header = sheet.getRange(1, 1, 1, n);
  header.setValues([COLUMNS.map(function (c) { return c[0]; })])
    .setBackground(BRAND.night).setFontColor('#FFFFFF').setFontWeight('bold')
    .setFontFamily('Roboto').setFontSize(10).setVerticalAlignment('middle').setWrap(false);
  sheet.setRowHeight(1, 38);
  sheet.setFrozenRows(1);
  sheet.setFrozenColumns(0);
  COLUMNS.forEach(function (c, i) { sheet.setColumnWidth(i + 1, c[2]); });

  // body
  const body = sheet.getRange(2, 1, sheet.getMaxRows() - 1, n);
  body.setFontFamily('Roboto').setFontSize(10).setFontColor(BRAND.ink).setVerticalAlignment('middle')
    .setWrapStrategy(SpreadsheetApp.WrapStrategy.CLIP);
  colRange_(sheet, '_timestamp').setNumberFormat('ddd d mmm yyyy, h:mm am/pm');
  colRange_(sheet, '_followup').setNumberFormat('d mmm yyyy');
  colRange_(sheet, '_id').setFontFamily('Roboto Mono').setFontColor(BRAND.muted);
  colRange_(sheet, 'phone').setNumberFormat('@');
  colRange_(sheet, 'message').setWrapStrategy(SpreadsheetApp.WrapStrategy.WRAP);
  colRange_(sheet, '_notes').setWrapStrategy(SpreadsheetApp.WrapStrategy.WRAP).setBackground('#FFFBEA');
  colRange_(sheet, 'name').setFontWeight('bold');
  colRange_(sheet, '_status').setHorizontalAlignment('center').setFontWeight('bold');

  // dropdowns & validation
  colRange_(sheet, '_status').setDataValidation(
    SpreadsheetApp.newDataValidation().requireValueInList(STATUSES.map(function (s) { return s[0]; }), true)
      .setAllowInvalid(false).setHelpText('Pick where this lead is up to.').build());
  colRange_(sheet, '_followup').setDataValidation(
    SpreadsheetApp.newDataValidation().requireDate().setAllowInvalid(false).setHelpText('Enter a date, e.g. 14/10/2026').build());

  // conditional formatting: status colours, overdue follow-ups, fresh leads
  const statusCol = colLetter_('_status');
  const followCol = colLetter_('_followup');
  const timeCol = colLetter_('_timestamp');
  const rules = STATUSES.map(function (s) {
    return SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo(s[0])
      .setBackground(s[1]).setFontColor(s[2]).setRanges([colRange_(sheet, '_status')]).build();
  });
  rules.push(SpreadsheetApp.newConditionalFormatRule()
    .whenFormulaSatisfied('=AND($' + followCol + '2<>"",$' + followCol + '2<=TODAY(),NOT(REGEXMATCH($' + statusCol + '2,"Won|Lost|Spam")))')
    .setBackground('#FDECE8').setFontColor('#C23B26').setBold(true)
    .setRanges([colRange_(sheet, '_followup')]).build());
  rules.push(SpreadsheetApp.newConditionalFormatRule()
    .whenFormulaSatisfied('=AND($' + timeCol + '2<>"",$' + statusCol + '2="New",NOW()-$' + timeCol + '2>1)')
    .setFontColor('#C23B26').setBold(true)
    .setRanges([colRange_(sheet, '_timestamp')]).build());
  sheet.setConditionalFormatRules(rules);

  // zebra banding
  sheet.getBandings().forEach(function (b) { b.remove(); });
  const band = sheet.getRange(1, 1, sheet.getMaxRows(), n)
    .applyRowBanding(SpreadsheetApp.BandingTheme.LIGHT_GREY, true, false);
  band.setHeaderRowColor(BRAND.night).setFirstRowColor('#FFFFFF').setSecondRowColor(BRAND.band);

  // filter on the header so every column can be sorted/filtered
  if (!sheet.getFilter()) sheet.getRange(1, 1, sheet.getMaxRows(), n).createFilter();

  // warn (don't block) before anyone edits the header row
  sheet.getProtections(SpreadsheetApp.ProtectionType.RANGE).forEach(function (pr) {
    if (pr.getDescription() === 'Lead headers') pr.remove();
  });
  header.protect().setDescription('Lead headers').setWarningOnly(true);
  sheet.setTabColor(BRAND.indigo);
}

function buildDashboard_(ss) {
  let d = ss.getSheetByName(CONFIG.DASHBOARD_NAME);
  if (d) { d.getCharts().forEach(function (c) { d.removeChart(c); }); d.clear(); d.clearConditionalFormatRules(); }
  else d = ss.insertSheet(CONFIG.DASHBOARD_NAME);
  ss.setActiveSheet(d);
  ss.moveActiveSheet(ss.getSheets().length);

  const L = "'" + CONFIG.SHEET_NAME + "'!";
  const id = L + colLetter_('_id') + '2:' + colLetter_('_id');
  const time = L + colLetter_('_timestamp') + '2:' + colLetter_('_timestamp');
  const status = L + colLetter_('_status') + '2:' + colLetter_('_status');
  const service = L + colLetter_('service') + '2:' + colLetter_('service');
  const source = L + colLetter_('utm_source') + '2:' + colLetter_('utm_source');
  const campaign = L + colLetter_('utm_campaign') + '2:' + colLetter_('utm_campaign');

  d.setHiddenGridlines(true);
  if (d.getMaxColumns() < 10) d.insertColumnsAfter(d.getMaxColumns(), 10 - d.getMaxColumns());
  [24, 190, 110, 110, 24, 190, 110, 110, 24, 24].forEach(function (w, i) { d.setColumnWidth(i + 1, w); });
  d.getRange('A:J').setFontFamily('Roboto').setFontColor(BRAND.ink).setVerticalAlignment('middle');

  d.getRange('B2').setValue('Website leads').setFontSize(20).setFontWeight('bold');
  d.getRange('B3').setValue('Updates automatically from the Leads tab. Times in ' + CONFIG.TIMEZONE + '.').setFontColor(BRAND.muted);
  d.setRowHeight(2, 40);

  // KPI tiles
  const kpis = [
    ['B5', 'Total leads', '=COUNTA(' + id + ')'],
    ['C5', 'Last 7 days', '=COUNTIF(' + time + ',">="&(TODAY()-6))'],
    ['D5', 'Last 30 days', '=COUNTIF(' + time + ',">="&(TODAY()-29))'],
    ['F5', 'Open leads', '=COUNTIF(' + status + ',"New")+COUNTIF(' + status + ',"Contacted")+COUNTIF(' + status + ',"Call booked")+COUNTIF(' + status + ',"Proposal sent")'],
    ['G5', 'Won', '=COUNTIF(' + status + ',"Won")'],
    ['H5', 'Win rate', '=IFERROR(COUNTIF(' + status + ',"Won")/(COUNTIF(' + status + ',"Won")+COUNTIF(' + status + ',"Lost")),"–")'],
  ];
  kpis.forEach(function (k) {
    const label = d.getRange(k[0]);
    const value = label.offset(1, 0);
    label.setValue(k[1]).setFontColor(BRAND.muted).setFontSize(9).setBackground(BRAND.paper);
    value.setFormula(k[2]).setFontSize(22).setFontWeight('bold').setBackground(BRAND.paper).setHorizontalAlignment('left');
  });
  d.getRange('H6').setNumberFormat('0%');
  d.setRowHeight(6, 44);
  d.getRange('B5:D6').setBorder(true, true, true, true, false, false, BRAND.line, SpreadsheetApp.BorderStyle.SOLID);
  d.getRange('F5:H6').setBorder(true, true, true, true, false, false, BRAND.line, SpreadsheetApp.BorderStyle.SOLID);

  // Leads by service
  sectionHeader_(d, 'B8', ['Service', 'Leads', 'Won']);
  SERVICES.forEach(function (s, i) {
    const r = 9 + i;
    d.getRange('B' + r).setValue(s);
    d.getRange('C' + r).setFormula('=COUNTIF(' + service + ',B' + r + ')');
    d.getRange('D' + r).setFormula('=COUNTIFS(' + service + ',B' + r + ',' + status + ',"Won")');
  });

  // Leads by status
  sectionHeader_(d, 'F8', ['Status', 'Leads', 'Share']);
  STATUSES.forEach(function (s, i) {
    const r = 9 + i;
    d.getRange('F' + r).setValue(s[0]).setBackground(s[1]).setFontColor(s[2]).setFontWeight('bold');
    d.getRange('G' + r).setFormula('=COUNTIF(' + status + ',F' + r + ')');
    d.getRange('H' + r).setFormula('=IFERROR(G' + r + '/COUNTA(' + id + '),0)').setNumberFormat('0%');
  });

  // Leads by ad source and campaign (blank UTM = direct, organic or referral)
  sectionHeader_(d, 'B18', ['Source (utm_source)', 'Leads']);
  d.getRange('B19').setFormula('=IFERROR(QUERY(ARRAYFORMULA({IF(' + source + '="","(none: direct / organic)",' + source + '),' + id + '}),"select Col1, count(Col2) where Col2 is not null group by Col1 order by count(Col2) desc limit 12 label Col1 \'\', count(Col2) \'\'",0),"No leads yet")');
  sectionHeader_(d, 'F18', ['Campaign (utm_campaign)', 'Leads']);
  d.getRange('F19').setFormula('=IFERROR(QUERY(ARRAYFORMULA({IF(' + campaign + '="","(none)",' + campaign + '),' + id + '}),"select Col1, count(Col2) where Col2 is not null group by Col1 order by count(Col2) desc limit 12 label Col1 \'\', count(Col2) \'\'",0),"No leads yet")');

  // Weekly trend (last 8 weeks, weeks start Monday) + chart
  sectionHeader_(d, 'B31', ['Week starting', 'Leads']);
  for (let k = 0; k < 8; k++) {
    const r = 32 + k;
    d.getRange('B' + r).setFormula('=TODAY()-WEEKDAY(TODAY(),3)-' + (7 * (7 - k))).setNumberFormat('d mmm');
    d.getRange('C' + r).setFormula('=COUNTIFS(' + time + ',">="&B' + r + ',' + time + ',"<"&(B' + r + '+7))');
  }
  d.getRange('B32:C39').setHorizontalAlignment('left');
  const chart = d.newChart().setChartType(Charts.ChartType.COLUMN)
    .addRange(d.getRange('B31:C39'))
    .setPosition(31, 6, 0, 0)
    .setOption('title', 'Leads per week')
    .setOption('legend', { position: 'none' })
    .setOption('colors', [BRAND.indigo])
    .setOption('backgroundColor', '#FFFFFF')
    .setOption('width', 460).setOption('height', 240)
    .build();
  d.insertChart(chart);
  d.setTabColor(BRAND.saffron);
}

function sectionHeader_(sheet, a1, labels) {
  const r = sheet.getRange(a1).offset(0, 0, 1, labels.length);
  r.setValues([labels]).setFontWeight('bold').setFontColor('#FFFFFF').setBackground(BRAND.night).setFontSize(9);
}

/* ------------------------------------------------------------------ privacy: retention & abuse limits */

// Deletes rows past their retention period (see CONFIG). Runs daily via the trigger set up in setup().
function purgeOldLeads() {
  const sheet = getLeadsSheet_();
  const last = sheet.getLastRow();
  if (last < 2) return 0;
  const tCol = colIndex_('_timestamp') - 1, sCol = colIndex_('_status') - 1;
  const values = sheet.getRange(2, 1, last - 1, COLUMNS.length).getValues();
  const now = new Date().getTime(), DAY = 86400000;
  let removed = 0;
  for (let i = values.length - 1; i >= 0; i--) {
    const ts = values[i][tCol];
    if (!(ts instanceof Date) && isNaN(new Date(ts).getTime())) continue;
    const ageDays = (now - new Date(ts).getTime()) / DAY;
    const status = String(values[i][sCol] || '');
    const limit = status === 'Spam' ? CONFIG.SPAM_RETENTION_DAYS
      : status === 'Won' ? CONFIG.CLIENT_RETENTION_YEARS * 365
      : CONFIG.RETENTION_MONTHS * 30.44;
    if (ageDays > limit) { sheet.deleteRow(i + 2); removed++; }
  }
  if (removed) console.log('Data clean-up removed ' + removed + ' row(s).');
  return removed;
}

function installRetention_() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'purgeOldLeads') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('purgeOldLeads').timeBased().everyDays(1).atHour(3).create();
}

// Simple site-wide rate limit so a bot can't flood the sheet.
function rateOk_() {
  const cache = CacheService.getScriptCache();
  const key = 'rate_' + Math.floor(Date.now() / 60000);
  const n = Number(cache.get(key) || 0) + 1;
  cache.put(key, String(n), 120);
  return n <= CONFIG.MAX_PER_MINUTE;
}

/* ------------------------------------------------------------------ helpers */

function addTestLead() {
  const res = doPost({ parameter: {
    name: 'Test Lead (delete me)', email: 'test@example.com', phone: '0400 000 000', business: 'Example Pty Ltd',
    website: 'example.com.au', service: 'Google SEO', budget: '$1,000–$2,000 / month', message: 'Testing the website form connection.',
    page: '/google-seo.html', landing_page: '/google-seo.html?utm_source=google&utm_medium=cpc&utm_campaign=seo-audit',
    utm_source: 'google', utm_medium: 'cpc', utm_campaign: 'seo-audit', utm_term: 'seo agency', gclid: 'TEST-GCLID',
  } });
  SpreadsheetApp.getActiveSpreadsheet().toast('Test lead added: ' + res.getContent(), 'Hiroki leads', 5);
}

function notify_(lead) {
  if (String(CONFIG.NOTIFY_EMAIL).toLowerCase() === 'off') return;
  const to = CONFIG.NOTIFY_EMAIL || Session.getEffectiveUser().getEmail();
  if (!to) return;
  const rows = [
    ['Service', lead.service], ['Name', lead.name], ['Email', lead.email], ['Phone', lead.phone],
    ['Business', lead.business], ['Website', lead.website], ['Budget', lead.budget], ['Message', lead.message],
    ['Page', lead.page], ['Source', [lead.utm_source, lead.utm_medium, lead.utm_campaign].filter(String).join(' / ') || 'direct / organic'],
  ].filter(function (r) { return r[1]; });
  const html = '<div style="font-family:Arial,sans-serif;color:#0F1433">' +
    '<p style="font-size:16px;margin:0 0 12px"><b>New website lead</b> · ' + esc_(lead._id) + '</p>' +
    '<table cellpadding="6" style="border-collapse:collapse;font-size:14px">' +
    rows.map(function (r) { return '<tr><td style="color:#62678A;vertical-align:top">' + esc_(r[0]) + '</td><td>' + esc_(String(r[1]).replace(/^'/, '')) + '</td></tr>'; }).join('') +
    '</table><p style="margin-top:16px"><a href="' + SpreadsheetApp.getActiveSpreadsheet().getUrl() + '">Open the leads sheet</a></p></div>';
  const msg = { to: to, subject: 'New lead: ' + (lead.name || 'Website enquiry') + ' · ' + (lead.service || 'General'), htmlBody: html, name: 'Hiroki Digital website' };
  if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(lead.email)) msg.replyTo = lead.email;
  MailApp.sendEmail(msg);
}

function clean_(v, max) {
  if (v === undefined || v === null) return '';
  let s = String(v).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '').trim().slice(0, max || 2000);
  if (/^[=+\-@]/.test(s)) s = "'" + s; // stop spreadsheet formula injection
  return s;
}

function makeId_(d) {
  const stamp = Utilities.formatDate(d, CONFIG.TIMEZONE, 'yyMMdd');
  const rand = Math.random().toString(36).slice(2, 6).toUpperCase();
  return 'HD-' + stamp + '-' + rand;
}

function colIndex_(key) {
  for (let i = 0; i < COLUMNS.length; i++) if (COLUMNS[i][1] === key) return i + 1;
  throw new Error('Unknown column ' + key);
}

function colLetter_(key) {
  let n = colIndex_(key), s = '';
  while (n > 0) { const m = (n - 1) % 26; s = String.fromCharCode(65 + m) + s; n = Math.floor((n - 1) / 26); }
  return s;
}

function colRange_(sheet, key) {
  return sheet.getRange(2, colIndex_(key), sheet.getMaxRows() - 1, 1);
}

function esc_(s) {
  return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; });
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
