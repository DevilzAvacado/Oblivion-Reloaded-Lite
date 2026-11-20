# ORSE Feature Audit and Lite Development Decisions

## Source material inspected

The supplied `Data.zip` is an installed-data package, not a source-code package. It contains game assets, the compiled `OblivionReloaded.dll`, `OblivionReloadedShaders.dll`, `OblivionReloadedFastMM.dll`, and configuration files. It does not contain ORSE C++ source files, HLSL source for its replacement renderer, project files, symbols, or a build system.

This means the package supports an audit of exposed features and configuration, but it does not support a source-level port of ORSE's renderer. Lite must not reuse ORSE's compiled DLLs or shader DLLs: they replace the same plugin and shader paths and are not an AMD/Steam Deck implementation.

## Roadmap audit

| Roadmap area | Existing Lite foundation | Development decision |
|---|---|---|
| Adaptive grass distance | Grass hook already forwards the game's fade/end distances and performs cell frustum checks. | Added an opt-in frame-time-driven distance controller. It is disabled by default until validated on hardware. |
| Extended grass cell rendering | The existing grass hook traverses the loaded grid-cell array. | Do not extend the cell radius by default. More grass cells can increase CPU and GPU work, which conflicts with the Deck performance target. |
| Occlusion culling | Frustum culling is active; a separate occlusion implementation exists behind `EXPERIMENTAL_FEATURE`. | Do not enable the legacy occlusion path. Its query code synchronously waits for GPU query completion with `D3DGETDATA_FLUSH`, which risks stalling the render thread. An asynchronous query lifecycle and performance measurements are prerequisites. |
| Smart FPS control | A legacy frame-rate manager and hook exist behind `EXPERIMENTAL_FEATURE`. | Keep SteamOS frame pacing as the single limiter. Do not add a second sleeping limiter to the Deck profile. |
| Adaptive scene quality | The grass controller provides a narrow first step. | Do not automatically reduce global object/actor/LOD visibility without separate GPU/CPU telemetry and visual validation. |
| Shadow caster presets | Lite already has object-category shadow toggles, cascade configuration, exterior and interior shadow settings. | Preserve the current shadow pipeline. Additional presets can be configuration profiles later; no second shadow implementation is needed. |
| Memory management | Texture management is already represented in the active configuration and hook path. A separate heap manager is experimental. | Keep current texture management. Do not activate FastMM/heap replacement without compatibility and memory-stress testing. |
| Camera and character features | Camera, equipment, mounted-combat and animation source modules are present in the inherited tree, but their hook activation is guarded by `EXPERIMENTAL_FEATURE`. | Do not enable the global experimental switch. The active Rust configuration and C++ FFI model do not contain the complete experimental settings, and the switch enables unrelated systems together. These features need isolated feature gates and ABI audits. |
| Weather/interior fixes | Existing settings and hooks cover precipitation and underwater behavior. | No ORSE-specific fix can be safely ported from the supplied binary-only package. Add a fix only with a reproducible Lite issue and a regression test. |
| Stability fixes | Static profile checks and an x86 CI build exist. | Add regression cases for any independently reproduced defect. A binary package without source or symbols is insufficient to transplant internal fixes. |

## Adaptive grass-distance controller

The controller added in this development branch:

- Is opt-in through `Main.AdaptiveGrassDistance`.
- Uses `Main.GrassTargetFrameRate` (valid values 30–90; otherwise 60).
- Uses `Main.GrassMinimumDistanceScale` (valid values 0.40–0.90; otherwise 0.65).
- Smooths the elapsed frame-time sample.
- Reduces grass fade/end distances only after sustained frame-time overload.
- Restores distance more slowly, with hysteresis to limit oscillation.
- Does not change grass density, cell loading, shaders, shadows, or AO.
- Defaults to disabled pending Steam Deck testing.

## Release gate

The Windows x86 build and static checks can establish source/configuration consistency. They cannot establish correct grass rendering, stable cell transitions, absence of crashes during gameplay, useful frame-time improvement, or power/battery impact on Steam Deck OLED.

A stable release that advertises the new performance behavior requires:

1. Successful Windows x86 plugin and Rust Configurator builds.
2. Successful static profile and FFI checks.
3. xOBSE loading under the target Proton version.
4. In-game A/B testing of adaptive grass distance at the same save/location/settings.
5. Verification of grass visibility at cell boundaries and after interior/exterior transitions.
6. Repeated frame-time, FPS, CPU/GPU utilization and power measurements.
7. Regression testing of shadows, AO, menus, loading, save loading and DXVK rendering.

Until those runtime checks are completed, this branch is a development candidate, not a stable release.