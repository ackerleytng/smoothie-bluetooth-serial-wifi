#!/bin/bash

chromium_window=$(xdotool search --onlyvisible --class chromium | head -1)
xdotool windowactivate ${chromium_window}
xdotool key ctrl+F5
