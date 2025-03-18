#!/bin/bash
locust --headless --users 100 --spawn-rate 0.55555 --run-time 5m --html gpu_embedding_run.html