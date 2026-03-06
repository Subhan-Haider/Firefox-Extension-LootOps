# Privacy Policy for LootOps

**Last Updated: January 2026**

## 1. Introduction
LootOps ("we", "our", or "the extension") is a browser extension dedicated to helping users find free video games on the Epic Games Store and Steam. We are committed to protecting your privacy. This policy explains that we do **not** collect, store, or share any of your personal data.

## 2. No Data Collection
LootOps is built with a "Privacy First" architecture.
*   **We do not collect personal information**: We do not know your name, email, IP address, or location.
*   **We do not track browsing history**: The extension only interacts with specific game store URLs (`store.epicgames.com` and `store.steampowered.com`) solely to identify free game promotions. It does not monitor your activity on any other websites.
*   **We do not use analytics**: There are no third-party tracking scripts (e.g., Google Analytics, Mixpanel) embedded in the extension.

## 3. Local Storage Usage
LootOps uses your browser's local storage API (`chrome.storage.local`) strictly for functional purposes:
*   **Preferences:** To remember your settings (e.g., Dark Mode vs. Light Mode, Notification preferences).
*   **Cache:** To temporarily store the list of free games so the extension loads faster.

This data never leaves your device and is deleted if you uninstall the extension.

## 4. Permissions Usage
*   **Alarms:** Used only to schedule background checks for new games.
*   **Notifications:** Used only to alert you when a new free game is found.
*   **Host Permissions:** Used strictly to fetch public pricing data from Epic Games and Steam.

## 5. Third-Party Services
The extension communicates directly with:
*   **Epic Games Store API**: To fetch public game data.
*   **Steam Store**: To check for public discounts.

These requests are standard HTTP requests and are subject to the respective privacy policies of Epic Games and Valve Corporation. LootOps does not send any user-identifiable data to these services.

## 6. Contact
If you have questions about this policy, please open an issue on our GitHub repository:
https://github.com/Subhan-Haider/LootOps
