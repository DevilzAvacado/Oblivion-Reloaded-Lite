#pragma once

/*
 * Adaptive grass distance is deliberately opt-in. It only scales the vanilla
 * grass fade/end distances supplied to this hook; it does not alter grass
 * density, cell loading, or the renderer's shader path.
 *
 * Frame-time hysteresis prevents rapid distance oscillation around the target:
 * quality is reduced after sustained overload and restored more slowly.
 */
static float UpdateAdaptiveGrassDistance(const ffi::MainStruct* SettingsMain) {
	static float DistanceScale = 1.0f;
	static float FrameTimeAverageMs = 0.0f;
	static float OverBudgetSeconds = 0.0f;
	static float RecoverySeconds = 0.0f;
	static double LastUpdateMs = 0.0;

	if (!SettingsMain || !SettingsMain->AdaptiveGrassDistance || !TheFrameRateManager) {
		DistanceScale = 1.0f;
		FrameTimeAverageMs = 0.0f;
		OverBudgetSeconds = 0.0f;
		RecoverySeconds = 0.0f;
		LastUpdateMs = 0.0;
		return 1.0f;
	}

	const double NowMs = TheFrameRateManager->GetPerformance();
	const float FrameTimeMs = (float)(TheFrameRateManager->ElapsedTime * 1000.0);
	if (!(FrameTimeMs > 0.0f) || FrameTimeMs > 250.0f) {
		LastUpdateMs = NowMs;
		return DistanceScale;
	}

	if (LastUpdateMs <= 0.0 || NowMs <= LastUpdateMs || (NowMs - LastUpdateMs) > 500.0) {
		LastUpdateMs = NowMs;
		FrameTimeAverageMs = FrameTimeMs;
		OverBudgetSeconds = 0.0f;
		RecoverySeconds = 0.0f;
		return DistanceScale;
	}

	float DeltaSeconds = (float)((NowMs - LastUpdateMs) / 1000.0);
	LastUpdateMs = NowMs;
	if (DeltaSeconds > 0.25f) DeltaSeconds = 0.25f;

	// Exponential moving average with an approximately 350 ms response window.
	const float Alpha = DeltaSeconds / (0.35f + DeltaSeconds);
	FrameTimeAverageMs += (FrameTimeMs - FrameTimeAverageMs) * Alpha;

	unsigned int TargetFrameRate = SettingsMain->GrassTargetFrameRate;
	if (TargetFrameRate < 30 || TargetFrameRate > 90) TargetFrameRate = 60;
	const float TargetFrameTimeMs = 1000.0f / (float)TargetFrameRate;

	float MinimumScale = SettingsMain->GrassMinimumDistanceScale;
	if (!(MinimumScale >= 0.40f && MinimumScale <= 0.90f)) MinimumScale = 0.65f;

	if (FrameTimeAverageMs > TargetFrameTimeMs * 1.10f) {
		OverBudgetSeconds += DeltaSeconds;
		RecoverySeconds = 0.0f;
		if (OverBudgetSeconds >= 0.45f) {
			DistanceScale -= 0.15f * DeltaSeconds;
		}
	}
	else if (FrameTimeAverageMs < TargetFrameTimeMs * 1.03f) {
		RecoverySeconds += DeltaSeconds;
		OverBudgetSeconds = 0.0f;
		if (RecoverySeconds >= 1.5f) {
			DistanceScale += 0.05f * DeltaSeconds;
		}
	}
	else {
		OverBudgetSeconds = 0.0f;
		RecoverySeconds = 0.0f;
	}

	if (DistanceScale < MinimumScale) DistanceScale = MinimumScale;
	if (DistanceScale > 1.0f) DistanceScale = 1.0f;
	return DistanceScale;
}

static void UpdateGrass(TESObjectCELL* OriginalCell, NiNode* GrassNode, float CameraPosX, float CameraPosY, float CameraPosZ, float CameraForwardX, float CameraForwardY, int Arg8, float StartFadingDistance, float EndDistance, float Arg11) {

	GridCellArray* CellArray = Tes->gridCellArray;
	UInt32 CellArraySize = CellArray->size * CellArray->size;
	const ffi::MainStruct* SettingsMain = TheSettingManager ? &TheSettingManager->Config->Main : NULL;
	const float DistanceScale = UpdateAdaptiveGrassDistance(SettingsMain);
	const float EffectiveStartFadingDistance = StartFadingDistance * DistanceScale;
	const float EffectiveEndDistance = EndDistance * DistanceScale;

	(void)OriginalCell;
	for (UInt32 i = 0; i < CellArraySize; i++) {
		if (TESObjectCELL* GridCell = CellArray->gridEntry[i].cell) {
			if (GridCell->niNode && TheOcclusionManager->InFrustum(GridCell->niNode)) {
				Pointers::Functions::CreateGrass(GridCell, GrassNode, CameraPosX, CameraPosY, CameraPosZ, CameraForwardX, CameraForwardY, Arg8, EffectiveStartFadingDistance, EffectiveEndDistance, Arg11);
			}
		}
	}

}

__declspec(naked) void UpdateGrassHook() {

	__asm {
		call	UpdateGrass
		jmp		Jumpers::UpdateGrass::Return
	}

}
