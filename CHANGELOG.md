# Changelog

## 0.3.0-beta.1 — Adaptive grass-distance preview

- Added an opt-in adaptive grass-distance controller to the existing grass-generation hook.
- Added configurable target frame rate and minimum grass-distance scale, with conservative input clamping.
- The controller smooths frame-time measurements, uses hysteresis to avoid rapid oscillation, and restores grass distance more slowly than it reduces it.
- Left the feature disabled by default pending real Steam Deck testing.
- Added static checks and a controlled A/B test protocol.
- Existing AO, DXVK RESZ handling, shadow defaults and Steam Deck profile remain unchanged.

**Pre-release status:** This beta adds the controller but leaves it disabled by default. The passing Windows x86 build and static checks do not validate grass transitions, actual frame-time gains, gameplay stability or power consumption on physical Steam Deck hardware.


## 0.2.0 — Lightweight ambient occlusion

- Enabled lightweight depth-aware ambient occlusion for fresh configurations.
- Reduced AO sampling to four depth samples.
- Reduced the separable blur to eight depth-aware taps per direction.
- Tuned AO radius and strength for restrained interior and exterior contact shading.
- Added shader staging so changed HLSL recompiles under the changed-or-missing shader compilation mode.
- Added profile checks for AO defaults and shader budget.

**Validation caveat:** The Windows x86 build and static profile checks do not establish in-game rendering correctness or Steam Deck performance, frame pacing, power draw or battery life.

## 0.1.0 — Steam Deck Lite source candidate

- Added conservative Steam Deck-oriented configuration defaults.
- Kept exterior and interior real-time shadow systems enabled.
- Reduced exterior near shadow-map size to 2048.
- Reduced interior shadow cube-map size to 1024 and shadowed light points to one.
- Disabled optional God Rays, motion blur, POM, custom precipitation, WetWorld, volumetric fog and replacement water effects.
- Kept ambient occlusion disabled.
- Disabled plugin SmartControl FPS cap to avoid competing with Steam's limiter.
- Preserved the inherited DXVK RESZ FVF/vertex-declaration restoration fix.
- Added COM reference cleanup and DXVK diagnostics.
- Added installation, build and validation documentation.

### Validation caveat

This is a source candidate, not a verified Steam Deck binary. Windows x86 compilation, xOBSE loading, Proton/DXVK rendering and real hardware performance measurements remain required.
