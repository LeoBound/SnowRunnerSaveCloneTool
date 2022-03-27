# SnowRunner Save Clone Tool
Clones the first SnowRunner profile into the other slots.

Beware that saves in slots 2-4 will be overwritten (however, they are backed up first).

Make sure to set mode_egs in settings.json accordingly to select EGS/Steam mode.

If using steam your profile ID is required. To set this change steam_profile_id.

## What it does:

- First, any currently running SnowRunner.exe instance is killed.

- After this, and before making changes a backup is made in the same directory as the save file directory, and "_backup" is appended to this clone. To restore this just remove "_backup" from the directory name.

- The script will autorun SnowRunner.lnk or SnowRunner.url from this directory after completing.

## Known Issues

Sometimes the cloned saves will not appear in slots 2-4, to fix this create a new save in the slot where it was not cloned and rerun the script.

