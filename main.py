from LUT_Generator import LUT_Generator
from SchematicGenerator import *

def main():

    lut_gen = LUT_Generator()
    stage1_LUT, left_right_LUT, stage2_LUT = lut_gen.generate_LUT()

    lut_gen.print_LUTs()

    print(stage1_LUT.values())
    print()
    print(left_right_LUT.values())
    print()
    print(stage2_LUT.values())

    create_lut_schematic(stage1_LUT.values(), "LUT1")
    create_decoder_schematic(stage1_LUT.keys(), "Decoder1")
    create_lut_schematic(left_right_LUT.values(), "LUT2")
    create_decoder_schematic(left_right_LUT.keys(), "Decoder2")
    create_3rd_lut_schematic(stage2_LUT.values(), "LUT3")
    create_3b_decoder_schematic(stage2_LUT.keys(), "Decoder3")

    return

if __name__ == '__main__':
    main()
