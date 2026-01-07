# Technical Specifications

## System Requirements

### Hardware Requirements

#### Minimum Configuration
- **CPU**: 4-core processor (Intel i5 or AMD Ryzen 5)
- **RAM**: 8GB DDR4
- **GPU**: CUDA-capable GPU with 4GB VRAM (NVIDIA GTX 1050 or better)
- **Storage**: 50GB available space (SSD recommended)
- **Cameras**: 2 smartphones with 1080p/30fps video capability

#### Recommended Configuration
- **CPU**: 6+ core processor (Intel i7 or AMD Ryzen 7)
- **RAM**: 16GB DDR4
- **GPU**: NVIDIA GTX 1660 or better (6GB+ VRAM)
- **Storage**: 100GB+ SSD
- **Cameras**: 3-4 smartphones with 1080p/60fps capability

#### Optimal Configuration (Used in Research)
- **CPU**: Intel i9-10900K (10 cores, 20 threads, 3.7-5.3 GHz)
- **RAM**: 32GB DDR4-3200
- **GPU**: NVIDIA RTX 3080 (16GB VRAM)
- **Storage**: 1TB NVMe SSD
- **Cameras**: 4× iPhone 12 Pro (1080p/60fps)

### Software Requirements

#### Operating System
- **Primary**: Ubuntu 20.04 LTS (recommended)
- **Alternative**: Windows 10/11 (with WSL2 for some components)
- **macOS**: Compatible but not tested extensively

#### Core Dependencies

**Python Environment**:
```
Python 3.9.7
pip 21.2.4
conda 4.10.3 (optional but recommended)
```

**Deep Learning**:
```
PyTorch 1.10.0
torchvision 0.11.1
CUDA 11.3
cuDNN 8.2.1
```

**Computer Vision**:
```
OpenCV 4.5.5
opencv-contrib-python 4.5.5
```

**Pose Estimation**:
```
AlphaPose (custom build from source)
YOLOv3-SPP (included with AlphaPose)
```

**3D Reconstruction**:
```
Pose2Sim 0.4.2
```

**Biomechanical Modeling**:
```
OpenSim 4.3
opensim-python 4.3
```

**Scientific Computing**:
```
NumPy 1.21.0
SciPy 1.7.0
pandas 1.3.0
scikit-learn 0.24.2
```

**Visualization**:
```
Matplotlib 3.4.2
seaborn 0.11.1
plotly 5.1.0
```

## Camera Setup Specifications

### Camera Requirements

**Minimum Specifications**:
- Resolution: 1080p (1920×1080)
- Frame Rate: 30 fps
- Shutter Speed: 1/250s or faster
- Focus: Manual or locked autofocus
- Exposure: Manual or locked auto-exposure

**Recommended Specifications**:
- Resolution: 1080p or 4K
- Frame Rate: 60 fps
- Shutter Speed: 1/500s or faster
- Focus: Manual focus
- Exposure: Manual exposure
- Codec: H.264 or H.265

### Camera Placement

**2-Camera Setup** (Minimum):
```
Camera 1: Front-Left (45° from sagittal plane)
Camera 2: Front-Right (45° from sagittal plane)
Distance: 2.0-2.5m from subject
Height: 1.0-1.2m (mid-limb level)
Angle: 90° separation
```

**3-Camera Setup** (Recommended):
```
Camera 1: Front-Left (45° from sagittal plane)
Camera 2: Front-Right (45° from sagittal plane)
Camera 3: Back-Center (180° from front)
Distance: 2.0-2.5m from subject
Height: 1.0-1.2m
Angles: 90° between front cameras, 180° to back
```

**4-Camera Setup** (Optimal):
```
Camera 1: Front-Left (45°)
Camera 2: Front-Right (45°)
Camera 3: Back-Left (135°)
Camera 4: Back-Right (135°)
Distance: 2.0-2.5m
Height: 1.0-1.2m
Angles: 90° separation between adjacent cameras
```

### Calibration Pattern

**Checkerboard Specifications**:
- Pattern: 6 rows × 8 columns (inner corners)
- Square Size: 25mm × 25mm
- Total Size: ~200mm × 150mm
- Material: High-contrast printed pattern on rigid foam board
- Flatness: < 1mm deviation across surface

## Data Formats

### Input Formats

**Video Files**:
- Format: MP4, AVI, MOV
- Codec: H.264, H.265
- Resolution: 1080p minimum
- Frame Rate: 30-60 fps
- Color Space: RGB

**Calibration Data**:
- Camera Matrix: 3×3 NumPy array
- Distortion Coefficients: 1×5 array (k1, k2, p1, p2, k3)
- Rotation Matrix: 3×3 array
- Translation Vector: 3×1 array
- Format: Pickle (.pkl) or JSON

### Intermediate Formats

**2D Keypoints** (JSON):
```json
{
  "frame_id": 123,
  "timestamp": 4.1,
  "people": [
    {
      "person_id": 1,
      "bbox": [x, y, width, height],
      "keypoints": [
        {"name": "nose", "x": 640.2, "y": 320.5, "confidence": 0.92},
        ...
      ]
    }
  ]
}
```

**3D Keypoints** (TRC - Track Row Column):
```
PathFileType	4	(X/Y/Z)	trajectory_file.trc
DataRate	CameraRate	NumFrames	NumMarkers	Units
30.00	30.00	900	26	mm
Frame#	Time	nose_x	nose_y	nose_z	...
1	0.0333	245.2	1234.5	-123.4	...
```

### Output Formats

**Joint Kinematics** (MOT - Motion):
```
ik_results.mot
nRows=900
nColumns=38
time	pelvis_tx	pelvis_ty	pelvis_tz	hip_flexion_r	knee_angle_r	...
0.0000	0.0	0.95	0.0	25.3	15.2	...
```

**Ground Reaction Forces** (MOT):
```
grf_results.mot
nRows=900
nColumns=10
time	ground_force_vx	ground_force_vy	ground_force_vz	...
0.0000	0.0	0.0	0.0	...
0.0333	-0.12	2.34	0.03	...
```

**Analysis Results** (CSV):
```csv
subject,trial,peak_vertical_grf,peak_ap_grf,contact_time,stride_length
S01,run_01,2.34,0.42,0.245,2.15
```

## Processing Pipeline Configuration

### Stage-by-Stage Parameters

**Stage 1: Camera Calibration**
```python
calibration_config = {
    'checkerboard_size': (6, 8),
    'square_size': 25,  # mm
    'num_images': 25,
    'reprojection_threshold': 0.5,  # pixels
    'flags': cv2.CALIB_RATIONAL_MODEL
}
```

**Stage 2: Video Enhancement**
```python
enhancement_config = {
    'deblur_strength': 0.7,
    'contrast_factor': 1.3,
    'denoise_strength': 0.5,
    'temporal_smoothing': True,
    'batch_size': 8,
    'gpu_acceleration': True
}
```

**Stage 3: 2D Pose Estimation**
```python
alphapose_config = {
    'detector': 'yolov3-spp',
    'pose_model': 'halpe26',
    'backbone': 'resnet50',
    'input_size': (256, 192),
    'confidence_threshold': 0.05,
    'nms_threshold': 0.6,
    'tracking': True,
    'gpu': True
}
```

**Stage 4: Camera Synchronization**
```python
sync_config = {
    'keypoint': 'pelvis',
    'coordinate': 'y',  # vertical
    'upsampling_factor': 10,
    'smoothing_window': 11,
    'correlation_threshold': 0.7
}
```

**Stage 5: 3D Triangulation**
```python
triangulation_config = {
    'method': 'weighted_DLT',
    'min_cameras': 2,
    'confidence_threshold': 0.3,
    'min_confidence_sum': 1.0,
    'outlier_threshold': 20,  # pixels
    'interpolation': 'cubic',
    'max_gap_size': 10,
    'butterworth_order': 4,
    'butterworth_cutoff': 6  # Hz
}
```

**Stage 6: Keypoint-to-Marker Mapping**
```python
mapping_config = {
    'correlation_threshold': 0.7,
    'pelvis_width_ratio': 0.15,  # fraction of height
    'pelvis_depth_ratio': 0.10,
    'segment_ratios': {
        'thigh': 0.33,
        'shank': 0.33
    }
}
```

**Stage 7: GRF Estimation**
```python
opensim_config = {
    'model': 'Rajagopal2016',
    'ik_accuracy': 1e-5,
    'ik_constraint_weight': 10.0,
    'contact_threshold_height': 0.05,  # m
    'contact_threshold_velocity': 0.1,  # m/s
    'id_lowpass_cutoff': 6  # Hz
}
```

## Performance Benchmarks

### Processing Time (30-second video, 4 cameras)

| Stage | CPU Time | GPU Time | Total Time |
|-------|----------|----------|------------|
| Calibration | 2-5 min | N/A | 2-5 min (one-time) |
| Enhancement | 15 min | 4 min | 4 min |
| Pose Estimation | 60 min | 10 min | 10 min |
| Synchronization | 2 min | N/A | 2 min |
| Triangulation | 3 min | N/A | 3 min |
| Marker Mapping | 2 min | N/A | 2 min |
| GRF Estimation | 10 min | N/A | 10 min |
| **Total** | **94 min** | **14 min** | **31 min** |

*Note: Times based on recommended hardware configuration*

### Memory Requirements

| Stage | RAM Usage | VRAM Usage |
|-------|-----------|------------|
| Enhancement | 4 GB | 6 GB |
| Pose Estimation | 6 GB | 8 GB |
| Triangulation | 2 GB | N/A |
| OpenSim | 4 GB | N/A |
| **Peak** | **8 GB** | **8 GB** |

### Storage Requirements

**Per 30-second Trial** (4 cameras):
- Raw Videos: 500 MB
- Enhanced Videos: 800 MB
- 2D Keypoints: 5 MB
- 3D Trajectories: 2 MB
- OpenSim Results: 10 MB
- Visualizations: 50 MB
- **Total**: ~1.4 GB per trial

## Network Architecture Details

### AlphaPose Architecture

**Person Detector (YOLOv3-SPP)**:
- Input: 608×608 RGB image
- Backbone: Darknet-53
- Output: Bounding boxes + confidence scores

**Pose Estimator**:
- Input: 256×192 person crop
- Backbone: ResNet-50 (pretrained on ImageNet)
- Neck: Feature Pyramid Network (FPN)
- Head: Heatmap regression (26 channels)
- Output: 26 keypoint heatmaps (64×48 resolution)

**Post-Processing**:
- Heatmap decoding: Soft-argmax
- Confidence: Maximum heatmap value
- Tracking: DeepSORT algorithm

### Video Enhancement Network

**Architecture**: Modified U-Net
- Encoder: ResNet-18 (5 blocks)
- Decoder: Transposed convolutions (5 blocks)
- Skip Connections: Concatenation
- Temporal Module: ConvLSTM (hidden size: 256)

**Training**:
- Loss: L1 + Perceptual (VGG-based)
- Optimizer: Adam (lr=1e-4)
- Batch Size: 8 frames
- Training Data: 10,000 image pairs

## References

- [Methodology Documentation](../methodology/README.md)
- [Results & Findings](../results/README.md)
- [Dataset Information](../datasets/README.md)

---

**Back to**: [Main README](../../README.md)

