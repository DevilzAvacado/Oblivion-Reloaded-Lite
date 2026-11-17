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

## Frame pacing

Use SteamOS's per-game frame limiter rather than running a second limiter in the plugin. Pick a target only after establishing a stable baseline.

## Notes

Reduced shadow-map dimensions lower map memory use and render-target cost, but do not guarantee proportional FPS or wattage gains. Disabled effects can change water, fog, weather and surface appearance. This profile is a measurement starting point, not a benchmark result.
