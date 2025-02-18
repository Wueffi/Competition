from LUT_Generator import *
from DecoderGenerator import *


FOLDER = "schems/"

def main():

    first_LUT = {}

    create_lut_schematic(first_LUT, FOLDER + "LUT.schem")
    create_decoder_schematic(first_LUT.keys(), FOLDER + "Decoder.schem")


    return

if __name__ == '__main__':
    main()