# CR Matcher: an elegant and powerful method for joining tables.
## You can view our [report](https://docs.google.com/document/d/1Ge8miJBxsIRYBPqLYTDjGzcvLwCRj_gGt14z2D6E2XI/edit?usp=sharing) here !!!
## CR Matcher contains two components:
* **Column Matcher**: assist the user in identifying the most suitable column for joining based on the provided primary column.
* **Row Matcher**: handle the task of joining the two tables using the primary column and foreign column provided.

## Usage
### You need to provide three inputs for our CR Matcher:
* Primary table: a table contains primary column.
* Foreign table: a table contains foreign column.
* Primary column: a column contains primary key.
* (Optional) Foreign column: a column contains foreign key.

## CSV Matcher:
#### If you want to analysis your CSV data, you can use CSVMatcher to help you join your table:
`output_csv`: If you want to output a csv file, set **True**, otherwise, set **False**.

`primary_file`: Input your primary table's csv file path.

`foreign_file`: Input your foreign table's csv file path.

`primary_column`: Input the primary column name you want to join. **e.g.** "Cities" or ["Cities", "Countries"]

`foreign_column`: Input the foreign column name you want to join. **e.g.** "Cities" or ["Cities", "Countries"]

`find_col`: Input the number you want **Column Matcher** to find the suitable foreign column.

```
from CRmatcher import CSVMatcher

CSV = CSVMatcher()

result = CSV.Match(output_csv, primary_file, foreign_file, primary_column, foreign_column, find_col)
```
#### If you want to join table with multiple primary column or foreign column, you can input `primary_column` or `foreign_column` as List.
```
result = CSV.Match(output_csv, primary_file, foreign_file, [primary_columns], [foreign_columns])
```
#### If you are not sure which column is most suitable for joining based on the Primary column, you can leave `foreign_column` empty:
```
result = CSV.Match(output_csv, primary_file, foreign_file, primary_column)
```
#### If you want **Column Matcher** to give you multiple suitable column, use `find_col` to define how may column you want to return:
```
result = CSV.Match(output_csv, primary_file, foreign_file, primary_column, find_col = 2)
```
## DB Matcher:
#### If you want to analysis your SQL Database data, you can use DBMatcher to help you join your table:
`config`: Input your database configuraion **e.g.** 
```
{
  "host": "127.0.0.1",
  "user": "root",
  "passwd": "pwd"
}
```
`output_csv`: If you want to output a csv file, set **True**, otherwise, set **False**.

`primary_file`: Input your primary table's csv file path.

`foreign_file`: Input your foreign table's csv file path.

`primary_column`: Input the primary column name you want to join. **e.g.** "Cities" or ["Cities", "Countries"]

`foreign_column`: Input the foreign column name you want to join. **e.g.** "Cities" or ["Cities", "Countries"]

`find_col`: Input the number you want **Column Matcher** to find the suitable foreign column.

```
from CRmatcher import DBMatcher

DB = DBMatcher(config)

result = DB.Match(output_csv, primary_file, foreign_file, primary_column, foreign_column, find_col)
```
#### If you want to join table with multiple primary column or foreign column, you can input `primary_column` or `foreign_column` as List.
```
result = DB.Match(output_csv, primary_file, foreign_file, [primary_columns], [foreign_columns])
```
#### If you are not sure which column is most suitable for joining based on the Primary column, you can leave `foreign_column` empty:
```
result = DB.Match(output_csv, primary_file, foreign_file, primary_column)
```
#### If you want **Column Matcher** to give you multiple suitable column, use `find_col` to define how may column you want to return:
```
result = DB.Match(output_csv, primary_file, foreign_file, primary_column, find_col = 2)
```





