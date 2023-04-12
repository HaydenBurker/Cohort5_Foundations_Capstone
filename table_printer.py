def format_rows(rows):
    formatted_rows = []
    for row in rows:
        row = list(row)
        for i in range(len(row)):
            
            if row[i] == None:
                row[i] = "NULL"
            if type(row[i]) == bytes:
                row[i] = str(row[i])
            elif type(row[i]) == float:
                row[i] = str(f'{row[i]:.3f}')
            if len(str(row[i])) > 30:
                row[i] = f"{str(row[i])[:27]}..."
        formatted_rows.append(row)
    return formatted_rows

def get_column_sizes(rows, fields):
    column_sizes = []
    for col in range(len(fields)):
        column_sizes.append(len(fields[col]))
        for row in rows:
            column_sizes[col] = max(column_sizes[col], len(str(row[col])))
    return column_sizes

def print_table(rows, fields = None):
    if fields == None and len(rows) > 0:
        fields = [f'Field {i+1}' for i in range(len(rows[0]))]
    rows = format_rows(rows)
    column_sizes = get_column_sizes(rows, fields)

    for i, field in enumerate(fields):
        column_size = column_sizes[i]
        print(f"{field:<{column_size}}", end='  ')
    print()
    
    for row in rows:
        row = list(row)
        for i, column_size in enumerate(column_sizes):
            print(f"{row[i]:<{column_size}}", end='  ')
        print()
