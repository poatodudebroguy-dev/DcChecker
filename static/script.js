const landing = document.getElementById('landing');
const lotSelect = document.getElementById('lotSelect');
const statusList = document.getElementById('statusList');
const mapEmbed = document.getElementById('mapEmbed');
const directionsLink = document.getElementById('directionsLink');
const contentSection = document.querySelector('.content');
const howItWorksSection = document.querySelector('.how-it-works-section');

const lotStatusData = {
  '97': {
    label: 'Lot 97',
    location: '4th Avenue (near Visitors Center)',
    mapQuery: 'CSUMB+Lot+97+parking',
    spaces: []
  },
  '1': { label: 'Lot 1', location: 'Divarty Street', mapQuery: 'CSUMB+Lot+1' },
  '13': { label: 'Lot 13', location: '6th Avenue', mapQuery: 'CSUMB+Lot+13' },
  '16': { label: 'Lot 16', location: 'Inter-Garrison Road', mapQuery: 'CSUMB+Lot+16' },
  '18': { label: 'Lot 18', location: '4th Avenue', mapQuery: 'CSUMB+Lot+18' },
  '19': { label: 'Lot 19', location: '6th Avenue', mapQuery: 'CSUMB+Lot+19' },
  '23': { label: 'Lot 23', location: 'Engineer Lane', mapQuery: 'CSUMB+Lot+23' },
  '28': { label: 'Lot 28', location: '6th Avenue', mapQuery: 'CSUMB+Lot+28' },
  '29': { label: 'Lot 29', location: '6th Avenue', mapQuery: 'CSUMB+Lot+29' },
  '30': { label: 'Lot 30', location: '6th Avenue', mapQuery: 'CSUMB+Lot+30' },
  '35': { label: 'Lot 35', location: 'Butler Street', mapQuery: 'CSUMB+Lot+35' },
  '37': { label: 'Lot 37', location: 'Butler Street', mapQuery: 'CSUMB+Lot+37' },
  '42': { label: 'Lot 42', location: 'B Street', mapQuery: 'CSUMB+Lot+42' },
  '59': { label: 'Lot 59', location: '7th Avenue and A Street', mapQuery: 'CSUMB+Lot+59' },
  '71': { label: 'Lot 71', location: 'Inter-Garrison Road', mapQuery: 'CSUMB+Lot+71' },
  '72': { label: 'Lot 72', location: 'Inter-Garrison Road', mapQuery: 'CSUMB+Lot+72' },
  '80': { label: 'Lot 80', location: 'General Jim Moore', mapQuery: 'CSUMB+Lot+80' },
  '82': { label: 'Lot 82', location: 'Inter-Garrison Road', mapQuery: 'CSUMB+Lot+82' },
  '82E': { label: 'Lot 82E', location: 'Inter-Garrison Road', mapQuery: 'CSUMB+Lot+82E' },
  '84': { label: 'Lot 84', location: '3rd Avenue', mapQuery: 'CSUMB+Lot+84' },
  '86': { label: 'Lot 86', location: 'Inter-Garrison Road', mapQuery: 'CSUMB+Lot+86' },
  '90': { label: 'Lot 90', location: 'Inter-Garrison Road', mapQuery: 'CSUMB+Lot+90' },
  '91': { label: 'Lot 91', location: '3rd Avenue', mapQuery: 'CSUMB+Lot+91' },
  '98': { label: 'Lot 98', location: 'Divarty Street', mapQuery: 'CSUMB+Lot+98' },
  '100': { label: 'Lot 100', location: '2nd Avenue', mapQuery: 'CSUMB+Lot+100' },
  '106': { label: 'Lot 106', location: '2nd Avenue', mapQuery: 'CSUMB+Lot+106' },
  '107': { label: 'Lot 107', location: '2nd Avenue', mapQuery: 'CSUMB+Lot+107' },
  '208': { label: 'Lot 208', location: 'Divarty Street', mapQuery: 'CSUMB+Lot+208' },
  '300': { label: 'Lot 300', location: 'General Jim Moore and 4th Avenue', mapQuery: 'CSUMB+Lot+300' },
  '301': { label: 'Lot 301', location: '4th Avenue', mapQuery: 'CSUMB+Lot+301' },
  '490': { label: 'Lot 490', location: '8th Street', mapQuery: 'CSUMB+Lot+490' },
  '508': { label: 'Lot 508', location: 'Divarty Street', mapQuery: 'CSUMB+Lot+508' },
  '903': { label: 'Lot 903', location: 'Divarty Street', mapQuery: 'CSUMB+Lot+903', directions: 'https://www.google.com/maps/search/?api=1&query=CSUMB+Lot+903' }
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

function updateHeading(lotId) {
  const lot = lotStatusData[lotId];
  const heading = document.querySelector('.status-heading h2');
  if (heading && lot) {
    heading.textContent = `${lot.label} status`;
  }
}

function renderStatusItems(lotId) {
  const lot = lotStatusData[lotId];
  if (!lot) {
    statusList.innerHTML = '<li class="status-item taken"><span class="icon">!</span><div><strong>Lot unavailable</strong><p>That lot is not active yet.</p></div></li>';
    return;
  }

  if (!lot.spaces || lot.spaces.length === 0) {
    statusList.innerHTML = '<li class="status-item taken"><span class="icon">i</span><div><strong>' + lot.label + '</strong><p>Detailed availability is not available for this lot yet. Map directions are active.</p></div></li>';
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
  if (directionsLink && lot) {
    directionsLink.href = lot.directions || `https://www.google.com/maps/search/?api=1&query=${query}`;
  }
}

async function fetchLiveStatus() {
  const lotId = lotSelect.value;
  if (lotId !== '97') return; // Currently only 97 is supported by YOLO

  try {
    const response = await fetch('/api/status');
    const data = await response.json();
    
    // Convert data object to array
    const newSpaces = Object.keys(data).map(key => {
      return {
        name: key,
        free: data[key] !== 'Occupied'
      };
    });
    
    // Sort spaces numerically if possible
    newSpaces.sort((a, b) => {
      const numA = parseInt(a.name.replace('Space ', ''));
      const numB = parseInt(b.name.replace('Space ', ''));
      if (!isNaN(numA) && !isNaN(numB)) return numA - numB;
      return a.name.localeCompare(b.name);
    });

    lotStatusData['97'].spaces = newSpaces;
    renderStatusItems('97');
  } catch (err) {
    console.error('Error fetching live status', err);
  }
}

lotSelect.addEventListener('change', event => {
  const selected = event.target.value;
  updateHeading(selected);
  updateMap(selected);
  renderStatusItems(selected);
});

const sectionFadeObserver = new IntersectionObserver(
  entries => {
    entries.forEach(entry => {
      const ratio = entry.intersectionRatio;
      const fadeStart = 0.1;
      const fadeEnd = 0.55;
      const progress = Math.min(Math.max((ratio - fadeStart) / (fadeEnd - fadeStart), 0), 1);
      if (contentSection) {
        contentSection.style.opacity = String(1 - progress);
        contentSection.style.transform = `translateY(-${progress * 18}px)`;
      }
    });
  },
  {
    root: null,
    threshold: Array.from({ length: 21 }, (_, i) => i / 20)
  }
);

window.addEventListener('scroll', updateLandingVisibility);
window.addEventListener('DOMContentLoaded', () => {
  updateLandingVisibility();
  updateHeading('97');
  renderStatusItems('97');
  updateMap('97');
  setInterval(fetchLiveStatus, 5000);
  fetchLiveStatus();
  if (howItWorksSection) {
    sectionFadeObserver.observe(howItWorksSection);
  }
});