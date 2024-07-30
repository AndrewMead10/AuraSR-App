# cli.py
import argparse
from pathlib import Path
from PIL import Image
from aura_sr import AuraSR


def upscale_image(input_path, output_path):
    aura_sr = AuraSR.from_pretrained("fal/AuraSR-v2")
    image = Image.open(input_path)
    upscaled_image = aura_sr.upscale_4x_overlapped(image)
    upscaled_image.save(output_path)


def main():
    parser = argparse.ArgumentParser(description="Upscale images using AuraSR")
    parser.add_argument("input", help="Input file or folder")
    parser.add_argument("output", help="Output folder")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if input_path.is_file():
        output_file = output_path / f"upscaled_{input_path.name}"
        upscale_image(input_path, output_file)
        print(f"Upscaled {input_path} to {output_file}")
    elif input_path.is_dir():
        output_path.mkdir(parents=True, exist_ok=True)
        for file in input_path.glob("*"):
            if file.suffix.lower() in [".png", ".jpg", ".jpeg"]:
                output_file = output_path / f"upscaled_{file.name}"
                upscale_image(file, output_file)
                print(f"Upscaled {file} to {output_file}")
    else:
        print("Invalid input path")


if __name__ == "__main__":
    main()
