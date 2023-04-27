# deactivate
# rm -rf .venv
# python -m venv .venv
# activate
# pip install sphinx
# pip install -e sdk/python
# pip install -r sdk/python/requirements-dev.txt
# pip install -r components/google-cloud/docs/requirements.txt
# pip install sphinx_rtd_theme
# pip install m2r2 sphinx_immaterial autodocsumm
# pip install -e components/google-cloud

cp components/google-cloud/docs/source/conf.py .
pushd components/google-cloud/docs
make clean html
open build/html/index.html
popd
# python -m sphinx -T -E -b html -d _build/doctrees -D language=en -c source . html