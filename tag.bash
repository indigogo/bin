#!/bin/bash

grep '!!!' $1 | awk -F '!!! ' '{print $2}'
