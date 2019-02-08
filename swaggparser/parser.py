import subprocess
import datetime
import shlex
import json
import uuid
import os
from time import sleep
from bs4 import BeautifulSoup


class SwaggParser(object):
    def __init__(self, swagger_version=2, project="petstore", in_folder="swagger"):
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

        for branch in self.branches:
            d = {}
            with open(self.root + 'html/' + branch.split('.')[0] + '.html', 'r') as f:
                html = BeautifulSoup(f.read())
                if self.version == 2:
                    methods = html.find_all(class_="opblock-summary-method")
                    paths = html.find_all(class_="opblock-summary-path")
                    parameter_containers = html.find_all(class_="opblock-body")
                    response_containers = html.find_all(class_="responses-table")
                    responses = [
                        [
                            {
                                "type": "json" if response.find("example") is not None and
                                                  response.find("example").get_text().startswith("{") else "class",
                                "body": json.dumps(response.find("example").get_text())
                                if response.find("example") is not None and
                                   response.find("example").get_text().startswith("{") else None
                            }
                            for response in container.find_all("tr", class_="response") if response.get("data-code") == "200"
                        ] for container in response_containers
                    ]
                    print([parameter for parameter in parameter_containers[5].find(class_="parameters")])
                    parameters = [
                        [
                            {
                                "class": parameter.find(class_="parameter__in").get_text().
                                    replace('(', '').replace(')', '')
                                if parameter.find(class_="parameter__in") is not None else None,
                                "name": parameter.find(class_="parameter__name").get_text().split('*')[0][:-1]
                                if parameter.find(class_="parameter__name") is not None else None
                                ,
                                "type": container.find(class_="body-param__example").get_text()
                                if parameter.find(class_="parameter__in") is not None and
                                   parameter.find(class_="parameter__in").get_text().
                                       replace('(', '').replace(')', '') == "body"
                                else parameter.find(class_="parameter__type").get_text().split('(')[0]
                                if parameter.find(class_="parameter__type") is not None else None
                            } for parameter in [container.find(class_="parameters")] #FIXME
                        ] for container in parameter_containers
                    ]

                    print(len(paths), len(methods), len(parameters), len(responses))
                    for i, path in enumerate(paths):
                        print(path.get_text(), methods[i].get_text())
                        if path not in d:
                            d[path.get_text()] = {}
                        d[path.get_text()][methods[i].get_text()] = {
                            "request": [
                                parameter for parameter in parameters[i]
                            ],
                            "response": responses[i]
                        }

            print(json.dumps(d, indent=4, sort_keys=True))

            exit(404)
            with open(self.root + 'json/' + branch.split('.')[0] + '.json', 'r') as f:
                swagger_ui = json.load(f)

            for key, call in swagger_ui.items():
                for key, method in call.items():
                    if "response" in method:
                        if method["response"]["type"] == "json":
                            with open(self.tmp_dir + "_" + str(uuid.uuid4()) + '.json', 'w') as f:
                                json.dump(json.loads(method["response"]["value"]), f)
                    for element in method["request"]["params"]:
                        if element["type"] == "body":
                            with open(self.tmp_dir + element["name"] + '.json', 'w') as f:
                                json.dump(json.loads(element["param"]), f)

        outfolder = self.output_folder + '/' + self.base_class.replace('.', '/') + '/'
        for filename in os.listdir(outfolder):
            try:
                os.remove(outfolder + filename)
            except Exception:
                pass

    def apify(self, project="vindeenjob", cls="VEJ"):
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

        print(header % (project, cls, cls, project))

        for branch in self.branches:
            with open(self.root + 'json/' + branch.split('.')[0] + '.json', 'r') as f:
                swagger_ui = json.load(f)

            for path, call in swagger_ui.items():
                for req, method in call.items():
                    query = "?"
                    body = ""
                    _path = []
                    if "request" in method:
                        for param in method["request"]["params"]:
                            if param["type"] == "query":
                                query += '"%s=" + %s + "&" + ' % (param["name"], param["name"])
                                _path.append({
                                    "value": param["name"],
                                    "type": param["param"] if param is not "string" else "String"
                                })
                            elif param["type"] == "path":
                                _path.append({
                                    "value": param["name"],
                                    "type": param["param"] if param is not "string" else "String"
                                })
                            elif param["type"] == "body":
                                body = ".body(" + param["name"].capitalize()+ ")"

                    if len(query) == 1:
                        query = ""
                    else:
                        query = query[:-9] + '"'
                    if "response" in method:
                        obj = "Object"
                        if not method["response"]["type"] == "json":
                            obj = method["response"]["type"].capitalize()

                        if method["response"]["value"] is not None and method["response"]["value"].startswith('['):
                            print(str("""
    public ArrayList<Object> getObjects(%s) {
        return rest%s.%s("%s|).statusCode(200).extractAsList(%s.class);
    }
""" % (", ".join(p["type"] + " " + p["value"] for p in _path),
   body, req.lower(),
   path.replace('{',  '" + ').replace('}', ' + "') + query, obj)).replace('+ "|', '').replace('|', '"').replace('?"', '?').replace('""', ''))
                        else:
                            print(str("""
    public Object getObject(%s) {
        return rest%s.%s("%s|).statusCode(200).extractAs(%s.class);
    }
""" % (", ".join(p["type"] + " " + p["value"] for p in _path),
   body, req.lower(),
   path.replace('{',  '" + ').replace('}', ' + "') + query, obj)).replace('+ "|', '').replace('|', '"').replace('?"', '?').replace('""', ''))

        print('}')

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
            except FileNotFoundError:
                pass

    def sufparse(self):
        sleep(15)
        t = []
        outfolder = self.output_folder + '/' + self.base_class.replace('.', '/') + '/'
        for filename in os.listdir(outfolder):
            if any(i.isdigit() for i in filename) and '_' not in filename:
                t.append(outfolder + filename)

        for f in t:
            print(f)
            try:
                os.remove(f)
            except FileNotFoundError:
                pass

    def create_pojos(self):
        for filename in os.listdir(self.tmp_dir):
            cmd = "java -jar lib/jsonschema2pojo-cli-1.0.0.jar -a JACKSON2 -T JSON -E -S -p %s -s %s -t %s" % (
                self.base_class, self.tmp_dir + filename, self.output_folder
            )
            print(cmd)
            formatted_cmd = shlex.split(cmd)
            subprocess.Popen(formatted_cmd)
