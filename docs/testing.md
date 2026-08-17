# Testing strategy

NetInstall is tested in layers before physical-disk deployment is enabled.

## 1. Unit tests

The GitHub Actions test workflow runs the Python test suite and CLI smoke tests on every push and pull request.

## 2. Catalog validation

Run:

```bash
python scripts/validate-catalog.py
```

The validator rejects missing boot artifacts for network-bootable installers, non-HTTPS artifact URLs, and malformed SHA-256 values.

## 3. QEMU integration target

The next integration target is an isolated QEMU VM using a disposable virtual disk. The VM must boot the NetInstall EFI artifact and reach the installer handoff without exposing a host disk.

A QEMU integration test must remain opt-in until the EFI artifact and network topology are stable. No CI test should ever pass a host block device to the VM.

## 4. Physical hardware

Only after QEMU passes should the bootstrap be tested on a disposable USB and then on the Dell Vostro 15 3568. Secure Boot and Wi-Fi capability must be tested separately because they depend on firmware and hardware support.
