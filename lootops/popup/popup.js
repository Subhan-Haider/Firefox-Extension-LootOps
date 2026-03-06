/**
 * LootOps: Nebula HUD Logic
 */

const renderVault = (games, targetId, isUpcoming = false) => {
	const zone = document.getElementById(targetId);
	const label = zone.previousElementSibling;

	if (!games || games.length === 0) {
		zone.style.display = "none";
		if (label) label.style.display = "none";
		return;
	}

	zone.style.display = "block";
	if (label) label.style.display = "flex";
	zone.innerHTML = "";

	games.forEach((game, i) => {
		const rawPrice = (game.price?.totalPrice?.fmtPrice?.originalPrice || "0").replace(/[^0-9.]/g, '');
		const val = parseFloat(rawPrice) || 0;
		const isHot = val >= 20;
		const priceStr = game.price?.totalPrice?.fmtPrice?.originalPrice || "FREE";
		const platform = game.isSteam ? "STEAM" : "EPIC";
		const endT = isUpcoming ? game.startDate : game.endDate;
		const tid = `t-${targetId}-${i}`;

		let img = "";
		if (game.isSteam) {
			img = game.keyImages?.[0]?.url || "../icons/icon128.png";
		} else {
			const wide = game.keyImages?.find(o => o.type === "OfferImageWide")?.url || game.keyImages?.[0]?.url;
			img = img = (wide || game.keyImages?.[0]?.url) + "?h=200&resize=1";
		}

		let url = game.link;
		if (!url) {
			const slug = game.catalogNs?.mappings?.[0]?.pageSlug || game.productSlug || game.urlSlug;
			url = `https://store.epicgames.com/${game.offerType === "BUNDLE" ? "bundles/" : "p/"}${slug}`;
		}

		const panel = document.createElement("a");
		panel.className = "loot-panel";
		panel.href = url;
		panel.style.animationDelay = `${i * 0.08}s`;

		// Build panel structure
		const imgBox = document.createElement("div");
		imgBox.className = "img-box";
		const imgEl = document.createElement("img");
		imgEl.className = "img-actual";
		imgEl.src = img;
		imgEl.alt = game.title;
		imgBox.appendChild(imgEl);

		const badgeLayer = document.createElement("div");
		badgeLayer.className = "badge-layer";
		const platformChip = document.createElement("div");
		platformChip.className = "chip";
		platformChip.textContent = platform;
		badgeLayer.appendChild(platformChip);
		if (isHot) {
			const hotChip = document.createElement("div");
			hotChip.className = "chip hot-chip";
			hotChip.textContent = "HOT";
			badgeLayer.appendChild(hotChip);
		}
		imgBox.appendChild(badgeLayer);

		const content = document.createElement("div");
		content.className = "loot-content";
		const title = document.createElement("div");
		title.className = "loot-title";
		title.textContent = game.title;
		content.appendChild(title);

		const stats = document.createElement("div");
		stats.className = "loot-stats";
		const timerGroup = document.createElement("div");
		timerGroup.className = "timer-group";
		const timerTag = document.createElement("span");
		timerTag.className = "timer-tag";
		timerTag.textContent = isUpcoming ? 'Unlocks' : 'Expires';
		const timerTick = document.createElement("span");
		timerTick.id = tid;
		timerTick.className = "timer-tick";
		timerTick.textContent = "--:--:--";
		timerGroup.appendChild(timerTag);
		timerGroup.appendChild(timerTick);

		const pricePill = document.createElement("div");
		pricePill.className = "price-pill";
		pricePill.textContent = priceStr;
		stats.appendChild(timerGroup);
		stats.appendChild(pricePill);
		content.appendChild(stats);

		const shareBtn = document.createElement("button");
		shareBtn.className = "quick-share";
		shareBtn.title = "Share Intel";
		shareBtn.dataset.title = game.title;
		shareBtn.dataset.url = url;

		const shareSvg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
		shareSvg.setAttribute("viewBox", "0 0 24 24");
		shareSvg.setAttribute("width", "12");
		shareSvg.setAttribute("height", "12");
		shareSvg.setAttribute("fill", "none");
		shareSvg.setAttribute("stroke", "currentColor");
		shareSvg.setAttribute("stroke-width", "3");
		shareSvg.setAttribute("stroke-linecap", "round");
		shareSvg.setAttribute("stroke-linejoin", "round");
		const poly1 = document.createElementNS("http://www.w3.org/2000/svg", "path");
		poly1.setAttribute("d", "M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8");
		const poly2 = document.createElementNS("http://www.w3.org/2000/svg", "polyline");
		poly2.setAttribute("points", "16 6 12 2 8 6");
		const linesvg = document.createElementNS("http://www.w3.org/2000/svg", "line");
		linesvg.setAttribute("x1", "12"); linesvg.setAttribute("y1", "2");
		linesvg.setAttribute("x2", "12"); linesvg.setAttribute("y2", "15");
		shareSvg.appendChild(poly1); shareSvg.appendChild(poly2); shareSvg.appendChild(linesvg);
		shareBtn.appendChild(shareSvg);

		panel.appendChild(imgBox);
		panel.appendChild(content);
		panel.appendChild(shareBtn);

		// Timer Logic
		const el = timerTick;
		if (endT) {
			const target = new Date(endT).getTime();
			const tick = () => {
				const now = Date.now();
				const dist = target - now;
				if (!el) return;

				if (dist < 0) {
					el.textContent = isUpcoming ? "GO LIVE" : "ENDED";
					el.className = "timer-tick";
					return;
				}

				const d = Math.floor(dist / 86400000);
				const h = Math.floor((dist % 86400000) / 3600000);
				const m = Math.floor((dist % 3600000) / 60000);
				const s = Math.floor((dist % 60000) / 1000);

				if (!isUpcoming) {
					if (dist < 3600000) el.className = "timer-tick urgent";
					else if (dist < 86400000) el.className = "timer-tick expiring";
				}

				if (d > 0) el.textContent = `${d}D ${h}H ${m}M`;
				else el.textContent = `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
			};
			tick();
			setInterval(tick, 1000);
		} else if (game.isSteam) {
			if (el) el.textContent = "LIMITED TIME";
		}

		// Share Event
		shareBtn.addEventListener('click', (e) => {
			e.preventDefault(); e.stopPropagation();
			const btn = e.currentTarget;
			const text = `FREE LOOT! ${btn.dataset.title} is currently $0.00. Grab it: ${btn.dataset.url}`;
			navigator.clipboard.writeText(text).then(() => {
				const oldSvg = btn.querySelector('svg').cloneNode(true);
				btn.textContent = "COPIED";
				btn.style.width = "auto";
				btn.style.padding = "0 8px";
				setTimeout(() => {
					btn.textContent = "";
					btn.appendChild(oldSvg);
					btn.style.width = "24px";
					btn.style.padding = "0";
				}, 2000);
			});
		});

		panel.onclick = (e) => {
			if (e.target.closest('.quick-share')) return;
			e.preventDefault();
			chrome.tabs.create({ url, active: true });
		};

		zone.appendChild(panel);
	});
};

const setupSystem = () => {
	const pnl = document.getElementById("sys-pnl");
	const open = document.getElementById("gear-open");
	const close = document.getElementById("gear-close");
	const sync = document.getElementById("sync-btn");

	open.onclick = () => pnl.classList.add("active");
	close.onclick = () => pnl.classList.remove("active");

	const sws = {
		lightMode: document.getElementById("sw-theme"),
		notifications: document.getElementById("sw-notif"),
		showBadge: document.getElementById("sw-badge")
	};

	chrome.storage.local.get(["settings"]).then(res => {
		const s = res.settings || { lightMode: false, notifications: true, showBadge: true };

		if (s.lightMode) document.body.classList.add("light-mode");

		Object.keys(sws).forEach(k => {
			if (s[k]) sws[k].classList.add("on");
			else sws[k].classList.remove("on");

			sws[k].onclick = () => {
				sws[k].classList.toggle("on");
				s[k] = sws[k].classList.contains("on");

				if (k === 'lightMode') document.body.classList.toggle("light-mode", s[k]);
				chrome.storage.local.set({ settings: s });
			};
		});
	});

	sync.onclick = () => {
		const original = sync.innerText;
		sync.innerText = "SYNCING...";
		chrome.runtime.sendMessage("forceRefresh").then(() => {
			setTimeout(() => window.location.reload(), 1000);
		});
	};

	document.querySelectorAll('.dev-badge').forEach(a => {
		a.onclick = (e) => {
			e.preventDefault();
			chrome.tabs.create({ url: a.href, active: true });
		};
	});
};

// Execution
chrome.runtime.sendMessage("currentGames").then(data => {
	if (!data) return;
	renderVault(data.currentGames, "loot-active", false);
	renderVault(data.upcomingGames, "loot-upcoming", true);

	if (data.currentGames) {
		const total = data.currentGames.reduce((acc, g) => {
			const p = parseFloat((g.price?.totalPrice?.fmtPrice?.originalPrice || "0").replace(/[^0-9.]/g, '')) || 0;
			return acc + p;
		}, 0);
		document.getElementById("savings-pill").innerText = `SAVED $${total.toFixed(2)}`;
	}
});

setupSystem();
