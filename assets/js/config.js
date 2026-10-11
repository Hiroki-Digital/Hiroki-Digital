/* Hiroki Digital — site settings. This is the only file you need to edit after deploying.
 *
 * sheetEndpoint  Paste the Web app URL from Google Apps Script (ends in /exec).
 *                See README.md → "Connect the form to Google Sheets". While it is empty,
 *                forms run in preview mode: they validate and show the thank-you page
 *                but do not save anything.
 * gtmId          Optional Google Tag Manager container ID (e.g. "GTM-ABC1234"). When set,
 *                every successful form sends a "generate_lead" event to the dataLayer
 *                so Google Ads / GA4 can count it as a conversion.
 * email          Shown as the fallback contact if a form ever fails to send.
 */
window.HIROKI = {
  sheetEndpoint: "",
  gtmId: "",
  email: "hello@hirokidigital.com",
  // On these domains an unconnected form shows an "email us" message instead of preview mode.
  liveHosts: ["hirokidigital.com", "www.hirokidigital.com"]
};
