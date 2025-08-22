import os
import dropbox
from pathlib import Path
from datetime import datetime, timezone, timedelta
import json


class DropboxVideoFetcher:
    def __init__(self, access_token, dropbox_root="/", local_root="videos", modified_within_days=2, refresh_token=None,
                 app_key=None, app_secret=None):
        # Use refresh token if available for automatic token renewal
        if refresh_token and app_key:
            self.dbx = dropbox.Dropbox(
                oauth2_access_token=access_token,
                oauth2_refresh_token=refresh_token,
                app_key=app_key,
                app_secret=app_secret
            )
        else:
            self.dbx = dropbox.Dropbox(access_token)

        self.dropbox_root = dropbox_root
        self.local_root = local_root
        self.modified_within_days = modified_within_days  # Keep as fallback
        self.timestamp_file = Path(local_root) / ".last_sync_timestamp"

        # Get last sync time or use fallback
        self.cutoff_date = self._get_last_sync_time()

    def _get_last_sync_time(self):
        """Get the last sync timestamp or fall back to days-based cutoff."""
        if self.timestamp_file.exists():
            try:
                with open(self.timestamp_file, 'r') as f:
                    timestamp_str = f.read().strip()
                    return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            except (ValueError, IOError):
                print("⚠ Could not read last sync timestamp, using fallback")

        # Fallback to days-based cutoff for first run
        from datetime import timedelta
        fallback_time = datetime.now(timezone.utc) - timedelta(days=self.modified_within_days)
        print(f"📅 Using fallback cutoff: {fallback_time.isoformat()}")
        return fallback_time

    def _save_sync_timestamp(self):
        """Save the current timestamp as the last sync time."""
        current_time = datetime.now(timezone.utc)
        os.makedirs(self.timestamp_file.parent, exist_ok=True)
        with open(self.timestamp_file, 'w') as f:
            f.write(current_time.isoformat())
        print(f"💾 Saved sync timestamp: {current_time.isoformat()}")

    def sync_videos(self):
        if not self.verify_and_suggest_path():
            return 0
        print(f"🔍 Scanning Dropbox for videos modified after: {self.cutoff_date.isoformat()}")
        download_count = self._scan_folder(self.dropbox_root)

        # Only update timestamp if sync completed successfully
        self._save_sync_timestamp()
        print(f"✅ Sync completed. Downloaded {download_count} new videos.")
        return download_count

    def list_available_folders(self):
        """List all folders in the Dropbox root to help identify the correct path."""
        print("🔍 Scanning Dropbox root directory for available folders:")
        try:
            result = self.dbx.files_list_folder("")
            folders_found = []
            for entry in result.entries:
                if isinstance(entry, dropbox.files.FolderMetadata):
                    folders_found.append(entry.name)
                    print(f"  📁 {entry.name}")

            if not folders_found:
                print("  ⚠️ No folders found in Dropbox root")
            return folders_found
        except Exception as e:
            print(f"❌ Could not list root folders: {e}")
            return []

    def verify_and_suggest_path(self):
        """Verify if the configured path exists, suggest alternatives if not."""
        try:
            self.dbx.files_get_metadata(self.dropbox_root)
            print(f"✅ Path verified: {self.dropbox_root}")
            return True
        except dropbox.exceptions.ApiError as e:
            if e.error.is_path() and e.error.get_path().is_not_found():
                print(f"❌ Path not found: {self.dropbox_root}")
                print("\nAvailable folders in your Dropbox root:")
                available_folders = self.list_available_folders()

                # Suggest likely matches
                suggestions = [f for f in available_folders if 'bird' in f.lower() or 'video' in f.lower()]
                if suggestions:
                    print(f"\n💡 Suggested paths based on folder names:")
                    for folder in suggestions:
                        print(f"  → /{folder}")

                return False
            else:
                print(f"❌ Unexpected error checking path: {e}")
                return False

    def _scan_folder(self, folder_path):
        download_count = 0
        try:
            result = self.dbx.files_list_folder(folder_path)
            entries = result.entries

            while True:
                for entry in entries:
                    if isinstance(entry, dropbox.files.FileMetadata):
                        # Convert naive datetime to UTC for comparison
                        entry_modified_utc = entry.client_modified.replace(tzinfo=timezone.utc)

                        if entry.name.endswith(".mp4") and entry_modified_utc > self.cutoff_date:
                            species = Path(entry.path_display).parts[-2]
                            if self._download_video(entry.path_display, species):
                                download_count += 1
                    elif isinstance(entry, dropbox.files.FolderMetadata):
                        download_count += self._scan_folder(entry.path_display)

                if result.has_more:
                    result = self.dbx.files_list_folder_continue(result.cursor)
                    entries = result.entries
                else:
                    break
        except dropbox.exceptions.ApiError as e:
            print(f"❌ Error scanning folder {folder_path}: {e}")

        return download_count

    def _download_video(self, dropbox_path, species_folder):
        local_dir = Path(self.local_root) / species_folder
        local_dir.mkdir(parents=True, exist_ok=True)
        filename = Path(dropbox_path).name
        local_path = local_dir / filename

        if local_path.exists():
            print(f"⏭ Skipping existing: {local_path}")
            return False

        print(f"⬇ Downloading: {dropbox_path} -> {local_path}")
        try:
            with open(local_path, "wb") as f:
                metadata, res = self.dbx.files_download(dropbox_path)
                f.write(res.content)
            return True
        except Exception as e:
            print(f"❌ Download failed for {dropbox_path}: {e}")
            return False