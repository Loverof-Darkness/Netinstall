# NetInstall bootstrap

NetInstall uses a small UEFI iPXE bootstrap instead of bundling an operating-system image on the USB device.

## Build locally

```bash
bash scripts/build-ipxe.sh
bash scripts/make-usb-tree.sh
```

The EFI binary is written to `dist/BOOTX64.EFI` and the FAT32-ready directory tree is written to `dist/usb-tree/`.

## Automated build

GitHub Actions builds the embedded iPXE EFI binary and publishes it as a workflow artifact. The build embeds `boot/ipxe/netinstall.ipxe` so the bootstrap can begin without loading a script from the USB filesystem first.

## Important limitations

- This produces an **unsigned** EFI binary. Secure Boot may reject it.
- `BOOTX64.EFI` is the UEFI x86_64 bootstrap; other architectures need separate builds.
- iPXE network-driver support is hardware dependent. A machine whose firmware exposes no usable network path cannot magically obtain Internet access from GitHub.
- Wi-Fi support must be tested on the target adapter. For maximum compatibility, wired PXE remains the first network-bootstrap target.
- The bootstrap does not contain an OS ISO. Large installation payloads are intentionally kept outside the bootstrap.

## Physical USB

After verifying the target USB device, format it as FAT32 and copy the contents of `dist/usb-tree/` to its root. The UEFI fallback path is `EFI/BOOT/BOOTX64.EFI`.

The project intentionally does not provide an automatic whole-disk flashing command at this stage; that will be added only after device-selection and destructive-operation safeguards are implemented.
