import sys
from generator_refactor.generator import generate

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python generate_html.py input_dir out_dir")
        sys.exit(1)
    generate(sys.argv[1], sys.argv[2])