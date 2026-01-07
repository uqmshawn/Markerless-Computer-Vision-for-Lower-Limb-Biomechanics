# Figures & Visualizations

This directory contains visual assets illustrating the markerless biomechanical analysis pipeline and results.

## Directory Structure

```
figures/
├── pipeline/              # Pipeline architecture diagrams
├── calibration/           # Camera calibration examples
├── pose-estimation/       # 2D pose detection visualizations
├── synchronization/       # Camera synchronization plots
├── triangulation/         # 3D reconstruction examples
├── marker-mapping/        # Keypoint-to-marker mapping visualizations
├── opensim/               # OpenSim modeling outputs
├── results/               # Results visualizations and comparisons
└── supplementary/         # Additional figures
```

## Figure Categories

### Pipeline Architecture

**pipeline-overview.png**
- Complete 7-stage pipeline flowchart
- Shows data flow from raw videos to GRF estimates
- Color-coded by processing stage

**pipeline-detailed.png**
- Detailed architecture with component specifications
- Technical details for each stage
- Input/output formats

### Camera Calibration

**calibration-setup.png**
- 4-camera setup configuration
- Camera positions and viewing angles
- Capture volume dimensions

**calibration-pattern.png**
- Checkerboard calibration pattern
- Corner detection visualization
- Reprojection error heatmap

**calibration-results.png**
- Undistorted vs. distorted images
- Calibration quality metrics
- Multi-view geometry visualization

### 2D Pose Estimation

**pose-detection-examples.png**
- Sample frames with detected keypoints
- Skeleton overlay on running gait
- Confidence score visualization

**pose-halpe26-keypoints.png**
- HALPE-26 keypoint configuration diagram
- Anatomical landmark labels
- Keypoint connectivity

**pose-confidence-distribution.png**
- Histogram of keypoint confidence scores
- Per-keypoint confidence comparison
- Quality metrics

### Camera Synchronization

**sync-cross-correlation.png**
- Cross-correlation plots for camera pairs
- Peak detection visualization
- Temporal alignment results

**sync-before-after.png**
- Pelvis trajectories before synchronization
- Aligned trajectories after synchronization
- Improvement quantification

### 3D Triangulation

**triangulation-multiview.png**
- Multi-view 2D detections
- 3D reconstruction visualization
- Reprojection onto each camera view

**triangulation-accuracy.png**
- 3D reconstruction error heatmap
- Per-keypoint accuracy comparison
- Error distribution plots

**triangulation-comparison.png**
- Weighted vs. unweighted DLT comparison
- Error reduction visualization
- Quality improvement metrics

### Marker Mapping

**mapping-keypoints-to-markers.png**
- HALPE-26 keypoints vs. Rajagopal markers
- Assignment visualization
- Virtual marker generation

**mapping-correlation-matrix.png**
- Trajectory similarity heatmap
- Hungarian algorithm results
- Assignment quality scores

### OpenSim Modeling

**opensim-model.png**
- Rajagopal 2016 musculoskeletal model
- Marker placement visualization
- Model scaling example

**opensim-ik-results.png**
- Inverse kinematics results
- Joint angle trajectories
- Marker residuals

**opensim-animation.gif**
- Animated stick figure during running
- Model motion visualization
- Multi-view rendering

### Results & Comparisons

**grf-comparison.png**
- Estimated vs. force plate GRF curves
- Vertical, AP, and ML components
- Correlation and error metrics

**grf-bland-altman.png**
- Bland-Altman plots for GRF components
- Limits of agreement
- Systematic bias analysis

**joint-angles-comparison.png**
- Markerless vs. marker-based joint angles
- Hip, knee, ankle trajectories
- RMSE and correlation

**accuracy-comparison-table.png**
- Comparison with prior methods
- Performance metrics table
- Visual accuracy ranking

**temporal-accuracy.png**
- Contact event detection
- Heel strike and toe-off timing
- Error distribution

### Supplementary Figures

**video-enhancement-examples.png**
- Before/after video enhancement
- Quality improvement metrics
- Impact on pose detection

**error-analysis.png**
- Error sources breakdown
- Sensitivity analysis
- Ablation study results

**clinical-applications.png**
- Example clinical use cases
- Gait analysis reports
- Rehabilitation monitoring

## Figure Formats

### Available Formats

- **PNG**: High-resolution raster images (300 DPI)
- **SVG**: Vector graphics for scalability
- **PDF**: Publication-ready figures
- **GIF**: Animations and sequences
- **MP4**: Video demonstrations

### Naming Convention

```
[category]_[description]_[variant].ext

Examples:
pipeline_overview_detailed.png
results_grf_comparison_vertical.png
opensim_model_scaled_subject01.png
```

## Usage Guidelines

### In Publications

All figures are available for use in publications with proper attribution:

```
Figure adapted from [Your Name] (2024). Markerless Computer Vision 
for Biomechanical Analysis. Master's Thesis, [University].
```

### In Presentations

High-resolution versions suitable for presentations are available in the `high-res/` subdirectories.

### Modifications

Source files (where available) are provided for modifications:
- **Diagrams**: Created with draw.io (XML files included)
- **Plots**: Generated with Python/Matplotlib (scripts in `scripts/`)
- **Schematics**: Created with Inkscape (SVG files)

## Generating Figures

### Requirements

```bash
pip install matplotlib seaborn plotly opencv-python pillow
```

### Example Scripts

**Generate GRF Comparison Plot**:
```python
python scripts/plot_grf_comparison.py \
    --estimated data/grf_estimated.mot \
    --ground_truth data/grf_force_plate.mot \
    --output figures/results/grf_comparison.png
```

**Generate Pipeline Diagram**:
```python
python scripts/generate_pipeline_diagram.py \
    --output figures/pipeline/pipeline_overview.png \
    --style detailed
```

## Figure Descriptions

### Key Figures for Quick Reference

1. **Pipeline Overview** (`pipeline/pipeline-overview.png`)
   - Shows complete processing workflow
   - Essential for understanding system architecture

2. **GRF Comparison** (`results/grf-comparison.png`)
   - Main validation results
   - Demonstrates accuracy vs. force plates

3. **Joint Angles** (`results/joint-angles-comparison.png`)
   - Kinematic validation
   - Shows agreement with marker-based system

4. **Accuracy Table** (`results/accuracy-comparison-table.png`)
   - Comparison with state-of-the-art
   - Quantitative performance metrics

5. **System Setup** (`calibration/calibration-setup.png`)
   - Camera configuration
   - Practical implementation guide

## Placeholder Notice

⚠️ **Note**: This repository currently contains placeholder references for figures. Actual figure files will be added progressively. 

To generate figures from your data:
1. See `scripts/` directory for plotting scripts
2. Provide your data in the formats specified in `data-samples/README.md`
3. Run the appropriate generation script

## References

- [Methodology Documentation](../docs/methodology/README.md)
- [Results & Findings](../docs/results/README.md)
- [Technical Specifications](../docs/technical-specs/README.md)

---

**Back to**: [Main README](../README.md)

