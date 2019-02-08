import click
import os
from swaggparser.parser import SwaggParser
from selenium.webdriver.chrome.webdriver import WebDriver
from time import sleep


@click.command()
@click.argument('project')
@click.argument('cls')
@click.argument('html_filename')
@click.argument('url')
@click.option('--in-folder', '-i', default="swagger")
@click.option('--branch', '-b', default=None)
@click.option('--swagger_version', '-sv', default=2)
def swaggerify(project, cls, html_filename, url, in_folder="swagger", branch=None, swagger_version=2):

    time_interval = 3
    driver = WebDriver("lib/chromedriver.exe")
    driver.get(url)
    sleep(time_interval)

    if branch:
        driver.execute_script(open("javascript/fetcher.js", 'r').read() + '; change_branch("%s");' % branch)
        sleep(time_interval)

    driver.execute_script(open("javascript/fetcher.js", 'r').read() + "; toggle();")
    sleep(time_interval)

    fname = in_folder + "/" + project + "/html/"

    if not os.path.exists(fname):
        os.makedirs(fname)

    with open(fname + html_filename + ".html", 'w') as f:
        f.write(driver.page_source)
        sleep(time_interval)

    sp = SwaggParser(swagger_version, project, in_folder)
    sp.preparse()
    sp.create_pojos()
    sp.sufparse()
    sp.apify(project, cls)


if __name__ == '__main__':
    swaggerify()
