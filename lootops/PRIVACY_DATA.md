# Chrome Web Store Privacy & Permissions Data

## Single Purpose Description
The sole purpose of LootOps is to help users discover and claim free video games. It automatically checks the Epic Games Store and Steam for 100% off promotions and provides a unified dashboard ("HUD") to view and access these offers.

## Permission Justification

### `alarms`
**Justification:**
This permission is required to schedule background checks for new free games. The extension sets alarms to wake up the service worker periodically (e.g., when a known promotion is set to expire or refresh) to fetch the latest game data without requiring the user to keep the extension open.

### `notifications`
**Justification:**
This permission is used to send "Supply Drop" alerts to the user when a new free game becomes available. The extension respects user settings and only sends alerts for confirmed 100% off deals (e.g., "New Supply Drop Detected: Game Title").

### `storage`
**Justification:**
This permission is necessary to adapt the user experience. It stores:
1.  **User Preferences:** Theme choice (Light/Dark mode) and notification settings.
2.  **Cached Game Data:** The list of currently active free games to ensure the popup loads instantly without repeated API calls.
3.  **Last Check Timestamp:** To prevent redundant network requests and duplicate notifications.

### `Host Permissions` (e.g. `https://store.steampowered.com/*`)
**Justification:**
The extension needs to access:
1.  `https://store-site-backend-static-ipv4.ak.epicgames.com/*`: To fetch the official JSON data for Epic Games Store promotions.
2.  `https://store.steampowered.com/*`: To scan the Steam search results page for games with a "-100%" discount tag. This allows the extension to detect "hidden" free-to-keep Steam games that do not have a centralized API.

## Remote Code
**Answer:** No, I am not using Remote code.

## Data Usage Collection

### **What user data do you plan to collect?**
**None.**

*You should leave all checkboxes (Personally identifiable information, Health, Financial, etc.) **UNCHECKED**.*

The extension processes public game data locally. It does not collect, transmit, or store any user-specific data, browsing history, or personal information on any external server.

### **Certifications**
You must check **ALL THREE** boxes:
*   [x] I do not sell or transfer user data to third parties, outside of the approved use cases
*   [x] I do not use or transfer user data for purposes that are unrelated to my item's single purpose
*   [x] I do not use or transfer user data to determine creditworthiness or for lending purposes

## Privacy Policy URL
Since you are not collecting user data, you technically might not *require* a complex policy, but it is highly recommended to have one to pass review smoothly. You can use a GitHub Gist or a file in your repo.

**Suggested URL:** `https://github.com/Subhan-Haider/LootOps/blob/main/PRIVACY_POLICY.md`

*(Note: I will create this PRIVACY_POLICY.md file for you in the next step so this link becomes valid).*
