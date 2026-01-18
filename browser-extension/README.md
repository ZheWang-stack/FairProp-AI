# FairProp Browser Extension

Real-time Fair Housing Act compliance checking for real estate platforms.

## Installation

### 1. Start the API Server

First, ensure the FairProp API is running:

```bash
cd /path/to/fairprop
python api_server.py
```

The API will start on `http://localhost:8000`

### 2. Load Extension in Chrome

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `browser-extension` folder from this project
5. The FairProp icon should appear in your extensions toolbar

## Usage

### Automatic Monitoring

The extension automatically monitors text fields on supported platforms:
- Zillow.com
- Realtor.com
- Redfin.com
- Trulia.com

Simply start typing in any listing description field, and FairProp will check for compliance in real-time.

### Manual Check

Click the FairProp icon in your toolbar to:
- See the current status
- Manually check any text by pasting it into the popup

## Supported Platforms

The extension works on major real estate platforms. To add more platforms, edit `manifest.json` and add the domain to the `content_scripts.matches` array.

## Troubleshooting

**"Connection Error" in popup:**
- Make sure the API server is running on `localhost:8000`
- Check that CORS is enabled in `api_server.py`

**Extension not working on a site:**
- Check if the site is in the `manifest.json` matches list
- Reload the extension after making changes

## Privacy

All compliance checks are performed locally. No data is sent to external servers.
