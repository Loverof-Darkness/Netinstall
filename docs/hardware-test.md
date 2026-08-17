# First physical test: Dell Vostro 15 3568

The first supported physical target is the Dell Vostro 15 3568 in UEFI mode.

## Recommended order

1. Keep the existing SSD untouched for the first test.
2. Build the bootstrap through the GitHub Actions `Build NetInstall Bootstrap` workflow.
3. Download the `netinstall-usb-tree` artifact.
4. Put the tree on a small FAT32 UEFI USB device.
5. Power on and press `F12`.
6. Select the UEFI USB entry.
7. Confirm that iPXE starts and reaches the NetInstall menu.
8. Use Ethernet for the first network test. Do not assume pre-boot Wi-Fi support.
9. Select Ubuntu or Debian and verify that the vendor network installer starts.
10. Only after the installer boot path is stable should an installation be attempted on a disposable target disk.

## Why Ethernet first?

The Vostro 15 3568 documents an integrated NIC/PXE boot option. Its firmware documentation does not establish a universal Wi-Fi pre-boot path for this model. A Linux Wi-Fi driver working after boot does not imply that the UEFI/iPXE environment can use the same adapter.

## Secure Boot

The current NetInstall iPXE binary is not signed by a NetInstall Secure Boot key. Disable Secure Boot only on a test machine if appropriate for the test, or use a separately signed/trusted build. Never weaken Secure Boot on a production-managed device merely to test this project.

## Disk safety

The current NetInstall CLI and bootstrap do not perform disk partitioning or formatting. Do not add a raw-device write step until the target-device selection UX has an explicit confirmation and the workflow has passed QEMU/disposable-media testing.
