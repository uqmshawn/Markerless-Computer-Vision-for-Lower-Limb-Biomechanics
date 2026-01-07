# Visual Assets Guide for GitHub README

This guide explains how to create and manage all visual assets that appear in the GitHub README homepage.

## 📋 Overview

The README displays visual assets prominently to help visitors quickly understand the project. All assets are stored in the `assets/` directory and referenced in `README.md`.

## 🎯 Quick Start

### Option 1: Generate Placeholders (Immediate)

```bash
# Create placeholder images with labels
python scripts/generate_placeholder_images.py
```

This creates placeholder images for all assets referenced in the README. These are temporary images with text labels that you should replace with actual visualizations.

### Option 2: Generate from Your Data (Recommended)

```bash
# Generate actual visualizations from your research data
python scripts/generate_all_visuals.py --data-dir results/ --output-dir assets/
```

This creates real visualizations from your data files.

### Option 3: Manual Creation

Follow the detailed instructions in `scripts/create_readme_visuals.md` to create each asset manually using your preferred tools.

## 📁 Asset Inventory

### Hero Section (Top of README)

**1. Hero Banner** - `assets/hero-image.png` (1200×400 px)
- **Purpose**: Main visual at the top of README
- **Content**: 4-panel layout showing complete system
  - Panel 1: Multi-camera setup
  - Panel 2: Subject with skeleton overlay
  - Panel 3: 3D reconstruction
  - Panel 4: GRF curves
- **Status**: ⚠️ Placeholder - Replace with actual composite

**2. Running Analysis Demo** - `assets/demos/running-analysis.gif` (600×400 px, 3-5s)
- **Purpose**: Animated demonstration of system in action
- **Content**: Multi-view capture + skeleton overlay + GRF curve
- **Status**: ⚠️ Placeholder - Create from video footage

**3. 3D Reconstruction Demo** - `assets/demos/3d-reconstruction.gif` (400×400 px, 3-5s)
- **Purpose**: Show 3D skeleton reconstruction
- **Content**: Rotating 3D skeleton view
- **Status**: ⚠️ Placeholder - Create from 3D data

### Key Achievements Section

**4. GRF Comparison** - `assets/results/grf-comparison.png` (800×600 px)
- **Purpose**: Main validation results
- **Content**: 3-panel plot (Vertical, AP, ML GRF)
- **Script**: `scripts/generate_all_visuals.py` (included)
- **Status**: ✅ Can be auto-generated from data

**5. Accuracy Comparison** - `assets/results/accuracy-comparison.png` (800×400 px)
- **Purpose**: Compare with state-of-the-art
- **Content**: Table showing performance metrics
- **Script**: See `scripts/create_readme_visuals.md`
- **Status**: ⚠️ Manual creation recommended

### System Architecture Section

**6. Pipeline Flowchart** - `assets/pipeline/pipeline-flowchart.png` (1200×800 px)
- **Purpose**: Visual overview of 7-stage pipeline
- **Content**: Flowchart with all stages, arrows, colors
- **Script**: `scripts/generate_all_visuals.py` (included)
- **Status**: ✅ Can be auto-generated

### Visual Examples Section

**7. Camera Setup** - `assets/setup/camera-setup.png` (800×600 px)
- **Purpose**: Show camera configuration
- **Content**: Top-down view with 4 cameras, dimensions
- **Script**: `scripts/generate_all_visuals.py` (included)
- **Status**: ✅ Can be auto-generated

**8. Pose Detection Demo** - `assets/demos/pose-detection.gif` (400×400 px, 2-3s)
- **Purpose**: Show 2D pose estimation
- **Content**: Video frame with skeleton overlay
- **Status**: ⚠️ Placeholder - Create from video

**9. Calibration Example** - `assets/setup/calibration-example.png` (600×400 px)
- **Purpose**: Show calibration process
- **Content**: Checkerboard detection in multiple views
- **Status**: ⚠️ Manual creation from calibration images

**10. Joint Angles** - `assets/results/joint-angles.png` (800×600 px)
- **Purpose**: Show kinematic validation
- **Content**: Hip, knee, ankle angle trajectories
- **Status**: ⚠️ Create using script template

**11. Temporal Accuracy** - `assets/results/temporal-accuracy.png` (700×500 px)
- **Purpose**: Show contact event detection
- **Content**: Heel strike and toe-off timing
- **Status**: ⚠️ Create using script template

## 🔧 Generation Workflow

### Step 1: Prepare Your Data

Ensure you have the following data files in your `results/` directory:

```
results/
├── grf_estimated.mot          # Your estimated GRF
├── grf_force_plate.mot        # Ground truth GRF
├── ik_markerless.mot          # Markerless joint angles
├── ik_markers.mot             # Marker-based joint angles
├── keypoints_2d/              # 2D pose detections
├── keypoints_3d.trc           # 3D reconstructions
└── videos/                    # Original videos
```

### Step 2: Generate Core Visualizations

```bash
# Auto-generate what can be automated
python scripts/generate_all_visuals.py --data-dir results/ --output-dir assets/

# This creates:
# - assets/pipeline/pipeline-flowchart.png
# - assets/results/grf-comparison.png
# - assets/setup/camera-setup.png
```

### Step 3: Create GIFs from Videos

```bash
# Extract and create running analysis GIF
ffmpeg -i results/videos/running_trial.mp4 -ss 00:00:05 -t 3 \
  -vf "scale=600:-1" temp.mp4

# Add skeleton overlay (use your visualization script)
python scripts/overlay_skeleton.py \
  --video temp.mp4 \
  --keypoints results/keypoints_2d/frame_%04d.json \
  --output temp_skeleton.mp4

# Convert to GIF
ffmpeg -i temp_skeleton.mp4 \
  -vf "fps=15,scale=600:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
  -loop 0 assets/demos/running-analysis.gif

# Optimize
gifsicle -O3 --colors 128 assets/demos/running-analysis.gif \
  -o assets/demos/running-analysis.gif
```

### Step 4: Create Remaining Plots

Use the templates in `scripts/create_readme_visuals.md` to create:
- Joint angles comparison
- Temporal accuracy plot
- Accuracy comparison table

### Step 5: Create Hero Image

Combine multiple images into a single banner:

```python
from PIL import Image

# Load component images
img1 = Image.open('assets/setup/camera-setup.png')
img2 = Image.open('path/to/skeleton_overlay.png')
img3 = Image.open('path/to/3d_reconstruction.png')
img4 = Image.open('assets/results/grf-comparison.png')

# Resize to same height (400px)
height = 400
imgs = [img1, img2, img3, img4]
imgs_resized = [img.resize((300, height)) for img in imgs]

# Concatenate horizontally
total_width = sum(img.width for img in imgs_resized)
hero = Image.new('RGB', (total_width, height))

x_offset = 0
for img in imgs_resized:
    hero.paste(img, (x_offset, 0))
    x_offset += img.width

hero.save('assets/hero-image.png')
```

### Step 6: Optimize All Images

```bash
# Install optimization tools
pip install pillow-simd
npm install -g svgo

# Optimize PNGs
for file in assets/**/*.png; do
    pngquant --quality=80-95 "$file" --output "$file" --force
done

# Optimize GIFs
for file in assets/**/*.gif; do
    gifsicle -O3 --colors 128 "$file" -o "$file"
done
```

## ✅ Quality Checklist

Before committing assets to the repository:

### Image Quality
- [ ] All images are clear and readable
- [ ] Text is legible at GitHub's display size
- [ ] Colors are consistent across images
- [ ] No artifacts or compression issues

### File Sizes
- [ ] PNG images < 500 KB each
- [ ] GIF animations < 5 MB each
- [ ] Total assets folder < 20 MB

### Completeness
- [ ] All 11 assets are present
- [ ] No broken image links in README
- [ ] Placeholder images replaced with actual data

### Technical
- [ ] Correct dimensions for each asset
- [ ] Proper file formats (PNG for static, GIF for animated)
- [ ] Images optimized for web

## 🧪 Testing

Preview your README locally before pushing:

```bash
# Install grip (GitHub README preview)
pip install grip

# Preview README
grip README.md

# Open http://localhost:6419 in browser
```

Check that:
1. All images load correctly
2. Images are properly sized
3. GIFs animate smoothly
4. Layout looks good on different screen sizes

## 📊 Asset Status Dashboard

| Asset | File | Size | Status | Priority |
|-------|------|------|--------|----------|
| Hero Banner | `assets/hero-image.png` | 1200×400 | ⚠️ Placeholder | High |
| Pipeline Flowchart | `assets/pipeline/pipeline-flowchart.png` | 1200×800 | ✅ Auto-gen | High |
| GRF Comparison | `assets/results/grf-comparison.png` | 800×600 | ✅ Auto-gen | High |
| Accuracy Table | `assets/results/accuracy-comparison.png` | 800×400 | ⚠️ Manual | Medium |
| Joint Angles | `assets/results/joint-angles.png` | 800×600 | ⚠️ Template | Medium |
| Temporal Accuracy | `assets/results/temporal-accuracy.png` | 700×500 | ⚠️ Template | Medium |
| Camera Setup | `assets/setup/camera-setup.png` | 800×600 | ✅ Auto-gen | High |
| Calibration Example | `assets/setup/calibration-example.png` | 600×400 | ⚠️ Manual | Low |
| Running Demo GIF | `assets/demos/running-analysis.gif` | 600×400 | ⚠️ Video | High |
| Pose Detection GIF | `assets/demos/pose-detection.gif` | 400×400 | ⚠️ Video | Medium |
| 3D Reconstruction GIF | `assets/demos/3d-reconstruction.gif` | 400×400 | ⚠️ Video | Medium |

**Legend**:
- ✅ Auto-gen: Can be automatically generated
- ⚠️ Manual: Requires manual creation
- ⚠️ Template: Script template available
- ⚠️ Video: Requires video processing
- ⚠️ Placeholder: Currently using placeholder

## 🎓 Best Practices

1. **Use High-Quality Source Data**: Better input = better visualizations
2. **Consistent Styling**: Use same color schemes and fonts across all assets
3. **Optimize for Web**: Compress images without losing quality
4. **Test on Different Devices**: Check how images look on mobile and desktop
5. **Version Control**: Keep source files (e.g., .ai, .psd) in a separate directory
6. **Document Changes**: Update this guide when adding new assets

## 📚 Additional Resources

- **Detailed Instructions**: `scripts/create_readme_visuals.md`
- **Asset Organization**: `assets/README.md`
- **Auto-generation Script**: `scripts/generate_all_visuals.py`
- **Placeholder Generator**: `scripts/generate_placeholder_images.py`

## 🆘 Troubleshooting

**Images not showing in README**:
- Check file paths are correct (case-sensitive)
- Ensure files are committed to repository
- Verify file extensions match references

**GIFs too large**:
- Reduce frame rate (15 fps is usually sufficient)
- Decrease resolution
- Reduce color palette (128 colors)
- Shorten duration (3-5 seconds max)

**Poor image quality**:
- Increase DPI when generating (150-300)
- Use vector formats (SVG) when possible
- Avoid excessive compression

---

**Last Updated**: 2024-01-XX

**Maintainer**: [Your Name]

**Questions?** See `CONTRIBUTING.md` or open an issue.

