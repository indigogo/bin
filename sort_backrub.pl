#!/usr/bin/perl
$name = shift( @ARGV );
$num = shift( @ARGV );
$n = shift( @ARGV );

#$list = `grep -n 'Low Score\:' backrub.$num.out -A 24 | grep 'Total weighted' | awk '{print 1+(\$1-141)/64 "\t" \$5}' | sort -rnk 2 | tail -n $n | awk '{printf "backrub/$name.$num\_%0"4"d_low.pdb\\n", \$1}'`;
$list = `grep -n 'Low Score\:' backrub.*.out -A 24 | grep 'Total weighted' | awk -F '\.out-' '{print \$1"\t"\$2}' | awk -F '- Total' '{print \$1"\t"\$2}'  | awk '{print \$1 "\t" 1+(\$2-141)/64 "\t" \$5}' | sort -rnk 3 | tail -n $n | awk -F 'backrub\.' '{print \$1"\t"\$2}' | awk '{printf "$name%s\_%0"4"d_low.pdb\\n", \$1, \$2}' `;
#$list = `grep -n 'Low Score\:' backrub.*.out -A 24 | grep 'Total weighted' | awk -F '\.out-' '{print \$1"\t"\$2}' | awk -F '- Total' '{print \$1"\t"\$2}'  | awk '{print \$1 "\t" 1+(\$2-141)/64 "\t" \$5}' | sort -rnk 3 | tail -n $n | awk '{printf "backrub/%s\_%0"4"d_low.pdb  %s\\n", \$1, \$2, \$3}' `;
print "$list";
