// Preisrechner: 1.000 € pro Tag, unter der Woche 500 € pro Tag Aufschlag.
(function () {
  var state = { days: 2, weekend: true, onsite: false };
  var hints = {
    1: '1 Tag: für kleine, klar umrissene Aufgaben.',
    2: '2 Tage, empfohlen: Thema gelöst, und du baust danach selbst weiter.',
    3: '3 Tage: für mehrere oder größere Abläufe.'
  };
  var fmt = function (n) { return n.toLocaleString('de-DE') + ' €'; };

  function render() {
    var total = state.days * 1000 + (state.weekend ? 0 : state.days * 500);
    var breakdown = state.days + ' × 1.000 €';
    if (!state.weekend) breakdown += ' + ' + state.days + ' × 500 €';
    breakdown += state.onsite ? ' · zzgl. Reisekosten' : ' · remote';

    document.getElementById('total').textContent = fmt(total);
    document.getElementById('breakdown').textContent = breakdown;
    document.getElementById('dayHint').textContent = hints[state.days];

    document.querySelectorAll('.seg').forEach(function (group) {
      var key = group.dataset.group;
      group.querySelectorAll('button').forEach(function (btn) {
        var v = Number(btn.dataset.value);
        var current = key === 'days' ? state.days : Number(state[key]);
        btn.setAttribute('aria-pressed', v === current ? 'true' : 'false');
      });
    });
  }

  document.querySelectorAll('.seg').forEach(function (group) {
    group.addEventListener('click', function (e) {
      var btn = e.target.closest('button');
      if (!btn) return;
      var key = group.dataset.group;
      var v = Number(btn.dataset.value);
      state[key] = key === 'days' ? v : v === 1;
      render();
    });
  });

  render();
})();
