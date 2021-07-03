test: 
	env BUCKTRIX_DIR="../.bucktrix" poetry run python3 -m bucktrix send "this is test"

build: bucktrix/*
	poetry run pyinstaller -n bucktrix -F bucktrix/__main__.py

publish: bucktrix/*
	poetry publish --build -u __token__ 