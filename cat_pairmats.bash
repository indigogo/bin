#!/bin/bash

ls contact.*.pairmat | sort -n -t '.' +1 | xargs cat
