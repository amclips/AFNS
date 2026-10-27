// AFNS site JS: mobile nav, copy-link, placeholder X links.
(function () {
  var t = document.querySelector('.nav-toggle'), nav = document.getElementById('site-nav');
  if (t && nav) t.addEventListener('click', function () {
    var open = t.getAttribute('aria-expanded') === 'true';
    t.setAttribute('aria-expanded', String(!open)); nav.classList.toggle('open', !open);
  });
  document.querySelectorAll('.copy-link').forEach(function (b) {
    b.addEventListener('click', function () {
      var u = b.dataset.url || location.href;
      (navigator.clipboard ? navigator.clipboard.writeText(u) : Promise.reject()).then(function () {
        b.textContent = 'Link copied'; setTimeout(function () { b.textContent = 'Copy link'; }, 2000);
      }, function () { prompt('Copy this link:', u); });
    });
  });
  document.querySelectorAll('[data-placeholder="true"]').forEach(function (a) { a.title = 'AFNS X account coming soon'; });
})();
