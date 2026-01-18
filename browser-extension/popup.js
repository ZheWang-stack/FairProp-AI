// FairProp Popup Script

const API_ENDPOINT = 'http://localhost:8000/api/scan';

document.getElementById('checkBtn').addEventListener('click', async () => {
    const text = document.getElementById('textInput').value;
    const resultDiv = document.getElementById('result');
    const button = document.getElementById('checkBtn');

    if (!text.trim()) {
        resultDiv.className = 'warning';
        resultDiv.textContent = 'Please enter some text to check';
        resultDiv.style.display = 'block';
        return;
    }

    button.textContent = 'Checking...';
    button.disabled = true;

    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text })
        });

        if (!response.ok) {
            throw new Error('API unavailable');
        }

        const result = await response.json();

        if (result.is_safe) {
            resultDiv.className = 'safe';
            resultDiv.innerHTML = `<strong>✓ Compliant</strong><br>Score: ${result.score}/100`;
        } else {
            resultDiv.className = 'warning';
            let html = `<strong>⚠️ Issues Found (Score: ${result.score}/100)</strong><ul style="margin: 8px 0 0 0; padding-left: 20px; font-size: 12px;">`;

            result.flagged_items.slice(0, 3).forEach(item => {
                html += `<li>${item.category}: "${item.found_word}"</li>`;
            });

            if (result.flagged_items.length > 3) {
                html += `<li><em>+${result.flagged_items.length - 3} more</em></li>`;
            }

            html += '</ul>';
            resultDiv.innerHTML = html;
        }

        resultDiv.style.display = 'block';

    } catch (error) {
        resultDiv.className = 'warning';
        resultDiv.innerHTML = '<strong>⚠️ Connection Error</strong><br>Make sure FairProp API is running on localhost:8000';
        resultDiv.style.display = 'block';
    } finally {
        button.textContent = 'Check Compliance';
        button.disabled = false;
    }
});
