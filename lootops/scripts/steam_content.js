/**
 * LootQuest: Steam Content Script
 * Supports discovery of free games
 */

const checkSteamFreebies = () => {
    if (typeof chrome === 'undefined' || !chrome.runtime?.id) return;

    const rows = document.querySelectorAll('a.search_result_row');
    const freebies = [];

    rows.forEach(row => {
        const discountPct = row.querySelector('.discount_pct');
        if (discountPct && discountPct.textContent.trim() === '-100%') {
            const title = row.querySelector('.title').textContent;
            const link = row.href;
            const img = row.querySelector('img')?.src;
            freebies.push({ title, link, img, platform: 'Steam' });
        }
    });

    if (freebies.length > 0) {
        chrome.runtime.sendMessage({ action: 'steamDiscovery', games: freebies }, () => {
            if (chrome.runtime.lastError) { /* Context invalidated */ }
        });
    }
};

// Initialize
if (document.readyState === 'complete') {
    checkSteamFreebies();
} else {
    window.addEventListener('load', () => {
        checkSteamFreebies();
    });
}
