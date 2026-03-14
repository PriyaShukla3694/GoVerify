# Technology Stack

This minimal stack guarantees extreme developer velocity for the 48-hour BLOCKATHON. All tools selected are free tier or open-source. 

## Frontend Engineering
- **Core Library**: React.js with Vite implementation for instant hot module reloading.
- **Offline Mechanisms**: Default Browser APIs: `navigator.onLine`, `IndexedDB`, and Vite PWA Plugin configuration to manage cache busting and Service Worker registration.
- **Styling**: Tailwind CSS purely for rapidly painting responsive UI boxes without manually touching CSS structure.

## Backend Engineering
- **Web App Framework**: Python Flask. Lean footprint, straightforward routing annotations without boilerplate bloat.
- **Security / Cross-Origin**: `flask-cors` plugin ensuring the Vite local dev server can query the Python API securely.
- **Package Management**: Standard `pip` utilizing `requirements.txt`.

## Data Science / Machine Learning
- **Algorithmic Engine**: `scikit-learn` to execute predictions.
- **Execution Loading**: Python's `joblib` object parser.
- **Math/Parsing**: `numpy` / `pandas` (only used off-server during the static data generation step).

## Database Storage
- **Protocol**: SQLite3. Ships natively with Python, meaning 0 network ports to bind, 0 docker instances, and total portability via `db.sqlite` files across devices.

## Demo / Presentation Deployment
- By executing Flask locally on `0.0.0.0`, the complete stack can be hosted to local wireless network judges securely. Mobile browser views connect purely via IP. This circumvents cloud platform signups and guarantees sub-millisecond network demo operations.
