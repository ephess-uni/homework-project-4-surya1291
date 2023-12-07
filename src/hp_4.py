# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    
    dates_formatted = [datetime.strptime(dates_old, "%Y-%m-%d").strftime('%d %b %Y') for dates_old in old_dates]
    return dates_formatted

def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str) or not isinstance(n, int):
        
        raise TypeError()
    
    list_ranges = []
    
    start_date = datetime.strptime(start, '%Y-%m-%d')
    
    for i in range(n):
        
        list_ranges.append(start_date + timedelta(days=i))
        
    return list_ranges


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    
    st1 = date_range(start_date, len(values))
    k = list(zip(st1, values))
    return k

def fees_report(infile, outfile):
    
    hdrs = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".split(','))
    fees_data = defaultdict(float)
    
    with open(infile, 'r') as f:
        lines = DictReader(f, fieldnames=hdrs)
        rows = [row for row in lines]

    rows.pop(0)
    for each_line in rows:
        patronID = each_line['patron_id']
        on_date_due = datetime.strptime(each_line['date_due'], "%m/%d/%Y")
        on_date_returned = datetime.strptime(each_line['date_returned'], "%m/%d/%Y")
        delays = (on_date_returned - on_date_due).days
        fees_data[patronID]+= 0.25 * delays if delays > 0 else 0.0
        
    fee_set_data = [
        {'patron_id': parton_ids, 'late_fees': f'{fees:0.2f}'} for parton_ids, fees in fees_data.items()
    ]
    with open(outfile, 'w') as read_file:
        load_data = DictWriter(read_file,['patron_id', 'late_fees'])
        load_data.writeheader()
        load_data.writerows(fee_set_data)




# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
