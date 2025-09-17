uv init --app leading-scraping

uv init --lib packages/domain
uv init --lib packages/application
uv init --lib packages/infrastructure
uv init --lib packages/infrastructure-ioc

uv add --package leading-scraping domain --frozen
uv add --package leading-scraping application --frozen
uv add --package leading-scraping infrastructure --frozen
uv add --package leading-scraping infrastructure-ioc --frozen

uv add --package application domain --frozen
uv add --package infrastructure domain --frozen
uv add --package infrastructure-ioc domain --frozen
uv add --package infrastructure-ioc application --frozen
uv add --package infrastructure-ioc infrastructure --frozen

uv sync --no-group dev