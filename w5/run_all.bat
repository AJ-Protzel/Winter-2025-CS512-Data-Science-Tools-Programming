@echo off

REM Change to the directory where your database and SQL files are located
cd /d C:\School\Winter-2025-CS512-Data-Science-Tools-Programming\w5

REM Open SQLite and run the SQL files in order
sqlite3 transactions.db ".read sql_scripts\create_tables.sql"
sqlite3 transactions.db ".read sql_scripts\populate_tables.sql"
sqlite3 transactions.db ".read sql_scripts\delete_transfer_records.sql"

REM Run additional commands from commands.sql
sqlite3 transactions.db ".read commands.sql"

echo All SQL scripts have been executed successfully.
pause