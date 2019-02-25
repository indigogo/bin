#!/bin/bash

squeue | grep cking | awk '{print $1}' | xargs scancel
