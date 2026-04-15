def createRawTable(table: dict, column_width: int=30) -> None:
    '''
    Prints a table in the terminal

    Arguments:
        table (dict): The dictionary of data to been displayed
        column_width (int, optional): The width of each column being printed

    Returns:
        None
    '''

    #Defining the table header and body
    table_headers = list(table.keys())
    table_body = [table[header] for header in table_headers]

    #Printing the header row
    print("|" + "|".join([
        f"{table_header.title():^{column_width}}" for table_header in table_headers
    ]) + "|")
    #Printing the separator row between the table header and body
    print("|:" + ":|:".join(["-" * (column_width - 2)] * len(table_headers)) + ":|")
    #Printing the body of the table
    for row_number in range(len(table_body[0])):
        print("|" + "|".join([
            f"{table[table_header][row_number]:^{column_width}}" if column_number == 0 else f"{table[table_header][row_number]:^{column_width}.3f}" for column_number, table_header in enumerate(table_headers)
        ]) + "|")
