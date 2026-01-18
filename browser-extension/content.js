// FairProp Content Script - Monitors text input fields for compliance

(function () {
    'use strict';

    const API_ENDPOINT = 'http://localhost:8000/api/scan';
    let checkTimeout = null;
    const DEBOUNCE_DELAY = 1000; // Wait 1 second after typing stops

    // Create floating compliance indicator
    function createComplianceIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'fairprop-indicator';
        indicator.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      padding: 12px 20px;
      border-radius: 8px;
      background: #4CAF50;
      color: white;
      font-family: Arial, sans-serif;
      font-size: 14px;
      font-weight: bold;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      z-index: 10000;
      display: none;
      cursor: pointer;
      transition: all 0.3s ease;
    `;
        indicator.innerHTML = '✓ FairProp Active';
        document.body.appendChild(indicator);
        return indicator;
    }

    const indicator = createComplianceIndicator();

    // Show indicator briefly on page load
    indicator.style.display = 'block';
    setTimeout(() => {
        indicator.style.display = 'none';
    }, 3000);

    // Find all text input fields and textareas
    function findTextFields() {
        return document.querySelectorAll('textarea, input[type="text"], [contenteditable="true"]');
    }

    // Check text for compliance
    async function checkCompliance(text, element) {
        if (!text || text.length < 10) return;

        try {
            const response = await fetch(API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text })
            });

            if (!response.ok) {
                console.warn('FairProp API unavailable');
                return;
            }

            const result = await response.json();
            displayResults(result, element);
        } catch (error) {
            console.warn('FairProp check failed:', error);
        }
    }

    // Display compliance results
    function displayResults(result, element) {
        // Remove existing warnings
        const existingWarning = element.parentElement.querySelector('.fairprop-warning');
        if (existingWarning) {
            existingWarning.remove();
        }

        if (!result.is_safe) {
            const warning = document.createElement('div');
            warning.className = 'fairprop-warning';
            warning.style.cssText = `
        margin-top: 8px;
        padding: 12px;
        background: #fff3cd;
        border-left: 4px solid #ff9800;
        border-radius: 4px;
        font-size: 13px;
        color: #856404;
      `;

            let warningHTML = `<strong>⚠️ Compliance Warning (Score: ${result.score}/100)</strong><ul style="margin: 8px 0 0 0; padding-left: 20px;">`;

            result.flagged_items.slice(0, 3).forEach(item => {
                warningHTML += `<li><strong>${item.category}:</strong> "${item.found_word}" - ${item.suggestion}</li>`;
            });

            if (result.flagged_items.length > 3) {
                warningHTML += `<li><em>...and ${result.flagged_items.length - 3} more issues</em></li>`;
            }

            warningHTML += '</ul>';
            warning.innerHTML = warningHTML;

            element.parentElement.insertBefore(warning, element.nextSibling);

            // Update indicator
            indicator.style.background = '#ff9800';
            indicator.innerHTML = `⚠️ ${result.flagged_items.length} Issue${result.flagged_items.length > 1 ? 's' : ''}`;
            indicator.style.display = 'block';
        } else {
            // All clear
            indicator.style.background = '#4CAF50';
            indicator.innerHTML = '✓ Compliant';
            indicator.style.display = 'block';
            setTimeout(() => {
                indicator.style.display = 'none';
            }, 2000);
        }
    }

    // Monitor text fields
    function monitorField(field) {
        field.addEventListener('input', function () {
            clearTimeout(checkTimeout);
            checkTimeout = setTimeout(() => {
                const text = field.value || field.textContent;
                checkCompliance(text, field);
            }, DEBOUNCE_DELAY);
        });
    }

    // Initialize monitoring
    function init() {
        const fields = findTextFields();
        fields.forEach(monitorField);

        // Watch for dynamically added fields
        const observer = new MutationObserver(() => {
            const newFields = findTextFields();
            newFields.forEach(field => {
                if (!field.dataset.fairpropMonitored) {
                    field.dataset.fairpropMonitored = 'true';
                    monitorField(field);
                }
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    // Start when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    console.log('FairProp Compliance Checker loaded');
})();
