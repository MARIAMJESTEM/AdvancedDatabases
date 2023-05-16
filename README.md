# AdvancedDatabases project

## Creating a local version of the database:
1. Run pgAdmin 
2. Register your own server (name does not matter). Specify:
    * `localhost` as host name/address, 
    * `5432` as port
    * `postgres` as maintenance database, username and password
4. Create a database named `advanced_databases`
5. Run the `database_architecture.py` script


## Running:
- Create database and fill it with sample data: `database_architecture.py`
- Run API + Web server: `python __main__.py`
