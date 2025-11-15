#!/usr/bin/env python3
"""Script to draw and visualize IHP CMIM capacitors.

This demonstrates how to create and work with capacitors in the IHP PDK.
"""

import gdsfactory as gf
from ihp import PDK, cells

# Activate the IHP PDK
PDK.activate()

def main():
    """Generate capacitor examples."""

    print("=" * 60)
    print("IHP CMIM Capacitor Examples")
    print("=" * 60)

    # 1. Load the reference capacitor from GDS file
    print("\n1. Reference CMIM capacitor (from GDS file):")
    c_ref = cells.fixed.cmim()
    print(f"   - Component: {c_ref.name}")
    print(f"   - Layers: {list(c_ref.layers)}")
    print(f"   - Bounding box: {c_ref.bbox}")

    # 2. Create custom CMIM capacitors with different dimensions
    print("\n2. Custom CMIM capacitors:")

    sizes = [
        (3.0, 3.0),   # Small
        (5.0, 5.0),   # Medium
        (8.0, 8.0),   # Large
        (10.0, 10.0), # Extra large
    ]

    capacitors = []
    for i, (width, length) in enumerate(sizes, 1):
        cap = cells.capacitors.cmim(width=width, length=length)
        capacitors.append(cap)

        print(f"\n   Capacitor {i}:")
        print(f"     - Size: {width} x {length} um")
        print(f"     - Capacitance: {cap.info.get('capacitance_fF', 'N/A'):.2f} fF")
        print(f"     - Area: {cap.info.get('area_um2', 'N/A'):.2f} um²")
        print(f"     - Ports: {[p.name for p in cap.ports]}")

    # 3. Create a grid of capacitors
    print("\n3. Creating a grid layout with all capacitors...")
    grid = gf.grid(capacitors, spacing=30.0, shape=(2, 2))
    print(f"   - Grid contains {len(capacitors)} capacitors")
    print(f"   - Grid bounding box: {grid.bbox}")

    # 4. Create a capacitor with specific capacitance value
    print("\n4. Design a capacitor for target capacitance:")
    target_cap_fF = 100.0  # Target: 100 fF
    cap_density = 1.5      # fF/um²

    # Calculate required area
    required_area = target_cap_fF / cap_density
    side_length = required_area ** 0.5

    cap_target = cells.capacitors.cmim(width=side_length, length=side_length)
    print(f"   - Target capacitance: {target_cap_fF} fF")
    print(f"   - Required size: {side_length:.2f} x {side_length:.2f} um")
    print(f"   - Actual capacitance: {cap_target.info.get('capacitance_fF', 'N/A'):.2f} fF")

    # 5. Export the designs
    print("\n5. Exporting GDS files...")

    # Export reference capacitor
    c_ref.write_gds("output_cmim_reference.gds")
    print("   ✓ Saved: output_cmim_reference.gds")

    # Export medium custom capacitor
    capacitors[1].write_gds("output_cmim_5x5.gds")
    print("   ✓ Saved: output_cmim_5x5.gds")

    # Export target capacitor
    cap_target.write_gds("output_cmim_target_100fF.gds")
    print("   ✓ Saved: output_cmim_target_100fF.gds")

    # Export grid
    grid.write_gds("output_capacitor_grid.gds")
    print("   ✓ Saved: output_capacitor_grid.gds")

    # 6. Show layer information
    print("\n6. Layer information for CMIM capacitor:")
    print("   - Metal4 (bottom plate)")
    print("   - Metal5 (top plate)")
    print("   - MIM (dielectric)")
    print("   - Via4 (connections)")
    print("   - TopMetal1 (routing)")
    print("   - TopVia1 (vias)")
    print("   - MemCap (capacitor marker)")
    print("   - Metal4nofill (no-fill region)")

    print("\n" + "=" * 60)
    print("Done! GDS files generated successfully.")
    print("You can open them in KLayout to visualize.")
    print("=" * 60)

    # 7. Show information about the reference capacitor
    print("\n7. Comparing reference vs custom capacitor:")
    print(f"   Reference: {c_ref.name}")
    print(f"     - Bounding box: {c_ref.bbox}")
    print(f"\n   Custom (5x5um): {capacitors[1].name}")
    print(f"     - Bounding box: {capacitors[1].bbox}")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
