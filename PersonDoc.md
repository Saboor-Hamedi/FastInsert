# FastInsert

This project helps developers to insert data into a database in a fast way. There are many things that you can do with this project.

# Install

```python 
pip install fastinsert 
```

# Usage 

```python
from fastinsert import FastInsert   
``` 

# Example
## Loign 

```
FastInsert --host localhost --user root --password 123456 --port 3307/3306 
```

Collation is optional -- collation 'add your collation'


## Queries 

```mysql 
use db_name 
``` 
desc table
```mysql 
desc table_name
```
show create tables 

```mysql 
show create table table_name
```

insert into certian table: You must select database, and
``` mysql 
table table_name
``` 

Enter the number of records to insert: example, 10
this must be integer

select all table 

```mysql 
select * from table_name
```
select with limit, first use database, and then 
```mysql 
table_name->all(1) or table_name->all()
```
