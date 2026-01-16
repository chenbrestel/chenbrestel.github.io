'''
show_intensity_along_video.py
'''

import cv2
import numpy as np

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time


def show_intensity_along_video(video_path, positions):

    # Optimized settings for 1hr video performance

    # Key optimizations
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_FPS, 10)  # Downsample to 10fps (3x speedup)
    intensities = {pos: [] for pos in positions}
    frame_times = []
    frame_count = 0

    print("Processing video... (estimated 20-30 min for 1hr @10fps)")

    start_time = time.time()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        # Fast grayscale conversion
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Accurate frame timing
        frame_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
        frame_times.append(frame_time)

        # Vectorized pixel sampling (faster than loops)
        y_coords, x_coords = zip(*positions)
        pixel_vals = gray[y_coords, x_coords]
        for i, pos in enumerate(positions):
            intensities[pos].append(pixel_vals[i])

        frame_count += 1
        if frame_count % 100 == 0:
            elapsed = time.time() - start_time
            print(f"Processed {frame_count} frames in {elapsed / 60:.1f} min")

    cap.release()

    # Interactive Plotly visualization
    fig = make_subplots(specs=[[{"secondary_y": False}]])
    colors = ['blue', 'red', 'green', 'orange', 'purple']

    for i, (pos, vals) in enumerate(intensities.items()):
        fig.add_trace(
            go.Scatter(
                x=frame_times,
                y=vals,
                mode='lines',
                name=f'Pixel {pos}',
                line=dict(color=colors[i % len(colors)]),
                hovertemplate=f'Pixel {pos}<br>Time: %{{x:.1f}}s<extra></extra><br>Intensity: %{{y:.0f}}'
            )
        )

    fig.update_layout(
        title='Pixel Intensity Over Time (10fps downsampled)',
        xaxis_title='Time (seconds)',
        yaxis_title='Intensity (0-255)',
        hovermode='x unified',
        showlegend=True,
        height=600
    )

    fig.update_xaxes(range=[0, max(frame_times)])
    fig.show()

    # Save interactive HTML with pixel data embedded
    fig.write_html('pixel_intensities.html', include_plotlyjs='cdn')
    print("Saved interactive plot to 'pixel_intensities.html'")
    print(f"Total processing time: {(time.time() - start_time) / 60:.1f} minutes")


if __name__ == '__main__':
    video_path = 'video.mp4'
    positions = [(600, 250),
                 (600, 377),
                 (600, 532),
                 (600, 670)]  # Pixel locations
    show_intensity_along_video(video_path, positions)
