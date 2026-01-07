#!/usr/bin/env python3
"""
Generate all visual assets for GitHub README from your research data.

Usage:
    python scripts/generate_all_visuals.py --data-dir results/ --output-dir assets/

Requirements:
    pip install matplotlib seaborn numpy pandas pillow opencv-python
"""

import argparse
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def load_mot_file(filepath):
    """Load OpenSim MOT file."""
    # Skip header lines and load data
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # Find where data starts
    data_start = 0
    for i, line in enumerate(lines):
        if line.startswith('endheader'):
            data_start = i + 2  # Skip endheader and column names
            break
    
    # Load data
    data = []
    for line in lines[data_start:]:
        if line.strip():
            data.append([float(x) for x in line.split()])
    
    return np.array(data)

def create_grf_comparison(data_dir, output_path):
    """Generate GRF comparison plot."""
    print("Generating GRF comparison...")
    
    try:
        grf_est = load_mot_file(os.path.join(data_dir, 'grf_estimated.mot'))
        grf_fp = load_mot_file(os.path.join(data_dir, 'grf_force_plate.mot'))
    except FileNotFoundError:
        print("  ⚠ GRF data files not found, creating example plot")
        # Create example data
        time = np.linspace(0, 1, 100)
        grf_fp = np.column_stack([time, 
                                  1.5 * np.sin(2*np.pi*time)**2,
                                  0.3 * np.sin(4*np.pi*time),
                                  0.2 * np.cos(4*np.pi*time)])
        grf_est = grf_fp + np.random.normal(0, 0.05, grf_fp.shape)
    
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    
    components = ['Vertical', 'Anterior-Posterior', 'Medial-Lateral']
    indices = [1, 2, 3]
    
    for ax, comp, idx in zip(axes, components, indices):
        time = grf_fp[:, 0]
        ax.plot(time, grf_fp[:, idx], 'k-', linewidth=2.5, label='Force Plate', alpha=0.8)
        ax.plot(time, grf_est[:, idx], 'r--', linewidth=2, label='Estimated', alpha=0.8)
        
        ax.set_xlabel('Time (s)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Force (BW)', fontsize=12, fontweight='bold')
        ax.set_title(f'{comp} GRF', fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=11, framealpha=0.9)
        
        # Calculate and display RMSE
        rmse = np.sqrt(np.mean((grf_fp[:, idx] - grf_est[:, idx])**2))
        r = np.corrcoef(grf_fp[:, idx], grf_est[:, idx])[0, 1]
        
        stats_text = f'RMSE: {rmse:.3f} BW\nr = {r:.3f}'
        ax.text(0.95, 0.95, stats_text, transform=ax.transAxes, 
               ha='right', va='top', fontsize=10,
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.suptitle('Ground Reaction Force Estimation vs. Force Plate', 
                fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"  ✓ Saved to {output_path}")

def create_pipeline_flowchart(output_path):
    """Generate pipeline flowchart."""
    print("Generating pipeline flowchart...")
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    stages = [
        ("1. Camera\nCalibration", "Intrinsic & Extrinsic\nParameters"),
        ("2. Video\nEnhancement", "Deblurring &\nContrast"),
        ("3. 2D Pose\nEstimation", "AlphaPose\nHALPE-26"),
        ("4. Camera\nSynchronization", "Cross-Correlation\nAlignment"),
        ("5. 3D\nTriangulation", "Weighted DLT\nReconstruction"),
        ("6. Marker\nMapping", "Hungarian\nAlgorithm"),
        ("7. GRF\nEstimation", "OpenSim\nInverse Dynamics")
    ]
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE']
    
    y_start = 9
    box_height = 1.0
    box_width = 4.0
    spacing = 0.5
    
    for i, ((stage, details), color) in enumerate(zip(stages, colors)):
        y = y_start - i * (box_height + spacing)
        
        # Main box
        box = FancyBboxPatch((1, y), box_width, box_height,
                            boxstyle="round,pad=0.15",
                            facecolor=color, edgecolor='black',
                            linewidth=2.5, alpha=0.9)
        ax.add_patch(box)
        
        # Stage name
        ax.text(3, y + 0.65, stage, ha='center', va='center',
               fontsize=13, fontweight='bold', color='white')
        
        # Details
        ax.text(3, y + 0.25, details, ha='center', va='center',
               fontsize=9, style='italic', color='white', alpha=0.9)
        
        # Arrow to next stage
        if i < len(stages) - 1:
            arrow_y_start = y - 0.05
            arrow_y_end = y - spacing + box_height + 0.05
            arrow = FancyArrowPatch((3, arrow_y_start), (3, arrow_y_end),
                                   arrowstyle='->', mutation_scale=30,
                                   linewidth=3, color='black', alpha=0.7)
            ax.add_patch(arrow)
    
    # Add input/output labels
    ax.text(3, y_start + 1.2, 'INPUT: Raw Smartphone Videos',
           ha='center', fontsize=12, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    
    final_y = y_start - len(stages) * (box_height + spacing)
    ax.text(3, final_y - 0.5, 'OUTPUT: Ground Reaction Forces',
           ha='center', fontsize=12, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    ax.set_xlim(0, 6)
    ax.set_ylim(final_y - 1, y_start + 1.5)
    ax.axis('off')
    ax.set_title('Markerless Biomechanical Analysis Pipeline',
                fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"  ✓ Saved to {output_path}")

def create_camera_setup_diagram(output_path):
    """Generate camera setup diagram."""
    print("Generating camera setup diagram...")
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Capture volume
    volume = mpatches.Rectangle((2, 2), 4, 6, linewidth=3,
                               edgecolor='black', facecolor='lightgray',
                               alpha=0.3, linestyle='--')
    ax.add_patch(volume)
    
    # Cameras
    camera_configs = [
        (1, 5, 'Camera 1\n(Front)', 0),
        (7, 5, 'Camera 2\n(Back)', 180),
        (4, 1, 'Camera 3\n(Side L)', 90),
        (4, 9, 'Camera 4\n(Side R)', 270)
    ]
    
    for x, y, label, angle in camera_configs:
        # Camera icon (triangle)
        camera = mpatches.FancyBboxPatch((x-0.25, y-0.25), 0.5, 0.5,
                                        boxstyle="round,pad=0.08",
                                        facecolor='#4ECDC4', edgecolor='black',
                                        linewidth=2)
        ax.add_patch(camera)
        
        # Label
        ax.text(x, y-0.9, label, ha='center', va='top',
               fontsize=11, fontweight='bold',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Viewing angle line
        dx = 1.5 * np.cos(np.radians(angle))
        dy = 1.5 * np.sin(np.radians(angle))
        ax.arrow(x, y, dx, dy, head_width=0.2, head_length=0.15,
                fc='blue', ec='blue', alpha=0.5, linewidth=2)
    
    # Subject
    subject = mpatches.Circle((4, 5), 0.4, facecolor='red',
                             edgecolor='black', linewidth=2)
    ax.add_patch(subject)
    ax.text(4, 4.2, 'Subject', ha='center', va='top',
           fontsize=12, fontweight='bold')
    
    # Dimensions
    ax.annotate('', xy=(6.2, 2), xytext=(6.2, 8),
               arrowprops=dict(arrowstyle='<->', lw=2, color='black'))
    ax.text(6.7, 5, '6.0 m', ha='left', va='center',
           fontsize=11, fontweight='bold', rotation=90)
    
    ax.annotate('', xy=(2, 1.5), xytext=(6, 1.5),
               arrowprops=dict(arrowstyle='<->', lw=2, color='black'))
    ax.text(4, 1.0, '4.0 m', ha='center', va='top',
           fontsize=11, fontweight='bold')
    
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('4-Camera Setup Configuration (Top View)',
                fontsize=15, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"  ✓ Saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Generate README visual assets')
    parser.add_argument('--data-dir', default='results/',
                       help='Directory containing result data files')
    parser.add_argument('--output-dir', default='assets/',
                       help='Output directory for generated images')
    args = parser.parse_args()
    
    # Create output directories
    os.makedirs(os.path.join(args.output_dir, 'pipeline'), exist_ok=True)
    os.makedirs(os.path.join(args.output_dir, 'results'), exist_ok=True)
    os.makedirs(os.path.join(args.output_dir, 'setup'), exist_ok=True)
    os.makedirs(os.path.join(args.output_dir, 'demos'), exist_ok=True)
    
    print("=" * 60)
    print("Generating Visual Assets for GitHub README")
    print("=" * 60)
    
    # Generate visualizations
    create_pipeline_flowchart(
        os.path.join(args.output_dir, 'pipeline', 'pipeline-flowchart.png')
    )
    
    create_grf_comparison(
        args.data_dir,
        os.path.join(args.output_dir, 'results', 'grf-comparison.png')
    )
    
    create_camera_setup_diagram(
        os.path.join(args.output_dir, 'setup', 'camera-setup.png')
    )
    
    print("=" * 60)
    print("✓ All visualizations generated successfully!")
    print(f"\nOutput directory: {args.output_dir}")
    print("\nNext steps:")
    print("1. Review generated images")
    print("2. Replace with actual data if using example data")
    print("3. Generate GIFs using FFmpeg (see create_readme_visuals.md)")
    print("4. Optimize images for web")
    print("5. Commit to repository")
    print("\nSee scripts/create_readme_visuals.md for detailed instructions.")

if __name__ == '__main__':
    main()

