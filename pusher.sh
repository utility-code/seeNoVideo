black "."
isort .
# pdoc --force --html -o docs airjugaad
# mv docs/airjugaad/index.html docs/index.md
# mv docs/airjugaad/* docs/
if [[ ! -z $1 ]]; then
        git add . && git commit -m $1 && git push
fi
