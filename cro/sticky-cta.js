// forge-bespoke / The Groundwork Collective / cro/sticky-cta.js
// Show sticky WhatsApp bar after the user scrolls past the hero.
// Desktop: hidden entirely. Mobile (<=720px): shown after ~80% viewport scroll.
// Honors prefers-reduced-motion (no slide animation when set).

(function () {
  "use strict";

  function init() {
    var bar = document.getElementById("sticky-cta");
    if (!bar) return;

    var threshold = 0.8; // 80% of viewport height scrolled
    var ticking = false;

    function update() {
      var scrollY = window.pageYOffset || document.documentElement.scrollTop;
      var viewport = window.innerHeight || document.documentElement.clientHeight;
      var show = scrollY > viewport * threshold;
      if (show) {
        bar.classList.add("is-visible");
      } else {
        bar.classList.remove("is-visible");
      }
      ticking = false;
    }

    function onScroll() {
      if (!ticking) {
        window.requestAnimationFrame(update);
        ticking = true;
      }
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    update();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
