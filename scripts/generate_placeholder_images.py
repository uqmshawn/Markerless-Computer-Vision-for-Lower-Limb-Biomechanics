#!/usr/bin/env python3
"""
Generate placeholder images for GitHub README.

This script creates placeholder images with text labels for all assets
referenced in the README. Replace these with actual images from your research.
"""

import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Create assets directories
ASSETS_DIR = "assets"
DIRS = [
    "assets/pipeline",
    "assets/results",
    "assets/demos",
    "assets/setup",
    "assets/badges",
    "assets/logos"
]

for dir_path in DIRS:
    os.makedirs(dir_path, exist_ok=True)

def create_placeholder(width, height, text, filename, bg_color=(240, 240, 245)):
    """Create a placeholder image with centered text."""
    # Create image
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fall back to default if not available
    try:
        font_size = min(width, height) // 15
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Add border
    border_color = (100, 100, 120)
    border_width = 3
    draw.rectangle(
        [(0, 0), (width-1, height-1)],
        outline=border_color,
        width=border_width
    )
    
    # Add text
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    
    draw.text((text_x, text_y), text, fill=(60, 60, 80), font=font)
    
    # Add "PLACEHOLDER" watermark
    try:
        watermark_font = ImageFont.truetype("arial.ttf", font_size // 2)
    except:
        watermark_font = font
    
    watermark_text = "PLACEHOLDER - Replace with actual image"
    watermark_bbox = draw.textbbox((0, 0), watermark_text, font=watermark_font)
    watermark_width = watermark_bbox[2] - watermark_bbox[0]
    
    watermark_x = (width - watermark_width) // 2
    watermark_y = height - 40
    
    draw.text((watermark_x, watermark_y), watermark_text, 
              fill=(150, 150, 160), font=watermark_font)
    
    # Save
    img.save(filename)
    print(f"Created: {filename}")

def create_animated_placeholder(width, height, text, filename):
    """Create a simple animated GIF placeholder."""
    frames = []
    colors = [
        (240, 240, 245),
        (245, 240, 240),
        (240, 245, 240),
        (245, 245, 240)
    ]
    
    for i, color in enumerate(colors):
        frame_text = f"{text}\nFrame {i+1}/{len(colors)}"
        img = Image.new('RGB', (width, height), color=color)
        draw = ImageDraw.Draw(img)
        
        # Border
        draw.rectangle([(0, 0), (width-1, height-1)], 
                      outline=(100, 100, 120), width=3)
        
        # Text
        try:
            font = ImageFont.truetype("arial.ttf", min(width, height) // 20)
        except:
            font = ImageFont.load_default()
        
        # Center text
        lines = frame_text.split('\n')
        y_offset = height // 3
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            draw.text((x, y_offset), line, fill=(60, 60, 80), font=font)
            y_offset += bbox[3] - bbox[1] + 10
        
        frames.append(img)
    
    # Save as GIF
    frames[0].save(
        filename,
        save_all=True,
        append_images=frames[1:],
        duration=500,
        loop=0
    )
    print(f"Created: {filename}")

# Generate all placeholder images
print("Generating placeholder images...")
print("=" * 60)

# Hero image
create_placeholder(
    1200, 400,
    "Markerless Biomechanical Analysis System\n4-Camera Setup + Skeleton + GRF Curves",
    f"{ASSETS_DIR}/hero-image.png"
)

# Pipeline diagrams
create_placeholder(
    1200, 800,
    "7-Stage Pipeline Flowchart\nCalibration → Enhancement → Pose → Sync → 3D → Mapping → GRF",
    f"{ASSETS_DIR}/pipeline/pipeline-flowchart.png"
)

create_placeholder(
    1000, 1200,
    "Detailed Architecture\nTechnical Components & Data Flow",
    f"{ASSETS_DIR}/pipeline/architecture-detailed.png"
)

# Results graphs
create_placeholder(
    800, 600,
    "GRF Comparison\nEstimated vs. Force Plate\nVertical, AP, ML Components",
    f"{ASSETS_DIR}/results/grf-comparison.png"
)

create_placeholder(
    800, 400,
    "Accuracy Comparison Table\nOur System vs. State-of-the-Art Methods",
    f"{ASSETS_DIR}/results/accuracy-comparison.png"
)

create_placeholder(
    800, 600,
    "Joint Kinematics Comparison\nHip, Knee, Ankle Angles\nMarkerless vs. Marker-Based",
    f"{ASSETS_DIR}/results/joint-angles.png"
)

create_placeholder(
    700, 500,
    "Contact Event Detection\nHeel Strike & Toe-Off Timing\nTemporal Accuracy",
    f"{ASSETS_DIR}/results/temporal-accuracy.png"
)

# Setup images
create_placeholder(
    800, 600,
    "4-Camera Setup Configuration\nTop-Down View with Angles & Distances",
    f"{ASSETS_DIR}/setup/camera-setup.png"
)

create_placeholder(
    600, 400,
    "Calibration Example\nCheckerboard Detection in Multiple Views",
    f"{ASSETS_DIR}/setup/calibration-example.png"
)

# Demo GIFs
create_animated_placeholder(
    600, 400,
    "Running Analysis Demo\nMulti-View + Skeleton + GRF",
    f"{ASSETS_DIR}/demos/running-analysis.gif"
)

create_animated_placeholder(
    400, 400,
    "2D Pose Detection\nReal-Time Keypoint Tracking",
    f"{ASSETS_DIR}/demos/pose-detection.gif"
)

create_animated_placeholder(
    400, 400,
    "3D Reconstruction\nRotating Skeleton View",
    f"{ASSETS_DIR}/demos/3d-reconstruction.gif"
)

print("=" * 60)
print(f"\nGenerated {len(DIRS)} placeholder images in {ASSETS_DIR}/")
print("\nNext steps:")
print("1. Run your pipeline on actual data")
print("2. Use visualization scripts to generate real images")
print("3. Replace placeholders with actual images")
print("4. Optimize images for web (compress, resize)")
print("\nSee assets/README.md for detailed instructions.")

