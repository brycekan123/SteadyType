chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({ isAutocorrectEnabled: true });
});
