# NetInstall

Universal network-based operating system deployment and recovery toolkit.

NetInstall is designed around a small bootstrap environment that can start on a target machine, establish network connectivity, retrieve the current deployment manifest from GitHub-hosted infrastructure, and launch the appropriate OS installation workflow.

## Project goals

- Network-first OS installation and recovery
- UEFI/PXE/iPXE-oriented boot paths
- Small bootstrap media instead of carrying complete OS images
- GitHub-hosted manifests and release artifacts
- Modular OS installation backends
- Linux and Windows support as first-class targets
- Clear separation between bootstrap, networking, orchestration, and installers
- Reproducible builds and automated validation

## Current status

Early development. The repository currently contains the project foundation and architecture contract. Boot media and installer implementations will be added incrementally.

## High-level architecture

```text
Target machine
      |
      v
Bootstrap (USB / PXE / HTTP Boot / iPXE)
      |
      v
Network initialization
      |
      v
NetInstall engine
      |
      +---- GitHub manifest / release metadata
      |
      +---- OS backend selection
      |
      v
OS-specific installation workflow
      |
      v
Target disk
```

## Design principle

NetInstall must not assume that the target currently has a working operating system. The bootstrap layer is therefore intentionally independent from the installed OS and is responsible only for reaching a minimal execution environment and bringing up networking.

## Development

The core application is Python-based. Low-level boot artifacts may use technologies appropriate to the target firmware and boot path, including UEFI executables, iPXE scripts, and minimal Linux-based recovery environments.

See `docs/architecture.md` for the initial architecture contract.
