# Network boot pipeline

NetInstall separates the network bootstrap from OS installation media.

1. UEFI/iPXE loads the NetInstall bootstrap.
2. The bootstrap reaches the remote catalog over HTTPS.
3. The runtime selects an architecture-compatible OS.
4. The catalog resolves signed/verified kernel and initrd artifacts.
5. The runtime renders an iPXE boot entry.
6. The selected installer receives its unattended-install configuration.

The repository intentionally does not bundle large OS images. Artifact URLs and SHA-256 values belong in the catalog/release metadata. An entry without kernel and initrd artifacts cannot be booted and is rejected by the resolver.

## Security properties

- Artifact URLs must be HTTPS in production.
- SHA-256 values are verified by the downloader before use.
- The boot menu is data-driven rather than embedding arbitrary shell input.
- Installer configuration is separate from the bootstrap binary.
