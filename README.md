# CR Matcher: an elegant and powerful method for joining tables.
## CR Matcher contains two components:
* **Column Matcher**: assist the user in identifying the most suitable column for joining based on the provided primary column.
* **Row Matcher**: handle the task of joining the two tables using the primary column and foreign column provided.

## Usage
### You need to provide three inputs for our CR Matcher:
* Primary table: a table contains primary column.
* Foreign table: a table contains foreign column.
* Primary column: a column contains primary key.
* (Optional) Foreign column: a column contains foreign key.

### Column Matcher:
#### If you are not sure which column is most suitable for joining based on the Primary column, you can use Column Matcher to find the most appropriate column.
```
from CRmatcher import column_matcher

# build a col_matcher

col_matcher = column_matcher()

# To utilize ColumnMatcher effectively, you will need a table in JSON format that contains relevant and valuable information for the search process.

tables = col_matcher.files_to_tables(primary_table, foreign_table)

# Using the method "get_column_matching" to get the foreign_column.

foreign_column = col_matcher.get_column_matching(tables[0], tables[1], primary_column)
```
### Row Matcher:
#### After you have foreign column, you can use Row Matcher to generate the final join table. (Currently, Row Matcher would output the result to a csv file.)
```
from CRmatcher import FileRowMatcher

# build a row_matcher

row_matcher = FileRowMatcher()

# Using the method "find" to generate the result

row_matcher.find(output_table, foreign_column, primary_column, foreign_table, primary_table)
```
### note: You can find the demo code in demo.py and demo2.py





