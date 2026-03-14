import { openDB } from 'idb';

const DB_NAME = 'CitizensFormDB';
const STORE_NAME = 'sync-queue';

export const initDB = async () => {
  return openDB(DB_NAME, 1, {
    upgrade(db) {
      if (!db.objectStoreNames.contains(STORE_NAME)) {
        db.createObjectStore(STORE_NAME, { keyPath: 'id', autoIncrement: true });
      }
    },
  });
};

export const saveToSyncQueue = async (payload) => {
  const db = await initDB();
  const tx = db.transaction(STORE_NAME, 'readwrite');
  await tx.store.add({ ...payload, timestamp: Date.now() });
  await tx.done;
};

export const getSyncQueue = async () => {
  const db = await initDB();
  return db.getAll(STORE_NAME);
};

export const clearSyncItem = async (id) => {
  const db = await initDB();
  const tx = db.transaction(STORE_NAME, 'readwrite');
  await tx.store.delete(id);
  await tx.done;
};
