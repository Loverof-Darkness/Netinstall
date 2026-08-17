# NetInstall bootstrap releases

A tagged release is built by GitHub Actions and publishes the UEFI bootstrap plus a ready-to-copy USB tree.

## Release contents

- `BOOTX64.EFI` — x86_64 UEFI iPXE bootstrap.
- `BOOTX64.EFI.sha256` — SHA-256 checksum for the EFI binary.
- `netinstall-bootstrap.tar.gz` — packaged bootstrap and USB tree.

## USB layout

Copy the contents of the generated `usb-tree/` directory to the root of a FAT32-formatted USB device:

```text
EFI/
└── BOOT/
    └── BOOTX64.EFI
```

The repository does not publish a disk image that blindly overwrites a physical device. The release artifact is a file tree so the user can select and prepare the target media explicitly.

## Secure Boot

The current bootstrap is not signed for Secure Boot. Disable Secure Boot for initial testing, or use an approved signing/enrollment process before deployment on Secure-Boot-enforced systems.

## Network limitation

The current iPXE bootstrap is primarily an Ethernet/PXE-oriented first stage. Wi-Fi-only recovery requires a firmware/driver-capable recovery environment and is tracked separately; do not assume every laptop can connect to Wi-Fi from the iPXE EFI binary.
