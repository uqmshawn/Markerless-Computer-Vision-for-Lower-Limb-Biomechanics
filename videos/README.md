# Demo Videos & Examples

This directory contains demonstration videos showing the markerless biomechanical analysis pipeline in action.

## Directory Structure

```
videos/
├── running/               # Running gait examples
├── walking/               # Walking gait examples
├── jumping/               # Jumping examples
├── pipeline-demos/        # Step-by-step pipeline demonstrations
├── comparisons/           # Side-by-side comparisons
└── tutorials/             # Tutorial videos
```

## Video Categories

### Running Gait Examples

**running_example_01.mp4**
- Subject: Male, 28 years, 72 kg
- Speed: 11.5 km/h
- Duration: 30 seconds
- Shows: Complete running trial with 4-camera views

**running_multiview.mp4**
- Synchronized 4-camera views
- Shows same trial from all camera angles
- Demonstrates camera coverage

**running_with_skeleton.mp4**
- Running with 2D skeleton overlay
- Shows AlphaPose keypoint detection
- Confidence scores displayed

**running_3d_reconstruction.mp4**
- 3D skeleton reconstruction
- Rotating view of reconstructed motion
- Comparison with marker-based capture

### Walking Gait Examples

**walking_example_01.mp4**
- Subject: Female, 26 years, 65 kg
- Speed: 4.5 km/h
- Duration: 30 seconds
- Shows: Normal walking gait

**walking_slow_motion.mp4**
- Slow-motion walking (60 fps)
- Detailed view of foot contact
- Keypoint tracking visualization

### Jumping Examples

**jump_vertical.mp4**
- Vertical jump demonstration
- Shows takeoff and landing phases
- GRF estimation during impact

**jump_landing.mp4**
- Drop landing from 30 cm box
- High-impact GRF estimation
- Joint kinematics during landing

### Pipeline Demonstrations

**pipeline_stage1_calibration.mp4**
- Camera calibration process
- Checkerboard detection
- Calibration quality visualization

**pipeline_stage2_enhancement.mp4**
- Before/after video enhancement
- Shows improvement in quality
- Impact on pose detection

**pipeline_stage3_pose_estimation.mp4**
- Real-time pose estimation
- Keypoint detection and tracking
- Confidence score visualization

**pipeline_stage4_synchronization.mp4**
- Multi-camera synchronization
- Cross-correlation visualization
- Aligned vs. unaligned comparison

**pipeline_stage5_triangulation.mp4**
- 3D reconstruction process
- Multi-view triangulation
- Reprojection visualization

**pipeline_stage6_marker_mapping.mp4**
- Keypoint-to-marker mapping
- Virtual marker generation
- OpenSim marker set

**pipeline_stage7_grf_estimation.mp4**
- OpenSim inverse dynamics
- GRF curve generation
- Comparison with force plate

**pipeline_complete.mp4**
- Complete pipeline from start to finish
- All 7 stages in sequence
- 5-minute overview

### Comparisons

**comparison_markerless_vs_markers.mp4**
- Side-by-side comparison
- Markerless vs. marker-based motion capture
- Synchronized playback

**comparison_grf_curves.mp4**
- Animated GRF curves
- Estimated vs. force plate
- Real-time comparison during gait

**comparison_joint_angles.mp4**
- Joint angle trajectories
- Markerless vs. marker-based
- Hip, knee, ankle angles

### Tutorials

**tutorial_01_setup.mp4**
- How to set up cameras
- Calibration procedure
- Best practices

**tutorial_02_data_collection.mp4**
- Recording guidelines
- Subject preparation
- Quality control

**tutorial_03_processing.mp4**
- Running the pipeline
- Parameter selection
- Troubleshooting

**tutorial_04_analysis.mp4**
- Interpreting results
- Quality assessment
- Report generation

## Video Specifications

### Format Details

**Resolution**: 1920×1080 (1080p)
**Frame Rate**: 30 or 60 fps
**Codec**: H.264
**Container**: MP4
**Audio**: None (silent videos)
**Duration**: 10 seconds to 5 minutes

### File Sizes

- Short clips (10-30s): 10-50 MB
- Medium videos (1-2 min): 50-150 MB
- Long tutorials (3-5 min): 150-300 MB
- Full trials (30s, 4 cameras): 500 MB

## Viewing Recommendations

### Software

**Desktop**:
- VLC Media Player (recommended)
- Windows Media Player
- QuickTime Player (macOS)

**Web**:
- Modern browsers with HTML5 video support
- Chrome, Firefox, Safari, Edge

### Playback Tips

- Use slow-motion playback (0.25× - 0.5×) for detailed analysis
- Frame-by-frame stepping for precise event detection
- Side-by-side comparison using video editing software

## Creating Your Own Videos

### Recording Guidelines

**Camera Settings**:
- Resolution: 1080p minimum
- Frame Rate: 30-60 fps
- Shutter Speed: 1/250s or faster
- Focus: Manual or locked autofocus
- Exposure: Manual or locked auto-exposure

**Lighting**:
- Even, diffuse lighting
- Avoid harsh shadows
- Sufficient brightness (avoid underexposure)
- Consistent lighting throughout trial

**Subject Preparation**:
- Form-fitting clothing
- Contrasting colors (subject vs. background)
- Avoid baggy or loose clothing
- Appropriate footwear

**Camera Placement**:
- 2-4 cameras
- 2.0-2.5m distance from subject
- 1.0-1.2m height
- 90-180° coverage

### Processing Videos

**Enhancement**:
```bash
python scripts/enhance_video.py \
    --input raw_video.mp4 \
    --output enhanced_video.mp4 \
    --deblur 0.7 \
    --contrast 1.3
```

**Pose Estimation**:
```bash
python scripts/run_alphapose.py \
    --video enhanced_video.mp4 \
    --output keypoints/ \
    --visualize
```

**Create Comparison Video**:
```bash
python scripts/create_comparison.py \
    --estimated grf_estimated.mot \
    --ground_truth grf_force_plate.mot \
    --video running_trial.mp4 \
    --output comparison_video.mp4
```

## Annotations

### Overlay Information

Videos may include the following overlays:

**2D Pose Estimation**:
- Keypoint markers (colored circles)
- Skeleton connections (lines)
- Confidence scores (color-coded)
- Bounding boxes

**3D Reconstruction**:
- 3D skeleton (rotating view)
- Coordinate axes
- Ground plane
- Camera positions

**GRF Curves**:
- Real-time force curves
- Vertical, AP, ML components
- Peak force indicators
- Contact events (heel strike, toe-off)

**Joint Angles**:
- Angle trajectories
- Range of motion indicators
- Comparison with normative data

## Placeholder Notice

⚠️ **Note**: Due to file size limitations and privacy considerations, this repository contains references to demo videos rather than the actual video files.

### Accessing Videos

**Option 1: Generate from Your Data**
- Use the provided scripts to process your own videos
- Follow the tutorials in `docs/methodology/`

**Option 2: Request Sample Videos**
- Contact repository maintainer for sample videos
- Available for research and educational purposes

**Option 3: Public Dataset**
- Use AddBiomechanics dataset (https://addbiomechanics.org/)
- Process through the pipeline to generate videos

## Video Demonstrations Available Online

Selected demonstration videos are available at:
- [YouTube Channel - To be added]
- [Project Website - To be added]
- [Supplementary Materials - To be added]

## Creating Visualizations

### Example: GRF Comparison Video

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load data
grf_estimated = load_mot_file('grf_estimated.mot')
grf_ground_truth = load_mot_file('grf_force_plate.mot')
video = cv2.VideoCapture('running_trial.mp4')

# Create figure with video + GRF plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

def update(frame):
    # Update video frame
    ret, img = video.read()
    ax1.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    # Update GRF plot
    ax2.clear()
    ax2.plot(grf_ground_truth[:frame, 1], label='Force Plate')
    ax2.plot(grf_estimated[:frame, 1], label='Estimated')
    ax2.legend()
    ax2.set_ylabel('Vertical GRF (BW)')
    ax2.set_xlabel('Frame')

# Create animation
anim = FuncAnimation(fig, update, frames=len(grf_estimated))
anim.save('comparison_video.mp4', fps=30)
```

## References

- [Methodology Documentation](../docs/methodology/README.md)
- [Results & Findings](../docs/results/README.md)
- [Figures & Visualizations](../figures/README.md)

---

**Back to**: [Main README](../README.md)

