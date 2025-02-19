from LUT_Generator import LUT_Generator
from SchematicGenerator import *


FOLDER = "schems/"

def main():

    lut_gen = LUT_Generator()
    stage1_LUT, left_right_LUT, stage2_LUT = lut_gen.generate_LUT()

    lut_gen.print_LUTs()

    create_lut_schematic(stage1_LUT, FOLDER + "LUT.schem")
    create_decoder_schematic(stage1_LUT.keys(), FOLDER + "Decoder.schem")


    return

if __name__ == '__main__':
    main()