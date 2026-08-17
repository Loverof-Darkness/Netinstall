# Wi-Fi recovery design

The first-stage `BOOTX64.EFI` is intentionally small and currently targets wired networking. A universal Wi-Fi implementation cannot be assumed at UEFI/iPXE level because Wi-Fi adapter drivers, firmware, WPA authentication, and regulatory handling are platform dependent.

NetInstall therefore uses two stages:

1. **Bootstrap stage** — UEFI/iPXE, suitable for Ethernet and firmware-provided network boot paths.
2. **Recovery OS stage** — a small Linux environment with kernel modules, firmware, WPA authentication, DHCP, and the NetInstall client. This stage can be loaded by the bootstrap when the machine needs Wi-Fi.

The recovery OS must:

- detect the wireless adapter;
- load the matching kernel module and firmware;
- allow the user to select an SSID and enter a password locally;
- obtain an address using DHCP;
- verify HTTPS connectivity;
- fetch only signed/pinned NetInstall metadata;
- download the selected installer kernel/initrd;
- hand off to the installer without exposing the Wi-Fi password to GitHub.

## Security boundary

Wi-Fi credentials are entered on the target machine and remain local to the recovery environment. They must never be committed to the repository, embedded in a public URL, or placed in catalog metadata.

## Current status

The recovery-OS builder is a separate milestone from the Ethernet/iPXE bootstrap. Until that builder is validated on physical adapters, NetInstall must not claim universal Wi-Fi-only recovery.
