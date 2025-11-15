import gdsfactory as gf
from ihp import PDK, cells

# Activate IHP PDK
PDK.activate()

def create_annotated_capacitor():
    """Create a capacitor with annotations showing structure."""

    print("Creating annotated capacitor layout...")

    # Main component
    c = gf.Component("annotated_capacitor")

    # Create a 5x5 um capacitor
    cap = cells.capacitors.cmim(width=5.0, length=5.0)
    c.add_ref(cap)

    # Add title
    c.add_label(
        text="IHP CMIM CAPACITOR - 5x5um",
        position=(0, 15),
        layer="Metal1drawing",
    )

    # Add specs
    c.add_label(
        text="37.5 fF",
        position=(0, 12),
        layer="Metal1drawing",
    )

    # Add layer labels
    labels = [
        ("Metal4 (Bottom)", (-15, 5)),
        ("Metal5 (Top)", (-15, 3)),
        ("MIM Dielectric", (-15, 1)),
        ("Via4 Array", (-15, -1)),
        ("TopMetal1", (-15, -3)),
    ]

    for text, pos in labels:
        c.add_label(
            text=text,
            position=pos,
            layer="Metal1drawing",
        )

    return c

def create_size_comparison():
    """Create a visual comparison of different capacitor sizes."""

    print("Creating size comparison...")

    c = gf.Component("size_comparison")

    sizes = [
        (3.0, "3x3um\n13.5fF"),
        (5.0, "5x5um\n37.5fF"),
        (8.0, "8x8um\n96fF"),
        (10.0, "10x10um\n150fF"),
    ]

    x_offset = 0
    for i, (size, label_text) in enumerate(sizes):
        # Create capacitor
        cap = cells.capacitors.cmim(width=size, length=size)
        cap_ref = c.add_ref(cap)
        cap_ref.x = x_offset

        # Add label
        c.add_label(
            text=label_text,
            position=(x_offset, -15),
            layer="Metal1drawing",
        )

        x_offset += size + 10  # 10 um spacing

    # Add title
    c.add_label(
        text="CAPACITOR SIZE COMPARISON",
        position=(15, 15),
        layer="Metal1drawing",
    )

    return c

def create_reference_comparison():
    """Create reference vs custom comparison."""

    print("Creating reference comparison...")

    c = gf.Component("ref_vs_custom")

    # Reference
    ref = cells.fixed.cmim()
    ref_inst = c.add_ref(ref)
    ref_inst.x = -20

    c.add_label(
        text="REFERENCE\n(from GDS)",
        position=(-20, -15),
        layer="Metal1drawing",
    )

    # Custom
    custom = cells.capacitors.cmim(width=5.0, length=5.0)
    custom_inst = c.add_ref(custom)
    custom_inst.x = 20

    c.add_label(
        text="CUSTOM\n(programmatic)",
        position=(20, -15),
        layer="Metal1drawing",
    )

    # Title
    c.add_label(
        text="REFERENCE vs CUSTOM COMPARISON",
        position=(0, 20),
        layer="Metal1drawing",
    )

    return c

def main():
    """Generate all visualizations."""

    print("=" * 70)
    print("IHP CAPACITOR VISUALIZATION")
    print("=" * 70)

    # 1. Annotated capacitor
    print("\n1. Creating annotated capacitor...")
    c1 = create_annotated_capacitor()
    c1.write_gds("viz_annotated_capacitor.gds")
    print("   ✓ Saved: viz_annotated_capacitor.gds")

    # 2. Size comparison
    print("\n2. Creating size comparison...")
    c2 = create_size_comparison()
    c2.write_gds("viz_size_comparison.gds")
    print("   ✓ Saved: viz_size_comparison.gds")

    # 3. Reference comparison
    print("\n3. Creating reference comparison...")
    c3 = create_reference_comparison()
    c3.write_gds("viz_reference_comparison.gds")
    print("   ✓ Saved: viz_reference_comparison.gds")

    # 4. Create a complete demo layout
    print("\n4. Creating complete demo layout...")
    demo = gf.Component("complete_demo")

    # Add all three visualizations
    ann_ref = demo.add_ref(c1)
    ann_ref.y = 60

    size_ref = demo.add_ref(c2)
    size_ref.y = 0

    ref_ref = demo.add_ref(c3)
    ref_ref.y = -60

    demo.write_gds("viz_complete_demo.gds")
    print("   ✓ Saved: viz_complete_demo.gds")

    # Summary
    print("\n" + "=" * 70)
    print("VISUALIZATION FILES CREATED")
    print("=" * 70)
    print("\nGenerated files:")
    print("  1. viz_annotated_capacitor.gds   - Single capacitor with labels")
    print("  2. viz_size_comparison.gds       - Different sizes side-by-side")
    print("  3. viz_reference_comparison.gds  - Reference vs custom")
    print("  4. viz_complete_demo.gds         - All visualizations combined")

    print("\n📖 View with KLayout:")
    print("   klayout viz_complete_demo.gds")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
