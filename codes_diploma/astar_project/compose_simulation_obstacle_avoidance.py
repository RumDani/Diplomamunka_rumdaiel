"""Harom szimulacios kepkocka egyetlen, beillesztheto abrahoz."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from PIL import Image


FRAME_DIRECTORY = Path(__file__).resolve().parent / "results" / "figures"
FRAME_NAMES = (
    "simulation_02_frame_0100.png",
    "simulation_03_frame_0250.png",
    "simulation_04_frame_0500.png",
)
CROP_BOX = (570, 235, 1810, 1035)


def main():
    figure, axes = plt.subplots(1, 3, figsize=(18, 6), dpi=180)
    figure.subplots_adjust(wspace=0.03, left=0, right=1, top=1, bottom=0)

    for axis, filename in zip(axes, FRAME_NAMES):
        image_path = FRAME_DIRECTORY / filename
        if not image_path.exists():
            raise FileNotFoundError(f"Hianyzo szimulacios kepkocka: {image_path}")
        with Image.open(image_path) as source_image:
            grid_image = source_image.crop(CROP_BOX)
        axis.imshow(grid_image)
        axis.axis("off")

    output_path = FRAME_DIRECTORY / "simulation_obstacle_avoidance_sequence.png"
    figure.savefig(output_path, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    print(f"Abra mentve: {output_path}")


if __name__ == "__main__":
    main()
