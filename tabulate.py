
def createRawTable(table, column_width=30):
    table_headers = list(table.keys())
    table_body = [table[header] for header in table_headers]

    print("|" + "|".join([
        f"{table_header.title():^{column_width}}" for table_header in table_headers
    ]) + "|")
    print("|:" + ":|:".join(["-" * (column_width - 2)] * len(table_headers)) + ":|")
    for row_number in range(len(table_body[0])):
        print("|" + "|".join([
            f"{table[table_header][row_number]:^{column_width}}" if column_number == 0 else f"{table[table_header][row_number]:^{column_width}.3f}" for column_number, table_header in enumerate(table_headers)
        ]) + "|")
