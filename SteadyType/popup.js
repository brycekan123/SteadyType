document.addEventListener('DOMContentLoaded', () => {
  const toggleGlobalCheckbox = document.getElementById('toggle-correct');
  const domainCheckbox = document.getElementById('enable-domain');
  const globalStatusText = document.getElementById('global-status-text');
  const domainStatusText = document.getElementById('domain-status-text');

  // Get current tab domain
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const url = new URL(tabs[0].url);
    const currentDomain = url.hostname;

    // Initialize status from storage
    chrome.storage.sync.get(['globalEnabled', 'enabledDomains'], (data) => {
      const globalEnabled = data.globalEnabled || false;
      const enabledDomains = data.enabledDomains || [];
      const domainEnabled = enabledDomains.includes(currentDomain);

      toggleGlobalCheckbox.checked = globalEnabled;
      globalStatusText.textContent = globalEnabled ? 'Enabled Everywhere' : 'Disabled by Default';

      domainCheckbox.checked = domainEnabled;
      domainStatusText.textContent = globalEnabled ? 'Enabled Everywhere' : (domainEnabled ? 'Enabled for this Domain' : 'Disabled for this Domain');
      domainCheckbox.disabled = globalEnabled;
    });

    // Toggle SteadyType globally
    toggleGlobalCheckbox.addEventListener('change', () => {
      chrome.storage.sync.get(['globalEnabled', 'enabledDomains'], (data) => {
        const globalEnabled = data.globalEnabled;
        chrome.storage.sync.set({ globalEnabled: !globalEnabled }, () => {
          toggleGlobalCheckbox.checked = !globalEnabled;
          globalStatusText.textContent = !globalEnabled ? 'Enabled Everywhere' : 'Disabled by Default';

          domainCheckbox.disabled = !globalEnabled;
          domainStatusText.textContent = !globalEnabled ? 'Enabled Everywhere' : (domainCheckbox.checked ? 'Enabled for this Domain' : 'Disabled for this Domain');
        });
      });
    });

    // Toggle SteadyType for the current domain
    domainCheckbox.addEventListener('change', () => {
      chrome.storage.sync.get(['globalEnabled', 'enabledDomains'], (data) => {
        const globalEnabled = data.globalEnabled;
        if (!globalEnabled) {
          let enabledDomains = data.enabledDomains || [];
          const domainEnabled = enabledDomains.includes(currentDomain);

          if (domainEnabled) {
            // Remove the current domain from the list
            enabledDomains = enabledDomains.filter(domain => domain !== currentDomain);
          } else {
            // Add the current domain to the list
            enabledDomains.push(currentDomain);
          }

          // Update storage and UI with the modified domain list
          chrome.storage.sync.set({ enabledDomains: enabledDomains }, () => {
            domainCheckbox.checked = !domainEnabled;
            domainStatusText.textContent = !domainEnabled ? 'Enabled for this Domain' : 'Disabled for this Domain';
          });
        }
      });
    });
  });
});
