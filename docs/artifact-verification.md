# Artifact verification

NetInstall does not bundle operating-system images. The catalog references official upstream netboot artifacts.

Before an artifact is used for a production deployment, its SHA-256 must be pinned in the catalog. The helper below downloads each HTTPS artifact and produces a reviewable, hash-pinned catalog:

```bash
python scripts/pin-artifact-hashes.py \
  catalog/operating-systems.json \
  /tmp/operating-systems.pinned.json
```

Review the generated hashes and then replace the catalog intentionally. The runtime downloader verifies a pinned SHA-256 before accepting an artifact.

Ubuntu 24.04 provides an official AMD64 netboot directory containing `linux` and `initrd`; Ubuntu also publishes release checksums for its release images. Debian 13 provides the current AMD64 Debian Installer netboot `linux` and `initrd.gz` artifacts. The project records those upstream locations but does not guess checksums when an upstream checksum for the exact netboot artifact has not been independently verified.
