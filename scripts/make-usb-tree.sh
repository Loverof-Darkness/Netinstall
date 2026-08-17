#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${1:-${ROOT}/dist/usb-tree}"

rm -rf "$OUT"
mkdir -p "$OUT/EFI/BOOT" "$OUT/netinstall"

if [[ ! -f "$ROOT/dist/BOOTX64.EFI" ]]; then
  echo "Missing dist/BOOTX64.EFI; run scripts/build-ipxe.sh first." >&2
  exit 1
fi

cp "$ROOT/dist/BOOTX64.EFI" "$OUT/EFI/BOOT/BOOTX64.EFI"
cp "$ROOT/boot/ipxe/netinstall.ipxe" "$OUT/netinstall/netinstall.ipxe"
cp "$ROOT/boot/ipxe/catalog.ipxe" "$OUT/netinstall/catalog.ipxe"
cp "$ROOT/catalog/operating-systems.json" "$OUT/netinstall/operating-systems.json"

cat > "$OUT/netinstall/README.txt" <<'EOF'
NetInstall bootstrap

EFI/BOOT/BOOTX64.EFI is the UEFI iPXE bootstrap.
The remaining files are reference/control files and are not the OS payload.

For a physical USB, copy this tree to a FAT32-formatted UEFI USB device.
Do not overwrite a disk unless you have verified its device path.
EOF

printf 'USB tree prepared at %s\n' "$OUT"
