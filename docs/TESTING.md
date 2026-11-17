# Validation plan

## Static checks

- Parse `Extra/OblivionReloaded.dll.config` as XML.
- Confirm exterior near and interior shadows remain enabled.
- Confirm optional Lite-disabled effects are off.
- Confirm fresh configurations enable AO and use four AO samples with an eight-tap blur kernel.
- Confirm the RESZ depth-resolve saves and restores FVF and vertex declaration.
- Confirm COM references acquired in the RESZ path are released.
- Compile the x86 DLL in Release configuration.

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
