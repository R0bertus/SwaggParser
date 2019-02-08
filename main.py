from swaggparser.parser import SwaggParser
from selenium.webdriver.chrome.webdriver import WebDriver
from time import sleep


def main(url, project="sol", cls="Sollicitatie", in_folder="swagger", branch=None, swagger_version=2, time_interval=3):
    driver = WebDriver("lib/chromedriver.exe")
    driver.get(url)
    sleep(time_interval)

    if branch:
        driver.execute_script(open("javascript/fetcher.js", 'r').read() + "; change_branch(%s);" % branch)
        sleep(time_interval)

    driver.execute_script(open("javascript/fetcher.js", 'r').read() + "; toggle();")
    sleep(time_interval)

    with open(in_folder + "/" + project + "/html/" + cls, 'w') as f:
        f.write(driver.page_source)
        sleep(time_interval)

    sp = SwaggParser(swagger_version, project, in_folder)
    sp.preparse()
    sp.create_pojos()
    sp.sufparse()
    sp.apify(project, cls)


if __name__ == '__main__':
    main(
        url="http://sollicitaties01-rel1prd.vdab.be:8080/sollicitaties/swagger-ui.html",
        branch="http://sollicitaties01-rel1prd.vdab.be:8080/sollicitaties/v2/api-docs?group=sollicitaties.v2"
    )
