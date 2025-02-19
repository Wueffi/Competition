from LUT_Generator import LUT_Generator
from SchematicGenerator import *


FOLDER = "schems/"

def main():

    lut_gen = LUT_Generator()
    stage1_LUT, left_right_LUT, stage2_LUT = lut_gen.generate_LUT()

    lut_gen.print_LUTs()

    create_lut_schematic(stage1_LUT, FOLDER + "LUT1.schem")
    create_decoder_schematic(stage1_LUT.keys(), FOLDER + "Decoder1.schem")

    create_lut_schematic(left_right_LUT, FOLDER + "LUT2.schem")
    create_decoder_schematic(left_right_LUT.keys(), FOLDER + "Decoder2.schem")

    create_lut_schematic(stage2_LUT, FOLDER + "LUT3.schem")
    create_decoder_schematic(stage2_LUT.keys(), FOLDER + "Decoder3.schem")

    return

if __name__ == '__main__':
    main()