# main.py
from lexer import ObsLexer
from parser import ObsParser
from translator import translate

import sys
import os

if __name__ == "__main__":
    filename = sys.argv[1]

    with open(filename) as f:
        text = f.read()

    lexer = ObsLexer()
    parser = ObsParser()

    ast = parser.parse(lexer.tokenize(text))
    c_code = translate(ast)

    out_name = "out/" + os.path.basename(filename).replace(".obs", ".c")
    with open(out_name, "w") as f:
        f.write(c_code)

    print(f"Arquivo gerado: {out_name}")
