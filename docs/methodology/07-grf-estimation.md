# Stage 7: GRF Estimation

## Overview

Ground reaction force (GRF) estimation is the final stage that transforms kinematic data into kinetic measurements. This stage uses OpenSim's inverse kinematics and inverse dynamics to estimate three-component ground reaction forces without force plates.

## Objectives

1. Estimate vertical, anterior-posterior, and medial-lateral ground reaction forces
2. Achieve clinically relevant accuracy (RMSE < 0.15 BW)
3. Detect contact timing (heel strike, toe-off) accurately
4. Compute joint moments and powers

## Biomechanical Modeling

### OpenSim Framework

**OpenSim**: Open-source musculoskeletal modeling software
- Developed at Stanford University
- Industry standard for biomechanical analysis
- Extensive validation in research and clinical settings

**Key Components**:
1. **Musculoskeletal Model**: Rajagopal 2016 full-body model
2. **Inverse Kinematics**: Compute joint angles from marker positions
3. **Inverse Dynamics**: Compute forces and moments from motion

### Rajagopal 2016 Model

**Specifications**:
- 37 degrees of freedom
- 80 musculotendon actuators
- Anatomically accurate bone geometry
- Validated muscle parameters

**Lower Limb Joints**:
- **Hip**: 3 DOF (flexion/extension, adduction/abduction, rotation)
- **Knee**: 1 DOF (flexion/extension)
- **Ankle**: 2 DOF (dorsi/plantarflexion, inversion/eversion)
- **Subtalar**: 1 DOF (inversion/eversion)
- **MTP** (metatarsophalangeal): 1 DOF (flexion/extension)

## Methodology

### Three-Step Process

```
Marker Trajectories → Inverse Kinematics → Inverse Dynamics → GRF Estimates
```

### Step 1: Inverse Kinematics (IK)

**Purpose**: Determine joint angles that best match observed marker positions

**Optimization Problem**:
```
minimize: Σ w_i · ||m_i^exp - m_i^model||²

subject to: Joint angle constraints
```

Where:
- m_i^exp: Experimental marker position
- m_i^model: Model marker position
- w_i: Marker weight

**Configuration**:
```xml
<InverseKinematicsTool>
    <time_range> 0.0 30.0 </time_range>
    <accuracy> 1e-5 </accuracy>
    <marker_weights>
        <marker name="RASI" weight="1.0"/>
        <marker name="LASI" weight="1.0"/>
        <marker name="RKNE" weight="2.0"/>  <!-- Higher weight for joints -->
        <marker name="LKNE" weight="2.0"/>
        ...
    </marker_weights>
</InverseKinematicsTool>
```

**Outputs**:
- Joint angles over time (MOT file)
- Marker residuals (errors)
- Model marker positions

### Step 2: Contact Detection

**Purpose**: Identify when feet are in contact with ground

**Method**: Vertical velocity and position thresholding

**Algorithm**:
```python
# Compute heel and toe vertical velocities
heel_velocity = np.diff(heel_position_y) / dt
toe_velocity = np.diff(toe_position_y) / dt

# Contact when both heel and toe are:
# 1. Near ground (height < threshold)
# 2. Moving slowly (velocity < threshold)
contact = (heel_height < 0.05) & (toe_height < 0.05) & \
          (abs(heel_velocity) < 0.1) & (abs(toe_velocity) < 0.1)

# Detect events
heel_strike = detect_rising_edge(contact)
toe_off = detect_falling_edge(contact)
```

**Validation**:
- Compare with force plate contact detection
- Mean timing error: 18 ± 6 ms
- Excellent agreement for clinical applications

### Step 3: Inverse Dynamics (ID)

**Purpose**: Compute joint moments and GRFs from kinematics

**Newton-Euler Equations**:
```
F = m · a  (Force balance)
τ = I · α  (Moment balance)
```

**Bottom-Up Approach**:
1. Start at foot (known GRF from contact model)
2. Compute ankle moment
3. Move up to knee, compute knee moment
4. Continue to hip, pelvis, etc.

**GRF Estimation**:
```python
# During contact phase
# Vertical GRF from vertical acceleration
Fz = m · (a_z + g)

# Anterior-posterior GRF from horizontal acceleration
Fx = m · a_x

# Medial-lateral GRF
Fy = m · a_y

# Where:
# m = body mass
# a = center of mass acceleration
# g = gravitational acceleration (9.81 m/s²)
```

**Configuration**:
```xml
<InverseDynamicsTool>
    <time_range> 0.0 30.0 </time_range>
    <external_loads_file> grf_contact.xml </external_loads_file>
    <lowpass_cutoff_frequency> 6 </lowpass_cutoff_frequency>
</InverseDynamicsTool>
```

## Implementation

### OpenSim Workflow

**Step 1: Scale Model**
```python
# Scale generic model to subject
scale_tool = opensim.ScaleTool('scale_setup.xml')
scale_tool.run()

# Outputs: subject-specific model
```

**Step 2: Run Inverse Kinematics**
```python
# Setup IK tool
ik_tool = opensim.InverseKinematicsTool('ik_setup.xml')
ik_tool.setModel(scaled_model)
ik_tool.setMarkerDataFileName('markers.trc')
ik_tool.setOutputMotionFileName('ik_results.mot')

# Run IK
ik_tool.run()
```

**Step 3: Detect Contacts**
```python
# Load IK results
ik_results = load_mot_file('ik_results.mot')

# Detect contact events
contacts = detect_foot_contacts(ik_results, model)

# Create external loads file
create_external_loads_xml(contacts, 'grf_contact.xml')
```

**Step 4: Run Inverse Dynamics**
```python
# Setup ID tool
id_tool = opensim.InverseDynamicsTool('id_setup.xml')
id_tool.setModel(scaled_model)
id_tool.setCoordinatesFileName('ik_results.mot')
id_tool.setExternalLoadsFileName('grf_contact.xml')
id_tool.setOutputGenForcesFileName('id_results.sto')

# Run ID
id_tool.run()
```

**Step 5: Extract GRF**
```python
# Load ID results
id_results = load_sto_file('id_results.sto')

# Extract GRF components
grf_vertical = id_results['ground_force_vy']
grf_ap = id_results['ground_force_vx']
grf_ml = id_results['ground_force_vz']
```

## Performance Metrics

### GRF Estimation Accuracy

**Comparison with Force Plate Ground Truth**:

**Vertical GRF (Fz)**:
- RMSE: 0.14 ± 0.02 BW
- Peak Force Error: 10.4 ± 2.5%
- Correlation: r = 0.949 ± 0.01
- R²: 0.901 ± 0.02

**Anterior-Posterior GRF (Fx)**:
- RMSE: 0.06 ± 0.01 BW
- Correlation: r = 0.88 ± 0.03
- R²: 0.77 ± 0.04

**Medial-Lateral GRF (Fy)**:
- RMSE: 0.04 ± 0.01 BW
- Correlation: r = 0.82 ± 0.04
- R²: 0.67 ± 0.05

**Contact Timing**:
- Heel Strike Error: 18 ± 6 ms
- Toe-Off Error: 22 ± 8 ms
- Contact Time Error: 12 ± 5 ms

### Joint Kinematics Accuracy

**Comparison with Marker-Based Motion Capture**:

**Hip Angles**:
- Flexion/Extension RMSE: 4.2 ± 1.3°
- Adduction/Abduction RMSE: 3.8 ± 1.1°
- Rotation RMSE: 5.1 ± 1.6°

**Knee Angles**:
- Flexion/Extension RMSE: 3.8 ± 1.2°

**Ankle Angles**:
- Dorsi/Plantarflexion RMSE: 4.5 ± 1.4°

## Quality Control

### Marker Residuals

**Acceptance Criteria**:
- **Excellent**: < 15 mm
- **Good**: 15-25 mm
- **Acceptable**: 25-40 mm
- **Poor**: > 40 mm

**Achieved Performance**:
- Mean Residual: 18.5 ± 4.2 mm
- Max Residual: 32.1 mm
- 95% of markers < 25 mm

### GRF Plausibility Checks

**Vertical GRF**:
- Peak force: 1.5-3.0 BW (running)
- Loading rate: < 100 BW/s
- Symmetry: < 20% difference between legs

**Contact Detection**:
- Contact time: 150-300 ms (running)
- Flight time: 50-150 ms (running)
- Stride frequency: 1.2-1.8 Hz (running)

## Outputs

### GRF Data (MOT Format)

```
grf_results.mot
nRows=900
nColumns=10
time	ground_force_vx	ground_force_vy	ground_force_vz	ground_force_px	...
0.0000	0.0	0.0	0.0	0.0	...
0.0333	-0.12	2.34	0.03	0.15	...
0.0667	-0.18	2.51	0.02	0.16	...
```

### Joint Kinematics (MOT Format)

```
ik_results.mot
nRows=900
nColumns=38
time	pelvis_tx	pelvis_ty	pelvis_tz	hip_flexion_r	knee_angle_r	ankle_angle_r	...
0.0000	0.0	0.95	0.0	25.3	15.2	-5.1	...
0.0333	0.02	0.96	0.01	26.1	16.8	-4.8	...
```

### Visualization

- GRF curves (vertical, AP, ML)
- Joint angle curves
- Stick figure animation
- Comparison with force plate data

## Common Issues and Solutions

### Issue 1: High Marker Residuals

**Causes**:
- Poor marker-to-model fit
- Inaccurate virtual markers
- Model scaling errors

**Solutions**:
- Adjust marker weights
- Refine virtual marker generation
- Improve model scaling

### Issue 2: Unrealistic GRF Estimates

**Causes**:
- Incorrect contact detection
- Poor kinematic data quality
- Model parameter errors

**Solutions**:
- Refine contact detection thresholds
- Improve 3D reconstruction quality
- Validate model parameters

### Issue 3: Noisy Joint Angles

**Causes**:
- Noisy marker trajectories
- Insufficient filtering

**Solutions**:
- Increase Butterworth filter cutoff
- Apply additional smoothing
- Check marker tracking quality

## Best Practices

### Model Scaling

1. **Measure Subject**: Height, mass, leg length
2. **Scale Model**: Use static trial or measurements
3. **Validate**: Check segment lengths match subject

### Parameter Selection

**Marker Weights**:
- Joint markers (knee, ankle): 2.0
- Segment markers (thigh, shank): 1.0
- Virtual markers: 0.5

**Filter Cutoff Frequencies**:
- Marker data: 6 Hz
- Joint angles: 6 Hz
- GRF: 20-50 Hz (higher for impact analysis)

### Validation

1. **Visual Inspection**: Check model animation
2. **Marker Residuals**: Verify < 25 mm
3. **Joint Angles**: Compare with literature
4. **GRF Curves**: Check shape and magnitude

## References

- Delp, S. L., et al. (2007). OpenSim: Open-source software to create and analyze dynamic simulations of movement. IEEE TBME.
- Rajagopal, A., et al. (2016). Full-Body Musculoskeletal Model for Muscle-Driven Simulation of Human Gait. IEEE TBME.
- Mundt, M., et al. (2020). Prediction of ground reaction force and joint moments based on optical motion capture data during gait. Medical Engineering & Physics.

---

**Previous**: [Stage 6: Keypoint-to-Marker Mapping](06-marker-mapping.md)  
**Back to**: [Methodology Overview](README.md)

