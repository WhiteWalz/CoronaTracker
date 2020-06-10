import CoronaTracker
import sqlite3
import csv

def run():
    """Main execution method for the module. Will take the information stored in the database to appropriately
        analyze the sequences and find their closest relative via FOGSAA.
        NOTE: GenerateSQL.py must be run prior to this module."""

    conn = sqlite3.connect('Sequences.db')
    curs_main = conn.cursor()
    curs_supp = conn.cursor()
    sql_index = 2
    spreads = []

    """This section will loop through every sequence available in the details table, retrieve its sequence
        as well as the sequences of any samples which have come in the prior 40 days (days can be adjusted)
        and then compare them to find the primary sample's best match, storing the two as a spread in a list."""

    curs_main.execute('''SELECT * FROM details WHERE rowid=?;''', [sql_index])
    current_row = curs_main.fetchone()
    #Only retrieve information on sequences which have a date and sequence available.
    while current_row and current_row[2]:
        curs_main.execute('''SELECT genome FROM nucleotides WHERE id=?;''', [current_row[0]])
        current_genome = curs_main.fetchone()
        if not current_genome:
            sql_index += 1
            curs_main.execute('''SELECT * FROM details WHERE rowid=?;''', [sql_index])
            current_row = curs_main.fetchone()
            continue
        oldest_time = CoronaTracker.ComparisonUtility.getStopDate(current_row[2], days=40)
        curs_main.execute('''SELECT id, location FROM details WHERE date < ? AND date > ?;''',
                            [current_row[2], oldest_time])
        current_best = [None, -100000]
        for row in curs_main.fetchall():
            curs_supp.execute('''SELECT genome FROM nucleotides WHERE id=?;''', [current_row[0]])
            compared_genome = curs_supp.fetchone()[0]
            if not compared_genome:
                continue
            likeness_score = CoronaTracker.ComparisonUtility.compareSequences(current_genome, compared_genome)
            if likeness_score > current_best[1]:
                current_best = [row[0], likeness_score]
        main_sequence = CoronaTracker.Sequence(current_row[0], current_row[1])
        curs_supp.execute('''SELECT * FROM details WHERE id=?;''', [current_best[0]])
        ancestor = curs_supp.fetchone()
        if not ancestor:
            sql_index += 1
            curs_main.execute('''SELECT * FROM details WHERE rowid=?;''', [sql_index])
            current_row = curs_main.fetchone()
            continue
        ancestor_sequence = CoronaTracker.Sequence(ancestor[0], ancestor[1])
        spreads.append(CoronaTracker.Spread(start_seq=ancestor_sequence, end_seq=main_sequence))

        sql_index += 1
        curs_main.execute('''SELECT * FROM details WHERE rowid=?;''', [sql_index])
        current_row = curs_main.fetchone()
        print('Analyzing row:\n' + str(current_row))

    curs_supp.close()

    #Once all samples have been analyzed, stores the list of spreads in the spreads table.
    for spread in spreads:
        print('Inserting spread into DB:' + str(spread))
        curs_main.execute('''INSERT INTO spreads VALUES (?, ?, ?, ?, ?);''',
                            [spread.start_id, spread.end_id, spread.start_loc, spread.end_loc, spread.strength])
    conn.commit()
    conn.close()

if __name__ == "__main__":
    run()