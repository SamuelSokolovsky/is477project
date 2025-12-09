# Kaggle API Setup Guide

This guide explains how to set up Kaggle API authentication to download Dataset 1 (ESPN Soccer Data).

## Why You Need This

Dataset 1 is hosted on Kaggle and requires authentication to download. Without Kaggle credentials, the project will automatically skip Dataset 1 and use only Dataset 2 (GitHub data).

## Getting Your Kaggle API Credentials

### Step 1: Create/Login to Kaggle Account
1. Go to [kaggle.com](https://www.kaggle.com)
2. Create an account or log in

### Step 2: Generate API Token
1. Go to your account settings: https://www.kaggle.com/settings
2. Scroll down to the "API" section
3. Click **"Create New Token"**
4. This will download a file called `kaggle.json`

### Step 3: View Your Credentials
Open the downloaded `kaggle.json` file. It will look like this:
```json
{
  "username": "your_username",
  "key": "your_api_key_here"
}
```

## Authentication Methods

You have **three options** to provide your credentials:

### Option 1: Environment Variables (Recommended)

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   KAGGLE_USERNAME=your_username
   KAGGLE_KEY=your_api_key
   ```

3. The `.env` file is git-ignored and will NOT be committed

### Option 2: kaggle.json File

Place your `kaggle.json` file in the appropriate location:

- **Linux/Mac**: `~/.kaggle/kaggle.json`
- **Windows**: `C:\Users\<YourUsername>\.kaggle\kaggle.json`

Make sure the file has proper permissions (Unix/Mac):
```bash
chmod 600 ~/.kaggle/kaggle.json
```

### Option 3: Set Environment Variables Manually

**Linux/Mac:**
```bash
export KAGGLE_USERNAME=your_username
export KAGGLE_KEY=your_api_key
```

**Windows (PowerShell):**
```powershell
$env:KAGGLE_USERNAME="your_username"
$env:KAGGLE_KEY="your_api_key"
```

**Windows (Command Prompt):**
```cmd
set KAGGLE_USERNAME=your_username
set KAGGLE_KEY=your_api_key
```

## Verifying Setup

Run the data acquisition script:
```bash
python scripts/01_acquire.py
```

If successful, you should see:
- "Kaggle API credentials found"
- Dataset 1 files downloading

If credentials are missing, you'll see warnings and Dataset 1 will be skipped (the pipeline will still work with Dataset 2 only).

## Troubleshooting

### "Kaggle API credentials not found"
- Check that `.env` file exists and has correct format
- Or check that `kaggle.json` is in the right location
- Make sure there are no typos in your credentials

### "401 Unauthorized"
- Your API key may be incorrect
- Try generating a new token from Kaggle settings

### "403 Forbidden"
- You may need to accept the dataset's terms on Kaggle website
- Visit: https://www.kaggle.com/datasets/excel4soccer/espn-soccer-data
- Click "Download" to accept terms

## Security Notes

- **NEVER commit** `.env` or `kaggle.json` to version control
- These files are already in `.gitignore`
- Don't share your API key publicly
- You can regenerate your token anytime from Kaggle settings

## Sources

- [Kaggle API Documentation](https://www.kaggle.com/docs/api)
- [KaggleHub GitHub](https://github.com/Kaggle/kagglehub)
- [Kaggle API GitHub](https://github.com/Kaggle/kaggle-api)
