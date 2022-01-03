# Dek Khang Khai

## :gear: Run local
1. Install python virtual environment such as Ancona pipenv etc.
2. Install python package by using
```
    pip install -r requirements.txt
```
3. Create environment variable file by using
```
touch .env
```
4. In environment variable file should include the list below
```
DKK_DISCORD_TOKEN=[Discord bot token]
DKK_DISCORD_PREFIX=[Discord bot prefix]
DKK_DB_HOST=[Database host]
DKK_DB_USER=[Database user]
DKK_DB_PASSWORD=[Database password]
DKK_DB_DATABASE=[Database name]
```
5. Run
```
python main.py
```