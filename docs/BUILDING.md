# Building Oblivion Reloaded Lite

## Toolchain

The inherited project is a 32-bit Windows DLL. Build on Windows with Visual Studio C++ desktop workload, the Visual C++ v142 toolset expected by the project, Windows SDK, DirectX 9 SDK dependencies, Rust stable and the `i686-pc-windows-msvc` target.

## Build

From a Visual Studio Developer Command Prompt:

```powershell
rustup target add i686-pc-windows-msvc
cargo build --manifest-path Configurator/Cargo.toml --release --target i686-pc-windows-msvc
New-Item -ItemType Directory -Force Configurator/target/release | Out-Null
Copy-Item Configurator/target/i686-pc-windows-msvc/release/Configurator.dll.lib Configurator/target/release/Configurator.dll.lib -Force
msbuild TESReloaded.sln /m /p:Configuration=Release /p:Platform=x86
cmd /c build.bat OblivionReloaded
```

The copy is needed because the Visual Studio project references `Configurator/target/release/Configurator.dll.lib`, while Cargo's explicit x86 target writes into a target-triple subdirectory.

The installable output is `build/OblivionReloaded/`. Package its contents without adding an extra enclosing directory.

A successful compile does not prove xOBSE loading, shader correctness under DXVK, or in-game stability. See [TESTING.md](TESTING.md).
