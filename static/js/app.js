// app.js - Frontend logic for StreamLoop

document.addEventListener('DOMContentLoaded', () => {
    const carousel = document.getElementById('carousel');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const positionIndicator = document.getElementById('position-indicator');
    const selectedTitleEl = document.getElementById('selected-title');
    const detailsBtn = document.getElementById('details-btn');
    const resetBtn = document.getElementById('reset-btn');
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    const resultsContainer = document.getElementById('results-container');
    const searchResultsSection = document.getElementById('search-results');
    const categoryFilters = document.getElementById('category-filters');
    const infoToggle = document.getElementById('info-toggle');
    const infoContent = document.getElementById('info-content');
    const structureVisual = document.getElementById('structure-visual');
    const modal = document.getElementById('details-modal');
    const modalClose = document.getElementById('modal-close');

    let catalog = [];
    let current = null; // will store current item object
    let size = 0;
    let isLoading = false;

    const setLoading = (state) => {
        isLoading = state;
        prevBtn.disabled = state;
        nextBtn.disabled = state;
        detailsBtn.disabled = state || !current;
        resetBtn.disabled = state;
    };

    const fetchJSON = (url, options = {}) => fetch(url, options).then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
    });

    const loadCatalog = async () => {
        setLoading(true);
        try {
            const data = await fetchJSON('/api/catalog');
            catalog = data.items;
            current = data.current;
            size = data.size;
            renderCarousel();
            updateInfoPanel();
        } catch (e) {
            console.error('Failed to load catalog', e);
        } finally {
            setLoading(false);
        }
    };

    const renderCarousel = () => {
        carousel.innerHTML = '';
        catalog.forEach(item => {
            const card = document.createElement('div');
            card.className = 'card' + (current && item.id === current.id ? ' selected' : '');
            card.dataset.id = item.id;
            card.innerHTML = `
                <img src="${item.poster_url}" alt="${item.title}" onerror="this.src='/static/images/placeholder.svg'" />
                <div class="info">
                    <h3>${item.title}</h3>
                    <p>${item.release_year} • ${item.category}</p>
                </div>
            `;
            card.addEventListener('click', () => selectById(item.id));
            carousel.appendChild(card);
        });
        updatePosition();
        detailsBtn.disabled = !current;
    };

    const updatePosition = () => {
        const index = catalog.findIndex(i => current && i.id === current.id);
        const pos = index >= 0 ? index + 1 : 0;
        positionIndicator.textContent = `Item ${pos} of ${size}`;
        selectedTitleEl.textContent = current ? current.title : '';
    };

    const navigate = async (direction) => {
        if (isLoading) return;
        setLoading(true);
        try {
            const endpoint = direction === 'next' ? '/api/next' : '/api/previous';
            const data = await fetchJSON(endpoint, { method: 'POST' });
            current = data;
            renderCarousel();
        } catch (e) {
            console.error('Navigation error', e);
        } finally {
            setLoading(false);
        }
    };

    const selectById = async (id) => {
        if (isLoading) return;
        setLoading(true);
        try {
            const data = await fetchJSON(`/api/select/${id}`, { method: 'POST' });
            current = data;
            renderCarousel();
        } catch (e) {
            console.error('Select error', e);
        } finally {
            setLoading(false);
        }
    };

    const resetCatalog = async () => {
        if (isLoading) return;
        setLoading(true);
        try {
            await fetchJSON('/api/reset', { method: 'POST' });
            await loadCatalog();
        } catch (e) {
            console.error('Reset error', e);
        } finally {
            setLoading(false);
        }
    };

    const showDetails = () => {
        if (!current) return;
        document.getElementById('modal-poster').src = current.poster_url;
        document.getElementById('modal-title').textContent = current.title;
        document.getElementById('modal-description').textContent = current.description;
        document.getElementById('modal-year').textContent = current.release_year;
        document.getElementById('modal-genre').textContent = current.category;
        document.getElementById('modal-type').textContent = current.content_type;
        document.getElementById('modal-rating').textContent = current.rating;
        document.getElementById('modal-duration').textContent = current.duration;
        modal.hidden = false;
    };

    const hideModal = () => { modal.hidden = true; };

    const loadCategories = async () => {
        try {
            const cats = await fetchJSON('/api/categories');
            categoryFilters.innerHTML = '';
            const allChip = document.createElement('div');
            allChip.className = 'chip active';
            allChip.textContent = 'All';
            allChip.dataset.category = '';
            allChip.addEventListener('click', () => filterByCategory(''));
            categoryFilters.appendChild(allChip);
            cats.forEach(cat => {
                const chip = document.createElement('div');
                chip.className = 'chip';
                chip.textContent = cat;
                chip.dataset.category = cat;
                chip.addEventListener('click', () => filterByCategory(cat));
                categoryFilters.appendChild(chip);
            });
        } catch (e) { console.error('Categories load error', e); }
    };

    const filterByCategory = async (category) => {
        // Update active chip
        document.querySelectorAll('.chip').forEach(c => c.classList.toggle('active', c.dataset.category === category));
        if (!category) {
            await loadCatalog();
            return;
        }
        setLoading(true);
        try {
            const data = await fetchJSON(`/api/category/${encodeURIComponent(category)}`);
            catalog = data.items;
            // Keep existing current if it exists in filtered list, otherwise clear.
            if (current && !catalog.some(i => i.id === current.id)) current = null;
            size = catalog.length;
            renderCarousel();
        } catch (e) { console.error('Filter error', e); }
        finally { setLoading(false); }
    };

    const performSearch = async () => {
        const query = searchInput.value.trim();
        if (!query) return;
        setLoading(true);
        try {
            const data = await fetchJSON(`/api/search?q=${encodeURIComponent(query)}`);
            const results = data.results;
            resultsContainer.innerHTML = '';
            if (results.length === 0) {
                resultsContainer.textContent = 'No results found.';
            } else {
                results.forEach(item => {
                    const card = document.createElement('div');
                    card.className = 'card';
                    card.innerHTML = `
                        <img src="${item.poster_url}" alt="${item.title}" onerror="this.src='/static/images/placeholder.svg'" />
                        <div class="info"><h3>${item.title}</h3><p>${item.release_year} • ${item.category}</p></div>
                    `;
                    card.addEventListener('click', () => selectById(item.id));
                    resultsContainer.appendChild(card);
                });
            }
            searchResultsSection.hidden = false;
        } catch (e) { console.error('Search error', e); }
        finally { setLoading(false); }
    };

    const updateInfoPanel = async () => {
        // Show a simple textual representation of node order
        try {
            const data = await fetchJSON('/api/catalog');
            const ids = data.items.map(i => i.id);
            structureVisual.textContent = ids.join(' <-> ');
        } catch (e) { console.error('Info panel update error', e); }
    };

    // Event listeners
    prevBtn.addEventListener('click', () => navigate('previous'));
    nextBtn.addEventListener('click', () => navigate('next'));
    resetBtn.addEventListener('click', resetCatalog);
    detailsBtn.addEventListener('click', showDetails);
    modalClose.addEventListener('click', hideModal);
    window.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !modal.hidden) hideModal(); });
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') performSearch(); });
    infoToggle.addEventListener('click', () => {
        const expanded = !infoContent.hidden;
        infoContent.hidden = expanded;
        infoToggle.innerHTML = expanded ? 'How the Data Structure Works &#x25BC;' : 'How the Data Structure Works &#x25B2;';
    });

    // Initial load
    loadCatalog();
    loadCategories();
});
