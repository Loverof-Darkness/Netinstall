# Installer configuration delivery

NetInstall keeps boot artifacts and installer configuration separate.

## Ubuntu Autoinstall

Ubuntu documents network delivery of Autoinstall configuration through cloud-init/NoCloud. The installer can receive a `#cloud-config` document containing a top-level `autoinstall:` section. A network-based NoCloud datasource is referenced with the `autoinstall ds=nocloud-net;s=<URL>/` kernel argument. See the official Ubuntu installation documentation for the exact release-specific boot layout.

NetInstall's renderer generates `user-data` and `meta-data`; it does not store plaintext passwords. Callers must provide a crypt-style password hash.

## Debian Preseed

Debian Installer accepts a network preconfiguration file using `preseed/url=<URL>` and supports automated installation with `auto=true`/critical priority. Network configuration that is required before the preseed file can be fetched must be supplied through installer boot parameters or DHCP.

## Fedora Kickstart

Fedora Anaconda accepts a network Kickstart location through `inst.ks=<URL>`. Kickstart files can describe the installation and partitioning policy, so NetInstall treats them as privileged deployment configuration and does not generate destructive defaults automatically.

## GitHub as the distribution layer

Static example configuration can be hosted in this repository. Per-machine configuration should be generated at deployment time and served from a trusted HTTPS endpoint; it should not be committed to a public repository because it can contain account and installation secrets.
