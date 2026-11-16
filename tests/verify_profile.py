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
print("Oblivion Reloaded Lite profile checks passed.")
