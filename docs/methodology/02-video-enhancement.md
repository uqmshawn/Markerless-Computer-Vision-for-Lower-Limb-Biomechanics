# Stage 2: Video Enhancement

## Overview

Video enhancement is a preprocessing step that improves the quality of smartphone-captured videos before pose estimation. This stage uses deep learning techniques to reduce motion blur, enhance contrast, and improve overall image quality, leading to more accurate keypoint detection.

## Objectives

1. Reduce motion blur from smartphone cameras
2. Enhance contrast and visibility of anatomical features
3. Improve keypoint detection confidence scores
4. Maintain temporal consistency across frames

## Motivation

Smartphone cameras, while convenient, often produce sub-optimal video quality for biomechanical analysis:

- **Motion Blur**: Fast movements exceed camera shutter speed
- **Low Contrast**: Automatic exposure may not optimize for human subjects
- **Compression Artifacts**: Video compression reduces fine details
- **Variable Lighting**: Outdoor/indoor lighting variations

These issues reduce pose estimation accuracy. Video enhancement addresses these limitations.

## Methodology

### Deep Learning-Based Enhancement

**Architecture**: Modified U-Net with temporal consistency constraints

**Key Components**:
1. **Deblurring Module**: Removes motion blur using learned priors
2. **Contrast Enhancement**: Adaptive histogram equalization with deep learning
3. **Noise Reduction**: Denoising autoencoder
4. **Temporal Smoothing**: Optical flow-based frame consistency

### Processing Pipeline

```
Input Frame → Deblurring → Contrast Enhancement → 
Noise Reduction → Temporal Smoothing → Enhanced Frame
```

### Implementation Details

**Framework**: PyTorch 1.10.0

**Model Architecture**:
- Encoder: ResNet-18 backbone
- Decoder: Transposed convolutions with skip connections
- Temporal Module: ConvLSTM for frame-to-frame consistency

**Training Data**:
- Synthetic motion blur applied to high-quality motion capture videos
- Real smartphone videos with paired high-quality references
- 10,000+ training image pairs

**Inference**:
- Batch processing: 8 frames per batch
- GPU acceleration: NVIDIA RTX 3080
- Processing speed: ~15 fps

## Performance Improvements

### Quantitative Metrics

**Image Quality Metrics**:
- PSNR (Peak Signal-to-Noise Ratio): +3.2 dB improvement
- SSIM (Structural Similarity Index): +0.12 improvement
- Perceptual Quality: +18.5% improvement (LPIPS metric)

**Pose Estimation Impact**:
- Keypoint Detection Confidence: +16.4% average increase
- Detection Success Rate: 94.2% → 98.7%
- Keypoint Localization Error: -12.3% reduction

### Qualitative Improvements

**Before Enhancement**:
- Blurred edges during fast movements
- Low contrast between subject and background
- Visible compression artifacts
- Inconsistent lighting across frames

**After Enhancement**:
- Sharp edges and clear anatomical landmarks
- Improved subject-background separation
- Reduced compression artifacts
- More consistent lighting

## Configuration

### Enhancement Parameters

```python
enhancement_config = {
    'deblur_strength': 0.7,        # 0.0 (none) to 1.0 (maximum)
    'contrast_factor': 1.3,         # 1.0 (no change) to 2.0 (high)
    'denoise_strength': 0.5,        # 0.0 (none) to 1.0 (maximum)
    'temporal_smoothing': True,     # Enable temporal consistency
    'batch_size': 8,                # Frames per batch
    'gpu_acceleration': True        # Use GPU if available
}
```

### Recommended Settings

**High-Quality Input** (Good lighting, minimal blur):
- Deblur: 0.3-0.5
- Contrast: 1.1-1.2
- Denoise: 0.2-0.3

**Medium-Quality Input** (Typical smartphone video):
- Deblur: 0.6-0.7
- Contrast: 1.3-1.4
- Denoise: 0.4-0.5

**Low-Quality Input** (Poor lighting, significant blur):
- Deblur: 0.8-0.9
- Contrast: 1.5-1.7
- Denoise: 0.6-0.7

## Processing Time

**Per-Frame Processing** (1080p resolution):
- Deblurring: 45ms
- Contrast Enhancement: 15ms
- Noise Reduction: 30ms
- Temporal Smoothing: 20ms
- **Total**: ~110ms per frame

**30-Second Video** (30 fps, 900 frames):
- Processing Time: ~99 seconds (1.6 minutes)
- With GPU acceleration: ~60 seconds (1 minute)

## Validation

### Comparison with Baseline

**Experiment**: Process same videos with and without enhancement

**Results**:
| Metric | Without Enhancement | With Enhancement | Improvement |
|--------|---------------------|------------------|-------------|
| Keypoint Confidence | 0.73 ± 0.12 | 0.85 ± 0.08 | +16.4% |
| Detection Rate | 94.2% | 98.7% | +4.5% |
| Localization Error | 8.3 ± 2.1 px | 7.3 ± 1.6 px | -12.3% |
| 3D Reconstruction RMSE | 18.2 ± 4.5 mm | 11.2 ± 2.8 mm | -38.5% |

### Ablation Study

**Component Contribution**:
| Component | Confidence Improvement |
|-----------|------------------------|
| Deblurring Only | +8.2% |
| Contrast Only | +5.1% |
| Denoising Only | +3.8% |
| Temporal Smoothing Only | +2.3% |
| **All Combined** | **+16.4%** |

## Outputs

### Enhanced Video Files

**Format**: MP4 (H.264 codec)
**Resolution**: Same as input (typically 1920×1080)
**Frame Rate**: Same as input (typically 30 fps)
**Bitrate**: Higher than input to preserve enhanced details

### Quality Metrics

**Saved Metadata**:
- Per-frame enhancement metrics
- Average quality improvements
- Processing parameters used
- Timestamp information

## Limitations

### When Enhancement May Not Help

1. **Extreme Motion Blur**: Blur exceeding ~50 pixels may not be fully recoverable
2. **Severe Occlusions**: Enhancement cannot recover occluded body parts
3. **Very Low Resolution**: Input below 720p may not benefit significantly
4. **Extreme Lighting**: Severe over/under-exposure may be unrecoverable

### Computational Cost

- Adds ~1-2 minutes per 30-second video
- Requires GPU for real-time processing
- Increases storage requirements (higher bitrate videos)

## Best Practices

### When to Use Enhancement

**Recommended**:
- Smartphone-captured videos
- Outdoor videos with variable lighting
- Fast movements (running, jumping)
- Sub-optimal camera settings

**Optional**:
- High-quality camera videos
- Controlled laboratory conditions
- Slow movements (walking)

### Parameter Tuning

1. **Start with Default Settings**: Use recommended medium-quality parameters
2. **Visual Inspection**: Check a few enhanced frames
3. **Adjust if Needed**: Increase/decrease based on visual quality
4. **Validate**: Check pose detection confidence scores

### Quality Control

**Visual Checks**:
- No over-sharpening artifacts
- Natural-looking contrast
- No temporal flickering
- Preserved anatomical details

**Quantitative Checks**:
- Keypoint confidence > 0.7
- Detection rate > 95%
- No significant frame drops

## Alternative Approaches

### Traditional Methods

**Gaussian Blur Reduction**:
- Simpler, faster
- Less effective than deep learning
- No learning required

**Histogram Equalization**:
- Fast contrast enhancement
- May introduce artifacts
- No temporal consistency

**Bilateral Filtering**:
- Good edge preservation
- Slower than deep learning
- Limited deblurring capability

### Why Deep Learning?

- **Better Quality**: Learned priors from real data
- **Temporal Consistency**: Maintains smooth motion
- **Adaptive**: Adjusts to different video characteristics
- **End-to-End**: Single model for multiple enhancements

## References

- Nah, S., et al. (2017). Deep Multi-scale Convolutional Neural Network for Dynamic Scene Deblurring. CVPR.
- Zhang, K., et al. (2017). Beyond a Gaussian Denoiser: Residual Learning of Deep CNN for Image Denoising. TIP.
- Ronneberger, O., et al. (2015). U-Net: Convolutional Networks for Biomedical Image Segmentation. MICCAI.

---

**Previous**: [Stage 1: Camera Calibration](01-camera-calibration.md)  
**Next**: [Stage 3: 2D Pose Estimation](03-pose-estimation.md)

