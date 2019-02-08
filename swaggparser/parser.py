import subprocess
import datetime
import random
import shlex
import json
import uuid
import os
from time import sleep
from bs4 import BeautifulSoup


class SwaggParser(object):
    def __init__(self, swagger_version=2, project="sol", in_folder="swagger"):
        self.root = in_folder + '/' + project + '/'
        with open(self.root + 'config.json', 'r') as f:
            config = json.load(f)

        self.version = swagger_version
        self.project = config["project"]
        self.base_class = config["base_class"]
        self.output_folder = config["output_folder"]
        self.branches = config["branches"]
        self.tmp_dir = self.root + 'tmp/' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '/'

        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)

        if not os.path.exists(self.root + "/html"):
            os.makedirs(self.root + "/html")

        if not os.path.exists(self.root + "/json"):
            os.makedirs(self.root + "/json")

        for branch in self.branches:
            d = {}
            with open(self.root + 'html/' + branch.split('.')[0] + '.html', 'r') as f:
                html = BeautifulSoup(f.read(), "lxml")
                if self.version == 2:
                    methods = html.find_all(class_="opblock-summary-method")
                    paths = html.find_all(class_="opblock-summary-path")
                    parameter_containers = html.find_all(class_="opblock-body")
                    response_containers = html.find_all(class_="responses-table")
                    responses = [
                        [
                            {
                                "type": "json" if response.find("pre", class_="example") is not None and
                                                  response.find("pre", class_="example").get_text().startswith("{") else "class",
                                "body": response.find("pre", class_="example").get_text().replace('\n', '')
                                if response.find("pre", class_="example") is not None and
                                   response.find("pre", class_="example").get_text().startswith("{") else None
                            }
                            for response in container.find_all("tr", class_="response")
                            if response.find('td', class_="response-col_status").get_text() == "200"
                        ] for container in response_containers
                    ]
                    parameters = [
                        [
                            {
                                "class": parameter.find(class_="parameter__in").get_text().
                                    replace('(', '').replace(')', '')
                                if parameter.find(class_="parameter__in") is not None else None,
                                "name": parameter.find(class_="parameter__name").get_text().split('*')[0].split('\u00a0')[0]
                                if parameter.find(class_="parameter__name") is not None else None
                                ,
                                "type": container.find(class_="body-param__example").get_text().replace('\n', '')
                                if parameter.find(class_="parameter__in") is not None and
                                   parameter.find(class_="parameter__in").get_text().
                                       replace('(', '').replace(')', '').replace('\n', '') == "body"
                                else parameter.find(class_="parameter__type").get_text().split('(')[0]
                                if parameter.find(class_="parameter__type") is not None else None
                            } for parameter in (container.find(class_="parameters").find_all('tr')[1:]
                        if container.find(class_="parameters") is not None else [])
                        ] for container in parameter_containers
                    ]

                    for i, path in enumerate(paths):
                        if path not in d:
                            d[path.get_text()] = {}
                        d[path.get_text()][methods[i].get_text()] = {
                            "request": [
                                parameter for parameter in parameters[i]
                            ],
                            "response": responses[i]
                        }

            json.dump(d, open(self.root + "/json/" + branch.split('.')[0] + ".json", 'w'), indent=4, sort_keys=True)

            with open(self.root + '/json/' + branch.split('.')[0] + '.json', 'r') as f:
                swagger_ui = json.load(f)

            for key, call in swagger_ui.items():
                for key, method in call.items():
                    for element in method["response"]:
                        if element["type"] == "json":
                            with open(self.tmp_dir + "_" + str(uuid.uuid4()) + '.json', 'w') as f:
                                json.dump(json.loads(element["body"]), f)
                    for element in method["request"]:
                        if element["type"].startswith("{"):
                            if not os.path.exists(self.tmp_dir + element["name"] + '.json'):
                                with open(self.tmp_dir + element["name"] + '.json', 'w') as f:
                                    json.dump(json.loads(element["type"]), f)
                            else:
                                with open(self.tmp_dir + "_" + str(uuid.uuid4()) + '.json', 'w') as f:
                                    json.dump(json.loads(element["type"]), f)

        outfolder = self.output_folder + '/' + self.base_class.replace('.', '/') + '/'
        if not os.path.exists(outfolder):
            os.makedirs(outfolder)

        for filename in os.listdir(outfolder):
            try:
                print("remove: " + outfolder + filename)
                os.remove(outfolder + filename)
            except Exception:
                pass

    def apify(self, project="vindeenjob", cls="VEJ"):
        text = ""
        header = """
        
package be.vdab.%s.utils
        
import java.util.ArrayList;

import static be.vdab.qa.framework.properties.VDABProperties.getProperty;
import static be.vdab.qa.framework.rest.RestAssuredService.given;

public class %sAPI {
    private RestAssuredService rest;
    private RestAssuredService restAdmin;

    public %sAPI() {
        VDABProperties.loadProperties();

        rest = given(
                getProperty("service.%s.url"),
                "HEADER_NAME",
                "HEADER_VALUE"
        );
    }"""
        text += header % (project, cls, cls, project)
        for branch in self.branches:
            with open(self.root + 'json/' + branch.split('.')[0] + '.json', 'r') as f:
                swagger_ui = json.load(f)

            for path, call in swagger_ui.items():
                for req, method in call.items():
                    query = "?"
                    body = ""
                    _path = []
                    if "request" in method:
                        for param in method["request"]:
                            """
                            if param["class"] == "query":
                                query += '"%s=" + %s + "&" + ' % (param["name"], param["name"])
                                _path.append({
                                    "value": param["name"],
                                    "type": param["param"] if param is not "string" else "String"
                                })
                            """
                            if param["class"] == "path":
                                _path.append({
                                    "value": param["name"],
                                    "type": param["type"].capitalize()
                                })
                            elif param["class"] == "body":
                                body = ".body(" + param["name"].capitalize() + ")"

                    if len(query) == 1:
                        query = ""
                    else:
                        query = query[:-9] + '"'

                    obj = "Object"
                    if "response" in method:
                        for param in method["response"]:
                            if not param["type"] == "json":
                                obj = param["type"].capitalize()

                            if param["type"] is "json" and param["body"].startswith('['):
                                text += str("""
    public ArrayList<Object> getObjects(%s) {
        return rest%s.%s("%s|).statusCode(200).extractAsList(%s.class);
    }
""" % (", ".join(p["type"] + " " + p["value"] for p in _path),
   body, req.lower(),
   path.replace('{',  '" + ').replace('}', ' + "') + query, obj)).replace('+ "|', '').replace('|', '"').replace('?"', '?').replace('""', '')
                            else:
                                text += str("""
    public Object getObject(%s) {
        return rest%s.%s("%s|).statusCode(200).extractAs(%s.class);
    }
""" % (", ".join(p["type"] + " " + p["value"] for p in _path),
   body, req.lower(),
   path.replace('{',  '" + ').replace('}', ' + "') + query, obj)).replace('+ "|', '').replace('|', '"').replace('?"', '?').replace('""', '')
                            break
                        else:
                            text += str("""
    public void voidRequest(%s) {
        return rest%s.%s("%s|).statusCode(200);
    }
""" % (", ".join(p["type"] + " " + p["value"] for p in _path),
   body, req.lower(),
   path.replace('{',  '" + ').replace('}', ' + "') + query)).replace('+ "|', '').replace('|', '"').replace('?"', '?').replace('""', '')

        text += '}'
        outfolder = self.output_folder + '/' + '/'.join(self.base_class.replace('.', '/').split('/')[:-1]) + '/utils/'

        if not os.path.exists(outfolder):
            os.makedirs(outfolder)

        with open(outfolder + cls + '.java', 'w') as f:
            f.write(text)

    def preparse(self):
        d = []
        for filename in os.listdir(self.tmp_dir):
            with open(self.tmp_dir + filename, 'r') as f:
                d.append({"json": f.read(), "base": not filename.startswith('_'), "file": self.tmp_dir + filename})

        t = []
        for i, m in enumerate(d):
            for j, n in enumerate(d):
                if i != j:

                    if m["json"][0] == "[":
                        m["json"] = m["json"][1:-1]

                    if n["json"][0] == "[":
                        n["json"] = n["json"][1:-1]

                    if m["json"] == n["json"]:
                        if n["base"]:
                            t.append(m["filen"])
                        else:
                            t.append(n["file"])

        for f in t:
            print(f)
            try:
                os.remove(f)
            except Exception:
                pass

    def sufparse(self):
        for _ in range(random.randint(10, 16), 0, -1):  # Hehe random :-)
            sleep(1)
            print("Wacht nog %s seconden tot het verwerkt is" % _)
        t = []
        outfolder = self.output_folder + '/' + self.base_class.replace('.', '/') + '/'
        for filename in os.listdir(outfolder):
            if any(i.isdigit() for i in filename) and '_' not in filename:
                t.append(outfolder + filename)

        for f in t:
            try:
                os.remove(f)
            except Exception:
                pass

    def create_pojos(self):
        for filename in os.listdir(self.tmp_dir):
            cmd = "java -jar lib/jsonschema2pojo-cli-1.0.0.jar -a JACKSON2 -T JSON -E -S -p %s -s %s -t %s" % (
                self.base_class, self.tmp_dir + filename, self.output_folder
            )
            print(cmd)
            formatted_cmd = shlex.split(cmd)
            subprocess.Popen(formatted_cmd)
