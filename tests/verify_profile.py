#!/usr/bin/env python3
"""Static checks for the Oblivion Reloaded Lite default profile."""
from pathlib import Path
import xml.etree.ElementTree as ET

raw = Path("Extra/OblivionReloaded.dll.config").read_text(encoding="utf-8")
# The inherited config contains three top-level sections, so wrap them for XML parsing.
root = ET.fromstring("<Config>" + raw + "</Config>")
source = Path("TESReloaded/Core/RenderManager.cpp").read_text(encoding="utf-8")

def value(path):
    element = root.find(path)
    assert element is not None, f"Missing config element: {path}"
    return element.attrib.get("Value")

# Retain the lighting/shadow systems.
assert value("./_Shaders/ShadowsInteriors/Main/Enabled") == "1"
assert value("./_Shaders/ShadowsInteriors/Main/TorchesCastShadows") == "1"
assert value("./_Shaders/ShadowsExteriors/Near/Enabled") == "1"

# Keep optional effects off in the Deck-first profile.
for effect in ("GodRays", "MotionBlur", "POM", "Precipitations",
               "WetWorld", "VolumetricFog", "Water"):
    assert value(f"./_Shaders/{effect}/Status/Enabled") == "0", effect

assert value("./_Main/FrameRate/SmartControl/SmartControl") == "0"
assert value("./_Shaders/ShadowsExteriors/Near/ShadowMapSize") == "2048"
assert value("./_Shaders/ShadowsInteriors/Main/ShadowCubeMapSize") == "1024"
assert value("./_Shaders/ShadowsInteriors/Main/LightPoints") == "1"

# DXVK RESZ fix: preserve and restore both D3D9 vertex format mechanisms.
resolve = source.split("void RenderManager::ResolveDepthBuffer()", 1)[1].split("\\nvoid ", 1)[0]
for token in ("GetFVF", "GetVertexDeclaration", "SetFVF(dCurrFVF)",
              "SetVertexDeclaration(pCurrDecl)", "pCurrDecl->Release()",
              "pCurrVS->Release()", "pCurrPS->Release()"):
    assert token in resolve, f"Missing RESZ state/refcount handling: {token}"

assert "pDxvkInterop->Release()" in source
assert "D3D->Release()" in source
# Lightweight AO defaults and shader budget.
main_defaults = Path("Configurator/src/main_config.rs").read_text(encoding="utf-8")
effect_defaults = Path("Configurator/src/effect_config.rs").read_text(encoding="utf-8")
effect_template = Path("Configurator/effect.ini").read_text(encoding="utf-8")
ao_shader = Path("Extra/Shaders/OblivionReloaded/Effects/AmbientOcclusion.fx.hlsl").read_text(encoding="utf-8")
assert "AmbientOcclusion : true," in main_defaults
assert "Samples : 4" in effect_defaults
assert "StrengthMultiplier : 0.75" in effect_defaults
assert "StrengthMultiplier : 0.85" in effect_defaults
assert "Samples = 4" in effect_template
assert "static const int samples = 4;" in ao_shader
assert "static const int cKernelSize = 8;" in ao_shader
assert "float2(-4.0f * TESR_ReciprocalResolution.x" in ao_shader
assert "float2( 4.0f * TESR_ReciprocalResolution.x" in ao_shader
assert "CompileEffects : 2" in main_defaults
# Adaptive grass distance is opt-in and mirrored across the Rust/C++ FFI.
main_config = Path("Configurator/src/main_config.rs").read_text(encoding="utf-8")
ffi_config = Path("TESReloaded/Core/SettingStructure.h").read_text(encoding="utf-8")
grass_hook = Path("TESReloaded/Core/Hooks/Oblivion/Grass.cpp").read_text(encoding="utf-8")
assert "AdaptiveGrassDistance : false" in main_config
assert "GrassTargetFrameRate : 60" in main_config
assert "GrassMinimumDistanceScale : 0.65" in main_config
for field in ("bool AdaptiveGrassDistance;", "uint8_t GrassTargetFrameRate;",
              "float GrassMinimumDistanceScale;"):
    assert field in ffi_config, f"Missing C++ FFI field: {field}"
for token in ("UpdateAdaptiveGrassDistance", "ElapsedTime * 1000.0",
              "TargetFrameTimeMs * 1.10f", "TargetFrameTimeMs * 1.03f",
              "DistanceScale -= 0.15f * DeltaSeconds",
              "DistanceScale += 0.05f * DeltaSeconds",
              "EffectiveStartFadingDistance", "EffectiveEndDistance"):
    assert token in grass_hook, f"Missing adaptive grass behavior: {token}"
assert "SettingsMain->AdaptiveGrassDistance" in grass_hook
# Publishing must run on tags or an explicitly named release branch, never on master.
release_workflow = Path(".github/workflows/build-release.yml").read_text(encoding="utf-8")
assert "if: startsWith(github.ref, 'refs/tags/v') || startsWith(github.ref, 'refs/heads/release/')" in release_workflow
assert "github.ref == 'refs/heads/master'" not in release_workflow
assert "Oblivion-Reloaded-Lite-$env:PACKAGE_VERSION.zip" in release_workflow
assert "release_tag=$releaseTag" in release_workflow
assert "target_commitish: ${{ github.sha }}" in release_workflow

print("Oblivion Reloaded Lite profile checks passed.")
