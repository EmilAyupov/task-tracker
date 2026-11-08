docker build -t task-tracker-tests .
docker run --rm task-tracker-tests

docker compose version
mkdir -p allure-results
docker compose run --rm tests

pytest -v --alluredir=/app/allure-results
allure serve allure-results

git switch --orphan gh-pages
git commit --allow-empty -m "Initialize GitHub Pages"
git push -u origin gh-pages
git switch main
