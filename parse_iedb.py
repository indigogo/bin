#!/usr/local/bin/python

import os
import xml.etree.ElementTree as ET
import glob

#import mhc name list, create dict number->name,class
mhcxml = ET.parse('MhcAlleleNameList.xml')
mhcroot = mhcxml.getroot()
mhc_id2class_name = {}
for mhc in mhcxml.findall('MhcAlleleName'):
    mhcid = mhc.find('MhcAlleleRestrictionId').text
    mhcname = mhc.find('DisplayedRestriction').text
    mhcclass = mhc.find('Class').text
    mhc_id2class_name[ mhcid ] = ( mhcclass, mhcname )

#this is the first part of every XML tag for some reason after you parse it
uri = '{http://www.iedb.org/schema/CurationSchema}'

#TODO debug glob of smaller list of files
#xml_list = glob.glob('raw/*xml')
xml_list = glob.glob('raw/*xml')


# data structure to hold all the epitope data
# dict of class->name->list of tuples (sequence,value)
tcellepdata = {}
#init class I and II
tcellepdata[ 'I' ] = {}
tcellepdata[ 'II' ] = {}
tcellepdata[ 'non classical' ] = {}
tcellepdata[ 'unknown' ] = {}

mhcepdata = {}
#init class I and II
mhcepdata[ 'I' ] = {}
mhcepdata[ 'II' ] = {}
mhcepdata[ 'non classical' ] = {}


# for all xml files
for xmlfile in xml_list:
		# if this XML is unparseable, skip with error message
    try:
      tree = ET.parse( xmlfile )
    except:
      print( 'WARNING!:\tUnparseable file ' + xmlfile )
      continue
    root = tree.getroot()
    # top of tree is by Reference
    for reference in root.findall( uri + 'Reference' ):
        for epitope in reference.find( uri + 'Epitopes' ).findall( uri + 'Epitope' ):
            # skip if this is not a linear epitope and we cant get a sequence
            try:
								#get the LinearSequence of the first element of EpitopeStructure
                sequence = epitope.find( uri + 'EpitopeStructure' )[0].find(uri+'LinearSequence').text
            except:
                continue
            for assays in epitope.findall( uri + 'Assays' ):

                for tcellactiv in assays.findall( uri + 'TCell' ):
                    assay = tcellactiv.find( uri + 'AssayInformation')
                    #skip if no qualitative measurement
                    if len( assay.findall( uri + 'QualitativeMeasurement') ) < 1:
                        continue
                    measurement = assay.find( uri + 'QualitativeMeasurement' ).text
                    #get mhc associated info, if not there, list as unknown
                    try:
                        mhcid = tcellactiv.find( uri + 'MhcAllele').find( uri + 'MhcAlleleId').text
                        mhcclass = mhc_id2class_name[ mhcid ][ 0 ]
                        mhcname = mhc_id2class_name[ mhcid ][ 1 ]
                    except:
                        mhcclass = 'unknown'
                        mhcname = 'unknown'

                    # if we havent seen mhcname before, init a blank list
                    if not mhcname in tcellepdata[ mhcclass ]:
                        tcellepdata[ mhcclass ][ mhcname ] = []
                    tcellepdata[ mhcclass ][ mhcname ].append( ( sequence, measurement ) )



                for mhcbinding in assays.findall( uri + 'MhcBinding' ):
                    mhcid = mhcbinding.find( uri + 'MhcAlleleId').text
                    assay = mhcbinding.find( uri + 'AssayInformation')
                    #skip if no quantitative measurement
                    if len( assay.findall( uri + 'QuantitativeMeasurement') ) < 1:
                        continue
                    ic50 = mhcbinding.find( uri + 'AssayInformation').find( uri + 'QuantitativeMeasurement').text
                    #use our dict to map id num to name and class
                    mhcclass = mhc_id2class_name[ mhcid ][ 0 ]
                    mhcname = mhc_id2class_name[ mhcid ][ 1 ]
                    # if we havent seen mhcname before, init a blank list
                    if not mhcname in mhcepdata[ mhcclass ]:
                        mhcepdata[ mhcclass ][ mhcname ] = []
                    mhcepdata[ mhcclass ][ mhcname ].append( ( sequence, ic50 ) )
	
  
for mhcclass in tcellepdata:
    if not os.path.isdir( 'tcell' ):
        os.mkdir( 'tcell' )
    #see if directory exists
    dirname = 'tcell/class-' + mhcclass
    if not os.path.isdir( dirname ):
        os.mkdir( dirname )
    
    for mhcname in tcellepdata[ mhcclass ]:
        # the filename should not have crazy characters
        fname = mhcname
        fname = fname.replace( '*', '' )
        fname = fname.replace( '/', '' )
        fname = fname.replace( ':', '' )
        fname = fname.replace( ' ', '' )
        file = open( dirname + '/' + fname + '.expdata', 'w' )
        # write header
        file.write( 'sequence,bindingIC50\n')
        seqvals = tcellepdata[ mhcclass ][ mhcname ]
        for seqval in seqvals:
            file.write( str( seqval[ 0 ] ) + ',' + str( seqval[ 1 ] ) + '\n' )
        file.close()

for mhcclass in mhcepdata:
    if not os.path.isdir( 'mhc' ):
        os.mkdir( 'mhc' )
    #see if directory exists
    dirname = 'mhc/class-' + mhcclass
    if not os.path.isdir( dirname ):
        os.mkdir( dirname )
    
    for mhcname in mhcepdata[ mhcclass ]:
        # the filename should not have crazy characters
        fname = mhcname
        fname = fname.replace( '*', '' )
        fname = fname.replace( '/', '' )
        fname = fname.replace( ':', '' )
        fname = fname.replace( ' ', '' )
        file = open( dirname + '/' + fname + '.expdata', 'w' )
        # write header
        file.write( 'sequence,bindingIC50\n')
        seqvals = mhcepdata[ mhcclass ][ mhcname ]
        for seqval in seqvals:
            file.write( str( seqval[ 0 ] ) + ',' + str( seqval[ 1 ] ) + '\n' )
        file.close()


