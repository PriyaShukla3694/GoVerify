import { getSyncQueue, clearSyncItem } from './offlineStorage';

export const syncOfflineData = async () => {
  if (!navigator.onLine) return; // Prevent dispatch if offline

  const pendingForms = await getSyncQueue();
  if (pendingForms.length === 0) return;

  console.log(`SyncManager: Found ${pendingForms.length} offline items to sync.`);

  for (const item of pendingForms) {
    try {
      const response = await fetch('http://localhost:5000/api/v1/form/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: item.session_id,
          payload: item.payload,
          metadata: { ...item.metadata, background_synced: true }
        })
      });

      if (response.ok) {
        console.log(`Successfully synced offline form ID: ${item.id}`);
        await clearSyncItem(item.id);
      }
    } catch (e) {
      console.warn("Sync failed. Server unreachable, will try later.");
      break; 
    }
  }
};

// Global listener initialization attached straight to the window
export const initSyncListeners = () => {
    window.addEventListener('online', () => {
        console.log("Network online. Triggering synchronization pipeline.");
        syncOfflineData();
    });
};
