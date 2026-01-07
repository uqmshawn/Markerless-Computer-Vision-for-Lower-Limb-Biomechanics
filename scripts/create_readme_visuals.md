# Creating Visual Assets for GitHub README

This guide explains how to create all the visual assets referenced in the main README.md file.

## Quick Start

```bash
# 1. Generate placeholder images first
python scripts/generate_placeholder_images.py

# 2. Run your pipeline to get actual data
python main.py --config config/default.yaml

# 3. Generate actual visualizations
python scripts/generate_all_visuals.py --data-dir results/
```

## Asset Checklist

### Required Images

- [ ] `assets/hero-image.png` - Main banner (1200×400)
- [ ] `assets/pipeline/pipeline-flowchart.png` - Pipeline diagram (1200×800)
- [ ] `assets/results/grf-comparison.png` - GRF curves (800×600)
- [ ] `assets/results/accuracy-comparison.png` - Accuracy table (800×400)
- [ ] `assets/results/joint-angles.png` - Joint kinematics (800×600)
- [ ] `assets/results/temporal-accuracy.png` - Contact events (700×500)
- [ ] `assets/setup/camera-setup.png` - Camera configuration (800×600)
- [ ] `assets/setup/calibration-example.png` - Calibration (600×400)

### Required GIFs

- [ ] `assets/demos/running-analysis.gif` - Running demo (600×400, 3-5s)
- [ ] `assets/demos/pose-detection.gif` - Pose estimation (400×400, 2-3s)
- [ ] `assets/demos/3d-reconstruction.gif` - 3D skeleton (400×400, 3-5s)

## Detailed Instructions

### 1. Hero Image (1200×400)

**Composition**: 4-panel layout showing the complete system

**Panel 1**: Multi-camera setup (300×400)
**Panel 2**: Subject with skeleton overlay (300×400)
**Panel 3**: 3D reconstruction (300×400)
**Panel 4**: GRF curves (300×400)

**Creation**:
```python
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(12, 4))
gs = GridSpec(1, 4, figure=fig)

# Panel 1: Camera setup
ax1 = fig.add_subplot(gs[0, 0])
# Add camera setup image or diagram

# Panel 2: Skeleton overlay
ax2 = fig.add_subplot(gs[0, 1])
# Add video frame with skeleton

# Panel 3: 3D reconstruction
ax3 = fig.add_subplot(gs[0, 2])
# Add 3D skeleton view

# Panel 4: GRF curves
ax4 = fig.add_subplot(gs[0, 3])
# Add GRF plot

plt.tight_layout()
plt.savefig('assets/hero-image.png', dpi=150, bbox_inches='tight')
```

### 2. Pipeline Flowchart (1200×800)

**Tool**: Use draw.io, Lucidchart, or Python's graphviz

**Elements**:
- 7 boxes for each stage
- Arrows showing data flow
- Icons for each stage
- Color coding by category

**draw.io Template**:
1. Open https://app.diagrams.net/
2. Create new diagram
3. Add 7 rounded rectangles
4. Add arrows between them
5. Add icons and labels
6. Export as PNG (300 DPI)

**Python Alternative**:
```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(12, 8))

stages = [
    "1. Camera\nCalibration",
    "2. Video\nEnhancement",
    "3. 2D Pose\nEstimation",
    "4. Camera\nSync",
    "5. 3D\nTriangulation",
    "6. Marker\nMapping",
    "7. GRF\nEstimation"
]

colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE']

y_positions = [7, 6, 5, 4, 3, 2, 1]

for i, (stage, color, y) in enumerate(zip(stages, colors, y_positions)):
    # Draw box
    box = FancyBboxPatch((1, y-0.3), 3, 0.6, 
                         boxstyle="round,pad=0.1", 
                         facecolor=color, 
                         edgecolor='black', 
                         linewidth=2)
    ax.add_patch(box)
    
    # Add text
    ax.text(2.5, y, stage, ha='center', va='center', 
            fontsize=12, fontweight='bold')
    
    # Add arrow to next stage
    if i < len(stages) - 1:
        arrow = FancyArrowPatch((2.5, y-0.4), (2.5, y_positions[i+1]+0.4),
                               arrowstyle='->', mutation_scale=20, 
                               linewidth=2, color='black')
        ax.add_patch(arrow)

ax.set_xlim(0, 5)
ax.set_ylim(0, 8)
ax.axis('off')

plt.tight_layout()
plt.savefig('assets/pipeline/pipeline-flowchart.png', dpi=150, bbox_inches='tight')
```

### 3. GRF Comparison (800×600)

**Data Required**: 
- `grf_estimated.mot` - Your estimated GRF
- `grf_force_plate.mot` - Ground truth from force plate

**Script**:
```python
import numpy as np
import matplotlib.pyplot as plt

# Load data
time, grf_est = load_mot_file('results/grf_estimated.mot')
time, grf_fp = load_mot_file('results/grf_force_plate.mot')

# Create figure
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

components = ['Vertical', 'Anterior-Posterior', 'Medial-Lateral']
indices = [1, 2, 3]  # Column indices in MOT file

for ax, comp, idx in zip(axes, components, indices):
    ax.plot(time, grf_fp[:, idx], 'k-', linewidth=2, label='Force Plate')
    ax.plot(time, grf_est[:, idx], 'r--', linewidth=2, label='Estimated')
    
    ax.set_xlabel('Time (s)', fontsize=11)
    ax.set_ylabel('Force (BW)', fontsize=11)
    ax.set_title(f'{comp} GRF', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    
    # Add RMSE annotation
    rmse = np.sqrt(np.mean((grf_fp[:, idx] - grf_est[:, idx])**2))
    ax.text(0.95, 0.95, f'RMSE: {rmse:.3f} BW', 
            transform=ax.transAxes, ha='right', va='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('assets/results/grf-comparison.png', dpi=150, bbox_inches='tight')
```

### 4. Accuracy Comparison Table (800×400)

**Script**:
```python
import matplotlib.pyplot as plt
import pandas as pd

# Data
data = {
    'Method': ['Our System', 'Needham et al.', 'Seethapathi et al.', 'Marker-Based'],
    'Vertical RMSE (BW)': [0.14, 0.18, 0.22, 0.08],
    'Correlation (r)': [0.95, 0.91, 0.87, 0.98],
    'Equipment': ['Smartphones', 'RGB Cameras', 'RGB Cameras', 'Markers + Cameras']
}

df = pd.DataFrame(data)

fig, ax = plt.subplots(figsize=(10, 4))
ax.axis('tight')
ax.axis('off')

table = ax.table(cellText=df.values, colLabels=df.columns,
                cellLoc='center', loc='center',
                colWidths=[0.25, 0.25, 0.2, 0.3])

table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 2)

# Color header
for i in range(len(df.columns)):
    table[(0, i)].set_facecolor('#4ECDC4')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Highlight our system
for i in range(len(df.columns)):
    table[(1, i)].set_facecolor('#FFE5E5')

plt.savefig('assets/results/accuracy-comparison.png', dpi=150, bbox_inches='tight')
```

### 5. Joint Angles Comparison (800×600)

**Script**:
```python
import matplotlib.pyplot as plt

# Load data
time, angles_markerless = load_mot_file('results/ik_markerless.mot')
time, angles_markers = load_mot_file('results/ik_markers.mot')

fig, axes = plt.subplots(3, 1, figsize=(10, 8))

joints = ['Hip Flexion', 'Knee Flexion', 'Ankle Dorsiflexion']
columns = [5, 6, 7]  # Adjust based on your MOT file

for ax, joint, col in zip(axes, joints, columns):
    ax.plot(time, angles_markers[:, col], 'k-', linewidth=2, label='Marker-Based')
    ax.plot(time, angles_markerless[:, col], 'b--', linewidth=2, label='Markerless')
    
    ax.set_ylabel('Angle (°)', fontsize=11)
    ax.set_title(joint, fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    
    # Calculate RMSE
    rmse = np.sqrt(np.mean((angles_markers[:, col] - angles_markerless[:, col])**2))
    ax.text(0.02, 0.95, f'RMSE: {rmse:.1f}°', 
            transform=ax.transAxes, ha='left', va='top',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

axes[-1].set_xlabel('Time (s)', fontsize=11)
plt.tight_layout()
plt.savefig('assets/results/joint-angles.png', dpi=150, bbox_inches='tight')
```

### 6. Camera Setup Diagram (800×600)

**Tool**: Draw.io or Python matplotlib

**Python Script**:
```python
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(10, 8))

# Draw capture volume (rectangle)
volume = patches.Rectangle((2, 2), 4, 6, linewidth=2, 
                          edgecolor='black', facecolor='lightgray', alpha=0.3)
ax.add_patch(volume)

# Draw cameras (triangles)
camera_positions = [
    (1, 5, 'Camera 1\n(Front)'),
    (7, 5, 'Camera 2\n(Back)'),
    (4, 1, 'Camera 3\n(Left)'),
    (4, 9, 'Camera 4\n(Right)')
]

for x, y, label in camera_positions:
    # Camera icon
    triangle = patches.FancyBboxPatch((x-0.2, y-0.2), 0.4, 0.4,
                                     boxstyle="round,pad=0.05",
                                     facecolor='blue', edgecolor='black')
    ax.add_patch(triangle)
    ax.text(x, y-0.7, label, ha='center', fontsize=10, fontweight='bold')

# Add dimensions
ax.text(4, 0.5, '4.0 m', ha='center', fontsize=11)
ax.text(0.5, 5, '6.0 m', ha='center', rotation=90, fontsize=11)

# Add subject
subject = patches.Circle((4, 5), 0.3, facecolor='red', edgecolor='black')
ax.add_patch(subject)
ax.text(4, 4.3, 'Subject', ha='center', fontsize=10, fontweight='bold')

ax.set_xlim(0, 8)
ax.set_ylim(0, 10)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('4-Camera Setup Configuration (Top View)', 
            fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('assets/setup/camera-setup.png', dpi=150, bbox_inches='tight')
```

### 7. Demo GIFs

**Running Analysis GIF**:
```bash
# Extract 3-second clip from video
ffmpeg -i results/running_trial.mp4 -ss 00:00:05 -t 3 -vf "scale=600:-1" temp.mp4

# Add skeleton overlay (use your visualization script)
python scripts/overlay_skeleton.py --video temp.mp4 --keypoints results/keypoints.json --output temp_skeleton.mp4

# Convert to GIF
ffmpeg -i temp_skeleton.mp4 -vf "fps=15,scale=600:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 running-analysis.gif

# Optimize
gifsicle -O3 --colors 128 running-analysis.gif -o assets/demos/running-analysis.gif
```

## Optimization

### Image Compression
```bash
# PNG optimization
pngquant --quality=80-95 input.png --output output.png

# Or use online tools
# - TinyPNG (https://tinypng.com/)
# - Squoosh (https://squoosh.app/)
```

### GIF Optimization
```bash
# Reduce colors and optimize
gifsicle -O3 --colors 128 input.gif -o output.gif

# Resize if needed
gifsicle --resize 600x400 input.gif -o output.gif
```

## Checklist Before Committing

- [ ] All images are properly sized
- [ ] File sizes are reasonable (< 500 KB for images, < 5 MB for GIFs)
- [ ] Images are clear and readable
- [ ] Text is legible at GitHub's display size
- [ ] Colors are consistent across images
- [ ] All referenced files exist
- [ ] Images display correctly in README preview

## Testing

Preview your README locally:
```bash
# Install grip
pip install grip

# Preview README
grip README.md

# Open http://localhost:6419 in browser
```

---

**See also**: `assets/README.md` for more details on asset organization.

