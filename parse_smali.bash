#!/bin/bash
grep '.......<font color="red">Y</font>.......' $1 -o | awk -F '<|>' '{print $1$3$5}'
