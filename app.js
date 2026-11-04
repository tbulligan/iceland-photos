let allPhotos = [];
let currentView = 'highlights'; // 'highlights' or 'all'
let filteredPhotos = [];
let activeIndex = 0;
let map, markersLayer, photoMarkers = new Map();
let captionTimer = null;
let preloadedNext = null, preloadedPrev = null;

// Init
async function init() {
  try {
    const res = await fetch('data.json?v=' + Date.now());
    allPhotos = await res.json();
    updateViewCounts();
    initMap();
    setView(currentView);
    initEvents();
  } catch (err) {
    console.error('Failed to load photos:', err);
  }
}

function updateViewCounts() {
  const heroesCount = allPhotos.filter(p => p.is_hero).length;
  const totalCount = allPhotos.length;
  const btnHighlights = document.getElementById('btn-highlights');
  const btnAll = document.getElementById('btn-all');
  if (btnHighlights) btnHighlights.textContent = `★ Highlights (${heroesCount})`;
  if (btnAll) btnAll.textContent = `Full Journey (${totalCount})`;
}

// Satellite Map (Esri World Imagery, Zero API Key)
function initMap() {
  map = L.map('map', {
    zoomControl: false,
    attributionControl: false
  }).setView([64.9631, -19.0208], 6.5);

  L.control.zoom({ position: 'bottomright' }).addTo(map);

  L.tileLayer(
    'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    { maxZoom: 19 }
  ).addTo(map);

  markersLayer = L.layerGroup().addTo(map);
}

// View Toggle: Highlights vs All
function setView(view) {
  currentView = view;
  document.querySelectorAll('.switch-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.view === view);
  });

  if (view === 'highlights') {
    filteredPhotos = allPhotos.filter(p => p.is_hero);
  } else {
    filteredPhotos = [...allPhotos];
  }

  renderGrid();
  updateMapMarkers();
}

// Render Card Grid
function renderGrid() {
  const grid = document.getElementById('gallery-grid');
  grid.innerHTML = '';

  filteredPhotos.forEach((photo, idx) => {
    const card = document.createElement('div');
    card.className = 'photo-card';
    card.id = `card-${photo.filename}`;
    card.tabIndex = 0;

    const starHtml = photo.is_hero ? '<div class="card-star">★</div>' : '';

    card.innerHTML = `
      <div class="card-img-wrap">
        ${starHtml}
        <img class="card-thumb" src="${photo.thumb}" alt="${photo.title}" loading="lazy" />
      </div>
      <div class="card-caption">
        <div class="card-title">${photo.title}</div>
        <div class="card-sub">
          <span class="card-place">${photo.place}</span>
          <span class="card-date">${photo.date_display}</span>
        </div>
      </div>
    `;

    card.addEventListener('mouseenter', () => highlightMarker(photo.filename));
    card.addEventListener('mouseleave', () => unhighlightMarker(photo.filename));
    card.addEventListener('click', () => openLightbox(idx));
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') openLightbox(idx);
    });

    grid.appendChild(card);
  });
}

// Map Markers
function updateMapMarkers() {
  markersLayer.clearLayers();
  photoMarkers.clear();

  // Group coordinates
  const coordGroups = new Map();
  filteredPhotos.forEach(p => {
    if (p.lat && p.lon) {
      const key = `${p.lat.toFixed(3)},${p.lon.toFixed(3)}`;
      if (!coordGroups.has(key)) coordGroups.set(key, []);
      coordGroups.get(key).push(p);
    }
  });

  coordGroups.forEach((group, key) => {
    const p = group[0];
    const isHero = group.some(item => item.is_hero);

    const icon = L.divIcon({
      className: isHero ? 'custom-pin is-hero' : 'custom-pin',
      iconSize: isHero ? [17, 17] : [13, 13],
      iconAnchor: isHero ? [8, 8] : [6, 6]
    });

    const marker = L.marker([p.lat, p.lon], { icon }).addTo(markersLayer);
    
    marker.on('click', () => {
      scrollToCard(p.filename);
    });

    group.forEach(item => {
      photoMarkers.set(item.filename, marker);
    });
  });

  const coords = filteredPhotos.filter(p => p.lat && p.lon).map(p => [p.lat, p.lon]);
  if (coords.length > 0) {
    map.fitBounds(L.latLngBounds(coords), { padding: [40, 40], maxZoom: 13 });
  }
}

function highlightMarker(fname) {
  const marker = photoMarkers.get(fname);
  if (marker && marker._icon) marker._icon.classList.add('active');
}

function unhighlightMarker(fname) {
  const marker = photoMarkers.get(fname);
  if (marker && marker._icon) marker._icon.classList.remove('active');
}

function scrollToCard(fname) {
  const card = document.getElementById(`card-${fname}`);
  if (card) {
    card.scrollIntoView({ behavior: 'smooth', block: 'center' });
    card.classList.add('highlighted');
    setTimeout(() => card.classList.remove('highlighted'), 1500);
  }
}

// =========================================
// SoTA FULLSCREEN LIGHTBOX (Pure Photo)
// =========================================
const lightbox = document.getElementById('lightbox');
const lbImg = document.getElementById('lb-img');
const lbCaption = document.getElementById('lb-caption');
const lbTopActions = document.querySelector('.lightbox-top-actions');
const capTitle = document.getElementById('cap-title');
const capSub = document.getElementById('cap-sub');

function openLightbox(index) {
  if (index < 0 || index >= filteredPhotos.length) return;
  activeIndex = index;
  updateLightbox();
  lightbox.classList.add('active');
  document.body.style.overflow = 'hidden';

  // Push state for TV Remote & Mobile Back button
  try {
    if (!history.state || !history.state.lightbox) {
      history.pushState({ lightbox: true }, '');
    }
  } catch (e) {}
}

function closeLightbox(fromPopstate = false) {
  if (!lightbox.classList.contains('active')) return;
  lightbox.classList.remove('active');
  document.body.style.overflow = '';
  lbImg.src = '';

  if (!fromPopstate && history.state && history.state.lightbox) {
    try { history.back(); } catch (e) {}
  }

  const p = filteredPhotos[activeIndex];
  if (p) {
    const card = document.getElementById(`card-${p.filename}`);
    if (card) card.focus();
  }
}

window.addEventListener('popstate', () => {
  if (lightbox.classList.contains('active')) {
    closeLightbox(true);
  }
});

function nextPhoto() {
  activeIndex = (activeIndex + 1) % filteredPhotos.length;
  updateLightbox();
}

function prevPhoto() {
  activeIndex = (activeIndex - 1 + filteredPhotos.length) % filteredPhotos.length;
  updateLightbox();
}

function updateLightbox() {
  const p = filteredPhotos[activeIndex];
  if (!p) return;

  // Release memory for smart TVs
  if (preloadedNext) preloadedNext.src = '';
  if (preloadedPrev) preloadedPrev.src = '';

  // Load 100% full-bleed image
  lbImg.src = p.src;

  // Essential Caption ONLY: Title + Location & Date
  capTitle.textContent = p.title;
  capSub.textContent = `${p.place}  •  ${p.date_display}`;

  // Auto-hide HUD after 2.5s for pure unobstructed photo
  showHudBriefly();

  // Sync map in background
  if (p.lat && p.lon && map) {
    map.panTo([p.lat, p.lon], { animate: true, duration: 0.5 });
    highlightMarker(p.filename);
  }

  // Bidirectional Preload (next + previous)
  const nextIdx = (activeIndex + 1) % filteredPhotos.length;
  const prevIdx = (activeIndex - 1 + filteredPhotos.length) % filteredPhotos.length;
  preloadedNext = new Image();
  preloadedNext.src = filteredPhotos[nextIdx].src;
  preloadedPrev = new Image();
  preloadedPrev.src = filteredPhotos[prevIdx].src;
}

function showHudBriefly() {
  lbCaption.classList.remove('hidden');
  if (lbTopActions) lbTopActions.classList.remove('hidden');
  clearTimeout(captionTimer);
  captionTimer = setTimeout(() => {
    lbCaption.classList.add('hidden');
    if (lbTopActions) lbTopActions.classList.add('hidden');
  }, 2500);
}

function toggleHud() {
  clearTimeout(captionTimer);
  const isHidden = lbCaption.classList.toggle('hidden');
  if (lbTopActions) lbTopActions.classList.toggle('hidden', isHidden);
}

function toggleFullscreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen().catch(() => {});
  } else {
    document.exitFullscreen();
  }
}

// Event Listeners
function initEvents() {
  // Touch & Click Zones
  document.getElementById('zone-prev').addEventListener('click', (e) => {
    e.stopPropagation();
    prevPhoto();
  });

  document.getElementById('zone-next').addEventListener('click', (e) => {
    e.stopPropagation();
    nextPhoto();
  });

  document.getElementById('zone-center').addEventListener('click', (e) => {
    e.stopPropagation();
    toggleHud();
  });

  // Top Lightbox Buttons
  document.getElementById('btn-lb-close').addEventListener('click', () => closeLightbox());
  document.getElementById('btn-lb-fs').addEventListener('click', toggleFullscreen);

  // Mouse move inside lightbox restores HUD
  lightbox.addEventListener('mousemove', () => {
    if (lightbox.classList.contains('active')) {
      showHudBriefly();
    }
  });

  // Mouse wheel scroll to navigate (throttled 250ms)
  let wheelThrottle = 0;
  window.addEventListener('wheel', (e) => {
    if (!lightbox.classList.contains('active')) return;
    const now = Date.now();
    if (now - wheelThrottle < 250) return;
    if (Math.abs(e.deltaY) > 20 || Math.abs(e.deltaX) > 20) {
      wheelThrottle = now;
      if (e.deltaY > 0 || e.deltaX > 0) nextPhoto();
      else prevPhoto();
    }
  }, { passive: true });

  // Switch Views
  document.getElementById('btn-highlights').addEventListener('click', () => setView('highlights'));
  document.getElementById('btn-all').addEventListener('click', () => setView('all'));

  // Mobile Touch Swipe
  let touchStartX = 0;
  lightbox.addEventListener('touchstart', (e) => {
    if (e.touches && e.touches.length === 1) touchStartX = e.touches[0].clientX;
  }, { passive: true });

  lightbox.addEventListener('touchend', (e) => {
    if (e.changedTouches && e.changedTouches.length === 1) {
      const diffX = e.changedTouches[0].clientX - touchStartX;
      if (Math.abs(diffX) > 40) {
        if (diffX < 0) nextPhoto();
        else prevPhoto();
      }
    }
  }, { passive: true });

  // Keyboard & TV Remote
  window.addEventListener('keydown', (e) => {
    const isLb = lightbox.classList.contains('active');

    if (isLb) {
      if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === 'd' || e.key === 'D' || e.key === 'l' || e.key === 'L') {
        e.preventDefault();
        nextPhoto();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp' || e.key === 'a' || e.key === 'A' || e.key === 'h' || e.key === 'H') {
        e.preventDefault();
        prevPhoto();
      } else if (e.key === ' ' || e.key === 'i' || e.key === 'I') {
        e.preventDefault();
        toggleHud();
      } else if (e.key === 'Escape' || e.key === 'Backspace' || e.keyCode === 461 || e.keyCode === 10009) {
        // 461 = LG webOS Back, 10009 = Tizen Back
        e.preventDefault();
        closeLightbox();
      } else if (e.key === 'f' || e.key === 'F') {
        toggleFullscreen();
      }
    } else {
      if (e.key === '1') setView('highlights');
      if (e.key === '2') setView('all');
      if (e.key === 'f' || e.key === 'F') toggleFullscreen();
    }
  });
}

// Start
window.addEventListener('DOMContentLoaded', init);
