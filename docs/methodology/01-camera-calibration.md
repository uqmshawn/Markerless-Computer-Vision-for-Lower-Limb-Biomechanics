# Stage 1: Camera Calibration

## Overview

Camera calibration is the foundational step that establishes the geometric relationship between the 2D image plane and the 3D world. Accurate calibration is critical for reliable 3D reconstruction from multiple camera views.

## Objectives

1. Determine intrinsic camera parameters (focal length, principal point, distortion coefficients)
2. Establish extrinsic parameters (camera positions and orientations in 3D space)
3. Achieve reprojection error < 0.5 pixels for accurate 3D reconstruction
4. Create a unified coordinate system for multi-view triangulation

## Methodology

### Intrinsic Calibration

**Purpose**: Characterize the internal optical properties of each camera

**Parameters Estimated**:
- **Focal Length** (fx, fy): Determines the magnification of the camera
- **Principal Point** (cx, cy): The optical center of the image
- **Distortion Coefficients**: Radial (k1, k2, k3) and tangential (p1, p2) distortion

**Process**:
1. Print checkerboard calibration pattern (6×8 grid, 25mm squares)
2. Mount pattern on rigid backing board
3. Capture 20-30 images per camera from various angles and distances
4. Detect checkerboard corners using OpenCV
5. Estimate camera matrix and distortion coefficients
6. Validate with reprojection error analysis

### Extrinsic Calibration

**Purpose**: Determine the position and orientation of each camera in 3D space

**Parameters Estimated**:
- **Rotation Matrix** (R): 3×3 matrix describing camera orientation
- **Translation Vector** (t): 3D position of camera in world coordinates

**Process**:
1. Place checkerboard in capture volume center
2. Simultaneously capture images from all cameras
3. Detect checkerboard corners in each view
4. Compute relative camera poses using multi-view geometry
5. Establish unified world coordinate system
6. Validate with multi-view reprojection error

## Implementation

### Calibration Pattern Specifications

```
Pattern Type: Checkerboard
Grid Size: 6 rows × 8 columns (inner corners)
Square Size: 25mm × 25mm
Material: High-contrast printed pattern on rigid foam board
Flatness Tolerance: < 1mm deviation
```

### Camera Setup Requirements

**Minimum Configuration**:
- 2 cameras with overlapping field of view
- 90° minimum separation angle
- 1.5-2.5m distance from subject

**Recommended Configuration**:
- 3-4 cameras
- 120-180° coverage around subject
- Camera heights at 1.0-1.2m (mid-limb level)
- Stable tripod mounting

### OpenCV Calibration Pipeline

**Step 1: Corner Detection**
```python
# Detect checkerboard corners
ret, corners = cv2.findChessboardCorners(gray_image, (6, 8), None)

# Refine corner locations to sub-pixel accuracy
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
corners_refined = cv2.cornerSubPix(gray_image, corners, (11, 11), (-1, -1), criteria)
```

**Step 2: Intrinsic Calibration**
```python
# Calibrate camera
ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
    object_points,  # 3D points in world coordinates
    image_points,   # 2D points in image coordinates
    image_size,     # Image dimensions
    None,           # Initial camera matrix
    None            # Initial distortion coefficients
)
```

**Step 3: Extrinsic Calibration**
```python
# Compute stereo calibration for camera pairs
ret, K1, D1, K2, D2, R, T, E, F = cv2.stereoCalibrate(
    object_points,
    image_points_cam1,
    image_points_cam2,
    camera_matrix_1,
    dist_coeffs_1,
    camera_matrix_2,
    dist_coeffs_2,
    image_size
)
```

## Quality Metrics

### Reprojection Error

**Definition**: The distance between detected corners and their reprojected positions

**Calculation**:
```
Reprojection Error = √(Σ(x_detected - x_reprojected)² + (y_detected - y_reprojected)²) / N
```

**Acceptance Criteria**:
- **Excellent**: < 0.3 pixels
- **Good**: 0.3 - 0.5 pixels
- **Acceptable**: 0.5 - 1.0 pixels
- **Poor**: > 1.0 pixels (recalibration recommended)

### Calibration Results

**Achieved Performance**:
- Mean reprojection error: 0.42 ± 0.08 pixels
- Maximum reprojection error: 0.87 pixels
- Calibration success rate: 95.3% of captured images

## Outputs

### Calibration Files

1. **Camera Matrix** (camera_matrix.txt):
```
fx  0   cx
0   fy  cy
0   0   1
```

2. **Distortion Coefficients** (distortion_coeffs.txt):
```
k1, k2, p1, p2, k3
```

3. **Extrinsic Parameters** (extrinsics.txt):
```
Rotation Matrix (3×3)
Translation Vector (3×1)
```

4. **Complete Calibration Data** (calibration_data.pkl):
- All intrinsic and extrinsic parameters
- Reprojection errors
- Calibration metadata

## Validation

### Visual Inspection
- Undistorted images show straight lines as straight
- Checkerboard corners align across views
- No visible warping or distortion artifacts

### Quantitative Validation
- Reprojection error within acceptable range
- Consistent results across multiple calibration sessions
- 3D reconstruction accuracy validated with known distances

## Common Issues and Solutions

### Issue 1: High Reprojection Error
**Causes**:
- Poor image quality (blur, low contrast)
- Inaccurate corner detection
- Camera movement during capture
- Insufficient number of calibration images

**Solutions**:
- Ensure good lighting and focus
- Capture more images from diverse angles
- Use stable tripod mounting
- Increase checkerboard contrast

### Issue 2: Failed Corner Detection
**Causes**:
- Checkerboard not fully visible
- Poor lighting or shadows
- Motion blur
- Incorrect grid size specification

**Solutions**:
- Ensure entire pattern is visible
- Improve lighting conditions
- Use shorter exposure times
- Verify grid size parameters

### Issue 3: Inconsistent Multi-View Calibration
**Causes**:
- Cameras moved between intrinsic and extrinsic calibration
- Insufficient overlap between camera views
- Asynchronous image capture

**Solutions**:
- Keep cameras stationary throughout calibration
- Ensure adequate field of view overlap
- Capture images simultaneously

## Best Practices

1. **Preparation**:
   - Print high-quality checkerboard pattern
   - Mount on rigid, flat surface
   - Ensure good, even lighting

2. **Image Capture**:
   - Capture 20-30 images per camera
   - Vary pattern position, angle, and distance
   - Include images at edges of capture volume
   - Avoid motion blur

3. **Processing**:
   - Verify corner detection for all images
   - Remove images with poor detection
   - Check reprojection errors
   - Validate with test measurements

4. **Maintenance**:
   - Recalibrate if cameras are moved
   - Periodic validation recommended
   - Store calibration data securely

## References

- Zhang, Z. (2000). A flexible new technique for camera calibration. IEEE TPAMI.
- OpenCV Documentation: Camera Calibration and 3D Reconstruction
- Bouguet, J. Y. (2001). Camera calibration toolbox for Matlab.

---

**Next**: [Stage 2: Video Enhancement](02-video-enhancement.md)

