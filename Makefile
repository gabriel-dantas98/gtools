build:
	sudo python3 setup.py sdist bdist_wheel

deploy:
	twine upload dist/*

check:
	twine check dist/*
	@echo "Success check!"

clean:
	python3 setup.py clean --all
	python3 -c "for p in __import__('pathlib').Path('.').rglob('__pycache__'): p.rmdir()"
	python3 -c "for p in __import__('pathlib').Path('.').rglob('*.py[co]'): p.unlink()"

.PHONY: build deploy check clean
