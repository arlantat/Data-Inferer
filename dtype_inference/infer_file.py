# %%

import calendar
import re
import time

import numpy as np
import pandas as pd
from pandas import DataFrame

FILE = 'salaries.csv'


def infer_and_convert_data_types(df: DataFrame):
    '''
    Notes on Categorical: I considered the non-atomic category columns (such as genres of a movie),
    and came to the conclusion that it is out of scope of this project, and should be left for
    the next pipeline.
    '''
    num_entries = len(df)
    for col_name in df.columns:
        # if dtype of the column is not object then pass
        if str(df.dtypes[col_name]) != 'object':
            continue

        # Categorical check
        uniques = len(df[col_name].str.lower().unique())
        if uniques <= 500 and uniques / len(df[col_name]) < 0.5:  # added a limit compared to the given version
            df[col_name] = pd.Categorical(df[col_name])

        # choose 100 entries to sample
        if num_entries >= 100:
            random_entries = df[col_name].sample(n=100, random_state=42)
        else:
            random_entries = df[col_name]

        # do nothing if values are too lengthy
        if exceed_max_len(random_entries):
            continue

        # Number check
        # Use more lenient threshold for test entries
        converted, num_col = process_number(random_entries, exceed_threshold=0.5)
        if converted:
            # then try again with stricter threshold for all entries
            converted, num_col = process_number(df[col_name], exceed_threshold=0.1)
            if converted:
                df[col_name] = num_col
                continue

        # do the same as process_number for datetime and timedelta

        # do the same operations with to_datetime and to_timedelta then pick which one is better
        # as it's not unlikely for a column to be both dt and td-valid
        time_col = None
        converted, dt_col = process_time(random_entries, 'to_datetime', pd.to_datetime, exceed_threshold=0.5)
        if converted:
            converted, dt_col = process_time(df[col_name], 'to_datetime', pd.to_datetime, exceed_threshold=0.1)
            if converted:
                time_col = dt_col
        converted, td_col = process_time(random_entries, 'to_timedelta', pd.to_timedelta, exceed_threshold=0.5)
        if converted:
            converted, td_col = process_time(df[col_name], 'to_timedelta', pd.to_timedelta, exceed_threshold=0.1)
            if converted:
                if time_col is None or time_col.isna().sum() > td_col.isna().sum():
                    time_col = td_col
        if time_col is not None:
            df[col_name] = time_col
            continue

    return df


def exceed_max_len(entries, max_len=70, exceed_threshold=0.2):
    '''Maps the column to dtype 'object' (False) if over 20% of entries has length >= 70'''
    lengthy_entries = 0
    for entry in entries:
        if not isinstance(entry, str):
            continue
        if len(entry) >= max_len:
            lengthy_entries += 1
    if lengthy_entries / len(entries) > exceed_threshold:
        return True
    return False


def process_number(entries, exceed_threshold):
    '''
    First iteration: try using pd.to_numeric. If cannot reach requirements, go to the second iteration.
    Second iteration: custom logic for handling strings, then try using pd.to_numeric again.
    Difference between my custom logic and original pandas.to_numeric:
    - Support for big number abbreviations (1K 1M 1B 1T)
    - Minimal non-numeric characters tolerance (for cases like $312 where pandas would ignore)
    - Innate support for thousands separator ',' without having to use kwarg

    Notes: I considered the case where there are only valid integers and NaNs. Since NaN is a float, there is
    no way to change the dtype of the column into int without converting the NaN into int. I could have
    use min_int or max_int but I weighed that keeping the column as float would be better (since converting
    the NaNs into int would affect arithmetic operations).
    '''
    none_count = entries.isna().sum()  # None should not be counted as either NaN or number
    outer_converted = pd.to_numeric(entries, errors='coerce')
    nan_count = outer_converted.isna().sum()
    total_count = len(entries)
    if total_count - none_count == 0:  # empty set
        return (False, entries)
    # allow up to 2 nans for very small datasets
    if nan_count <= 2:
        return (True, outer_converted)
    if (nan_count - none_count) / (total_count - none_count) > exceed_threshold:
        # try harder if pandas is not good enough
        pattern = r'[+-]?(?:\d{1,3}(?:,\d{3})*|\d+)(?:\.\d+)?(?:\s*[KMBT]?(?!\w))?'
        none_count = 0
        nan_count = 0
        inner_converted = []
        for entry in entries:
            if pd.isna(entry):
                none_count += 1
                inner_converted.append(np.nan)
                continue
            tokens = re.findall(pattern, entry, flags=re.IGNORECASE)
            if len(tokens) > 1 or len(tokens) == 0:  # multiple numbers or no number found
                nan_count += 1
                inner_converted.append(np.nan)
                continue
            # a string that contains a number, with condition, should still be a string
            non_number_len = len(entry) - len(tokens[0])
            if non_number_len >= 3:
                nan_count += 1
                inner_converted.append(np.nan)
                continue
            entry = tokens[0]
            number = [c for c in entry if (c.isdigit() or c == '.')]
            try:
                number = int(''.join(number))
            except ValueError:
                number = float(''.join(number))
            multiplier = 1000
            for abr in 'KMBT':
                if entry[-1] == abr:
                    number *= multiplier
                    break
                multiplier *= 1000
            inner_converted.append(number)
        if nan_count <= 2:
            return (True, inner_converted)
        # here the condition is different because nan_count isn't double-counted with none_count
        if (nan_count) / (total_count - none_count) > exceed_threshold:
            return (False, entries)
        else:
            return (True, inner_converted)
    return (True, outer_converted)


def process_time(entries, f_name, function, exceed_threshold):
    '''
    Same two iterations like process_number. Please refer to the function above.
    Difference between my custom logic and pandas.to_datetime:
    - Accept arbitrary separators other than limited separators given by pd for Year Month Day
    Difference between my custom logic and pandas.to_timedelta:
    - Allows unnecessary non-keywords as input (pd.to_timedelta alone works fine with
    "2 hours 30 minutes", but not "2 hours and 30 minutes")
    '''
    none_count = entries.isna().sum()  # None should not be counted as either NaT or time
    outer_converted = function(entries, errors='coerce')
    nat_count = outer_converted.isna().sum()
    total_count = len(entries)
    if total_count - none_count == 0:  # empty set
        return (False, entries)
    # allow up to 2 nats for very small datasets
    if nat_count <= 2:
        return (True, outer_converted)
    if (nat_count - none_count) / (total_count - none_count) > exceed_threshold:
        none_count = 0
        nat_count = 0
        inner_converted = []
        # for timedelta: remove all the unnecessary word then try to_timedelta again
        if f_name == 'to_timedelta':
            keywords = {'w', 'd', 'day', 'hours', 'hr', 'h', 'minutes', 'minute', 'min', 'm', 'seconds', 'second',
                        'sec', 's', 'millisecond', 'milli', 'ms', 'microsecond', 'micro', 'us', 'nanosecond', 'nano',
                        'ns'}
            for entry in entries:
                if pd.isna(entry):
                    none_count += 1
                    inner_converted.append(pd.NaT)
                    continue
                entry = entry.split(' ')
                modified_entry = ''
                for i, token in enumerate(entry):
                    if i == 0 and token[0] in '+-':
                        modified_entry += token + ' '
                        continue
                    if len(token) >= 2 and token[-1] == 's' and token[:-1] in keywords:
                        modified_entry += token[:-1] + ' '
                    elif token in keywords:
                        modified_entry += token + ' '
                    elif re.match(r'\d{1,4}:\d{2}(?:[^ ]*)?|\d+(?:[^ ]*)?', token):
                        if token[0] in '+-':
                            modified_entry += token[1:] + ' '
                        else:
                            modified_entry += token + ' '
                modified_entry = function(modified_entry, errors='coerce')
                inner_converted.append(modified_entry)
                if pd.isna(modified_entry):
                    nat_count += 1
        # for datetime: extract all digits and keywords then try to_datetime again
        else:
            pattern = r'([+-]?\d{1,2}:\d{2}(?:[^ ]*)?|[+-]?\d+|' + r'am|pm|utc|hour|minute|second|'
            pattern += '|'.join(calendar.month_abbr[1:]) + ')'
            for entry in entries:
                if pd.isna(entry):
                    none_count += 1
                    inner_converted.append(pd.NaT)
                    continue
                tokens = re.findall(pattern, entry, flags=re.IGNORECASE)
                entry = ' '.join(tokens)
                modified_entry = function(entry, errors='coerce')
                inner_converted.append(modified_entry)
                if pd.isna(modified_entry):
                    nat_count += 1
        if nat_count <= 2:
            return (True, inner_converted)
        # here the condition is different because nat_count isn't double-counted with none_count
        if (nat_count) / (total_count - none_count) > exceed_threshold:
            return (False, entries)
        else:
            return (True, inner_converted)
    return (True, outer_converted)


def load_data(filename):
    '''
    Load data from .csv, .xlsx, .xls, remove trailing and leading whitespaces in the process.
    '''
    if filename.lower().endswith('.csv'):
        return pd.read_csv(filename, thousands=',').applymap(lambda x: x.strip() if isinstance(x, str) else x)
    elif filename.lower().endswith('.xlsx') or filename.lower().endswith('.xls'):
        return pd.read_excel(filename, thousands=',').applymap(lambda x: x.strip() if isinstance(x, str) else x)
    else:
        raise ValueError("Unsupported file format.")


start = time.time()

# Test the function with your DataFrame
df = load_data(FILE)
print("Data types before inference:")
print(df.dtypes)

print('------------------------------')

df = infer_and_convert_data_types(df)

end = time.time()

print("Data types after inference:")
print(df.dtypes)
print(df)
print(f"Time elapsed: {end - start}s")

# %%
