aa3_to_aa1 = {'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D',
              'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G',
              'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
              'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S',
              'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'}

def load_fasta_seqs( file ):
  seq = ''
  seqs = []
  tags = []
  read_first = False
  for il, line in enumerate( file ):
    if line[ 0 ] == '>':
      tags.append( line.rstrip() )
      if not read_first:
        read_first = True
      else:
        seqs.append( seq )
        seq = ''
      continue
    seq += line.strip()
  seqs.append( seq ) # the last seq
  return seqs, tags

