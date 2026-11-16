# Changelog

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
