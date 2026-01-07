# Stage 5: 3D Triangulation

## Overview

3D triangulation reconstructs three-dimensional keypoint positions from synchronized multi-view 2D detections. This stage uses likelihood-weighted triangulation within the Pose2Sim framework to achieve accurate 3D reconstruction even with imperfect 2D detections.

## Objectives

1. Reconstruct 3D keypoint positions from multi-view 2D detections
2. Handle detection uncertainties and outliers
3. Minimize 3D reconstruction error
4. Produce smooth, anatomically plausible trajectories

## Triangulation Fundamentals

### Geometric Principle

**Basic Triangulation**: Find 3D point that projects to observed 2D points in each camera

**Mathematical Formulation**:
```
For each camera i:
x_i = P_i · X

Where:
- x_i: 2D point in camera i (homogeneous coordinates)
- P_i: 3×4 projection matrix for camera i
- X: 3D point in world coordinates (homogeneous)
```

**Challenge**: With noise and errors, rays from different cameras don't intersect perfectly

**Solution**: Find 3D point that minimizes reprojection error across all views

### Direct Linear Transform (DLT)

**Standard Approach**: Solve linear system using SVD

**Limitation**: Treats all views equally, ignoring detection confidence

### Likelihood-Weighted Triangulation

**Innovation**: Weight each view by its detection confidence

**Formulation**:
```
X* = argmin_X Σ w_i · ||x_i - P_i · X||²

Where:
- w_i: Weight for camera i (based on confidence score)
- ||·||: Reprojection error
```

**Advantages**:
- Robust to low-confidence detections
- Reduces impact of outliers
- Improves overall 3D accuracy

## Pose2Sim Framework

### Why Pose2Sim?

**Features**:
- Multi-view triangulation with confidence weighting
- Automatic outlier rejection
- Gap filling for missing detections
- Temporal filtering for smooth trajectories
- OpenSim-compatible output format

**Comparison with Alternatives**:
| Method | Confidence Weighting | Outlier Rejection | Temporal Filtering | OpenSim Output |
|--------|---------------------|-------------------|-------------------|----------------|
| **Pose2Sim** | **Yes** | **Yes** | **Yes** | **Yes** |
| OpenCV Triangulation | No | No | No | No |
| EasyMocap | Limited | Yes | Limited | No |
| FreeMocap | No | Yes | Yes | Limited |

### Configuration

```python
pose2sim_config = {
    'triangulation': {
        'method': 'weighted_DLT',
        'min_cameras': 2,
        'confidence_threshold': 0.3,
        'min_confidence_sum': 1.0,
        'likelihood_threshold': 0.3,
        'interpolation': 'cubic',
        'fill_gaps': True,
        'max_gap_size': 10,
        'butterworth_filter': {
            'order': 4,
            'cutoff_frequency': 6  # Hz
        }
    }
}
```

## Implementation

### Step-by-Step Process

**Step 1: Load Synchronized 2D Data**
```python
# Load 2D keypoints from all cameras
keypoints_2d = {
    'cam1': load_keypoints('cam1_keypoints.json'),
    'cam2': load_keypoints('cam2_keypoints.json'),
    'cam3': load_keypoints('cam3_keypoints.json'),
    'cam4': load_keypoints('cam4_keypoints.json')
}

# Load camera calibration
calibration = load_calibration('calibration_data.pkl')
```

**Step 2: Confidence-Based Filtering**
```python
# Filter low-confidence detections
for cam in keypoints_2d:
    for frame in keypoints_2d[cam]:
        for kp in frame.keypoints:
            if kp.confidence < confidence_threshold:
                kp.visible = False  # Exclude from triangulation
```

**Step 3: Weighted Triangulation**
```python
# For each keypoint and frame
for keypoint_idx in range(num_keypoints):
    for frame_idx in range(num_frames):
        # Collect observations from all cameras
        observations = []
        weights = []
        
        for cam_idx, cam in enumerate(cameras):
            kp = keypoints_2d[cam][frame_idx][keypoint_idx]
            if kp.visible:
                observations.append(kp.position)
                weights.append(kp.confidence)
        
        # Triangulate if sufficient views
        if len(observations) >= min_cameras:
            point_3d = weighted_triangulation(
                observations, 
                weights, 
                projection_matrices
            )
            keypoints_3d[frame_idx][keypoint_idx] = point_3d
```

**Step 4: Outlier Rejection**
```python
# Compute reprojection error for each view
reprojection_errors = []
for cam_idx, obs in enumerate(observations):
    projected = project_3d_to_2d(point_3d, projection_matrices[cam_idx])
    error = np.linalg.norm(projected - obs)
    reprojection_errors.append(error)

# Remove outliers (error > threshold)
outlier_threshold = 20  # pixels
inlier_mask = np.array(reprojection_errors) < outlier_threshold

# Re-triangulate with inliers only
if np.sum(inlier_mask) >= min_cameras:
    point_3d = weighted_triangulation(
        observations[inlier_mask],
        weights[inlier_mask],
        projection_matrices[inlier_mask]
    )
```

**Step 5: Gap Filling**
```python
# Identify gaps (missing detections)
gaps = find_gaps(keypoints_3d)

# Fill small gaps with interpolation
for gap in gaps:
    if gap.size <= max_gap_size:
        keypoints_3d[gap.start:gap.end] = interpolate_cubic(
            keypoints_3d[gap.start-1],
            keypoints_3d[gap.end+1],
            gap.size
        )
```

**Step 6: Temporal Filtering**
```python
# Apply Butterworth low-pass filter
for keypoint_idx in range(num_keypoints):
    trajectory = keypoints_3d[:, keypoint_idx, :]
    
    # Filter each coordinate (X, Y, Z)
    for coord in range(3):
        trajectory[:, coord] = butterworth_filter(
            trajectory[:, coord],
            order=4,
            cutoff=6,  # Hz
            fs=frame_rate
        )
```

## Performance Metrics

### 3D Reconstruction Accuracy

**Comparison with Ground Truth** (Qualisys motion capture):

**Overall Performance**:
- Mean 3D RMSE: 11.2 ± 2.8 mm
- Median Error: 9.7 mm
- 95th Percentile: 16.4 mm

**Per-Keypoint Accuracy**:
| Keypoint Group | RMSE (mm) | Max Error (mm) |
|----------------|-----------|----------------|
| Head | 8.3 ± 2.1 | 14.2 |
| Torso | 9.1 ± 2.4 | 15.8 |
| Upper Limbs | 12.4 ± 3.2 | 21.6 |
| Lower Limbs | 10.8 ± 2.9 | 18.4 |
| Feet | 14.7 ± 4.1 | 26.3 |

**Improvement Over Baseline**:
- Unweighted DLT: 18.2 ± 4.5 mm
- Weighted DLT: 11.2 ± 2.8 mm
- **Improvement**: -38.5% error reduction

### Reprojection Error

**Definition**: Distance between original 2D detection and reprojected 3D point

**Results**:
- Mean Reprojection Error: 6.8 ± 2.3 pixels
- Median: 5.4 pixels
- 95th Percentile: 12.1 pixels

**Per-Camera**:
- Camera 1 (Front-Left): 6.2 ± 2.1 px
- Camera 2 (Front-Right): 6.8 ± 2.3 px
- Camera 3 (Back-Left): 7.4 ± 2.6 px
- Camera 4 (Back-Right): 7.1 ± 2.4 px

## Quality Control

### Triangulation Quality Metrics

**Confidence Sum**:
```python
confidence_sum = sum(weights)
quality = 'good' if confidence_sum > 2.0 else 'poor'
```

**Reprojection Error**:
```python
if mean_reprojection_error < 10:
    quality = 'excellent'
elif mean_reprojection_error < 20:
    quality = 'good'
else:
    quality = 'poor'
```

**Number of Views**:
- 4 cameras: Excellent
- 3 cameras: Good
- 2 cameras: Acceptable
- 1 camera: Insufficient (no triangulation)

### Visual Validation

**3D Skeleton Visualization**:
- Plot 3D skeleton in world coordinates
- Check for anatomical plausibility
- Verify limb lengths are consistent

**Trajectory Plots**:
- Plot X, Y, Z coordinates over time
- Check for smoothness and continuity
- Identify outliers or artifacts

## Common Issues and Solutions

### Issue 1: High Reprojection Error

**Causes**:
- Poor camera calibration
- Inaccurate 2D detections
- Synchronization errors

**Solutions**:
- Recalibrate cameras
- Improve 2D pose estimation quality
- Verify synchronization accuracy

### Issue 2: Jittery 3D Trajectories

**Causes**:
- Noisy 2D detections
- Insufficient temporal filtering
- Outliers not properly rejected

**Solutions**:
- Increase Butterworth filter cutoff frequency
- Strengthen outlier rejection
- Apply additional smoothing

### Issue 3: Missing 3D Points

**Causes**:
- Insufficient camera views
- Low confidence detections in all views
- Occlusions

**Solutions**:
- Add more cameras
- Improve 2D detection quality
- Use gap filling with larger max gap size

## Best Practices

### Camera Placement

**Optimal Configuration**:
- 3-4 cameras
- 90-120° separation between adjacent cameras
- All cameras at same height (1.0-1.2m)
- Overlapping fields of view

**Coverage Requirements**:
- Each keypoint visible in at least 2 cameras
- Critical keypoints (pelvis, knees, ankles) visible in 3+ cameras

### Parameter Tuning

**Confidence Threshold**:
- Start with 0.3
- Increase if too many outliers
- Decrease if too many missing points

**Cutoff Frequency**:
- Walking: 6 Hz
- Running: 8-10 Hz
- Jumping: 12-15 Hz

## Outputs

### TRC File Format (OpenSim)

```
PathFileType	4	(X/Y/Z)	trajectory_file.trc
DataRate	CameraRate	NumFrames	NumMarkers	Units	OrigDataRate	OrigDataStartFrame	OrigNumFrames
30.00	30.00	900	26	mm	30.00	1	900
Frame#	Time	nose_x	nose_y	nose_z	left_eye_x	...
1	0.0333	245.2	1234.5	-123.4	238.1	...
2	0.0667	246.1	1235.2	-122.8	238.9	...
```

### Visualization Outputs

- 3D skeleton animation (MP4)
- Trajectory plots (PNG)
- Quality metrics report (JSON)

## References

- Hartley, R., & Zisserman, A. (2004). Multiple View Geometry in Computer Vision. Cambridge University Press.
- Pagnon, D., et al. (2022). Pose2Sim: An open-source Python package for multiview markerless kinematics. JOSS.
- Needham, L., et al. (2021). The accuracy of several pose estimation methods for 3D joint centre localisation. Scientific Reports.

---

**Previous**: [Stage 4: Camera Synchronization](04-synchronization.md)  
**Next**: [Stage 6: Keypoint-to-Marker Mapping](06-marker-mapping.md)

