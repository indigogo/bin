import sys
import pandas
from numpy import *
class zterm:
    def __init__(self, weight=-1, exclude_fraction=0.0, cutoff=None, goodzlimit=None):
        self.weight, self.exclude_fraction, self.cutoff, self.goodzlimit = weight, exclude_fraction, cutoff, goodzlimit
zterms = {}


#weight is the impact of that factor on the overall zscore (use negative weights for terms where lower values are better)
#exclude_fraction (0.0 - 1.0) will remove the worst x fraction of pdbs according to that factor
#cutoff is an absolute cutoff, in units of that score term, and all structures worse than that cutoff will be removed (worse is determined by the sign of the weight)
#goodzlimit is the maximum bonus that a structure can get for having a favorable score for that term, in units of unweighed z-scores.

#### EDIT HERE #####
zterms['avg_best_frag'] = zterm(weight=-5, cutoff=0.35)
zterms['avg_all_frags'] = zterm(weight=-0.5, goodzlimit=3)
zterms['fa_atr_per_res'] = zterm(weight=-2, cutoff=-3.5,exclude_fraction=0.2)
zterms['cavity_volume'] = zterm(weight=-0.5, cutoff=50, goodzlimit=3)
zterms['contact_core_SCN'] = zterm(weight=1.5)#,cutoff=225, goodzlimit=3)
zterms['buried_over_exposed'] = zterm(weight=1)#,cutoff=225, goodzlimit=3)
zterms['n_hphob_clusters'] = zterm(weight=-2,cutoff=3.5)#,cutoff=225, goodzlimit=3)
#zterms['buried_minus_exposed_per_res'] = zterm(weight=1, goodzlimit=3)#,cutoff=225, goodzlimit=3)
zterms['degree'] = zterm(weight=1, goodzlimit=3)#,cutoff=9.3, goodzlimit=3)
#zterms['exposed_np_per_res'] = zterm(weight=-3,cutoff=40, goodzlimit=3)
zterms['fxn_exposed_is_np'] = zterm(weight=-3, cutoff=0.52)#,cutoff=0.57, goodzlimit=3)
zterms['mismatch_probability'] = zterm(weight=-2.75, goodzlimit=4)#,cutoff=0.37, goodzlimit=3)
zterms['abego_res_profile'] = zterm(weight=3)#,cutoff=0.25, goodzlimit=3)
zterms['hphob_sc_contacts'] = zterm(weight=1.5,cutoff=4, goodzlimit=4)
zterms['contact_all'] = zterm(weight=1.5, goodzlimit=3)
#zterms['hphob_sc_degree'] = zterm(weight=0.5,cutoff=0.45, goodzlimit=3)
zterms['largest_hphob_cluster'] = zterm(weight=0.5, goodzlimit=2)
zterms['pack'] = zterm(weight=0.5, goodzlimit=3)
#zterms['ss_sc'] = zterm(weight=3.5,cutoff=0.65)
zterms['p_aa_pp'] = zterm(weight=-0.5,cutoff=0.65, goodzlimit=3)
zterms['rama'] = zterm(weight=-1,goodzlimit=2)
zterms['total_score'] = zterm(weight=-0.5, goodzlimit=3)
zterms['unsat_hbond'] = zterm(weight=-2, goodzlimit=3)
zterms['contig_not_hp_max'] = zterm(weight=-1.0)
zterms['contig_not_hp_avg'] = zterm(weight=--3.0)


##### STOP EDITING #####

df = pandas.io.parsers.read_table(sys.argv[1],delim_whitespace=True,skiprows=1)
starting_terms = [str(x) for x in df]

#calculate zscores
def zscore(my_average, my_std, goodzlimit, value):
    if goodzlimit != None:
        return min([goodzlimit, (float(value) - float(my_average))/float(my_std)])
    else:
        return (float(value) - float(my_average))/float(my_std)

def zscore_nolimit(my_average, my_std, value):
    return (float(value) - float(my_average))/float(my_std)

df['z_total'] = df['description'].map(lambda x: 0.0)
for z in zterms:
    if zterms[z].weight == 0: continue
    if z not in df:
        print '%s not found in %s, exiting' % (z, sys.argv[1])
        sys.exit(0)
    col_values = [float(x) for x in df[z].values]
    my_average, my_std = average(col_values), std(col_values)
    if zterms[z].goodzlimit == None:
        df['z_%s' % z] = df[z].map(lambda x: zscore_nolimit(my_average, my_std, float(x) ))
    else:
        df['z_%s' % z] = df[z].map(lambda x: zscore(my_average, my_std, zterms[z].goodzlimit, float(x) ))
    
    df['z_%s' % z] = (df['z_%s' % z] * (zterms[z].weight / abs(zterms[z].weight)))
    df['z_total'] += (df['z_%s' % z] * abs(zterms[z].weight))

#calculate whether exclude_fraction or cutoff generates the stricter numerical cutoff and save that
#the weight is used to determine whether cutoffs are upper bounds or lower bounds
for z in zterms:
    if zterms[z].weight == 0: continue
    col_values = [float(x) for x in df[z].values]
    if zterms[z].weight < 0:
        #lower is better
        if zterms[z].exclude_fraction > 0:
            high_cutoff = percentile(col_values, 100.0 - (100.0 * zterms[z].exclude_fraction))
            if zterms[z].cutoff == None:
                zterms[z].cutoff = high_cutoff
            else:
                zterms[z].cutoff = min([zterms[z].cutoff, high_cutoff])
    else:
        if zterms[z].exclude_fraction > 0:
            low_cutoff = percentile(col_values, 100.0 * zterms[z].exclude_fraction)
            if zterms[z].cutoff == None:
                zterms[z].cutoff = low_cutoff
            else:
                zterms[z].cutoff = max([zterms[z].cutoff, low_cutoff])

#note the fraction failing each term
for z in zterms:
    if zterms[z].weight == 0: continue
    if zterms[z].cutoff != None:
        if zterms[z].weight < 0:
            df_pass = df[df[z] <= zterms[z].cutoff]
        else:
            df_pass = df[df[z] >= zterms[z].cutoff]
        zterms[z].passing = len(df_pass.index) / float(len(df.index))
        if len(df_pass.index) == 0:
            if zterms[z].weight < 0:
                print 'Error: no items passing %s (cutoff %s, minimum %s)' % (z, zterms[z].cutoff, min(df[z].values))
            else:
                print 'Error: no items passing %s (cutoff %s, maximum %s)' % (z, zterms[z].cutoff, max(df[z].values))
            sys.exit(0)
    else:
        zterms[z].passing = 1.0

#remove all the items failing cutoffs
for z in zterms:
    if zterms[z].weight == 0: continue
    if zterms[z].cutoff != None:
        if zterms[z].weight < 0:
            df = df[df[z] < zterms[z].cutoff]
        else:
            df = df[df[z] > zterms[z].cutoff]

#sort by z_total
df = df.sort(columns='z_total',ascending=False)

#reorder columns in the table
new_order = ['description','z_total']
for x in starting_terms:
    if x in zterms:
        if zterms[x].weight != 0:
            new_order += ['z_%s' % x, x]
for x in starting_terms:
    if x not in new_order:
        new_order.append(x)
df = df[new_order]

#print output
pandas.options.display.max_colwidth=100000
lines= df.to_string(index=False).split('\n')
for line in lines:
    print line.strip()

#list the correlations
print
print 'term', 'correlation', 'fraction_passing'
for z in zterms:
    if zterms[z].weight != 0:
        print z, '%.3f' % corrcoef(df['z_%s' % z].values, df['z_total'].values)[0][1], '%.3f' % zterms[z].passing
    else:
        print z, '%.3f' % corrcoef(df['%s' % z].values, df['z_total'].values)[0][1], '1.0'
