#!/usr/bin/env python3
"""
Source Set WebP Maker

A script to convert images to WebP format and create multiple resized versions
for responsive web design. Creates a source set with specified widths.
"""

import os
import argparse
import sys
from pathlib import Path
from PIL import Image

# Supported input formats
SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.tif', '.gif'}

def create_directory(path):
    """Create directory if it doesn't exist."""
    Path(path).mkdir(parents=True, exist_ok=True)

def get_image_files(folder_path):
    """Get all image files from the folder."""
    folder = Path(folder_path)
    image_files = []
    
    for ext in SUPPORTED_FORMATS:
        image_files.extend(folder.glob(f'*{ext}'))
        image_files.extend(folder.glob(f'*{ext.upper()}'))
    
    return image_files

def resize_image(image, target_width):
    """Resize image maintaining aspect ratio."""
    if image.width <= target_width:
        return image
    
    ratio = target_width / image.width
    new_height = int(image.height * ratio)
    return image.resize((target_width, new_height), Image.Resampling.LANCZOS)

def convert_to_webp(input_path, output_path, quality=80):
    """Convert image to WebP format."""
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (WebP doesn't support RGBA)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create white background for transparent images
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            img.save(output_path, 'WEBP', quality=quality, method=6)
        return True
    except Exception as e:
        print(f"Error converting {input_path}: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Convert images to WebP format and create multiple resized versions for responsive web design.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f'''
Supported input formats: {', '.join(sorted(SUPPORTED_FORMATS))}

Example usage:
  python sourcesetwebpmaker.py --folder "/path/to/images" --savepath "/path/to/output" --widths 320 640 960 1200
  
The script will create the following structure:
  /path/to/output/
  ├── 320/
  ├── 640/
  ├── 960/
  ├── originalsize/
  └── sourceset_info.txt
        '''
    )
    
    parser.add_argument('--folder', required=True, 
                       help='Path to the folder containing source images')
    parser.add_argument('--savepath', required=True,
                       help='Path where the WebP images will be saved')
    parser.add_argument('--widths', nargs='+', type=int, default=[320, 640, 960],
                       help='List of target widths for resized versions (default: 320 640 960)')
    parser.add_argument('--quality', type=int, default=80, choices=range(1, 101),
                       metavar='[1-100]', help='WebP quality setting (default: 80)')
    
    args = parser.parse_args()
    
    # Validate inputs
    source_folder = Path(args.folder)
    if not source_folder.exists():
        print(f"Error: Source folder '{source_folder}' does not exist.")
        sys.exit(1)
    
    if not source_folder.is_dir():
        print(f"Error: '{source_folder}' is not a directory.")
        sys.exit(1)
    
    # Get image files
    image_files = get_image_files(source_folder)
    if not image_files:
        print(f"No supported image files found in '{source_folder}'.")
        print(f"Supported formats: {', '.join(sorted(SUPPORTED_FORMATS))}")
        sys.exit(1)
    
    print(f"Found {len(image_files)} image file(s) to process.")
    
    # Create output directory structure
    output_base = Path(args.savepath)
    create_directory(output_base)
    
    # Create width directories
    width_dirs = {}
    for width in args.widths:
        width_dir = output_base / str(width)
        create_directory(width_dir)
        width_dirs[width] = width_dir
    
    # Create originalsize directory
    original_dir = output_base / "originalsize"
    create_directory(original_dir)
    
    # Process images
    successful_conversions = 0
    
    for image_path in image_files:
        print(f"Processing: {image_path.name}")
        
        try:
            with Image.open(image_path) as original_img:
                # Create resized versions
                for width, width_dir in width_dirs.items():
                    if original_img.width > width:
                        resized_img = resize_image(original_img, width)
                        output_path = width_dir / f"{image_path.stem}.webp"
                        convert_to_webp(resized_img, output_path, args.quality)
                    else:
                        # If original is smaller than target width, use original
                        output_path = width_dir / f"{image_path.stem}.webp"
                        convert_to_webp(original_img, output_path, args.quality)
                
                # Create original size version
                original_output_path = original_dir / f"{image_path.stem}.webp"
                if convert_to_webp(original_img, original_output_path, args.quality):
                    successful_conversions += 1
                
        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")
            continue
    
    # Create info file
    info_file = output_base / "sourceset_info.txt"
    with open(info_file, 'w') as f:
        f.write("Source Set WebP Maker - Generated Files\n")
        f.write("=======================================\n\n")
        f.write(f"Source folder: {source_folder}\n")
        f.write(f"Output folder: {output_base}\n")
        f.write(f"Target widths: {', '.join(map(str, sorted(args.widths)))}\n")
        f.write(f"WebP quality: {args.quality}\n")
        f.write(f"Images processed: {len(image_files)}\n")
        f.write(f"Successful conversions: {successful_conversions}\n\n")
        f.write("Directory structure:\n")
        for width in sorted(args.widths):
            f.write(f"  {width}/ - Images resized to {width}px wide\n")
        f.write("  originalsize/ - Original size WebP conversions\n")
    
    print(f"\nProcessing complete!")
    print(f"Successfully converted {successful_conversions} out of {len(image_files)} images")
    print(f"Output saved to: {output_base}")
    print(f"Details saved to: {info_file}")

if __name__ == "__main__":
    main()
