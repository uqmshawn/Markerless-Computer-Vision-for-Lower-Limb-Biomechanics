# Assets for GitHub README

This directory contains all visual assets that are displayed in the main README.md file on GitHub.

## Directory Structure

```
assets/
├── pipeline/              # Pipeline diagrams and flowcharts
├── results/               # Results graphs and comparisons
├── demos/                 # Demo GIFs and short videos
├── setup/                 # Camera setup and calibration images
├── badges/                # Custom badges and icons
└── logos/                 # Project logos and branding
```

## Files for README Display

### Hero Image
**`hero-image.png`** - Main banner image showing the complete system
- Dimensions: 1200×400 px
- Shows: 4-camera setup + skeleton overlay + GRF curves

### Pipeline Diagram
**`pipeline/pipeline-flowchart.png`** - Complete 7-stage pipeline
- Dimensions: 1200×800 px
- Format: PNG with transparent background
- Shows: All stages with icons and data flow

### Results Comparison
**`results/grf-comparison.png`** - GRF estimation vs. force plate
- Dimensions: 800×600 px
- Shows: Vertical, AP, ML force curves side-by-side

**`results/accuracy-table.png`** - Performance metrics table
- Dimensions: 800×400 px
- Shows: Comparison with state-of-the-art methods

**`results/joint-angles.png`** - Joint kinematics comparison
- Dimensions: 800×600 px
- Shows: Hip, knee, ankle angles

### Demo GIFs
**`demos/running-analysis.gif`** - Running gait analysis demo
- Dimensions: 600×400 px
- Duration: 3-5 seconds
- Shows: Multi-view capture + skeleton + GRF curve

**`demos/pose-detection.gif`** - 2D pose estimation in action
- Dimensions: 400×400 px
- Duration: 2-3 seconds
- Shows: Real-time keypoint detection

**`demos/3d-reconstruction.gif`** - 3D skeleton reconstruction
- Dimensions: 400×400 px
- Duration: 3-5 seconds
- Shows: Rotating 3D skeleton view

### Setup Images
**`setup/camera-setup.png`** - 4-camera configuration diagram
- Dimensions: 800×600 px
- Shows: Top-down view with angles and distances

**`setup/calibration-example.png`** - Calibration process
- Dimensions: 600×400 px
- Shows: Checkerboard detection in multiple views

### Architecture Diagram
**`pipeline/architecture-detailed.png`** - Technical architecture
- Dimensions: 1000×1200 px
- Shows: Detailed component breakdown with technologies

## Image Specifications

### Format Guidelines
- **PNG**: For diagrams, screenshots, static images
- **GIF**: For short animations (< 5 seconds, < 5 MB)
- **SVG**: For scalable diagrams (when possible)
- **JPG**: For photographs (compressed)

### Size Guidelines
- Hero images: 1200×400 px
- Full-width diagrams: 1000-1200 px wide
- Inline images: 600-800 px wide
- Thumbnails: 300-400 px wide
- GIFs: 400-600 px, < 5 MB

### Optimization
- Compress PNG files with tools like TinyPNG
- Optimize GIFs with Gifsicle or similar
- Use appropriate resolution (2× for retina displays)
- Keep file sizes reasonable (< 500 KB for images, < 5 MB for GIFs)

## Creating Assets

### Pipeline Diagram
Use draw.io or similar tools:
1. Create flowchart with 7 stages
2. Use consistent colors and icons
3. Export as PNG (high resolution)
4. Optimize file size

### Results Graphs
Use Python/Matplotlib:
```python
import matplotlib.pyplot as plt
import numpy as np

# Create figure
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

# Plot vertical GRF
axes[0].plot(time, grf_force_plate, 'k-', label='Force Plate', linewidth=2)
axes[0].plot(time, grf_estimated, 'r--', label='Estimated', linewidth=2)
axes[0].set_xlabel('Time (s)')
axes[0].set_ylabel('Vertical GRF (BW)')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Save
plt.tight_layout()
plt.savefig('assets/results/grf-comparison.png', dpi=150, bbox_inches='tight')
```

### Demo GIFs
Use FFmpeg to create GIFs from videos:
```bash
# Extract 3-second clip
ffmpeg -i input.mp4 -ss 00:00:05 -t 3 -vf "scale=600:-1" temp.mp4

# Convert to GIF
ffmpeg -i temp.mp4 -vf "fps=15,scale=600:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 output.gif

# Optimize
gifsicle -O3 --colors 128 output.gif -o optimized.gif
```

## Placeholder Images

Until actual images are created, this directory contains placeholder references. To generate actual images:

1. **Run the pipeline** on your data
2. **Use visualization scripts** in `scripts/` directory
3. **Create diagrams** using provided templates
4. **Optimize and place** in appropriate subdirectories

## Usage in README

Images are referenced in README.md using relative paths:

```markdown
![Pipeline Overview](assets/pipeline/pipeline-flowchart.png)

![GRF Comparison](assets/results/grf-comparison.png)

![Demo](assets/demos/running-analysis.gif)
```

## Attribution

All images and diagrams are original work created for this thesis project, unless otherwise noted.

### Third-Party Assets
- Icons: [Source if applicable]
- Diagrams: Created with draw.io
- Graphs: Generated with Matplotlib

## License

All assets in this directory are released under the same MIT License as the project.

---

**Back to**: [Main README](../README.md)

