# User Workflow & Journey Mapping

## 1. Initial Access & Context Loading
1. The citizen user loads the web application on a mobile browser.
2. The deployed Service Worker instantly caches application UI assets silently into browser retention storage mapping.
3. Standard traditional application launches default view (e.g. dense layout featuring: "First Name", "Revenue Village", "Geographic Tehsil").

## 2. Interaction & Background Telemetry
4. The user begins navigating and filling the inputs.
5. Custom frontend React hooks latch onto `onKeyUp`, `onKeyDown`, and `onBlur` listeners. They aggregate keystroke dynamics quietly.
6. After interacting with ~2 fields, a JSON representation of behavioral metrics evaluates locally and forwards via Axios/Fetch API to the Flask classification endpoint.

## 3. Adaptive Layout Intervention
7. If the python backend grades the interaction footprint as belonging to a "Low Literacy" profile, it returns an affirmative intervention boolean flag.
8. The React frontend pops up an actionable, friendly localized modal: "This official form seems difficult. Want to try asking questions step-by-step?".
9. Changing mode strips off all extra fields and collapses layout into standard chat application components ("Aap kis district mein rehte ho?").

## 4. Smart Autofill Integration
10. The user begins spelling "Pau...".
11. The API fuzzy matches this prefix and pulls up "Pauri Garhwal", bypassing spelling errors entirely. 

## 5. Offline Resiliency Execution
12. Midway through filling, the local network connection drops.
13. The user continues. When hitting "Final Submit", the request realizes `navigator.onLine` is false.
14. The form payload bundles into `IndexedDB` queues labeled "SYNC_PENDING". 
15. A background web event listener waits. Upon detecting network restoration, the queue flushes its contents securely to the external server, signaling success seamlessly.
