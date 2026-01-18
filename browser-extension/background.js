// FairProp Background Service Worker

chrome.runtime.onInstalled.addListener(() => {
    console.log('FairProp Compliance Checker installed');

    // Set default settings
    chrome.storage.sync.set({
        enabled: true,
        apiEndpoint: 'http://localhost:8000/api/scan'
    });
});

// Listen for messages from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'checkCompliance') {
        // Forward to API
        fetch(request.apiEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: request.text })
        })
            .then(response => response.json())
            .then(data => sendResponse({ success: true, data }))
            .catch(error => sendResponse({ success: false, error: error.message }));

        return true; // Keep channel open for async response
    }
});
