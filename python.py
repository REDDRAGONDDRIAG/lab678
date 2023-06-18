import os
import argparse
import sys
import json
import xml.etree.ElementTree as ET
import yaml
import xmltodict

parser = argparse.ArgumentParser(description='Opis programu')
parser.add_argument('x', help='plik wejsciowy')
parser.add_argument('y', help='plik wyjsciowy')

args = parser.parse_args()

if not os.path.exists(args.x):
    print('Taka ścieżka do pliku nie istnieje, podaj poprawną')
    sys.exit()

def mainf(ext):
    if ext == '.json':
        def jsonl(ex):
            json_file = ex

            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)

            except ValueError as e:
                print('Błąd składni JSON:', e)
                sys.exit()
            else:
                print('Plik json ma poprawną składnie\n')

            if extension2 == '.xml':
                root = ET.Element('root')

                def create_xml_element(key, value, parent):
                    element = ET.Element(key)
                    if isinstance(value, dict):
                        for k, v in value.items():
                            create_xml_element(k, v, element)
                    else:
                        element.text = str(value)
                    parent.append(element)

                for key, value in data.items():
                    create_xml_element(key, value, root)

                tree = ET.ElementTree(root)
                tree.write(args.y, encoding='utf-8', xml_declaration=True)
                print(f'Plik został poprawnie przeformatowany z {extension} na {extension2} i zapisany {args.y}')

            if extension2 == '.yaml' or extension2 == '.yml':
                yaml_data = yaml.dump(data)
                with open(args.y, "w") as f:
                    f.write(yaml_data)
                    print(f'Plik został poprawnie przeformatowany z {extension} na {extension2} i zapisany {args.y}')

        jsonl(args.x)

    elif ext == '.xml':
        def xmll(ex):
            try:
                with open(ex, 'r') as f:
                    xml_str = f.read()
                    print('Plik xml ma poprawną składnie')

            except:
                print('Błąd składni pliku XML.')

            if extension2 == '.json':
                json_data = json.dumps(xml_str)
                with open(args.y, 'w') as f:
                    json.dump(json_data, f)
                    print(f'Plik został poprawnie przeformatowany z {extension} na {extension2} i zapisany {args.y}')

            if extension2 == '.yml' or extension2 == '.yaml':
                xml_dict = xmltodict.parse(xml_str)
                with open(args.y, 'w') as f:
                    yaml.dump(xml_dict, f)
                    print(f'Plik został poprawnie przeformatowany z {extension} na {extension2} i zapisany {args.y}')

        xmll(args.x)

    elif ext == '.yml' or ext == '.yaml':
        def yml(ex):
            with open(ex, "r") as f:
                try:
                    yaml_data = yaml.safe_load(f)
                    print("Plik YAML ma poprawną składnie")
                except yaml.YAMLError as e:
                    print("Błąd składni pliku YAML:", e)
                    sys.exit()

            if extension2 == '.json':
                json_data = json.dumps(yaml_data)
                with open(args.y, "w") as f:
                    json.dump(json_data, f)
                    print(f'Plik został poprawnie przeformatowany z {extension} na {extension2} i zapisany {args.y}')

            if extension2 == '.xml':
                def create_element(name, text=None):
                    element = ET.Element(name)
                    element.text = text
                    return element

                def yaml_to_xml(yaml_data, parent=None):
                    if isinstance(yaml_data, dict):
                        if parent is None:
                            parent = ET.Element("root")
                        for key, value in yaml_data.items():
                            child = create_element(key)
                            parent.append(child)
                            yaml_to_xml(value, child)
                        return parent
                    elif isinstance(yaml_data, list):
                        for item in yaml_data:
                            yaml_to_xml(item, parent)
                    else:
                        text = str(yaml_data)
                        if parent is not None:
                            parent.text = text
                        return create_element("value", text)

                xml_data = yaml_to_xml(yaml_data)

                with open(args.y, "wb") as f:
                    f.write(ET.tostring(xml_data))
                    print(f'Plik został poprawnie przeformatowany z {extension} na {extension2} i zapisany {args.y}')

        yml(args.x)

    else:
        print('Podałeś złe formaty plików')

mainf(extension)
