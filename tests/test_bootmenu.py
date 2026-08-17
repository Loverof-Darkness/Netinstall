from netinstall.bootmenu.generator import render
from netinstall.bootmenu.models import BootEntry


def test_boot_entry_renders_kernel_initrd_and_boot() -> None:
    entry = BootEntry(
        id="test-os",
        title="Test OS",
        installer="test",
        kernel_url="https://example.invalid/linux",
        initrd_urls=("https://example.invalid/initrd",),
        kernel_args=("quiet", "autoinstall"),
    )
    script = entry.to_ipxe()
    assert "kernel https://example.invalid/linux quiet autoinstall" in script
    assert "initrd https://example.invalid/initrd" in script
    assert script.endswith("boot")


def test_menu_contains_all_entries() -> None:
    entries = (
        BootEntry("one", "One", "test", "https://example.invalid/one", ("https://example.invalid/one-initrd",)),
        BootEntry("two", "Two", "test", "https://example.invalid/two", ("https://example.invalid/two-initrd",)),
    )
    script = render(entries)
    assert "item one One" in script
    assert "item two Two" in script
    assert ":one" in script
    assert ":two" in script
