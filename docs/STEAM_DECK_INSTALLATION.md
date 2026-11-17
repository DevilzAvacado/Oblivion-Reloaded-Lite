# Steam Deck installation guide

This guide covers the Steam version of **The Elder Scrolls IV: Oblivion** running on SteamOS through Proton. Oblivion Reloaded Lite is a **32-bit Windows xOBSE plugin**. It is not a native Linux plugin.

## Requirements

- Steam version of the original 2006 Windows release of Oblivion.
- SteamOS with a Proton compatibility tool selected for Oblivion.
- A current xOBSE release compatible with Oblivion 1.2.0.416 (the project targets xOBSE 22 or newer).
- Oblivion Reloaded Lite release ZIP.
- Enough free space to keep a backup of the game launcher and existing mod files.

Do not use this guide for the newer Oblivion Remastered.

## 1. Create the Proton prefix

1. Install Oblivion from Steam.
2. Launch it once from Steam, allow it to reach the main menu, then exit.
3. In Steam, open **Oblivion → Properties → Compatibility** and select a Proton version.
4. Keep that Proton selection consistent while installing and testing xOBSE and Lite.

The first launch creates the game's Wine/Proton prefix. xOBSE and the game must run inside this same prefix.

## 2. Install xOBSE

1. Download the latest xOBSE release from the [xOBSE GitHub releases](https://github.com/llde/xOBSE/releases) or the [Oblivion Nexus xOBSE page](https://www.nexusmods.com/oblivion/mods/37952).
2. Switch the Steam Deck to Desktop Mode and open the downloaded archive.
3. In the archive, locate the Steam-version files:
   - `obse_1_2_416.dll`
   - `obse_editor_1_2.dll`
   - `obse_steam_loader.dll`
   - `obse_loader.exe`
   - the included `Data` folder
4. Copy these into the Oblivion game root (the folder containing `Oblivion.exe`). Merge the included `Data` folder with the game's existing `Data` folder.
5. Back up the original `OblivionLauncher.exe` by renaming it to `OblivionLauncher.exe.original` (or another name you will remember).
6. Rename `obse_loader.exe` to `OblivionLauncher.exe`.
7. Return to Gaming Mode and launch Oblivion from Steam.

The launcher replacement is the xOBSE-documented method for launching the Steam/Proton game through xOBSE. Do not delete the original launcher backup. To revert, remove the replacement `OblivionLauncher.exe` and restore the original filename.

**Verify xOBSE before continuing.** Start the game and confirm it reaches the main menu. If it does not, fix the xOBSE/Proton launch first; Lite cannot load until xOBSE is running.

## 3. Install Oblivion Reloaded Lite

1. Download `Oblivion-Reloaded-Lite-v0.2.0.zip` from the [Lite Releases page](https://github.com/DevilzAvacado/Oblivion-Reloaded-Lite/releases).
2. Extract the archive into the **Oblivion game root**, alongside `Oblivion.exe`. Do not extract it into the `Data` directory.
3. Allow the archive's `Data` directory to merge with the existing `Data` directory.
4. Confirm that these paths exist:
   - `Data/OBSE/Plugins/OblivionReloaded.dll`
   - `Data/OBSE/Plugins/OblivionReloaded.dll.config`
   - `Data/Shaders/OblivionReloaded/`
   - `Data/Textures/` (if present in the release archive)
5. Launch Oblivion from Steam.

The case of `OBSE` versus `obse` in the folder name is not significant on the usual Windows/Proton filesystem, but keep the archive's directory structure intact.

## 4. DLL override: not required for Lite

**Do not add a Proton DLL override for `OblivionReloaded.dll`.** It is an xOBSE plugin loaded by xOBSE from `Data/OBSE/Plugins`; it is not a Windows DLL proxy that replaces a system library.

Lite does not ship a `d3d9.dll` proxy. Proton supplies the Direct3D 9 translation layer (DXVK) for the game. Do not add `WINEDLLOVERRIDES=d3d9=n,b`, copy another `d3d9.dll` into the game root, or force a native Direct3D 9 DLL for this mod. Such overrides are only relevant when another separately installed mod or wrapper explicitly requires them.

## 5. First-launch behavior and configuration

- The first launch may take longer because the updated ambient-occlusion shader can be recompiled.
- Fresh configurations enable Lite's reduced-cost ambient occlusion profile.
- Existing configurations are preserved. If you already have `Data/OBSE/Plugins/OblivionReloaded.ini` and AO is disabled there, enable `Effects.AmbientOcclusion` rather than deleting the whole configuration.
- AO quality values are in `Data/Shaders/OblivionReloaded/Effects/Effects.ini`.
- Keep the initial test at default settings. Change one setting at a time if troubleshooting.

## 6. Avoid plugin conflicts

- Do not install Lite alongside another copy of Oblivion Reloaded/E3 that provides `OblivionReloaded.dll`.
- Remove or disable duplicate `OblivionReloaded.dll` files from other mod staging/deployment sources.
- Do not install the standalone Oblivion Reloaded AI Redone DLL beside Lite. It is a separate replacement plugin and is not a compatible add-on DLL.
- Keep a backup of the original game files and INI configuration before replacing an existing OR installation.

## 7. Troubleshooting

| Symptom | Check |
|---|---|
| Game launches but Lite has no effect | Confirm xOBSE launches first and that `OblivionReloaded.dll` is under `Data/OBSE/Plugins`. |
| Game fails before reaching the menu | Restore the original `OblivionLauncher.exe` and verify the xOBSE installation independently. |
| xOBSE works but Lite does not load | Check for a duplicate/conflicting OR plugin, confirm the DLL is in the correct folder, and inspect the xOBSE/plugin logs. |
| First launch appears slower | Allow the initial shader compilation to finish before judging subsequent launch time. |
| Visual artifacts or crashes | Restore the backed-up configuration, test without other graphics injectors, and record the Proton version and relevant logs. |

## 8. What is and is not validated

The project CI verifies a Windows x86 build, staging and ZIP packaging. It does **not** certify Steam Deck runtime behavior, visual correctness under every Proton/DXVK version, frame pacing, power draw or battery life. No FPS or battery-life gain is guaranteed.

For controlled testing, use the same save, location, weather, time of day, resolution, Proton version and SteamOS frame limiter. See [Steam Deck profile notes](STEAM_DECK_PROFILE.md) and [testing notes](TESTING.md).

## References

- [xOBSE README and Steam/Proton installation instructions](https://github.com/llde/xOBSE/blob/master/README.md)
- [xOBSE releases](https://github.com/llde/xOBSE/releases)
- [Oblivion Script Extender on Nexus Mods](https://www.nexusmods.com/oblivion/mods/37952)
