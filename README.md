# PhyloSeq2CSV
# Language: Python
# Input: TXT
# Output: CSV
# Tested with: PluMA 1.1, Python 3.6

PluMA plugin to take PhyloSeq (McMurdie et al, 2013) data and transform to a CSV file of abundances.

The plugin accepts as input a TXT file of tab-delimited keyword-value pairs:
abundance       PhyloSeq abundances
taxonomy        PhyloSeq taxonomy
level   Taxonomic level (integer)

The output will be a single CSV file with taxa at level or higher (it will use the lowest level of classification <= level).
