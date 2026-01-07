# Dataset Information

## Overview

This research utilized three complementary datasets to validate the markerless GRF estimation pipeline:

1. **Laboratory Dataset** - Primary validation with force plate ground truth
2. **AddBiomechanics Dataset** - Cross-validation and reproducibility testing
3. **Vicon Reference Dataset** - Cross-platform consistency validation

## Dataset 1: Laboratory Dataset (Primary)

### Participants

**Sample Size**: 5 healthy adults
- **Gender**: 3 males, 2 females
- **Age**: 27.8 ± 5.2 years (range: 22-35)
- **Height**: 172.4 ± 8.6 cm
- **Mass**: 68.2 ± 11.4 kg
- **BMI**: 22.8 ± 2.1 kg/m²

**Inclusion Criteria**:
- Healthy adults aged 18-40 years
- No history of lower limb injury in past 6 months
- Able to run comfortably for 30 seconds
- No neurological or musculoskeletal disorders

**Exclusion Criteria**:
- Current lower limb pain or injury
- Pregnancy
- Cardiovascular conditions limiting exercise
- Unable to provide informed consent

### Equipment

**Motion Capture System**:
- **System**: Qualisys Miqus M3
- **Cameras**: 12 cameras
- **Sampling Rate**: 250 Hz
- **Resolution**: 1280×1024 pixels
- **Marker Set**: 43 reflective markers (Rajagopal configuration)
- **Calibration**: Wand calibration, residual < 0.5 mm

**Force Plates**:
- **System**: AMTI force plates (embedded in runway)
- **Number**: 2 plates
- **Sampling Rate**: 2000 Hz
- **Dimensions**: 600mm × 400mm per plate
- **Accuracy**: ±0.1% of full scale
- **Synchronization**: Hardware synchronized with Qualisys

**Smartphone Cameras**:
- **Model**: iPhone 12 Pro
- **Number**: 4 cameras
- **Resolution**: 1920×1080 (1080p)
- **Frame Rate**: 60 fps
- **Placement**: Front-left, front-right, back-left, back-right
- **Distance**: 2.2m from runway center
- **Height**: 1.1m (tripod-mounted)
- **Synchronization**: Software-based (cross-correlation)

### Protocol

**Preparation**:
1. Informed consent obtained
2. Anthropometric measurements recorded
3. Reflective markers placed (Rajagopal set)
4. Smartphone cameras positioned and calibrated
5. Warm-up: 5 minutes of walking and light jogging

**Data Collection**:
1. **Static Trial**: Standing calibration pose (5 seconds)
2. **Running Trials**: 
   - Self-selected comfortable running speed
   - 10-meter runway with embedded force plates
   - 5 successful trials per participant
   - Success criteria: Clean force plate contact, full body visible in all cameras
3. **Rest**: 1-2 minutes between trials

**Running Speeds**:
- Mean: 11.4 ± 0.8 km/h
- Range: 10.5-12.6 km/h
- Consistency: CV < 5% within participant

### Data Collected

**Per Trial**:
- Qualisys marker trajectories (250 Hz, TRC format)
- Force plate data (2000 Hz, C3D format)
- Smartphone videos (60 fps, MP4 format)
- Metadata: Speed, contact foot, trial quality

**Total Data**:
- Participants: 5
- Trials per participant: 5
- Total trials: 25
- Total running steps analyzed: 150 (6 steps per trial)

### Data Processing

**Qualisys Data**:
1. Gap filling: Cubic spline interpolation
2. Filtering: 4th-order Butterworth, 6 Hz cutoff
3. Export: TRC format for OpenSim

**Force Plate Data**:
1. Downsampling: 2000 Hz → 250 Hz (to match motion capture)
2. Filtering: 4th-order Butterworth, 50 Hz cutoff
3. Normalization: Forces normalized to body weight (BW)
4. Export: MOT format for OpenSim

**Smartphone Videos**:
1. Calibration: Checkerboard pattern (6×8, 25mm squares)
2. Processing: Through 7-stage pipeline
3. Output: GRF estimates for comparison with force plates

### Ground Truth

**Force Plate Measurements**:
- Vertical GRF (Fz): Peak 2.1-2.8 BW during running
- Anterior-Posterior GRF (Fx): Peak -0.4 to +0.5 BW
- Medial-Lateral GRF (Fy): Peak ±0.1 BW
- Contact Time: 220-280 ms
- Loading Rate: 40-80 BW/s

**Marker-Based Kinematics**:
- Hip Flexion Range: 35-55°
- Knee Flexion Range: 15-65°
- Ankle Dorsiflexion Range: -20° to +15°

## Dataset 2: AddBiomechanics Public Dataset

### Overview

**Source**: AddBiomechanics.org (Carter et al., 2023)
**Purpose**: Cross-validation and reproducibility testing
**Access**: Publicly available dataset

### Participants

**Sample Size**: 4 subjects (selected from larger dataset)
- **Gender**: 2 males, 2 females
- **Age**: 29.0 ± 7.0 years
- **Height**: 174.2 ± 9.1 cm
- **Mass**: 71.5 ± 12.3 kg

**Selection Criteria**:
- Running trials available
- High-quality marker tracking
- Force plate data available
- Similar speed to our laboratory dataset

### Equipment

**Motion Capture**:
- **System**: Qualisys
- **Cameras**: 12 cameras
- **Sampling Rate**: 250 Hz
- **Marker Set**: Full-body marker set (compatible with Rajagopal)

**Force Plates**:
- **System**: Bertec instrumented treadmill
- **Sampling Rate**: 1000 Hz
- **Synchronization**: Hardware synchronized

### Data Used

**Trials per Subject**: 3-5 running trials
**Total Trials**: 16 trials
**Total Steps**: ~100 steps

**Processing**:
- Downloaded marker trajectories (TRC format)
- Downloaded force plate data (MOT format)
- Simulated smartphone videos from marker positions
- Processed through pipeline for validation

### Purpose

1. **Cross-Validation**: Test pipeline on independent dataset
2. **Reproducibility**: Verify results generalize beyond our laboratory
3. **Treadmill vs. Overground**: Compare treadmill and overground running

### Results

**GRF Estimation Accuracy**:
- Vertical RMSE: 0.16 ± 0.03 BW (vs. 0.14 ± 0.02 BW in lab dataset)
- Correlation: r = 0.93 ± 0.02
- Consistency: < 15% difference from laboratory dataset

## Dataset 3: Vicon Reference Dataset

### Overview

**Purpose**: Cross-platform consistency validation
**Equipment**: Vicon motion capture system

### Participant

**Sample Size**: 1 subject
- **Gender**: Male
- **Age**: 28 years
- **Height**: 176 cm
- **Mass**: 72 kg

### Equipment

**Motion Capture**:
- **System**: Vicon Vantage
- **Cameras**: 8 cameras
- **Sampling Rate**: 200 Hz
- **Marker Set**: Plug-in-Gait marker set (adapted to Rajagopal)

### Data Collected

**Trials**: 3 running trials
**Purpose**: Verify pipeline works with different motion capture systems

### Results

**3D Reconstruction Accuracy**:
- RMSE: 12.1 ± 3.1 mm (vs. 11.2 ± 2.8 mm with Qualisys)
- Conclusion: Consistent performance across platforms

## Data Availability

### Laboratory Dataset

**Status**: Available upon reasonable request
**Contact**: [Repository maintainer]
**Format**: 
- Raw videos (MP4)
- Qualisys data (TRC, C3D)
- Force plate data (C3D, MOT)
- Processed results (CSV, JSON)

**Size**: ~50 GB total

### AddBiomechanics Dataset

**Status**: Publicly available
**Access**: https://addbiomechanics.org/
**Citation**: Carter et al. (2023)

### Vicon Dataset

**Status**: Limited availability (single subject)
**Purpose**: Validation only

## Ethical Approval

**Laboratory Dataset**:
- Ethics Committee: [Institution] Research Ethics Board
- Approval Number: [Number]
- Date: [Date]
- Informed Consent: Written consent obtained from all participants

**AddBiomechanics Dataset**:
- Publicly available dataset with appropriate ethical approvals
- See original publication for details

## Data Quality

### Quality Control Measures

**Motion Capture**:
- Marker visibility: > 95% across all trials
- Marker residuals: < 2 mm (Qualisys), < 3 mm (Vicon)
- Gap filling: < 5% of frames required interpolation

**Force Plates**:
- Calibration verified before each session
- Baseline drift: < 1 N
- Clean contacts: All trials manually verified

**Smartphone Videos**:
- Subject fully visible in all cameras
- No significant occlusions
- Consistent lighting throughout trials

### Data Exclusions

**Excluded Trials**:
- Poor marker tracking (> 10% gaps): 2 trials
- Incomplete force plate contact: 3 trials
- Camera occlusions: 1 trial
- **Total Excluded**: 6 trials (19% of collected data)

**Final Dataset**: 25 high-quality trials from 5 participants

## Statistical Power

**Sample Size Justification**:
- Primary outcome: Vertical GRF RMSE
- Expected effect size: 0.15 BW (based on pilot data)
- Alpha: 0.05
- Power: 0.80
- Required sample size: 20 trials
- **Achieved**: 25 trials (adequate power)

## Data Characteristics

### Running Kinematics

**Temporal Parameters**:
- Stride Time: 0.85 ± 0.08 s
- Contact Time: 0.25 ± 0.03 s
- Flight Time: 0.10 ± 0.02 s
- Cadence: 165 ± 12 steps/min

**Spatial Parameters**:
- Stride Length: 2.68 ± 0.24 m
- Step Width: 0.12 ± 0.03 m

**Joint Angles** (at initial contact):
- Hip Flexion: 42 ± 6°
- Knee Flexion: 18 ± 4°
- Ankle Dorsiflexion: 5 ± 3°

### Ground Reaction Forces

**Vertical GRF**:
- Peak Impact: 2.1 ± 0.3 BW
- Peak Active: 2.5 ± 0.4 BW
- Loading Rate: 58 ± 18 BW/s

**Anterior-Posterior GRF**:
- Peak Braking: -0.38 ± 0.08 BW
- Peak Propulsion: 0.42 ± 0.09 BW

**Medial-Lateral GRF**:
- Peak Lateral: 0.08 ± 0.03 BW
- Peak Medial: -0.06 ± 0.02 BW

## References

- Carter, A., et al. (2023). AddBiomechanics: Automating model scaling, inverse kinematics, and inverse dynamics from human motion data. bioRxiv.
- Rajagopal, A., et al. (2016). Full-Body Musculoskeletal Model for Muscle-Driven Simulation of Human Gait. IEEE TBME.

---

**Back to**: [Main README](../../README.md)

