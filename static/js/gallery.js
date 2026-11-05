/* Screenshot galleries on /portfolio: one picture at a time, dots to jump,
   automatic advance every 5 seconds. Autoplay pauses while the pointer or keyboard
   focus is inside, while the tab is hidden, and never runs for visitors who ask
   for reduced motion. */
(function () {
  var INTERVAL = 5000;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.querySelectorAll('[data-gallery]').forEach(function (g) {
    var slides = g.querySelectorAll('.slide');
    var dots = g.querySelectorAll('.dot');
    if (slides.length < 2) return;
    var current = 0, timer = null, hovering = false;

    function show(i) {
      current = (i + slides.length) % slides.length;
      slides.forEach(function (s, n) {
        var on = n === current;
        s.classList.toggle('is-active', on);
        s.setAttribute('aria-hidden', on ? 'false' : 'true');
      });
      dots.forEach(function (d, n) {
        var on = n === current;
        d.classList.toggle('is-active', on);
        if (on) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current');
      });
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }
    function start() {
      stop();
      if (reduce || hovering || document.hidden) return;
      timer = setInterval(function () { show(current + 1); }, INTERVAL);
    }

    dots.forEach(function (d, n) {
      d.addEventListener('click', function () { show(n); start(); });
    });
    g.addEventListener('mouseenter', function () { hovering = true; stop(); });
    g.addEventListener('mouseleave', function () { hovering = false; start(); });
    g.addEventListener('focusin', function () { hovering = true; stop(); });
    g.addEventListener('focusout', function () { hovering = false; start(); });
    document.addEventListener('visibilitychange', start);
    start();
  });
})();
