#!/usr/bin/python

import argparse
from argparse import ArgumentParser
import sys
import os
import re

# NOTE! path is system dependent build/test/debug/linux/4.4/64/x86/gcc/5.4/default/ 

# NOTE! to compile unit tests with scons,  ./scons.py  -k -j30 cat=test

if __name__ == '__main__':
#	parser = ArgumentParser()
#	parser.add_argument( '-file', type = str, default = 'file', required = True, help = 'input file' )
#	parser.add_argument( '-option', type = str, default = 'a', choices = [ 'a', 'b', 'c' ], help = 'option' )
#	parser.add_argument( '-options', type = str, nargs = '+', help = 'options list' )
#	args = parser.parse_args()

	os.system( "./scons.py -j10 cat=test" ) #TODO check if files exists to see if we need to compile
	os.system( "external/cxxtest/cxxtestgen.py --have-std --part -o build/test/debug/linux/4.4/64/x86/gcc/5.4/default/devel/cyrus/CyrusJSONMoverTests.cxxtest.cpp test/devel/cyrus/CyrusJSONMoverTests.cxxtest.hh" )
	# os.system( "clang++ -o build/test/debug/linux/4.4/64/x86/gcc/5.4/default/devel/cyrus/CyrusJSONMoverTests.cxxtest.o -c -std=c++11 -isystem external/boost_1_55_0/ -isystem external/ -isystem external/include/ -isystem external/dbio/ -isystem external/cxxtest/ -march=core2 -mtune=generic -pipe -Qunused-arguments -DUNUSUAL_ALLOCATOR_DECLARATION -ftemplate-depth-256 -stdlib=libstdc++ -W -Wall -Wextra -pedantic -Werror -Wno-long-long -Wno-strict-aliasing -march=native -mtune=native -stdlib=libc++ -Wno-unused-variable -O0 -g -DBOOST_ERROR_CODE_HEADER_ONLY -DBOOST_SYSTEM_NO_DEPRECATED -DBOOST_MATH_NO_LONG_DOUBLE_MATH_FUNCTIONS -DPTR_STD -Iexternal/cxxtest -I. -Itest -Isrc -Iexternal/include -Isrc/platform/macos/64/clang/9.0 -Isrc/platform/macos/64/clang -Isrc/platform/macos/64 -Isrc/platform/macos -Iexternal/boost_1_55_0 -Iexternal/libxml2/include -Iexternal -Iexternal/dbio -I/usr/include -I/usr/local/include build/test/debug/linux/4.4/64/x86/gcc/5.4/default/devel/cyrus/CyrusJSONMoverTests.cxxtest.cpp" )
# 	os.system( "clang++ -o build/test/debug/linux/4.4/64/x86/gcc/5.4/default/devel.test -stdlib=libc++ build/test/debug/linux/4.4/64/x86/gcc/5.4/default/devel/znhash/ZnHash.cxxtest.o build/test/debug/linux/4.4/64/x86/gcc/5.4/default/devel/mmt_msd/MMTMinPackingJob.cxxtest.o build/test/debug/linux/4.4/64/x86/gcc/5.4/default/devel/mmt_msd/MMTDriver.cxxtest.o build/test/debug/linux/4.4/64/x86/gcc/5.4/default/devel/mmt_msd/MMTReceiver.cxxtest.o build/test/debug/linux/4.4/64/x86/gcc/5.4/default/devel/cyrus/CyrusJSONMoverTests.cxxtest.o build/test/debug/linux/4.4/64/x86/gcc/5.4/default/devel/init/filter_creators.cxxtest.o build/test/debug/linux/4.4/64/x86/gcc/5.4/default/devel/init/mover_creators.cxxtest.o build/test/debug/linux/4.4/64/x86/gcc/5.4/default/devel/vardist_solaccess/VarSolDRotamerDots.cxxtest.o build/test/debug/linux/4.4/64/x86/gcc/5.4/default/devel/denovo_design/BuildBetaSheet.cxxtest.o build/test/debug/linux/4.4/64/x86/gcc/5.4/default/devel/denovo_design/CoreResiduesPerElementFilter.cxxtest.o build/test/debug/linux/4.4/64/x86/gcc/5.4/default/devel/denovo_design/FoldabilityFilter.cxxtest.o build/test/debug/linux/4.4/64/x86/gcc/5.4/default/devel/devel.cxxtest.o -Lexternal/lib -Lbuild/src/debug/linux/4.4/64/x86/gcc/5.4/default -Lbuild/external/debug/linux/4.4/64/x86/gcc/5.4/default -L/usr/lib -ldevel -lprotocols.7 -lprotocols.6 -lprotocols_e.5 -lprotocols_d.5 -lprotocols_c.5 -lprotocols_b.5 -lprotocols_a.5 -lprotocols_h.4 -lprotocols_g.4 -lprotocols_f.4 -lprotocols_e.4 -lprotocols_d.4 -lprotocols_c.4 -lprotocols_b.4 -lprotocols_a.4 -lprotocols.3 -lprotocols_b.2 -lprotocols_a.2 -lprotocols.1 -lcore.5 -lcore.4 -lcore.3 -lcore.2 -lcore.1 -lbasic -lnumeric -lutility -lObjexxFCL -lz -lcppdb -lsqlite3 -lcifparse -lxml2" )
	os.system( "time test/run.py --one CyrusJSONMoverTests --unmute=test" )

