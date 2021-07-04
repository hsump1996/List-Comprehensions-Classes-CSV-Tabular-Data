# tabletools.py
def read_csv(fn):
    rows, data = [], []
    with open(fn, 'r') as f:
        for i, line in enumerate(f):
            words = []
            for word in line.split(','):
                word = word.strip()
                try:
                    words.append(float(word))
                except ValueError:
                    words.append(word)

            if i == 0:
                cols = words
            else:
                rows.append(i - 1)
                data.append(words)
    return Table(data, rows, cols)
class LabeledList:
    def __init__(self, data=None, index=None):
        self.data = data
        self.index = index

        if not index:
            index = [i for i in range(len(data))]
            self.index = index

    def __str__(self):
        return repr(self)

    def __repr__(self):
        if not self.index:
            return ''

        vals_format = f'{{:>{max([len(str(e)) for e in self.data])}}}'
        labels_format = f'{{:>{max([len(str(e)) for e in self.index])}}}'

        return '\n'.join([
            vals_format.format(label) + " " + labels_format.format(value)
            for label, value in zip(self.index, self.data)
        ])

    def __getitem__(self, key_list):
        if isinstance(key_list, list):
            # Case 1
            if isinstance(key_list, LabeledList):
                index_array = [index for index, val in enumerate(self.index) if val in key_list.data]
            # Case 3
            elif type(key_list[0]) == bool:
                index_array = [index for index, val in enumerate(key_list) if val == True]
            # Case 2
            else:
                index_array = [index for index, val in enumerate(self.index) if val in key_list]
            return LabeledList([self.data[num] for num in index_array], [self.index[num] for num in index_array])
        else:
            index_array = [index for index, val in enumerate(self.index) if key_list == val]
            # Case 4a
            if len(index_array) == 1:
                return self.data[index_array[0]]
            # Case 4b
            else:
                return LabeledList([self.data[num] for num in index_array], [self.index[num] for num in index_array])

    def __iter__(self):
        return iter(self.data)

    def __eq__(self, scalar):
        return LabeledList([val == scalar for val in self.data])

    def __ne__(self, scalar):
        return LabeledList([val != scalar for val in self.data])

    def __gt__(self, scalar):
        return LabeledList([val < scalar for val in self.data])

    def __lt__(self, scalar):
        return LabeledList([val > scalar for val in self.data])

    def map(self, f):
        return LabeledList([f(val) for val in self.data])


class Table:

    def __init__(self, data, index=None, columns=None):
        self.data = data
        self.index = index
        self.columns = columns

        if index is None:
            index = [i for i in range(len(data))]
            self.index = index

        if columns is None:
            columns = [i for i in range(len(data[0]))]
            self.columns = columns

    def __repr__(self):
        rows_max_len = max([len(str(e)) for e in self.index]) if self.index else 0
        cols_max_len_list = [
            max([len(str(col)), *[len(str(line[i])) for line in self.data]])
            for i, col in enumerate(self.columns)
        ]
        max_len_list = [rows_max_len, *cols_max_len_list]

        first_line = ' '.join([
            f"{{:>{max_len_list[i]}}}".format(value)
            for i, value in enumerate(['', *self.columns])
        ])

        rest_lines = [
            ' '.join(f"{{:>{max_len_list[i]}}}".format(value) for i, value in enumerate([index, *line]))
            for index, line in zip(self.index, self.data)
        ]

        return '\n'.join([first_line, *rest_lines])

    def __str__(self):
        return repr(self)


    def __getitem__(self, col_list):
        #Case 1
        if type(col_list) == LabeledList:
            columnList = [colVal for colVal in self.columns if colVal in col_list.data]
            index_of_col_val_list = [index for index, colVal in enumerate(self.columns) if colVal in col_list.data]
            data = [[elem for index, elem in enumerate(line) if index in index_of_col_val_list]
                    for line in self.data]

            return Table(data, self.index, columnList)
        # Case 3
        elif type(col_list[0]) == bool:
            index_of_row_val_list = [index for index, val in enumerate(col_list) if val == True]
            data = [
                self.data[val] for val in index_of_row_val_list
            ]
            return Table(data, index_of_row_val_list, self.columns)

        #Case 2
        elif isinstance(col_list, list):
            index_of_col_val_list = [self.columns.index(val) for index, val in enumerate(col_list) if val in self.columns]
            data = [
                [line[index] for index in index_of_col_val_list]
                for line in self.data
            ]
            return Table(data, self.index, col_list)

        else:
            index_of_col_val_list = [index for index, val in enumerate(self.columns) if val == col_list]
            #Case 4a
            if len(index_of_col_val_list) == 1:
                indexList = [i for i in range(index_of_col_val_list[0]+1)]
                valueList = [elem for line in self.data for index, elem in enumerate(line) if index == index_of_col_val_list[0]]
                return LabeledList(valueList, indexList)

            #Case 4b
            else:
                colList = [col_list for i in range(len(index_of_col_val_list))]
                indexList = [i for i in range(len(index_of_col_val_list))]
                data = [
                    [line[index] for index in index_of_col_val_list]
                    for line in self.data
                ]
                return Table(data, indexList, colList)

    def head(self, n):
        return Table(self.data[:n], self.index[:n], self.columns)

    def tail(self, n):
        return Table(self.data[-n:], self.index[-n:], self.columns)


    def shape(self):
        returnTuple = (len(self.data), len(self.columns))
        return returnTuple

