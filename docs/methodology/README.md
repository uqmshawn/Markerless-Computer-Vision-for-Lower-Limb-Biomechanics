# Methodology Overview

This section provides comprehensive documentation of the 7-stage markerless biomechanical analysis pipeline.

## Pipeline Architecture

The system transforms raw, unsynchronized smartphone videos into clinically relevant ground reaction force estimates through seven sequential processing stages:

```
Raw Videos → Calibration → Enhancement → Pose Estimation → 
Synchronization → 3D Triangulation → Marker Mapping → GRF Estimation
```

## Processing Stages

### [Stage 1: Camera Calibration](01-camera-calibration.md)
**Purpose**: Establish geometric relationship between cameras and 3D world

**Key Components**:
- Intrinsic calibration (focal length, principal point, distortion)
- Extrinsic calibration (camera positions and orientations)
- Checkerboard pattern detection
- Reprojection error minimization

**Outputs**: Camera matrices, distortion coefficients, transformation matrices

---

### [Stage 2: Video Enhancement](02-video-enhancement.md)
**Purpose**: Improve video quality for more accurate pose detection

**Key Components**:
- Deep learning-based preprocessing
- Motion blur reduction
- Contrast enhancement
- Noise reduction

**Performance**: +16.4% improvement in keypoint detection confidence

---

### [Stage 3: 2D Pose Estimation](03-pose-estimation.md)
**Purpose**: Detect anatomical keypoints in each video frame

**Key Components**:
- AlphaPose framework with HALPE-26 configuration
- YOLOv3-SPP person detector
- ResNet-50 backbone network
- 26 anatomical keypoints per frame

**Outputs**: 2D keypoint coordinates with confidence scores

---

### [Stage 4: Camera Synchronization](04-synchronization.md)
**Purpose**: Temporally align unsynchronized video streams

**Key Components**:
- Cross-correlation of joint velocities
- Software-based temporal alignment
- Sub-frame accuracy synchronization

**Performance**: Achieves sub-frame temporal alignment accuracy

---

### [Stage 5: 3D Triangulation](05-triangulation.md)
**Purpose**: Reconstruct 3D positions from multi-view 2D detections

**Key Components**:
- Likelihood-weighted multi-view reconstruction
- Pose2Sim framework
- Confidence-based triangulation
- Outlier rejection

**Performance**: -38.2% reduction in 3D reconstruction error

---

### [Stage 6: Keypoint-to-Marker Mapping](06-marker-mapping.md)
**Purpose**: Map sparse pose keypoints to biomechanical model markers

**Key Components**:
- Hungarian algorithm for optimal assignment
- Vertical trajectory similarity matching
- Rajagopal OpenSim marker set alignment
- Cost matrix optimization

**Outputs**: Mapped 3D marker trajectories in OpenSim format

---

### [Stage 7: GRF Estimation](07-grf-estimation.md)
**Purpose**: Estimate ground reaction forces from kinematics

**Key Components**:
- OpenSim inverse kinematics
- Inverse dynamics analysis
- 3-component GRF estimation (Fx, Fy, Fz)
- Joint moment and power calculations

**Outputs**: Ground reaction force profiles, joint kinematics, joint kinetics

---

## Implementation Details

### Software Stack
- **Python**: 3.9.7
- **PyTorch**: 1.10.0 (deep learning)
- **OpenCV**: 4.5.5 (computer vision)
- **OpenSim**: 4.3 (biomechanical modeling)
- **Pose2Sim**: 0.4.2 (3D reconstruction)
- **NumPy**: 1.21.0 (numerical computing)
- **SciPy**: 1.7.0 (scientific computing)

### Hardware Requirements

**Minimum Configuration**:
- CPU: 4-core processor
- RAM: 8GB
- GPU: Basic CUDA-capable GPU
- Storage: 50GB available space

**Recommended Configuration**:
- CPU: 6+ core processor (Intel i7/AMD Ryzen 7 or better)
- RAM: 16GB+
- GPU: NVIDIA GTX 1660 or better
- Storage: 100GB+ SSD

**Optimal Configuration** (used in this research):
- CPU: Intel i9-10900K (10 cores)
- RAM: 32GB DDR4
- GPU: NVIDIA RTX 3080 (16GB VRAM)
- Storage: 1TB NVMe SSD

---

## Processing Time

Typical processing times for a 30-second video clip (4 cameras):

| Stage | Time | Bottleneck |
|-------|------|------------|
| Calibration | 2-5 min | One-time setup |
| Enhancement | 5-10 min | GPU processing |
| Pose Estimation | 10-15 min | GPU inference |
| Synchronization | 1-2 min | CPU computation |
| Triangulation | 2-3 min | Multi-view geometry |
| Marker Mapping | 1-2 min | Optimization |
| GRF Estimation | 5-10 min | OpenSim simulation |
| **Total** | **26-47 min** | - |

*Note: Times based on recommended hardware configuration*

---

## Data Flow

### Input Requirements
- **Video Format**: MP4, AVI, or MOV
- **Resolution**: Minimum 1080p (1920×1080)
- **Frame Rate**: 30-60 fps
- **Number of Cameras**: 2-4 (3-4 recommended)
- **Camera Placement**: 90-180° coverage around subject

### Output Formats
- **3D Kinematics**: TRC files (OpenSim format)
- **GRF Data**: MOT files (OpenSim format)
- **Visualizations**: PNG, MP4
- **Analysis Reports**: CSV, JSON

---

## Quality Control

### Validation Checks
1. **Calibration Quality**: Reprojection error < 0.5 pixels
2. **Pose Detection**: Confidence scores > 0.6
3. **Synchronization**: Cross-correlation peak > 0.8
4. **Triangulation**: Reprojection error < 20mm
5. **Marker Mapping**: Assignment cost < threshold
6. **GRF Estimation**: Residual forces < 10N

### Error Handling
- Automatic detection of failed frames
- Gap filling for missing keypoints
- Outlier rejection in triangulation
- Fallback strategies for poor quality data

---

## Next Steps

Explore detailed documentation for each stage:

1. [Camera Calibration](01-camera-calibration.md)
2. [Video Enhancement](02-video-enhancement.md)
3. [2D Pose Estimation](03-pose-estimation.md)
4. [Camera Synchronization](04-synchronization.md)
5. [3D Triangulation](05-triangulation.md)
6. [Keypoint-to-Marker Mapping](06-marker-mapping.md)
7. [GRF Estimation](07-grf-estimation.md)

