# Installer adapters

NetInstall uses OS-specific adapters behind a common deployment contract.

| OS | Adapter | Current stage |
|---|---|---|
| Ubuntu | `ubuntu-autoinstall` | Generates a non-destructive handoff plan |
| Debian | `debian-installer` | Generates a non-destructive handoff plan |
| Fedora | `fedora-kickstart` | Generates a non-destructive handoff plan |
| Windows | `windows-winpe` | Generates a non-destructive WinPE handoff plan |

The current adapters deliberately do **not** partition, format, or overwrite disks. They prepare the metadata needed for a later installer runtime.

Linux unattended installation will eventually use each distribution's supported installer mechanisms (for example Ubuntu Autoinstall, Debian Installer automation, and Fedora Kickstart). Windows deployment will use a WinPE-based workflow and requires user-provided/licensed Windows installation media; Microsoft media is not bundled with this project.
