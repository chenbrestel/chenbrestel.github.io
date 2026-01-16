'''
show_intensity_along_video.py
'''

import cv2
import numpy as np

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def show_intensity_along_video(video_path, positions):
    cap = cv2.VideoCapture(video_path)
    intensities = {pos: [] for pos in positions}
    frame_times = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_time = cap.get(cv2.CAP_PROP_POS_MSEC)
        frame_times.append(frame_time)
        for pos in positions:
            intensities[pos].append(gray[pos[1], pos[0]])

    cap.release()

    # Create interactive plot
    fig = make_subplots(specs=[[{"secondary_y": False}]])
    for pos, vals in intensities.items():
        fig.add_trace(
            go.Scatter(x=frame_times, y=vals, mode='lines',
                       name=f'Pixel {pos}', hovertemplate=f'Pixel {pos}<br>Time: %{{x:.2f}}s<br>Intensity: %{{y}}')
        )

    fig.update_layout(
        title='Pixel Intensity Over Time',
        xaxis_title='Time (seconds)',
        yaxis_title='Intensity (0-255)',
        hovermode='x unified'
    )
    fig.show()

    # Save as interactive HTML
    fig.write_html('pixel_intensities.html')


if __name__ == '__main__':
    video_path = 'video.mp4'
    positions = [(600, 250),
                 (600, 377),
                 (600, 532),
                 (600, 670)]  # Pixel locations
    show_intensity_along_video(video_path, positions)
