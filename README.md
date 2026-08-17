# NetInstall

Universal network-based operating-system deployment and recovery toolkit.

NetInstall boots a small UEFI/iPXE bootstrap, brings up networking, retrieves a GitHub-hosted catalog, and hands off to an OS-specific network installer. The repository deliberately does **not** bundle complete operating-system images.

## Current MVP

The current MVP supports an **x86_64 UEFI + network** path for:

- Ubuntu 24.04 LTS network installer
- Debian 13 (Trixie) network installer
- iPXE UEFI bootstrap generation
- Catalog-driven boot menu generation
- HTTPS-only artifact URLs
- SHA-256 pinning/verification infrastructure
- Non-destructive deployment planning
- Wi-Fi discovery on an already-running Linux environment
- GitHub Actions validation and bootstrap artifact builds

Fedora and Windows are represented as planned adapters and are intentionally not exposed as bootable catalog entries until their release-specific artifacts and workflows are verified.

## Architecture

```text
                         GitHub
                           |
                 catalog + control scripts
                           |
                           v
Target machine ---> UEFI / iPXE bootstrap
                           |
                           v
                    Network initialization
                           |
                           v
                    NetInstall menu
                     /           \
                    /             \
               Ubuntu           Debian
                 |                 |
             kernel/initrd     kernel/initrd
                 |                 |
                 +--------+--------+
                          |
                          v
                    OS installer
                          |
                          v
                       Target SSD
```

## Bootstrap options

### Tiny USB

Build the UEFI bootstrap through GitHub Actions or locally:

```bash
bash scripts/build-ipxe.sh
bash scripts/make-usb-tree.sh
```

Copy the resulting `dist/usb-tree` contents to a FAT32 UEFI USB device. The USB contains the small bootstrap, not the OS payload.

### PXE / HTTP Boot

The same iPXE control scripts can be used from a PXE or firmware HTTP-Boot environment when the target firmware and network adapter support that path.

## CLI

```bash
python -m pip install -e .
netinstall diagnose
netinstall wifi scan
netinstall network
netinstall github
netinstall os
netinstall deploy ubuntu-24.04
```

`deploy` is currently a **planning operation**. It does not partition, format, mount, or write a target disk.

## Artifact security

Production downloads require a SHA-256 pin. Generate a reviewable pinned catalog with:

```bash
python scripts/pin-artifact-hashes.py \
  catalog/operating-systems.json \
  /tmp/operating-systems.pinned.json
```

The pinned file must be reviewed and committed before using those artifacts in a production deployment workflow.

## Important limitations

- A completely blank laptop cannot magically use Wi-Fi unless its pre-OS firmware/bootstrap path supports the required wireless hardware. The Vostro 15 3568 should therefore be tested first over Ethernet/PXE or with the tiny USB bootstrap.
- Secure Boot requires a trusted/signed EFI artifact. The current iPXE build is not a NetInstall-signed Secure Boot binary.
- Windows deployment requires user-supplied/licensed installation media and a verified WinPE workflow; Windows media is not redistributed by this project.
- Fedora support remains planned until release-specific network-install artifacts are pinned and tested.
- The project must be tested in QEMU/disposable media before any destructive disk-writing backend is enabled.

## Development and safety

The Python deployment engine is intentionally non-destructive. Installer adapters generate handoff plans/configuration; privileged disk operations are a separate future layer that must require explicit target-device confirmation.

GitHub Actions runs catalog validation, menu-generation consistency checks, Python tests, and CLI smoke tests. The UEFI bootstrap build is also reproducible through `.github/workflows/build-bootstrap.yml`.

See `docs/architecture.md`, `docs/network-boot.md`, `docs/installer-configs.md`, and `docs/testing.md` for implementation details.
