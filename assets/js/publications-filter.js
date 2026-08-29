(() => {
  const buttons = Array.from(document.querySelectorAll('[data-access-filter]'));
  const cards = Array.from(document.querySelectorAll('.publication'));
  const yearGroups = Array.from(document.querySelectorAll('[data-year-group]'));
  const count = document.querySelector('#publication-result-count');

  if (!buttons.length || !cards.length || !count) return;

  const updateFilter = (selectedAccess) => {
    let visibleCards = 0;

    buttons.forEach((button) => {
      const selected = button.dataset.accessFilter === selectedAccess;
      button.classList.toggle('is-selected', selected);
      button.setAttribute('aria-pressed', String(selected));
    });

    cards.forEach((card) => {
      const visible = selectedAccess === 'all' || card.dataset.access === selectedAccess;
      card.hidden = !visible;
      if (visible) visibleCards += 1;
    });

    yearGroups.forEach((group) => {
      group.hidden = !group.querySelector('.publication:not([hidden])');
    });

    count.textContent = `${visibleCards} publication${visibleCards === 1 ? '' : 's'} shown.`;
  };

  buttons.forEach((button) => {
    button.addEventListener('click', () => updateFilter(button.dataset.accessFilter));
  });

  updateFilter('all');
})();
