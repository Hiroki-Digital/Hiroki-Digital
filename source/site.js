/* Hiroki Digital — site behaviour (no dependencies) */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");
  var CFG = window.HIROKI || {};

  function safe(fn, fallback) { try { return fn(); } catch (e) { return fallback; } }
  var store = {
    get: function (k) { return safe(function () { return JSON.parse(sessionStorage.getItem(k)); }, null); },
    set: function (k, v) { safe(function () { sessionStorage.setItem(k, JSON.stringify(v)); }); }
  };

  /* ---------- Tag Manager (optional) ---------- */
  /* ---------- analytics & ad tracking: only after the visitor agrees ---------- */
  // Nothing third-party loads unless gtmId is set in config.js AND the visitor accepts.
  window.dataLayer = window.dataLayer || [];
  var local = {
    get: function (k) { return safe(function () { return localStorage.getItem(k); }, null); },
    set: function (k, v) { safe(function () { localStorage.setItem(k, v); }); },
    del: function (k) { safe(function () { localStorage.removeItem(k); }); }
  };
  var hasTags = !!(CFG.gtmId && /^GTM-[A-Z0-9]+$/.test(CFG.gtmId));
  function loadTags() {
    if (window.__hdTags) return;
    window.__hdTags = true;
    window.dataLayer.push({ "gtm.start": Date.now(), event: "gtm.js" });
    var g = document.createElement("script");
    g.async = true;
    g.src = "https://www.googletagmanager.com/gtm.js?id=" + CFG.gtmId;
    document.head.appendChild(g);
  }
  function consentBanner() {
    if (document.querySelector(".consent")) return;
    var box = document.createElement("div");
    box.className = "consent";
    box.setAttribute("role", "region");
    box.setAttribute("aria-label", "Cookie choice");
    var base = document.body.getAttribute("data-base") || "";
    box.innerHTML = '<p>Can we use cookies from Google to measure which ads and pages bring in enquiries? This is optional and the site works the same either way. <a href="' + base + 'privacy.html#cookies">How we use them</a></p>' +
      '<div class="consent__btns"><button type="button" class="btn btn--primary" data-consent="granted">Accept</button><button type="button" class="btn btn--ghost" data-consent="denied">No thanks</button></div>';
    box.addEventListener("click", function (e) {
      var b = e.target.closest("[data-consent]");
      if (!b) return;
      var v = b.getAttribute("data-consent");
      local.set("hd_consent", v);
      box.remove();
      if (v === "granted") loadTags();
    });
    document.body.appendChild(box);
  }
  if (hasTags) {
    var choice = local.get("hd_consent");
    if (choice === "granted") loadTags();
    else if (choice !== "denied") consentBanner();
  }
  document.querySelectorAll("[data-cookie-settings]").forEach(function (el) {
    el.hidden = !hasTags;
    el.addEventListener("click", function (e) {
      e.preventDefault();
      local.del("hd_consent");
      consentBanner();
    });
  });

  /* ---------- ad attribution: keep the first-touch UTM / click IDs for the session ---------- */
  var KEYS = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "fbclid", "msclkid"];
  var params = safe(function () { return new URLSearchParams(location.search); }, null);
  var attr = store.get("hd_attr");
  var incoming = {};
  var hasIncoming = false;
  if (params) KEYS.forEach(function (k) { var v = params.get(k); if (v) { incoming[k] = v.slice(0, 200); hasIncoming = true; } });
  if (!attr || hasIncoming) {
    attr = Object.assign({}, hasIncoming ? incoming : {}, {
      landing_page: location.pathname + location.search,
      referrer: document.referrer && document.referrer.indexOf(location.host) === -1 ? document.referrer : (attr && attr.referrer) || ""
    });
    store.set("hd_attr", attr);
  }

  /* ---------- header ---------- */
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      nav.classList.toggle("is-open", !open);
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) { toggle.setAttribute("aria-expanded", "false"); nav.classList.remove("is-open"); }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) { toggle.setAttribute("aria-expanded", "false"); nav.classList.remove("is-open"); toggle.focus(); }
    });
  }
  var onScroll = function () { if (header) header.classList.toggle("is-scrolled", window.scrollY > 8); };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- play demo animations once they scroll into view ---------- */
  var animated = document.querySelectorAll("[data-anim]");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } });
    }, { threshold: 0.3 });
    animated.forEach(function (el) { io.observe(el); });
  } else {
    animated.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ---------- sticky mobile CTA: show after the hero, hide while the form is on screen ---------- */
  var mcta = document.querySelector(".mcta");
  var form = document.querySelector("form.lead-form");
  if (mcta && form && "IntersectionObserver" in window) {
    var formVisible = true, pastTop = false;
    var sync = function () { mcta.classList.toggle("is-on", pastTop && !formVisible); };
    new IntersectionObserver(function (en) { formVisible = en[0].isIntersecting; sync(); }).observe(form);
    window.addEventListener("scroll", function () { pastTop = window.scrollY > 420; sync(); }, { passive: true });
  }

  /* ---------- year ---------- */
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---------- thank-you page personalisation ---------- */
  var ty = document.querySelector("[data-ty]");
  if (ty && params) {
    var offers = {
      "Website design": ["homepage concept", "web-design.html"],
      "Marketing services": ["90-day growth plan", "digital-marketing.html"],
      "Google SEO": ["SEO audit and keyword gap report", "google-seo.html"]
    };
    var s = params.get("s");
    var o = offers[s];
    var slot = document.querySelector("[data-offer]");
    if (o && slot) slot.textContent = o[0];
    var nameSlot = document.querySelector("[data-name]");
    var n = String(store.get("hd_name") || "").replace(/[^\p{L}\p{M}' -]/gu, "").slice(0, 40);
    safe(function () { sessionStorage.removeItem("hd_name"); });
    if (n && nameSlot) nameSlot.textContent = ", " + n;
    if (params.get("demo") === "1") { var dn = document.querySelector(".demo-note"); if (dn) dn.hidden = false; }
  }

  /* ---------- lead form ---------- */
  if (!form) return;
  var started = Date.now();
  var statusEl = form.querySelector(".form-status");
  var btn = form.querySelector('button[type="submit"]');
  var emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  function setHidden(name, value) {
    var el = form.querySelector('input[type="hidden"][name="' + name + '"]');
    if (el) el.value = value || "";
  }
  KEYS.forEach(function (k) { setHidden(k, attr && attr[k]); });
  setHidden("landing_page", attr && attr.landing_page);
  setHidden("referrer", attr && attr.referrer);
  setHidden("page", location.pathname);

  var messages = {
    name: "Please enter your name.",
    email: "Please enter an email address like name@business.com.au.",
    service: "Choose the service you're interested in."
  };
  function fieldOf(el) { return el.closest(".field"); }
  function showError(name, msg) {
    var el = form.elements[name];
    if (!el) return;
    var first = el.length && !el.tagName ? el[0] : el;
    var f = fieldOf(first);
    if (!f) return;
    f.classList.toggle("has-error", !!msg);
    var err = f.querySelector(".field__err");
    if (err) { err.textContent = msg || ""; err.hidden = !msg; }
    var targets = el.length && !el.tagName ? Array.prototype.slice.call(el) : [el];
    targets.forEach(function (t) { if (msg) t.setAttribute("aria-invalid", "true"); else t.removeAttribute("aria-invalid"); });
  }
  function validate() {
    var bad = [];
    var name = (form.elements.name.value || "").trim();
    var email = (form.elements.email.value || "").trim();
    showError("name", name.length < 2 ? messages.name : ""); if (name.length < 2) bad.push("name");
    showError("email", !emailRe.test(email) ? messages.email : ""); if (!emailRe.test(email)) bad.push("email");
    var svc = form.elements.service;
    if (svc && svc.length && !svc.tagName) {
      var picked = Array.prototype.some.call(svc, function (r) { return r.checked; });
      showError("service", picked ? "" : messages.service); if (!picked) bad.push("service");
    }
    return bad;
  }
  form.addEventListener("input", function (e) {
    var f = fieldOf(e.target);
    if (f && f.classList.contains("has-error")) showError(e.target.name, "");
  });
  form.addEventListener("change", function (e) {
    if (e.target.name === "service") showError("service", "");
  });

  function serviceValue() {
    var svc = form.elements.service;
    if (!svc) return "";
    if (svc.length && !svc.tagName) { var c = Array.prototype.filter.call(svc, function (r) { return r.checked; })[0]; return c ? c.value : ""; }
    return svc.value;
  }
  function goThankYou(demo) {
    var first = (form.elements.name.value || "").trim().split(/\s+/)[0] || "";
    var base = document.body.getAttribute("data-base") || "";
    // The first name stays in the browser (session storage) so it never appears in URLs, logs or analytics.
    store.set("hd_name", first.slice(0, 40));
    var url = base + "thank-you.html?s=" + encodeURIComponent(serviceValue()) + (demo ? "&demo=1" : "");
    location.href = url;
  }
  function fail() {
    form.classList.remove("is-sending");
    btn.disabled = false;
    statusEl.hidden = false;
    statusEl.className = "form-status is-error";
    statusEl.textContent = "Your details didn't send. Check your connection and try again, or email " + (CFG.email || "us") + " directly.";
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    statusEl.hidden = true;
    var bad = validate();
    if (bad.length) {
      var el = form.elements[bad[0]];
      (el.length && !el.tagName ? el[0] : el).focus();
      return;
    }
    // quiet spam guard: honeypot filled or submitted faster than a person can type
    if (form.elements.company_fax.value || Date.now() - started < 2500) { goThankYou(!CFG.sheetEndpoint); return; }

    form.classList.add("is-sending");
    btn.disabled = true;
    var data = new FormData(form);
    data.delete("company_fax");
    data.set("service", serviceValue());
    data.set("submitted_at", new Date().toISOString());

    if (!CFG.sheetEndpoint && (CFG.liveHosts || []).indexOf(location.hostname) !== -1) {
      // Live site but the Google Sheet isn't connected yet: don't pretend it worked.
      form.classList.remove("is-sending");
      btn.disabled = false;
      statusEl.hidden = false;
      statusEl.className = "form-status is-error";
      statusEl.textContent = "Our form is being set up. Please email " + (CFG.email || "us") + " and we'll reply within one business day.";
      return;
    }
    if (!CFG.sheetEndpoint) {
      if (window.console) console.info("[Hiroki] Preview mode: add your Google Apps Script URL to assets/js/config.js to save leads.", Object.fromEntries(data));
      setTimeout(function () { goThankYou(true); }, 500);
      return;
    }
    // Conversion event for Google Ads / GA4 (only reaches Google if the visitor accepted cookies).
    window.dataLayer.push({ event: "generate_lead", lead_service: serviceValue(), form_page: location.pathname });
    var ctrl = "AbortController" in window ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, 15000);
    fetch(CFG.sheetEndpoint, {
      method: "POST",
      mode: "no-cors",              // Apps Script answers with a redirect; the row is written before it
      body: new URLSearchParams(data),
      signal: ctrl ? ctrl.signal : undefined
    }).then(function () { clearTimeout(timer); goThankYou(false); })
      .catch(function () { clearTimeout(timer); fail(); });
  });
})();
