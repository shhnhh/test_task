from flask import Flask, jsonify, request, Response
from xmltodict import parse, unparse
from json import loads

app = Flask(__name__)

with open('dict_document_type_cls.json', 'r') as file:
    dict_document_type = loads(file.read())

with open('template.xml', 'r') as file:
    xml_template = parse(file.read())

@app.route('/xml2json', methods = ['post'])
def xml2json():
    res_json = {}
    xml_data = parse(request.data)['EntrantChoice']['AddEntrant']
    IdDocumentType = str(xml_data['Identification']['IdDocumentType'])
    Fields = xml_data['Identification']['Fields']

    fields = []

    for entry in dict_document_type:
        if str(entry['Id']) == IdDocumentType:
            fields = entry['FieldsDescription']['fields']
            break

    for field in fields:
        res_json[field['xml_name']] = ''
        try:
            value = Fields[field['xml_name']]
            res_json[field['xml_name']] = value
        except:
            print('Нет тега', field['xml_name'])
            continue

    return jsonify(res_json)

@app.route('/json2xml', methods = ['post'])
def json2xml():

    def _repitem(obj, key, val):
        for i in obj:
            if i.lower() == key.lower():
                obj[i] = val
                return True
        for k, v in obj.items():
            if isinstance(v, dict):
                item = _repitem(v, key, val)
                if item:
                    return True
        return False
            
    json_data = loads(request.data)
    
    Fields = xml_template['EntrantChoice']['AddEntrant']['Identification']['Fields'] = {}

    for field in json_data:
        if _repitem(xml_template, field, json_data[field]) == False:
            Fields[field] = json_data[field]

    return Response(unparse(xml_template), mimetype='text/xml')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
