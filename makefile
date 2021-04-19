init: 
	poetry install

test: 
	poetry run python main.py send "this is test"

build: main.py bucky/*
	poetry run pyinstaller -n bucky -F main.py