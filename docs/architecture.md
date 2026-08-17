# NetInstall Architecture

## 1. Purpose

NetInstall is a network-first operating system deployment and recovery platform. Its defining use case is a machine with no usable installed operating system where the user wants to reach an installer without carrying the complete operating-system image on removable media.

The system is deliberately split into layers so that one bootstrap path can support multiple operating systems and multiple transport mechanisms.

## 2. Layers

### Bootstrap layer

The bootstrap is the first executable environment reached by the target machine. Supported paths are planned to include:

- UEFI removable-media bootstrap
- UEFI HTTP Boot where firmware supports it
- PXE
- iPXE

The bootstrap must remain small and should not contain full operating-system installation images.

### Network layer

The network layer establishes connectivity before the main NetInstall engine starts. It must support different network capabilities without assuming that the firmware itself provides a complete network stack.

The initial implementation will prioritize wired networking for maximum compatibility and then add wireless support through a minimal Linux-based environment where hardware drivers are available.

### Control plane

The NetInstall control plane retrieves signed or integrity-verified metadata describing available operating systems, installer artifacts, compatibility requirements, and installation backends.

GitHub is the project's source/distribution control plane for public manifests, source code, and release artifacts. GitHub is not itself treated as a PXE server or DHCP server.

### Installer layer

Each supported operating system is represented by an installer backend. Backends translate a common deployment request into OS-specific installation steps.

Examples planned for later development:

- Debian/Ubuntu family
- Fedora/RHEL family
- Arch-based systems
- Windows PE / Windows Setup
- Custom image workflows

### Storage layer

The storage layer is responsible for detecting disks, presenting safe installation targets, validating destructive operations, partitioning, and handing the target disk to the selected OS installer.

## 3. Intended boot flow

```text
Power on
  |
  v
Firmware / removable bootstrap / network boot
  |
  v
Minimal NetInstall bootstrap
  |
  v
Network initialization
  |
  v
Fetch release manifest
  |
  v
Select compatible deployment backend
  |
  v
Fetch required installer artifacts
  |
  v
Prepare target disk
  |
  v
Run OS-specific installation
  |
  v
Install bootloader + OS
  |
  v
Reboot into installed system
```

## 4. GitHub role

GitHub provides the public distribution and version-control layer:

- Repository source
- Bootstrap scripts and configuration
- Versioned manifests
- Release artifacts
- Checksums/signatures
- Documentation

A deployment client should not hard-code mutable URLs where avoidable. It should retrieve a versioned manifest and resolve artifacts from that metadata.

## 5. Security requirements

The installer will eventually be capable of destructive disk operations, so security is part of the architecture rather than an afterthought.

Planned requirements include:

- HTTPS for remote metadata and artifacts
- Cryptographic integrity checks for downloaded artifacts
- Explicit target-disk confirmation before destructive operations
- Versioned manifests
- Clear separation of trusted metadata from user-supplied input
- Safe handling of Wi-Fi credentials
- No storage of network credentials in Git

## 6. Compatibility philosophy

"Universal" means a common deployment framework, not a claim that every laptop firmware, Wi-Fi adapter, or operating system can use one identical boot path.

The engine should detect capabilities and choose the best available path rather than assuming native Wi-Fi boot, PXE, HTTP Boot, or a particular firmware implementation exists.
