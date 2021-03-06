# Checklist for new release

1. Run unittests
2. Update CHANGELOG.txt
3. Update version in setup.py
4. Push all changes to github
5. Test installation on a different machine in a fresh virtual environment
```bash
cd /tmp
git clone https://github.com/vecnet/vecnet.openmalaria
mkvirtualenv om
cd vecnet.openmalaria
python setup.py test
python setup.py install
deactivate
rmvirtualenv om
cd ..
rm -rf vecnet.openmalaria
```
6. Run unittests on a different machine

`python setup.py test`

7. Make a release/tag

https://github.com/vecnet/vecnet.openmalaria/releases -> Draft a new release

Use v0.6.2 format for tag name

8. Run `setup.py sdist bdist_egg bdist_wininst upload` command