const lot = {
  name: "North Student Lot",
  occupancy_estimate: 64,
  capacity: 220,
  confidence: 0.93,
  latitude: 34.0522,
  longitude: -118.2437
};

function getStatus(pct) {
  if (pct >= 0.98) return "FULL";
  if (pct >= 0.85) return "LIMITED";
  return "OPEN";
}

function getColor(pct) {
  if (pct >= 0.98) return "#d93025";
  if (pct >= 0.85) return "#f9ab00";
  return "#188038";
}

function render() {
  const pct = lot.occupancy_estimate / lot.capacity;
  const status = getStatus(pct);

  document.getElementById("status").textContent =
    `${status} (${lot.occupancy_estimate}/${lot.capacity})`;

  document.getElementById("meta").textContent =
    `Confidence: ${Math.round(lot.confidence * 100)}% | Updated: ${new Date().toLocaleTimeString()}`;

  const fill = document.getElementById("lot-fill");
  fill.style.width = `${pct * 100}%`;
  fill.style.background = getColor(pct);
}

/* FAKE LIVE UPDATES */
setInterval(() => {
  const change = Math.floor(Math.random() * 3) - 1;
  lot.occupancy_estimate = Math.max(
    0,
    Math.min(lot.capacity, lot.occupancy_estimate + change)
  );
  render();
}, 3000);

/* MAP */
const map = L.map("map").setView([lot.latitude, lot.longitude], 18);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "© OpenStreetMap"
}).addTo(map);

const marker = L.marker([lot.latitude, lot.longitude]).addTo(map);
marker.bindPopup("North Student Lot").openPopup();

render();