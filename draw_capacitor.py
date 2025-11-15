#!/usr/bin/env python3
"""Script to draw and visualize IHP capacitors.

This demonstrates how to create and work with capacitors in the IHP PDK.
"""

import gdsfactory as gf
from ihp import PDK, cells

# Activate the IHP PDK
PDK.activate()

def main():
    """Generate capacitor examples."""

    print("=" * 60)
    print("IHP Capacitor Examples")
    print("=" * 60)

    # 1. Load the reference capacitor from GDS file
    print("\n1. Reference CMIM capacitor (from GDS file):")
    c_ref = cells.fixed.cmim()
    print(f"   - Component: {c_ref.name}")
    print(f"   - Layers: {list(c_ref.layers)}")

    # 2. Create a custom CMIM capacitor with specific dimensions
    print("\n2. Custom CMIM capacitor (5x5 um):")
    c_custom = cells.capacitors.cmim(width=5.0, length=5.0)
    print(f"   - Component: {c_custom.name}")
    print(f"   - Width: {c_custom.info.get('width', 'N/A')} um")
    print(f"   - Length: {c_custom.info.get('length', 'N/A')} um")
    print(f"   - Capacitance: {c_custom.info.get('capacitance_fF', 'N/A')} fF")
    print(f"   - Area: {c_custom.info.get('area_um2', 'N/A')} um²")
    print(f"   - Ports: {[p.name for p in c_custom.ports]}")

    # 3. Create an RF CMIM capacitor
    print("\n3. RF CMIM capacitor (10x10 um):")
    c_rf = cells.capacitors.rfcmim(width=10.0, length=10.0)
    print(f"   - Component: {c_rf.name}")
    print(f"   - Width: {c_rf.info.get('width', 'N/A')} um")
    print(f"   - Length: {c_rf.info.get('length', 'N/A')} um")
    print(f"   - Capacitance: {c_rf.info.get('capacitance_fF', 'N/A')} fF")
    print(f"   - Type: {c_rf.info.get('type', 'N/A')}")
    print(f"   - Ports: {[p.name for p in c_rf.ports]}")

    # 4. Create a grid of capacitors with different sizes
    print("\n4. Creating a grid of capacitors with different sizes...")
    capacitors = []
    sizes = [3.0, 5.0, 8.0, 10.0]

    for size in sizes:
        cap = cells.capacitors.cmim(width=size, length=size)
        capacitors.append(cap)

    grid = gf.grid(capacitors, spacing=20.0, shape=(2, 2))
    print(f"   - Grid created with {len(capacitors)} capacitors")

    # 5. Export the designs
    print("\n5. Exporting designs...")

    # Export reference capacitor
    c_ref.write_gds("output_cmim_reference.gds")
    print("   - Saved: output_cmim_reference.gds")

    # Export custom capacitor
    c_custom.write_gds("output_cmim_custom.gds")
    print("   - Saved: output_cmim_custom.gds")

    # Export RF capacitor
    c_rf.write_gds("output_rfcmim.gds")
    print("   - Saved: output_rfcmim.gds")

    # Export grid
    grid.write_gds("output_capacitor_grid.gds")
    print("   - Saved: output_capacitor_grid.gds")

    print("\n" + "=" * 60)
    print("Done! You can view the GDS files in KLayout.")
    print("=" * 60)

    # Optionally show the capacitor in KLayout (if available)
    try:
        print("\nShowing capacitor in KLayout...")
        c_custom.show()
    except Exception as e:
        print(f"\nNote: Could not open KLayout viewer: {e}")
        print("You can manually open the generated GDS files in KLayout.")

if __name__ == "__main__":
    main()
