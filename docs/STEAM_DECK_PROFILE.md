# Steam Deck Lite profile

## Kept on

| Feature | Default | Purpose |
|---|---:|---|
| Exterior near shadows | On | Outdoor shadow improvement |
| Interior local shadows | On | Indoor lighting improvement |
| Interior torch shadows | On | Local-light definition |
| HDR pipeline | On | Retains existing tone-mapping path |
| Frustum culling | On | Avoids processing off-screen geometry |
| Anisotropic filtering | 8x | Texture clarity |
| Lightweight ambient occlusion | On | Subtle depth-aware contact shading with reduced shader sampling |

## Reduced

| Setting | Upstream | Lite |
|---|---:|---:|
| Exterior near shadow map | 4096 | 2048 |
| Interior shadow cube map | 2048 | 1024 |
| Interior shadowed light points | 2 | 1 |

Exterior far-shadow settings and caster selections remain inherited. If profiling still shows high cost, adjust shadow distance and caster coverage only after visual comparisons.

## Disabled by default

- God Rays / light shafts.
- Motion blur.
- Parallax occlusion mapping.
- Custom rain/snow shader.
- WetWorld puddles.
- Volumetric fog.
- Replacement water shader.
- Plugin SmartControl FPS cap.

These remaining optional effects are defaults, not hard-coded restrictions. They can be enabled through the configuration if desired.

## Adaptive grass distance (opt-in)

The plugin includes an adaptive grass-distance controller for testing on constrained hardware. It does not change grass density or replace the grass shader. Instead, it gradually scales the start-fade and end distances passed to the existing grass-generation routine.

The controller is disabled by default because its visual behavior and performance impact have not yet been measured on physical Steam Deck hardware. To test it, edit `Data/OBSE/Plugins/OblivionReloaded.ini`:

```toml
[Main]
AdaptiveGrassDistance = true
GrassTargetFrameRate = 60
GrassMinimumDistanceScale = 0.65
```

The controller uses a smoothed frame-time estimate and hysteresis. It reduces distance after sustained frame times exceed the target by 10%, then restores distance more slowly after frame times recover. Valid target rates are 30–90 FPS; the minimum distance multiplier is constrained to 0.40–0.90. Invalid values fall back to conservative defaults.

This is an opt-in quality adjustment, not a claim of guaranteed FPS improvement. Check for visible grass-distance transitions, repeated oscillation, missing grass at cell boundaries, and changes between interiors and exteriors. Keep the feature disabled if it causes distracting changes.

## Frame pacing

Use SteamOS's per-game frame limiter rather than running a second limiter in the plugin. Pick a target only after establishing a stable baseline.

## Notes

Reduced shadow-map dimensions lower map memory use and render-target cost, but do not guarantee proportional FPS or wattage gains. Disabled effects can change water, fog, weather and surface appearance. This profile is a measurement starting point, not a benchmark result.
