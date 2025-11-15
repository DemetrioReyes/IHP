#!/usr/bin/env python3
"""Compare custom capacitor with reference capacitor from IHP PDK.

This script demonstrates matching shapes to reference chip files.
"""

import gdsfactory as gf
from ihp import PDK, cells

# Activate the IHP PDK
PDK.activate()

def main():
    """Compare custom and reference capacitors."""

    print("=" * 70)
    print("CAPACITOR COMPARISON: Custom vs Reference")
    print("=" * 70)

    # Load reference capacitor
    print("\n📁 Loading reference capacitor from GDS file...")
    c_ref = cells.fixed.cmim()
    print(f"   ✓ Loaded: {c_ref.name}")
    print("   - File: ihp/gds/cmim.gds")
    print(f"   - Layers: {list(c_ref.layers)}")

    # Create custom capacitor with similar size
    print("\n🔨 Creating custom capacitor...")
    c_custom = cells.capacitors.cmim(width=5.0, length=5.0)
    print(f"   ✓ Created: {c_custom.name}")
    print(f"   - Width: {c_custom.info['width']} µm")
    print(f"   - Length: {c_custom.info['length']} µm")
    print(f"   - Capacitance: {c_custom.info['capacitance_fF']} fF")
    print(f"   - Layers: {list(c_custom.layers)}")

    # Compare layers
    print("\n🔍 Layer Comparison:")
    ref_layers = set(c_ref.layers)
    custom_layers = set(c_custom.layers)

    print(f"   Reference has {len(ref_layers)} layers")
    print(f"   Custom has {len(custom_layers)} layers")

    common_layers = ref_layers & custom_layers
    ref_only = ref_layers - custom_layers
    custom_only = custom_layers - ref_layers

    if common_layers:
        print(f"\n   ✓ Common layers ({len(common_layers)}): {sorted(common_layers)}")

    if ref_only:
        print(f"\n   ⚠ Only in reference ({len(ref_only)}): {sorted(ref_only)}")

    if custom_only:
        print(f"\n   ℹ Only in custom ({len(custom_only)}): {sorted(custom_only)}")

    # Create side-by-side comparison
    print("\n📊 Creating side-by-side comparison...")
    comparison = gf.Component("capacitor_comparison")

    # Add reference on the left
    ref_inst = comparison.add_ref(c_ref)
    ref_inst.x = 0

    # Add custom on the right
    custom_inst = comparison.add_ref(c_custom)
    custom_inst.x = 50  # 50 µm spacing

    # Add labels
    comparison.add_label(
        text="REFERENCE",
        position=(0, -20),
        layer="Metal1drawing",
    )

    comparison.add_label(
        text="CUSTOM",
        position=(50, -20),
        layer="Metal1drawing",
    )

    # Save comparison
    comparison.write_gds("output_comparison.gds")
    print("   ✓ Saved: output_comparison.gds")

    # Create XOR difference (shows differences in red)
    print("\n🔬 Creating XOR difference analysis...")
    try:
        from gdsfactory.difftest import xor

        # XOR comparison shows differences
        diff = xor(c_ref, c_custom)
        diff.write_gds("output_xor_difference.gds")
        print("   ✓ Saved: output_xor_difference.gds")
        print("   Note: Red areas show differences between reference and custom")
    except Exception as e:
        print(f"   ⚠ Could not create XOR: {e}")

    # Export individual capacitors
    print("\n💾 Exporting individual files...")
    c_ref.write_gds("output_reference_only.gds")
    print("   ✓ Saved: output_reference_only.gds")

    c_custom.write_gds("output_custom_only.gds")
    print("   ✓ Saved: output_custom_only.gds")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("\n✅ Generated Files:")
    print("   1. output_comparison.gds       - Side-by-side comparison")
    print("   2. output_reference_only.gds   - Reference capacitor only")
    print("   3. output_custom_only.gds      - Custom capacitor only")
    print("   4. output_xor_difference.gds   - Difference analysis")

    print("\n📖 How to view:")
    print("   klayout output_comparison.gds")

    print("\n🎯 Skills Demonstrated:")
    print("   ✓ Loading reference chip files")
    print("   ✓ Creating matching layouts programmatically")
    print("   ✓ Layer-by-layer comparison")
    print("   ✓ Geometric analysis (XOR)")
    print("   ✓ CAD file manipulation")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
