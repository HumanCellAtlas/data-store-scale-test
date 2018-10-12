deploy:
	git clean -df chalicelib vendor
	shopt -s nullglob; for wheel in vendor.in/*/*.whl; do unzip -q -o -d vendor $$wheel; done
	cp -R ../locustfiles chalicelib
	cp ../locustfile.py chalicelib
	chalice deploy --no-autogen-policy