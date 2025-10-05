# backend/cli.py
import click
from Scrapper import scrape

@click.command("scrape-jobs")
def scrape_jobs():
    """Scrape jobs and post to backend"""
    scrape.run()
