#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_DIR="${ROOT}/.build/ipxe"
IPXE_REF="${IPXE_REF:-master}"
IPXE_SCRIPT="${IPXE_SCRIPT:-${ROOT}/boot/ipxe/netinstall.ipxe}"

rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}"
git clone --depth 1 --branch "${IPXE_REF}" https://github.com/ipxe/ipxe.git "${BUILD_DIR}"

make -C "${BUILD_DIR}/src" bin-x86_64-efi/ipxe.efi \
  EMBED="${IPXE_SCRIPT}" \
  CONSOLE_SERIAL=1

mkdir -p "${ROOT}/dist"
cp "${BUILD_DIR}/src/bin-x86_64-efi/ipxe.efi" "${ROOT}/dist/BOOTX64.EFI"
sha256sum "${ROOT}/dist/BOOTX64.EFI" > "${ROOT}/dist/BOOTX64.EFI.sha256"
printf 'Built %s\n' "${ROOT}/dist/BOOTX64.EFI"
