#!/usr/bin/python

from phil import *
from fig_devel import *

def Help():
    print 'Usage: %s <outfile> <N_X> <N_Y> file1 {file2 file3 ... }'%argv[0]
    exit()

if len(argv) < 5:
    Help()

args = argv[:]

if args.count( '-fig2dev_args' ):
    pos = args.index( '-fig2dev_args')
    additional_fig2dev_args = args[pos+1]
    del args[pos]
    del args[pos]

outfile = args[1]
N_X = int(args[2])
N_Y = int(args[3])
files = args[4:]

if len(files) == 1:
    cmd = 'cp %s %s'%(files[0],outfile)
    Log( cmd )
    system(cmd)
    exit(0)


npages = 1 + ( len(files)-1 ) / (N_X*N_Y)

SHOW_LABELS = 1
LPR = 0

figfile = 'tmp.fig'
fig = open(figfile,'w')

## write the header
#orientation = 'Landscape'
orientation = 'Portrait'

if npages == 1: pages = 'Single'
else: pages = 'Multiple'
fig.write( Header( orientation, pages ) )

## how big for each png?
x_margin = 500
y_margin = 500

if orientation == 'Landscape':
    xdim,ydim = LONG_DIMENSION, SHORT_DIMENSION
else:
    ydim,xdim = LONG_DIMENSION, SHORT_DIMENSION

xbox = float( xdim - 2 * x_margin ) / N_X
ybox = float( ydim - 2 * y_margin ) / N_Y

## figure out the dimensions of the files
dims = []
for file in files:
    line = popen('file '+file).readlines()[0].split()
    if line[1] != 'PNG':
        print 'Not a png file? The "file" command says:',' '.join(line)
        Help()
    x = int(line[4])
    y = int(line[6][:-1])
    assert line[6][-1] == ','
    dims.append( [x,y] )

suffixlen = 0
while 1:
    suffix = files[0][-1-suffixlen:]
    all_have = 1
    for file in files:
        if file[-1-suffixlen:] != suffix:
            all_have = 0
            break
    if not all_have:
        break
    suffixlen += 1



## x is measured from left-hand side
## y is measured from top!!

for ii in range(N_X):
    for jj in range(npages * N_Y):
        file_index = jj * N_X + ii
        if file_index >= len(files): continue

        dim = dims[ file_index ]
        file_ratio = float( dim[0] ) / dim[1] ## x-pixels / y-pixels
        box_ratio = float( xbox ) / ybox
        if file_ratio > box_ratio:
            ## file is wider than box
            x_width = xbox
            y_width = x_width / file_ratio
        else:
            y_width = ybox
            x_width = y_width * file_ratio
        assert x_width <= xbox and y_width <= ybox
        assert abs( file_ratio - x_width / y_width ) < 1e-2

        Log( '%2d %2d  %5d x %5d  file_ratio= %9.3f box_ratio= %9.3f  xw= %6d yw=%6d   %s'\
                 %(ii,jj,dim[0],dim[1],file_ratio,box_ratio,x_width,y_width,files[file_index]) )

        ## the ii x jj png file
        x0 = intf( x_margin + ii * xbox )
        x1 = intf( x0 + x_width )

        y0 = intf( y_margin + jj * ybox )
        y1 = intf( y0 + y_width )

        fig.write( draw_picture( files[ file_index ], [x0,y0], [x1,y1] ) )

        label = files[ file_index ]
        if suffixlen: label = label[:-suffixlen]
        if SHOW_LABELS:
            max_x = intf( 3.0 * x_width /  4.0 )
            max_y = intf( y_width / 10.0 )
            fig.write( Text_box( label, 0, [x0,y0], [x0+max_x, y0+max_y ], COURIER, 32 ) )

fig.close()



## now convert. Note that .ps files don't seem to work right.
format = outfile.split('.')[-1]
cmd = 'fig2dev %s -L %s %s %s %s'%(additional_fig2dev_args, format, ' -M '*(format == 'pdf'), figfile, outfile )
Log( cmd )
system(cmd)

## here's how to print, but this doesn't quite work -- the top and bottom margins are screwed up.
## could change the margins if we are directly printing...
##
#if LPR and format == 'pdf':
#    cmd = 'acroread -toPostScript -pairs %s - | lpr'%outfile
#    print cmd
#    system(cmd)

