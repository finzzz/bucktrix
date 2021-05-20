test: 
	poetry run python main.py send "this is test"

build: bucktrix/*
	poetry run pyinstaller -n bucktrix -F bucktrix/__main__.py

publish: bucktrix/*
	poetry publish --build -u __token__ 