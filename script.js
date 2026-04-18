const landing = document.getElementById('landing');
const lotSelect = document.getElementById('lotSelect');
const statusList = document.getElementById('statusList');
const mapEmbed = document.getElementById('mapEmbed');

const lotStatusData = {
  '97': {
    label: 'Lot 97',
    mapQuery: 'CSUMB+Lot+97+parking',
    spaces: [
      { name: 'Space A1', free: true },
      { name: 'Space A2', free: false },
      { name: 'Space B1', free: true },
      { name: 'Space B2', free: false },
      { name: 'Space C1', free: true },
      { name: 'Space C2', free: true },
      { name: 'Space D1', free: false },
      { name: 'Space D2', free: true }
    ]
  }
};

function updateLandingVisibility() {
  const threshold = window.innerHeight * 0.3;
  if (window.scrollY > threshold) {
    landing.classList.add('hide');
    landing.classList.remove('show');
  } else {
    landing.classList.add('show');
    landing.classList.remove('hide');
  }
}

function renderStatusItems(lotId) {
  const lot = lotStatusData[lotId];
  if (!lot) {
    statusList.innerHTML = '<li class="status-item taken"><span class="icon">!</span><div><strong>Lot unavailable</strong><p>That lot is not active yet.</p></div></li>';
    return;
  }

  const items = lot.spaces.map(space => {
    return `<li class="status-item ${space.free ? 'free' : 'taken'}">
      <span class="icon">${space.free ? '✓' : '✕'}</span>
      <div>
        <strong>${space.name}</strong>
        <p>${space.free ? 'Free' : 'Occupied by a vehicle'}</p>
      </div>
    </li>`;
  });

  statusList.innerHTML = items.join('');
}

function updateMap(lotId) {
  const lot = lotStatusData[lotId];
  const query = lot ? lot.mapQuery : 'CSUMB+parking';
  mapEmbed.src = `https://www.google.com/maps?q=${query}&output=embed`;
}

function randomizeLotStatus() {
  const lot = lotStatusData['97'];
  lot.spaces = lot.spaces.map(space => ({
    ...space,
    free: Math.random() > 0.4
  }));
  renderStatusItems('97');
}

lotSelect.addEventListener('change', event => {
  const selected = event.target.value;
  updateMap(selected);
  renderStatusItems(selected);
});

window.addEventListener('scroll', updateLandingVisibility);
window.addEventListener('DOMContentLoaded', () => {
  updateLandingVisibility();
  renderStatusItems('97');
  updateMap('97');
  setInterval(randomizeLotStatus, 30000);
});