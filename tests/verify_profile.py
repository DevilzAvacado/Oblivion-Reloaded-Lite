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
resolve = source.split("void RenderManager::ResolveDepthBuffer()", 1)[1].split("\nvoid ", 1)[0]
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
print("Oblivion Reloaded Lite profile checks passed.")
