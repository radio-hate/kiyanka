# Kiyanka

Kiyanka is a Python-based CLI tool for resizing images with multiple strategies including padding, fitting, and cropping. Built on top of Pillow.

## Features

- 5 resize modes (thumbnail, contain, cover, fit, pad)
- Interactive command-line interface
- Optional RGBA padding color
- Easy installation via Poetry

## Resize Modes

ID | Mode       | Description
---|------------|------------------------------------------------------
0  | thumbnail  | Proportional downscale (in-place)
1  | contain    | Scales to fit inside the box
2  | cover      | Scales and crops to fill the box
3  | fit        | Similar to cover but supports alignment
4  | pad        | Adds padding to reach target size; supports RGBA

## Installation

poetry config virtualenvs.in-project true  
poetry install

## Run

poetry run python main.py

## Example

>> resize C:/images/cat.jpg 512,512 2 .png

For padding mode (4), you'll be prompted to enter a color:  
Enter pad color as R,G,B,A (e.g. 0,0,0,255): >> 255,255,255,255

## Project Structure

- main.py — Entry point, launches CLI
- cli.py — Command parsing and interaction
- logic.py — Controls image processing
- functions.py — Image resize and save logic
- models.py — Data class with input params and modes

## TODO

- CLI help for each mode
- Batch mode support
- Auto-select output format from extension

## Requirements

- Python 3.10.x
- Pillow
