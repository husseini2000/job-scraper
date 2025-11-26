"""Simple CLI for the job-scraper project.

Provides minimal commands so `project.scripts` in `pyproject.toml`
can point to `cli:main` and produce a working console script.
"""
from __future__ import annotations

import click


@click.group()
def cli() -> None:
	"""Job Scraper command line interface."""
	pass


@cli.command()
@click.option("--all", "all_sites", is_flag=True, help="Run pipeline for all sites")
def pipeline(all_sites: bool) -> None:
	"""Run the full ETL pipeline (stub)."""
	if all_sites:
		click.echo("Running pipeline for all sites (stub)")
	else:
		click.echo("Running pipeline (stub)")


@cli.command()
@click.option("--all", "all_sites", is_flag=True, help="Scrape all configured sites")
@click.option("--site", default=None, help="Run scraper for a single site")
def scrape(all_sites: bool, site: str | None) -> None:
	"""Run scrapers."""
	if all_sites:
		click.echo("Scraping all sites (stub)")
	elif site:
		click.echo(f"Scraping site: {site} (stub)")
	else:
		click.echo("No site specified. Use --all or --site <name>.")


def main() -> None:
	"""Entry point for setuptools console script."""
	cli()


if __name__ == "__main__":
	main()

