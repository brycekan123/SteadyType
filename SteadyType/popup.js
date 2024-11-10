let isAutocorrectEnabled = false;

document.getElementById("toggle-correct").addEventListener("click", () => {
  isAutocorrectEnabled = !isAutocorrectEnabled;
  chrome.storage.local.set({ isAutocorrectEnabled }, () => {
    document.getElementById("toggle-correct").textContent = isAutocorrectEnabled
      ? "Disable Autocorrect"
      : "Enable Autocorrect";
  });
});
