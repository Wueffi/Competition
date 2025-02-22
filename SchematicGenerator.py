import mcschematic


def create_decoder_schematic(input_patterns, filename):
    schem = mcschematic.MCSchematic()
    spacing = 2
    x = 0  # Starting X
    z = 1  # Starting Z

    for input_pattern in input_patterns:
        y = 0  # Starting Y
        for num in input_pattern:
            if num == 1:
                schem.setBlock((x, y, z), "minecraft:redstone_wall_torch[facing=north]")  # ON
                schem.setBlock((x, y + spacing, z), "minecraft:repeater[facing=south,delay=1,locked=false,powered=false]")  # OFF
            elif num == 2:
                schem.setBlock((x, y, z), "minecraft:repeater[facing=south,delay=1,locked=false,powered=false]")  # OFF
                schem.setBlock((x, y + spacing, z), "minecraft:redstone_wall_torch[facing=north]")  # ON
            elif num == 3:
                schem.setBlock((x, y, z), "minecraft:redstone_wall_torch[facing=north]")  # ON
                schem.setBlock((x, y + spacing, z), "minecraft:redstone_wall_torch[facing=north]")  # ON
            elif num == 0:
                schem.setBlock((x, y, z), "minecraft:repeater[facing=south,delay=1,locked=false,powered=false]")  # OFF
                schem.setBlock((x, y + spacing, z),
                               "minecraft:repeater[facing=south,delay=1,locked=false,powered=false]")  # OFF

            schem.setBlock((x, y + 1, z), "minecraft:smooth_quartz_slab[type=top]")
            schem.setBlock((x, y - 1, z), "minecraft:smooth_quartz_slab[type=top]")
            y += spacing * 2  # Move up

        x -= spacing  # Spacing

    schem.save("./schems", filename, mcschematic.Version.JE_1_20_1)
    print(f"Schematic saved as {filename}")

def create_lut_schematic(input_patterns, filename):
    schem = mcschematic.MCSchematic()
    spacing = 4
    z = 0  # Starting Z

    for input_pattern in input_patterns:
        y = 0  # Starting Y
        x = 0 # Starting X
        for num in input_pattern:
            if num == 2:
                schem.setBlock((x, y, z), "minecraft:redstone_wall_torch[facing=north]")  # ON
            elif num == 3:
                schem.setBlock((x, y + spacing, z), "minecraft:redstone_wall_torch[facing=north]")
            elif num == 4:
                schem.setBlock((x, y, z), "minecraft:redstone_wall_torch[facing=north]")
                schem.setBlock((x, y + spacing, z), "minecraft:redstone_wall_torch[facing=north]")
            elif num == 5:
                schem.setBlock((x, y + 2 * spacing, z), "minecraft:redstone_wall_torch[facing=north]")
            elif num == 6:
                schem.setBlock((x, y, z), "minecraft:redstone_wall_torch[facing=north]")
                schem.setBlock((x, y + 2 * spacing, z), "minecraft:redstone_wall_torch[facing=north]")
            elif num == 7:
                schem.setBlock((x, y + spacing, z), "minecraft:redstone_wall_torch[facing=north]")
                schem.setBlock((x, y + 2 * spacing, z), "minecraft:redstone_wall_torch[facing=north]")
            elif num == 8:
                schem.setBlock((x, y, z), "minecraft:redstone_wall_torch[facing=north]")
                schem.setBlock((x, y + spacing, z), "minecraft:redstone_wall_torch[facing=north]")
                schem.setBlock((x, y + 2 * spacing, z), "minecraft:redstone_wall_torch[facing=north]")

            x += 2
        z += 2

    schem.save("./schems", filename, mcschematic.Version.JE_1_20_1)
    print(f"Schematic saved as {filename}")

def create_3rd_lut_schematic(input_patterns, filename):
    schem = mcschematic.MCSchematic()
    spacing = 4
    z = 0  # Starting Z

    for input_pattern in input_patterns:
        y = 0  # Starting Y
        x = 0  # Starting X
        for num in input_pattern:
            if num == 1:
                schem.setBlock((x, y, z), "minecraft:redstone_wall_torch[facing=north]")  # ON
            elif num == 2:
                schem.setBlock((x, y + spacing, z), "minecraft:redstone_wall_torch[facing=north]")
            elif num == 3:
                schem.setBlock((x, y, z), "minecraft:redstone_wall_torch[facing=north]")
                schem.setBlock((x, y + spacing, z), "minecraft:redstone_wall_torch[facing=north]")
            x += 2
        z += 2

    schem.save("./schems", filename, mcschematic.Version.JE_1_20_1)
    print(f"Schematic saved as {filename}")

def create_3b_decoder_schematic(input_patterns, filename):
    schem = mcschematic.MCSchematic()
    spacing = 2
    x = 0  # Starting X
    z = 1  # Starting Z

    for input_pattern in input_patterns:
        y = 0  # Starting Y
        for num in input_pattern:
            if num == 1:
                schem.setBlock((x, y, z), "minecraft:redstone_wall_torch[facing=north]")  # ON
                schem.setBlock((x, y + spacing, z), "minecraft:repeater[facing=south,delay=1,locked=false,powered=false]")  # OFF
                schem.setBlock((x, y + 2 * spacing, z),"minecraft:repeater[facing=south,delay=1,locked=false,powered=false]")  # OFF
            elif num == 2:
                schem.setBlock((x, y, z), "minecraft:repeater[facing=south,delay=1,locked=false,powered=false]")  # OFF
                schem.setBlock((x, y + spacing, z), "minecraft:redstone_wall_torch[facing=north]")  # ON
                schem.setBlock((x, y + 2 * spacing, z),"minecraft:repeater[facing=south,delay=1,locked=false,powered=false]")  # OFF
            elif num == 3:
                schem.setBlock((x, y, z), "minecraft:redstone_wall_torch[facing=north]")  # ON
                schem.setBlock((x, y + spacing, z), "minecraft:redstone_wall_torch[facing=north]")  # ON
                schem.setBlock((x, y + 2 * spacing, z),"minecraft:repeater[facing=south,delay=1,locked=false,powered=false]")  # OFF
            elif num == 4:
                schem.setBlock((x, y + spacing, z),"minecraft:repeater[facing=south,delay=1,locked=false,powered=false]")  # OFF
                schem.setBlock((x, y, z),"minecraft:repeater[facing=south,delay=1,locked=false,powered=false]")  # OFF
                schem.setBlock((x, y + 2 * spacing, z),"minecraft:redstone_wall_torch[facing=north]")  # ON
            elif num == 5:
                schem.setBlock((x, y, z), "minecraft:redstone_wall_torch[facing=north]")  # ON
                schem.setBlock((x, y + spacing, z),"minecraft:repeater[facing=south,delay=1,locked=false,powered=false]")  # OFF
                schem.setBlock((x, y + 2 * spacing, z), "minecraft:redstone_wall_torch[facing=north]")  # ON
            elif num == 0:
                schem.setBlock((x, y, z), "minecraft:repeater[facing=south,delay=1,locked=false,powered=false]")  # OFF
                schem.setBlock((x, y + spacing, z),"minecraft:repeater[facing=south,delay=1,locked=false,powered=false]")  # OFF
                schem.setBlock((x, y + 2 * spacing, z),"minecraft:repeater[facing=south,delay=1,locked=false,powered=false]")  # OFF

            schem.setBlock((x, y + 1, z), "minecraft:smooth_quartz_slab[type=top]")
            schem.setBlock((x, y - 1, z), "minecraft:smooth_quartz_slab[type=top]")
            y += spacing * 3  # Move up

        x -= spacing  # Spacing

    schem.save("./schems", filename, mcschematic.Version.JE_1_20_1)
    print(f"Schematic saved as {filename}")
