import dropbox
from dropbox.oauth import DropboxOAuth2FlowNoRedirect
import json
from pathlib import Path

# Replace these with your actual Dropbox app credentials
APP_KEY = "jkn74wm0egbajhe"
APP_SECRET = "6hs5wdiz4ilq38d"
CONFIG_PATH = Path("config.json")


def generate_tokens():
    auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET, token_access_type='offline')

    print("1. Go to this URL and click 'Allow':")
    print(auth_flow.start())
    print("2. Copy the authorization code Dropbox gives you.")
    auth_code = input("3. Paste the authorization code here: ").strip()

    try:
        oauth_result = auth_flow.finish(auth_code)
    except Exception as e:
        print("❌ Error obtaining token:", e)
        return

    # New token fields
    dropbox_tokens = {
        "dropbox_access_token": oauth_result.access_token,
        "dropbox_refresh_token": oauth_result.refresh_token,
        "dropbox_account_id": oauth_result.account_id}



    # Load existing config or start fresh
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
    else:
        config = {}

    # Update only Dropbox-related fields
    config.update(dropbox_tokens)

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

    print("✅ Dropbox tokens saved to config.json (merged with existing config)")
    print("Temporary Access Token:", oauth_result.access_token)
    print("Refresh Token (for long-term use):", oauth_result.refresh_token)


if __name__ == "__main__":
    generate_tokens()
