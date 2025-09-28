# Source Set WebP Maker

A Python script that converts images to WebP format and creates multiple resized versions for responsive web design. Perfect for generating source sets for modern websites.

## Features

- 🔄 Convert multiple image formats to WebP
- 📱 Generate multiple responsive image sizes
- 🎯 Maintain aspect ratio during resizing
- 📁 Organized folder structure output
- ⚡ Fast batch processing
- 🛠️ Configurable quality settings
- 📄 Detailed processing summary

## Supported Input Formats

- JPEG/JPG
- PNG
- WebP
- BMP
- TIFF/TIF
- GIF

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository
2. Install required dependencies:

```bash
pip install -r requirements.txt
```
## Usage
### Basic usage
```python sourcesetmaker.py --folder "/path/to/your/images" --savepath "/path/to/output"```
### Advanced usage
``` python sourcesetmaker.py \
  --folder "/path/to/your/images" \
  --savepath "/path/to/output" \
  --widths 320 640 960 1200 1600 \
  --quality 85
```


#### Example usage in html
```
<picture>
  <source 
    type="image/webp"
    srcset="
      images/320/photo.webp 320w,
      images/640/photo.webp 640w,
      images/960/photo.webp 960w,
      images/originalsize/photo.webp 1200w"
    sizes="(max-width: 400px) 320px,
           (max-width: 800px) 640px,
           960px">
  <img 
    src="images/originalsize/photo.webp" 
    alt="Description" 
    loading="lazy">
</picture>
```
