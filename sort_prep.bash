#!/bin/bash

#perl -e '$path = `pwd`; chomp( $path ); foreach $t(1..2){ foreach $n(1..8){ @list = `pep_sort.pl prep/prep.t$t.$n.spec 0.5 total`; open FILE, ">prep.t$t.$n.pdblist"; foreach(@list){ $name = (split(/\t/, $_  ))[0]; print FILE "$path/prep/$name\n";  } } }'
perl -e '$path = `pwd`; chomp( $path ); foreach $n(1..8){ @list = `pep_sort.pl prep/prep.$n.spec 0.5 total`; open FILE, ">prep.$n.pdblist"; foreach(@list){ $name = (split(/\t/, $_  ))[0]; print FILE "$path/prep/$name\n";  } }'
