# Data Samples

This directory contains sample data files demonstrating the input and output formats used throughout the processing pipeline.

## Directory Structure

```
data-samples/
├── calibration/           # Camera calibration data
├── videos/                # Sample video clips
├── 2d-keypoints/          # 2D pose estimation outputs
├── 3d-trajectories/       # 3D reconstructed keypoints
├── opensim-inputs/        # OpenSim marker files
├── opensim-outputs/       # OpenSim results (kinematics, GRF)
└── visualizations/        # Sample visualizations
```

## File Formats

### Calibration Data

**camera_matrix.txt**
```
Intrinsic camera matrix (3×3):
fx  0   cx
0   fy  cy
0   0   1

Example:
1500.2  0       960.5
0       1502.1  540.3
0       0       1
```

**distortion_coeffs.txt**
```
Distortion coefficients (1×5):
k1, k2, p1, p2, k3

Example:
-0.123, 0.045, -0.001, 0.002, -0.012
```

**extrinsics.txt**
```
Rotation matrix (3×3) and translation vector (3×1):
R11  R12  R13  tx
R21  R22  R23  ty
R31  R32  R33  tz

Example:
0.998  -0.052  0.032   245.3
0.051   0.998  0.015  -123.4
-0.033 -0.013  0.999   1050.2
```

### 2D Keypoints (JSON)

**Format**: One JSON file per frame per camera

```json
{
  "version": "1.0",
  "frame_id": 123,
  "timestamp": 4.1,
  "camera_id": "cam1",
  "people": [
    {
      "person_id": 1,
      "bbox": [450, 120, 380, 720],
      "bbox_confidence": 0.95,
      "keypoints": [
        {
          "id": 0,
          "name": "nose",
          "x": 640.2,
          "y": 320.5,
          "confidence": 0.92
        },
        {
          "id": 1,
          "name": "left_eye",
          "x": 625.1,
          "y": 315.3,
          "confidence": 0.89
        }
        // ... 24 more keypoints
      ]
    }
  ]
}
```

**Keypoint Order** (HALPE-26):
```
0: nose
1: left_eye
2: right_eye
3: left_ear
4: right_ear
5: left_shoulder
6: right_shoulder
7: left_elbow
8: right_elbow
9: left_wrist
10: right_wrist
11: left_hip
12: right_hip
13: left_knee
14: right_knee
15: left_ankle
16: right_ankle
17: head
18: neck
19: hip (pelvis)
20: left_big_toe
21: left_small_toe
22: left_heel
23: right_big_toe
24: right_small_toe
25: right_heel
```

### 3D Trajectories (TRC)

**Format**: Track Row Column (OpenSim compatible)

```
PathFileType	4	(X/Y/Z)	trajectory_file.trc
DataRate	CameraRate	NumFrames	NumMarkers	Units	OrigDataRate	OrigDataStartFrame	OrigNumFrames
30.00	30.00	900	26	mm	30.00	1	900
Frame#	Time	nose_x	nose_y	nose_z	left_eye_x	left_eye_y	left_eye_z	...
1	0.0333	245.2	1234.5	-123.4	238.1	1230.2	-125.6	...
2	0.0667	246.1	1235.2	-122.8	238.9	1231.1	-125.1	...
3	0.1000	247.3	1236.8	-122.1	239.8	1232.5	-124.5	...
```

**Coordinate System**:
- X: Anterior-posterior (forward = positive)
- Y: Vertical (up = positive)
- Z: Medial-lateral (right = positive)
- Origin: Center of capture volume at ground level

### OpenSim Marker Files (TRC)

**Format**: Same as 3D trajectories but with OpenSim marker names

```
PathFileType	4	(X/Y/Z)	markers.trc
DataRate	CameraRate	NumFrames	NumMarkers	Units	OrigDataRate	OrigDataStartFrame	OrigNumFrames
30.00	30.00	900	43	mm	30.00	1	900
Frame#	Time	RASI_x	RASI_y	RASI_z	LASI_x	LASI_y	LASI_z	RKNE_x	RKNE_y	RKNE_z	...
1	0.0333	245.2	1034.5	-23.4	-245.2	1034.5	-23.4	198.3	567.2	-45.6	...
```

**Marker Names** (Rajagopal set):
```
Pelvis: RASI, LASI, RPSI, LPSI
Torso: C7, T10, CLAV, STRN, RBAK, LBAK
Right Leg: RTHI, RKNE, RTIB, RANK, RHEE, RTOE, RMT1, RMT5
Left Leg: LTHI, LKNE, LTIB, LANK, LHEE, LTOE, LMT1, LMT5
Right Arm: RSHO, RELB, RWRA, RWRB, RFIN
Left Arm: LSHO, LELB, LWRA, LWRB, LFIN
```

### Joint Kinematics (MOT)

**Format**: Motion file (OpenSim)

```
ik_results.mot
nRows=900
nColumns=38
inDegrees=yes
endheader
time	pelvis_tx	pelvis_ty	pelvis_tz	pelvis_tilt	pelvis_list	pelvis_rotation	hip_flexion_r	hip_adduction_r	hip_rotation_r	knee_angle_r	ankle_angle_r	...
0.0000	0.000	0.950	0.000	5.2	-1.3	2.1	25.3	-3.2	1.5	15.2	-5.1	...
0.0333	0.020	0.960	0.005	5.5	-1.4	2.3	26.1	-3.1	1.6	16.8	-4.8	...
0.0667	0.041	0.972	0.010	5.8	-1.5	2.5	27.2	-3.0	1.7	18.5	-4.3	...
```

**Joint Angles** (degrees):
- Pelvis: tx, ty, tz (translations in m), tilt, list, rotation
- Hip: flexion, adduction, rotation (right and left)
- Knee: flexion (right and left)
- Ankle: dorsiflexion, inversion (right and left)
- Subtalar: inversion (right and left)
- MTP: flexion (right and left)

### Ground Reaction Forces (MOT)

**Format**: Motion file with force data

```
grf_results.mot
nRows=900
nColumns=10
endheader
time	ground_force_vx	ground_force_vy	ground_force_vz	ground_force_px	ground_force_py	ground_force_pz	ground_torque_x	ground_torque_y	ground_torque_z
0.0000	0.000	0.000	0.000	0.000	0.000	0.000	0.000	0.000	0.000
0.0333	-0.120	2.340	0.030	0.150	0.020	-0.080	0.005	-0.002	0.001
0.0667	-0.180	2.510	0.020	0.160	0.021	-0.075	0.006	-0.003	0.001
```

**Force Components**:
- vx: Anterior-posterior force (N)
- vy: Vertical force (N)
- vz: Medial-lateral force (N)
- px, py, pz: Center of pressure (m)
- torque_x, torque_y, torque_z: Free moment (Nm)

**Normalization**: Forces often normalized to body weight (BW)
```
Force (BW) = Force (N) / (Mass (kg) × 9.81)
```

### Analysis Results (CSV)

**Format**: Comma-separated values

```csv
subject,trial,foot,peak_vertical_grf_bw,peak_ap_grf_bw,contact_time_ms,stride_length_m,stride_time_s,cadence_spm,hip_rom_deg,knee_rom_deg,ankle_rom_deg
S01,run_01,right,2.34,0.42,245,2.15,0.85,141,48.2,52.3,28.5
S01,run_01,left,2.38,0.40,248,2.18,0.85,141,47.8,51.9,29.1
S01,run_02,right,2.41,0.45,242,2.20,0.83,145,49.1,53.2,27.8
```

**Variables**:
- Temporal: contact_time, stride_time, cadence
- Spatial: stride_length, step_width
- Kinetic: peak forces, loading rate, impulse
- Kinematic: joint ROM, peak angles, angular velocities

## Sample Data

### Included Samples

Due to file size limitations, this repository includes:

1. **Calibration Data**: Complete calibration files for 4-camera setup
2. **2D Keypoints**: Sample frames from one trial
3. **3D Trajectories**: One complete gait cycle
4. **OpenSim Files**: Sample input and output files
5. **Visualizations**: Representative figures

### Full Dataset

For access to the complete dataset:
- **Laboratory Data**: Available upon reasonable request
- **AddBiomechanics Data**: Publicly available at https://addbiomechanics.org/

## Usage Examples

### Loading 2D Keypoints (Python)

```python
import json

# Load keypoints from JSON
with open('2d-keypoints/cam1_frame_0123.json', 'r') as f:
    data = json.load(f)

# Extract keypoints
keypoints = data['people'][0]['keypoints']
nose = next(kp for kp in keypoints if kp['name'] == 'nose')
print(f"Nose position: ({nose['x']}, {nose['y']}), confidence: {nose['confidence']}")
```

### Loading 3D Trajectories (Python)

```python
import numpy as np

# Load TRC file
def load_trc(filename):
    # Skip header lines
    data = np.loadtxt(filename, skiprows=6, delimiter='\t')
    time = data[:, 1]
    markers = data[:, 2:].reshape(-1, 26, 3)  # 26 markers, XYZ
    return time, markers

time, markers = load_trc('3d-trajectories/trial_01.trc')
```

### Loading OpenSim Results (Python)

```python
import opensim as osim

# Load motion file
motion = osim.Storage('opensim-outputs/ik_results.mot')

# Extract joint angles
time = osim.ArrayDouble()
motion.getTimeColumn(time)

hip_flexion = osim.ArrayDouble()
motion.getDataColumn('hip_flexion_r', hip_flexion)
```

## Data Quality Indicators

### Quality Metrics Included

Each data file may include quality metrics:

**2D Keypoints**:
- `confidence`: Per-keypoint detection confidence (0-1)
- `bbox_confidence`: Person detection confidence

**3D Trajectories**:
- `reprojection_error`: Mean reprojection error (pixels)
- `num_cameras`: Number of cameras used for triangulation
- `confidence_sum`: Sum of 2D confidences

**OpenSim Results**:
- `marker_residuals`: Per-marker fit error (mm)
- `max_residual`: Maximum marker error
- `rms_residual`: RMS marker error

## References

- [Methodology Documentation](../docs/methodology/README.md)
- [Technical Specifications](../docs/technical-specs/README.md)
- [Results & Findings](../docs/results/README.md)

---

**Back to**: [Main README](../README.md)

