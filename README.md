# Oblivion Reloaded Lite

Unofficial Steam Deck-first performance profile and source fork of [TESReloaded10](https://github.com/llde/TESReloaded10) for The Elder Scrolls IV: Oblivion.

> **Status: source release candidate, not a verified binary release.** The profile and source changes are committed, but a Windows x86 build and in-game SteamOS/Proton testing are still required. No FPS, wattage or battery-life claims are made without Deck measurements.

## Design

- Retains the original xOBSE plugin and Direct3D 9 renderer.
- Keeps exterior near shadows and interior local shadows enabled.
- Reduces exterior near shadow maps from 4096 to 2048.
- Reduces interior shadow cube maps from 2048 to 1024 and shadowed interior light points from two to one.
- Keeps post-process shadows disabled.
- Disables optional God Rays, motion blur, POM, custom precipitation, WetWorld, volumetric fog and replacement water effects by default.
- Ambient occlusion was already disabled upstream and remains disabled.
- Disables the plugin's SmartControl FPS cap; use Steam's frame limiter instead.

## DXVK / Proton

The inherited source already contains the E3/upstream DXVK RESZ workaround in `TESReloaded/Core/RenderManager.cpp`: it saves and restores both the D3D9 FVF and vertex declaration around depth-buffer resolution. This fork adds COM reference cleanup for the acquired D3D9 state objects and DXVK interop interface, and logs DXVK detection. Detection is diagnostic only; it does not switch rendering APIs.

This is a 32-bit Windows xOBSE DLL loaded by Oblivion through Proton, not a native Linux plugin.

## Installation

1. Install and verify xOBSE in the same Proton prefix as Oblivion.
2. Back up existing Oblivion Reloaded/E3 files and configuration.
3. Extract the release ZIP into the game's `Data` directory, preserving folders.
4. Verify `Data/obse/Plugins/OblivionReloaded.dll` and its adjacent `OblivionReloaded.dll.config`.
5. Launch through Steam with xOBSE and inspect its logs/title-screen load message.

Do not install alongside another Oblivion Reloaded/E3 copy that supplies the same DLL.

## Steam Deck baseline

Start at 1280x800 with vanilla game graphics settings, normal TDP and the Lite config. Use Steam's frame limiter. Compare vanilla and Lite using the same save, location, camera, weather, time of day, Proton version and TDP.

See [docs/STEAM_DECK_PROFILE.md](docs/STEAM_DECK_PROFILE.md), [docs/BUILDING.md](docs/BUILDING.md) and [docs/TESTING.md](docs/TESTING.md).

## Credits and license

Unofficial derivative of TESReloaded10, originally created by Alenet and maintained by Llde. Preserve [License.md](License.md), [COPYING.txt](COPYING.txt) and third-party notices. Upstream terms require unofficial binaries to identify as unofficial, disclaim official-channel support, and prohibit selling binaries. **UNOFFICIAL BUILD — do not seek support through official TESReloaded channels.**
