# Validation plan

## Static checks

- Parse `Extra/OblivionReloaded.dll.config` as XML.
- Confirm exterior near and interior shadows remain enabled.
- Confirm optional Lite-disabled effects are off.
- Confirm fresh configurations enable AO and use four AO samples with an eight-tap blur kernel.
- Confirm the RESZ depth-resolve saves and restores FVF and vertex declaration.
- Confirm COM references acquired in the RESZ path are released.
- Compile the x86 DLL in Release configuration.

## Adaptive grass-distance test

Test the adaptive controller separately from other graphics changes:

1. Use the same save, exterior location, camera direction, weather, time of day, resolution, frame cap and TDP.
2. Record a baseline with `AdaptiveGrassDistance = false`.
3. Enable it with a 60 FPS target and a 0.65 minimum distance scale.
4. Observe the same scene for at least two minutes, including a period of sustained load and a return to a less demanding area.
5. Record average FPS, 1% lows, frame times, CPU/GPU utilization and total system power.
6. Check for grass popping, visible distance changes, oscillation, missing grass near cell edges and unintended changes in interiors.
7. Repeat each condition at least three times and compare medians.

The controller must not be described as improving performance unless the measurements show a repeatable benefit. A successful compile and static test do not validate the in-game behavior.

## xOBSE / Proton smoke test

1. Back up the game directory and plugin configuration.
2. Install the ZIP into the game's Data directory.
3. Launch through Steam with xOBSE installed in the same prefix.
4. Verify the plugin load message and xOBSE logs.
5. Inspect exterior sun shadows on actors, trees and static geometry.
6. Inspect interior local shadows with a torch.
7. Verify AO contact shading in both interior and exterior scenes; check for halos, depth leaks, excessive darkening and flicker.
8. Switch first-person/third-person; check for ghost hands, broken geometry and state corruption.
9. Change cells, load saves, open menus and use local maps.
10. Enable DXVK HUD and verify the game is using the expected D3D9/Vulkan path.

## Performance A/B protocol

Use identical hardware, game build, Proton version, save, location, camera, weather, time of day, resolution, graphics settings, refresh rate and TDP limit. Run each configuration at least three times.

Record average FPS, 1% lows, frame-time data, CPU/GPU utilization, total system power and battery discharge if available. Include AO-on and AO-off runs from the same scene to isolate its cost. Compare medians and variability, not one best run.

## Stable-release gate

Do not label a binary stable until the x86 build succeeds, xOBSE loads under Proton, exterior/interior shadows render correctly, DXVK state artifacts are absent, no reproducible crash remains, and Deck performance/power measurements are published. CI cannot replace hardware validation.
