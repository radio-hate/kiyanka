# Kiyanka

Kiyanka is a Python-based CLI tool for image resizing and background removal using Pillow and rembg.

## Features

- 5 resize modes (thumbnail, contain, cover, fit, pad)
- Background removal using `rembg` (default mode: hard edges)
- Optional RGBA padding color for pad mode
- Interactive CLI
- Easy setup via Poetry

## Resize Modes

ID | Mode       | Description
---|------------|------------------------------------------------------
0  | thumbnail  | Proportional downscale (in-place)
1  | contain    | Scales to fit inside the box
2  | cover      | Scales and crops to fill the box
3  | fit        | Similar to cover but supports alignment
4  | pad        | Adds padding to reach target size; supports RGBA

## Installation

```bash
poetry config virtualenvs.in-project true
poetry install
```

## Run

```bash
poetry run python main.py
```

## Resize Example

```bash
>> resize C:/images/cat.jpg 512,512 2 .png
```

For padding mode (4), you'll be prompted to enter a color:

```
Enter pad color as R,G,B,A (e.g. 0,0,0,255): >> 255,255,255,255
```

## Background Removal Example

```bash
>> rembg C:/images/cat.jpg hard
```

Available edge modes: `soft` (alpha blend) or `hard` (binary mask).  
Default: `hard`.

## Project Structure

- `main.py` — Entry point, launches CLI
- `cli.py` — Command parsing and interaction
- `logic.py` — Controls image processing
- `functions.py` — Image operations
- `models.py` — Data classes and constants

## TODO

- GUI and context menu integration
- Batch mode

## Requirements

- Python 3.10+
- Pillow
- rembg