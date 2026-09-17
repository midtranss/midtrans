/*!
 * Meridian theme controller — MIDTRANS
 *
 * Flips the skin on the current page without a reload. It does NOT decide who
 * is allowed to flip it and it does NOT persist the choice: both belong to the
 * server. See INSTALL.md.
 *
 * No dependencies. Safe to load on every page, including pages that never
 * switch: it only reads and writes one attribute on <html>.
 */
(function (w, d) {
  'use strict';

  var SKIN = 'meridian';
  var ATTR = 'data-skin';
  var root = d.documentElement;

  function current() {
    return root.getAttribute(ATTR) === SKIN ? SKIN : 'default';
  }

  /* Suppress transitions and animations for one frame, so flipping the skin
     does not smear every colour on the page into its replacement. */
  function freeze() {
    var s = d.createElement('style');
    s.setAttribute('data-meridian-freeze', '');
    s.appendChild(d.createTextNode(
      '*,*::before,*::after{transition:none!important;animation:none!important}'
    ));
    (d.head || root).appendChild(s);
    return s;
  }

  function release(s) {
    var raf = w.requestAnimationFrame;
    if (!raf) { s.parentNode && s.parentNode.removeChild(s); return; }
    raf(function () {
      raf(function () { s.parentNode && s.parentNode.removeChild(s); });
    });
  }

  /* Apply a skin to the live page. Returns the skin actually in effect.
     Anything other than 'meridian' means the existing appearance. */
  function apply(skin) {
    var s = freeze();
    if (skin === SKIN) root.setAttribute(ATTR, SKIN);
    else root.removeAttribute(ATTR);
    void root.offsetHeight;          /* force the style flush inside the freeze */
    release(s);
    return current();
  }

  w.MidtransTheme = { SKIN: SKIN, ATTR: ATTR, get: current, preview: apply };
})(window, document);
