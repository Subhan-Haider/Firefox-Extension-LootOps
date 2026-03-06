/**
 * LootOps: Epic Games Reminder
 * Source by Subhan Haider
 */

const APP_NAME = "LootOps";
const ACCENT_COLOR = "#8b5cf6"; // Violet color from CSS

const setNewBadge = () => {
	chrome.storage.local.get(["settings"]).then((result) => {
		const settings = result.settings || { showBadge: true };
		if (settings.showBadge !== false) {
			chrome.action.setBadgeBackgroundColor({ color: ACCENT_COLOR });
			chrome.action.setBadgeText({ text: "NEW" });
		}
	});
};

const saveLastCheckDate = () => {
	chrome.storage.local.set({ lastCheckDate: new Date().getTime() }, () => {
		if (chrome.runtime.lastError) {
			console.error("Error saving check date: ", chrome.runtime.lastError);
		}
	});
};

const getUpcomingGames = (jsonData) =>
	jsonData.data.Catalog.searchStore.elements
		.filter((e) =>
			e.promotions?.upcomingPromotionalOffers[0]?.promotionalOffers.some(
				(offer) => offer.discountSetting?.discountPercentage === 0
			)
		)
		.map(e => ({
			...e,
			startDate: e.promotions.upcomingPromotionalOffers[0].promotionalOffers.find(o => o.discountSetting.discountPercentage === 0)?.startDate
		}))
		.sort((a, b) => a.title.localeCompare(b.title));

const getCurrentGames = (jsonData) =>
	jsonData.data.Catalog.searchStore.elements
		.filter((e) =>
			e.promotions?.promotionalOffers[0]?.promotionalOffers.some(
				(offer) => offer.discountSetting?.discountPercentage === 0
			)
		)
		.map(e => ({
			...e,
			endDate: e.promotions.promotionalOffers[0].promotionalOffers.find(o => o.discountSetting.discountPercentage === 0)?.endDate
		}))
		.sort((a, b) => {
			const aEnd = new Date(a.endDate || 0);
			const bEnd = new Date(b.endDate || 0);
			return aEnd - bEnd;
		});

const getCurrentGamesEarliestStartDate = (currentGames) => {
	const startDates = currentGames.map(
		(e) =>
			new Date(
				e.promotions?.promotionalOffers[0]?.promotionalOffers.filter(
					(offer) => offer.discountSetting?.discountPercentage == 0
				)[0]?.startDate
			)
	);
	return new Date(Math.min(...startDates)).getTime();
};

const getCurrentGamesEarliestEndDate = (currentGames) => {
	const endDates = currentGames.map(
		(e) =>
			new Date(
				e.promotions?.promotionalOffers[0]?.promotionalOffers.filter(
					(offer) => offer.discountSetting?.discountPercentage == 0
				)[0]?.endDate
			)
	);
	return new Date(Math.min(...endDates)).getTime();
};

const fetchSteamGames = () => {
	return fetch("https://store.steampowered.com/search/?maxprice=free&specials=1")
		.then(response => response.text())
		.then(html => {
			const games = [];
			const rowRegex = /<a href="([^"]+)"[^>]*class="[^"]*search_result_row[^"]*"[^>]*>([\s\S]*?)<\/a>/g;
			const discountRegex = /discount_pct">-100%<\/div>/;
			const priceRegex = /<div class="discount_original_price">([^<]+)<\/div>/;
			const titleRegex = /<span class="title">([^<]+)<\/span>/;
			const imgRegex = /<img src="([^"]+)"/;

			let match;
			while ((match = rowRegex.exec(html)) !== null) {
				const rowHtml = match[2];
				if (discountRegex.test(rowHtml)) {
					const titleMatch = rowHtml.match(titleRegex);
					const imgMatch = rowHtml.match(imgRegex);
					const priceMatch = rowHtml.match(priceRegex);
					if (titleMatch) {
						games.push({
							title: titleMatch[1],
							link: match[1],
							img: imgMatch ? imgMatch[1] : "",
							originalPrice: priceMatch ? priceMatch[1].trim() : "FREE",
							platform: "Steam",
							isSteam: true
						});
					}
				}
			}
			console.log("Fetched from Steam: ", games.length, " games found");
			chrome.storage.local.set({ steamGames: games });
			return games;
		})
		.catch(error => {
			console.error("Error fetching Steam data: ", error);
			return [];
		});
};

const sendNotification = (title, message, items = []) => {
	chrome.storage.local.get(["settings"]).then((result) => {
		const settings = result.settings || { notifications: true };
		if (settings.notifications) {
			const opts = {
				type: "basic",
				iconUrl: "icons/icon128.png",
				title: title,
				message: message,
				priority: 2,
			};
			if (items.length > 0) {
				opts.type = "list";
				opts.items = items;
			}
			chrome.notifications.create(opts);
		}
	});
};

const fetchAPI = () =>
	fetch("https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions")
		.then((response) => response.json())
		.then((data) => {
			console.log("Fetched from Epic Games Store API");
			chrome.storage.local.set({ games: data });

			const currentGames = getCurrentGames(data);
			if (currentGames.length > 0) {
				const earliestStartDate = getCurrentGamesEarliestStartDate(currentGames);

				chrome.storage.local.get(["lastCheckDate"]).then((result) => {
					if (result?.lastCheckDate < earliestStartDate) {
						setNewBadge();
						const titles = currentGames.map(g => g.title).join(", ");
						sendNotification(`${APP_NAME}: New Supply Drop`, `Incoming Intel: ${titles} are now available.`);
					}
				});

				chrome.alarms.create("new-games-alarm", {
					when: getCurrentGamesEarliestEndDate(currentGames) + 60000,
				});
			}

			// Also fetch Steam when Epic is fetched
			return fetchSteamGames().then(() => data);
		})
		.catch((error) => {
			console.error("Error fetching data: ", error);
		});

// Notification handler
chrome.notifications.onClicked.addListener((notificationId) => {
	chrome.notifications.clear(notificationId);
	fetchAPI().then((jsonData) => {
		const currentGames = getCurrentGames(jsonData);
		currentGames.forEach((e) => {
			const gameId = e.catalogNs?.mappings
				? e.catalogNs.mappings[0]?.pageSlug || e.productSlug || e.urlSlug
				: e.productSlug || e.urlSlug;
			const url = "https://store.epicgames.com/" + (e.offerType === "BUNDLE" ? "bundles/" : "p/") + gameId;
			chrome.tabs.create({ url });
		});
		chrome.action.setBadgeText({ text: "" });
		saveLastCheckDate();
	});
});

chrome.alarms.onAlarm.addListener((alarm) => {
	if (alarm.name === "new-games-alarm") {
		chrome.storage.local.get(["settings"]).then((result) => {
			const settings = result.settings || { notifications: true, showBadge: true };

			if (settings.showBadge) setNewBadge();

			if (settings.notifications) {
				chrome.notifications.create({
					type: "basic",
					iconUrl: "icons/icon128.png",
					title: `${APP_NAME}: New Free Games!`,
					message: "Epic loot is waiting for you. Click here to claim your free games now!",
					priority: 2,
				});
			}
		});
	}
});

chrome.runtime.onInstalled.addListener((details) => {
	if (details.reason === chrome.runtime.OnInstalledReason.INSTALL) {
		setNewBadge();
		chrome.storage.local.set({ lastCheckDate: 0 });
	} else if (details.reason === chrome.runtime.OnInstalledReason.UPDATE) {
		fetchAPI();
	}
});

chrome.runtime.onStartup.addListener(() => {
	fetchAPI();
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
	if (request == "currentGames") {
		saveLastCheckDate();
		Promise.all([
			chrome.storage.local.get(["games"]),
			chrome.storage.local.get(["steamGames"])
		]).then(([epicResult, steamResult]) => {
			if (!epicResult.games) return fetchAPI().then(data => ({ epicData: data, steamData: steamResult.steamGames || [] }));

			const jsonData = epicResult.games;
			const currentGames = getCurrentGames(jsonData);
			const earliestEndDate = getCurrentGamesEarliestEndDate(currentGames);

			if (earliestEndDate < new Date().getTime()) {
				return fetchAPI().then(data => ({ epicData: data, steamData: steamResult.steamGames || [] }));
			}
			return { epicData: jsonData, steamData: steamResult.steamGames || [] };
		}).then(({ epicData, steamData }) => {
			if (epicData) {
				const currentGames = getCurrentGames(epicData);
				const upcomingGames = getUpcomingGames(epicData);

				// Format Steam games to match the UI structure
				const currentSteamGames = steamData.map(g => ({
					title: g.title,
					keyImages: [{ url: g.img, type: 'Thumbnail' }],
					productSlug: g.link, // We'll handle this in popup.js
					urlSlug: g.link,
					isSteam: true,
					link: g.link,
					platform: 'Steam',
					price: { totalPrice: { fmtPrice: { originalPrice: g.originalPrice || 'FREE', discountPrice: 'FREE' } } }
				}));

				sendResponse({
					currentGames: [...currentGames, ...currentSteamGames],
					upcomingGames,
					earliestEndDate: getCurrentGamesEarliestEndDate(currentGames),
				});
			}
		});
		return true;
	}

	if (request === "forceRefresh") {
		fetchAPI().then(() => sendResponse({ success: true }));
		return true;
	}

	if (request.action === 'steamDiscovery') {
		chrome.storage.local.get(['steamGames']).then(result => {
			const existing = result.steamGames || [];
			const newGames = request.games.filter(ng => !existing.some(eg => eg.link === ng.link));
			if (newGames.length > 0) {
				const names = newGames.map(g => g.title).join(", ");
				chrome.storage.local.set({ steamGames: [...existing, ...newGames] });
				setNewBadge();
				sendNotification(`${APP_NAME}: Steam Intel Acquired`, `Assets Secured: ${names}`);
			}
		});
	}
});
