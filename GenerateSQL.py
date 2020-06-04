import sqlite3
import csv
from Bio import SeqIO

def run():
    generateDB()
    generateNucleotideTable()
    generateDetailTable()

def generateDB():
    conn = sqlite3.connect('Sequences.db')
    curs = conn.cursor()

    curs.execute('''CREATE TABLE IF NOT EXISTS nucleotides
                    (id text, genome text);''')

    curs.execute('''CREATE TABLE IF NOT EXISTS details
                    (id text, location text, date text);''')

    curs.execute('''CREATE TABLE IF NOT EXISTS spreads
                    (source_id text, end_id text, start_location text, end_location text, strength real);''')
    conn.commit()
    conn.close()

def generateNucleotideTable(fastaFile='sequences.fasta'):
    conn = sqlite3.connect('Sequences.db')
    curs = conn.cursor()
    for record in SeqIO.parse(fastaFile, "fasta"):
        seqID = record.id
        seqID = seqID[:seqID.find(".")]
        curs.execute('''INSERT INTO nucleotides VALUES
                        (?,?);''', [seqID, str(record.seq)])
    conn.commit()
    conn.close()

def generateDetailTable(csvFile='sequences.csv'):
    conn = sqlite3.connect('Sequences.db')
    curs = conn.cursor()
    with open(csvFile) as fil:
        for row in csv.reader(fil):
            print(row)
            seqID = row[0]
            location = row[1]
            date = row[2]
            curs.execute('''INSERT INTO details VALUES
                            (?,?,?);''', [seqID, location, date])
    conn.commit()
    conn.close()

if __name__ == "__main__":
    run()