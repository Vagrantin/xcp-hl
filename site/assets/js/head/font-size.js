// Font size selector.
//
// Hextra's head partial concatenates every assets/js/head/*.js into one
// render-blocking script, so the stored scale is applied to <html> before first
// paint. Restoring it from a deferred script instead would show the default
// size for a frame and then visibly reflow the page on every load.
//
// Hugo runs this file through ExecuteAsTemplate: do not introduce Go template
// delimiters into it.
(function () {
  'use strict';

  var KEY = 'xcphl-font-scale';
  var SCALES = ['s', 'm', 'l', 'xl'];
  var DEFAULT = 'm';

  function read() {
    try {
      var stored = localStorage.getItem(KEY);
      return SCALES.indexOf(stored) === -1 ? DEFAULT : stored;
    } catch (e) {
      // Private mode, or site data blocked. The default is still correct.
      return DEFAULT;
    }
  }

  function apply(scale) {
    document.documentElement.setAttribute('data-font-scale', scale);
    try {
      if (scale === DEFAULT) {
        localStorage.removeItem(KEY);
      } else {
        localStorage.setItem(KEY, scale);
      }
    } catch (e) {
      // Not persisting is survivable; the page is already at the right size.
    }
    sync(scale);
  }

  function sync(scale) {
    var index = SCALES.indexOf(scale);
    var groups = document.querySelectorAll('.hextra-font-size');
    for (var i = 0; i < groups.length; i++) {
      var dec = groups[i].querySelector('.hextra-font-size-dec');
      var inc = groups[i].querySelector('.hextra-font-size-inc');
      if (dec) dec.disabled = index <= 0;
      if (inc) inc.disabled = index >= SCALES.length - 1;
      groups[i].setAttribute('data-scale', scale);
    }
  }

  function step(delta) {
    var index = SCALES.indexOf(
      document.documentElement.getAttribute('data-font-scale') || DEFAULT
    );
    var next = Math.min(SCALES.length - 1, Math.max(0, index + delta));
    apply(SCALES[next]);
  }

  // Before paint.
  document.documentElement.setAttribute('data-font-scale', read());

  // The controls do not exist yet at this point in <head>.
  document.addEventListener('DOMContentLoaded', function () {
    var groups = document.querySelectorAll('.hextra-font-size');
    for (var i = 0; i < groups.length; i++) {
      groups[i].addEventListener('click', function (event) {
        var button = event.target.closest('button');
        if (!button) return;
        if (button.classList.contains('hextra-font-size-dec')) step(-1);
        else if (button.classList.contains('hextra-font-size-inc')) step(1);
        else if (button.classList.contains('hextra-font-size-reset')) apply(DEFAULT);
      });
    }
    sync(document.documentElement.getAttribute('data-font-scale') || DEFAULT);
  });
})();
