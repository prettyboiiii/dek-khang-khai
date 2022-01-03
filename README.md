# Dek Khang Khai
Dek Khang Khai is a discord bot that use for play gamble (tail or head), also include can convert text to speech and play it in voice channel

## :gear: Run on local
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
DKK_SELF_MESSAGE_DELETE_TIME=[The time input message will delete]
```
5. Run
```
python main.py
```

## :whale: Run on docker
1. Build image by using
```
sudo docker build -t [Image name] .
```
eg.
```
sudo docker build -t dkk-bot .
```
2. Run
```
sudo docker run --name dkk-bot-test -e DKK_DISCORD_TOKEN=<TOKEN> -e DKK_DISCORD_PREFIX=. -e  DKK_DB_HOST=<DB_HOST> -e DKK_DB_USER=<DB_USER> -e DKK_DB_PASSWORD=<DB_PASSWORD> -e DKK_DB_DATABASE=<DB_NAME> e DKK_SELF_MESSAGE_DELETE_TIME=10 [Image name]
```