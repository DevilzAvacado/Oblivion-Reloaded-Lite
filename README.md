# Oblivion Reloaded Lite

**Oblivion Reloaded Lite** is an unofficial, Steam Deck-oriented fork/profile of [TESReloaded10](https://github.com/llde/TESReloaded10) for *The Elder Scrolls IV: Oblivion*. It aims to retain useful dynamic lighting and shadow features while reducing the cost of optional rendering effects.

This project is a **32-bit Windows xOBSE plugin** intended to run with the Windows version of Oblivion under SteamOS/Proton. It is not a native Linux renderer or a standalone mod manager.

> **Build status: 0.2.0 builds successfully.** The Windows x86 CI workflow has compiled the Configurator and plugin, staged the installable files, and produced the release ZIP. Steam Deck in-game compatibility, visual quality, frame pacing, power draw and battery life have **not yet been validated on physical hardware**. No performance improvement is guaranteed.

## Project goals

- Preserve Oblivion Reloaded's exterior and interior shadowing systems.
- Use a lower-cost default configuration suitable as a starting point for Steam Deck testing.
- Keep optional post-processing and weather effects disabled unless a user deliberately enables them.
- Preserve the Direct3D 9 / DXVK depth-buffer compatibility path.
- Provide reproducible Windows x86 builds and a straightforward ZIP installation.

## What's included

### Lite graphics profile

The shipped configuration is deliberately conservative:

| Setting | Lite default |
| --- | --- |
| Exterior near shadow map | 2048 |
| Interior shadow cube map | 1024 |
| Shadowed interior light points | 1 |
| Exterior and interior shadow systems | Enabled |
| Post-process shadows | Disabled |
| Ambient occlusion | Enabled (4 samples, 8-tap separable blur) |
| God Rays, motion blur, POM | Disabled |
| Custom precipitation, WetWorld, volumetric fog, replacement water | Disabled |
| SmartControl frame-rate limiter | Disabled |

These are configuration choices, not measured performance results. Main options are stored in `Data/OBSE/Plugins/OblivionReloaded.ini`; AO quality values are stored in `Data/Shaders/OblivionReloaded/Effects/Effects.ini`.

### Adaptive grass distance (opt-in)

The current development branch includes an opt-in controller that gradually scales grass fade/end distances when smoothed frame times remain above a configurable target. It is disabled by default until visual behavior and performance are validated on physical Steam Deck hardware. See [ORSE feature audit and development decisions](docs/ORSE_FEATURE_AUDIT.md).

### Lightweight ambient occlusion

AO is enabled by default for fresh configurations with a deliberately reduced shader workload:

- Four depth samples in the AO pass.
- Eight depth-aware taps per blur direction (horizontal and vertical), down from twelve.
- Shorter sampling and blur radii with restrained interior/exterior strength.
- The existing depth-aware blur and fog fade are retained.

The updated HLSL source is staged newer than its cached shader binary so the default `CompileEffects = 2` setting recompiles the effect on first launch. This can cause a one-time shader compilation delay. Existing user INI values are preserved; users with an existing configuration that explicitly disables AO must enable `Effects.AmbientOcclusion` in `Data/OBSE/Plugins/OblivionReloaded.ini`. No Steam Deck performance measurements are claimed until tested on hardware.

### DXVK / Proton handling

The inherited source includes a DXVK RESZ depth-buffer workaround in `TESReloaded/Core/RenderManager.cpp`. It preserves and restores the Direct3D 9 FVF and vertex declaration around depth-buffer resolution. This fork adds COM reference cleanup for acquired D3D9 state objects and the DXVK interop interface, along with diagnostic DXVK detection.

DXVK detection is diagnostic; it does not replace or switch the rendering backend.

## Requirements

- The Windows version of *The Elder Scrolls IV: Oblivion*.
- A working xOBSE installation in the same game/Proton prefix.
- SteamOS/Proton for Steam Deck use, or a compatible Windows environment.
- No other Oblivion Reloaded/E3 installation providing the same plugin DLL.

## Installation

1. Install and verify xOBSE first. Confirm the game launches with xOBSE before adding this plugin.
2. Back up your current Oblivion Reloaded/E3 files and configuration.
3. Download the `Oblivion-Reloaded-Lite-v0.2.0.zip` asset from the [Releases page](https://github.com/DevilzAvacado/Oblivion-Reloaded-Lite/releases).
4. Extract the ZIP into the **Oblivion game root** (the folder containing `Oblivion.exe`), preserving the archive's folder structure. Do not extract it into `Data`.
5. Confirm these files exist:
   - `Data/OBSE/Plugins/OblivionReloaded.dll`
   - `Data/OBSE/Plugins/OblivionReloaded.dll.config`
6. Launch Oblivion through Steam with xOBSE. Check the xOBSE and plugin logs if the plugin does not load.

**Steam Deck users:** follow the separate [Steam Deck installation guide](docs/STEAM_DECK_INSTALLATION.md), including the Proton/xOBSE launcher setup and first-launch checks.

Do not install this alongside another Oblivion Reloaded/E3 copy that provides the same DLL. Remove the Lite files and restore your backup to roll back.

## Steam Deck testing baseline

For a controlled comparison:

- Start at 1280×800, with the same in-game graphics settings for each test.
- Keep the Proton version, TDP, frame-rate cap and refresh rate unchanged.
- Compare vanilla and Lite from the same save, location, camera angle, weather and time of day.
- Check for rendering errors, missing shadows, crashes and frame-time instability before changing the profile.
- Record FPS/frame times and power draw rather than relying on subjective impressions.

See [Steam Deck profile/testing notes](docs/STEAM_DECK_PROFILE.md), [build instructions](docs/BUILDING.md) and [testing notes](docs/TESTING.md).

## Building from source

The project includes a Windows x86 GitHub Actions build workflow. For local build prerequisites and commands, see [docs/BUILDING.md](docs/BUILDING.md).

The CI build for 0.2.0 completed successfully, including Configurator compilation, plugin compilation, staging and ZIP packaging. This verifies that the source can be built by that workflow; it does not establish that the plugin works correctly in-game on Steam Deck.

## Project status and limitations

- **Implemented:** conservative Lite configuration, retained DXVK RESZ path, COM cleanup, CI profile checks, Windows x86 build and ZIP packaging.
- **Not yet verified:** installation and runtime behavior in an actual SteamOS/Proton game session; visual correctness across interiors/exteriors; frame pacing; GPU/CPU load; wattage and battery impact.
- **Not claimed:** a specific FPS gain, lower wattage, longer battery life or universal compatibility.

Report reproducible issues with the game version, xOBSE version, Proton version, Deck model, relevant configuration and logs.

## Credits and license

This is an unofficial derivative of [TESReloaded10](https://github.com/llde/TESReloaded10), originally created by Alenet and maintained by Llde. Retain [License.md](License.md), [COPYING.txt](COPYING.txt) and all third-party notices when redistributing.

Upstream licensing terms require unofficial binaries to identify themselves as unofficial or use a distinct product name/description, prohibit selling binaries, and exclude support through official TESReloaded channels.

**UNOFFICIAL BUILD — not affiliated with or supported by the official TESReloaded project.**
