#!/usr/bin/env bash

ffmpeg -i input_video_samples/test5.mp4 -r 20 input_images/output_%04d.png