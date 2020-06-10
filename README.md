# CoronaTracker
Analysis of the spread of Covid-19 by comparing mutations between samples via Fast Optimized Global Sequence Alignment Algorithm (modified).

## Purpose
Each of these modules has a specific function in the overall goal of plotting the spread of coronavirus (or other infectious diseases by comparing their DNA. The theory being that, assuming a large enough sample size, the sample which most closely matches another sample out of all the ones which were observed prior is most likely an ancestor. That means the latter case can be said to have been infected by the older case, or at least are near each other in the infection chain. The four scripts for the program are:
1. CoronaTracker.py - Utilities used by the other modules, mainly GenerateSQL.py and Run.py. Do not execute it on its own.
2. GenerateSQL.py - Creates a SQLite database along with the necessary tables and populates two of them with the information obtained from the CSV and FASTA files. Must be run first if not already ran.
3. Run.py - Performs the comparisons on all genomes in the database and populates the third table, spreads, with the resulting chains. Should be run prior to ShowSpread.py
4. ShowSpread.py - Generates a tkinter based GUI to observe the spreads found through genome analysis.

## Method
The method I used in this is the Fast Optimized Global Sequence Alignment Algorithm (FOGSAA), with some of my own modifications. The standard FOGSAA algorithm sets a percentage match cutoff for the comparison to know when to end; my modified version instead runs until the next best fitness score to be checked is lower than the already obtained best match, ensuring there are no possible better matches. On top of this, my modified version throws all children into the priority queue and then takes whichever node has the best fitness score to expand, not necessarily limited to the children just obtained. I'm unsure on if this is a gain/loss in efficiency but I wanted to test the method and it seems to have comparable speed to standard FOGSAA at least when I observed it briefly. When the best match is obtained, it is then stored as a spread to eventually be stored in the spread table, containing the spread's start location, end location and each case's ID. The spread table also has a strength column which contains solely the value 1 in this version, in the event that I decide to add the ability to assign percent chance of origin to multiple cases instead of assuming the best fit is the guaranteed source.
NOTE: The csv file downloaded only contains the Accession, Geo_Location, Collection_Date columns. Adding more to the file and not restricting it to these will cause the program to crash. No other data is needed for it to run. Furthermore, the csv and fasta files should be saved in the same directory as 'sequences.csv' and 'sequences.fasta' and the database will be created as 'Sequences.db' in the same directory.

### References
- [FOGSAA](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3638164/)
- [Covid-19 samples source](https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/virus?SeqType_s=Nucleotide&VirusLineage_ss=SARS-CoV-2,%20taxid:2697049)
