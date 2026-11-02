# Install Milk Pets

When the user asks you to install this repository's desktop pets, first identify the target app.

- For local Codex custom pets: run `python3 tools/install.py` from this repository to install all three. Use `--pet naiwa`, `--pet naiji`, or `--pet naishu` only when one pet was requested.
- The installer uses `CODEX_HOME/pets` if configured, otherwise the current user's `.codex/pets` directory. It verifies approved sprite hashes and v2 dimensions and refuses to overwrite a different existing version.
- For ChatGPT Work: import the selected `pets/<name>/spritesheet.png` through the user's supported custom-pet upload flow. Installing local files does not upload to ChatGPT Work.
- Verify the reported files exist and keep `spriteVersionNumber: 2`. Do not rename the sprite independently of `spritesheetPath`.
- Do not change the active pet or restart the app unless the user asks. Tell them to select the installed pet in the pet picker.
- Do not upload the user's other files or publish anything as part of installation.
