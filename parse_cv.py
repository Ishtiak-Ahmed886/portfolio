import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile('Copy of CV of Ish.docx') as z:
    doc_xml = z.read('word/document.xml')
    rels_xml = z.read('word/_rels/document.xml.rels')

rels_root = ET.fromstring(rels_xml)
rels = {}
for child in rels_root:
    if 'Target' in child.attrib and 'Id' in child.attrib:
        rels[child.attrib['Id']] = child.attrib['Target']

doc_root = ET.fromstring(doc_xml)
for elem in doc_root.iter():
    if elem.tag.endswith('hyperlink'):
        r_id = elem.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
        text = ''.join(elem.itertext())
        target = rels.get(r_id, 'N/A')
        print(f'Text: "{text}" -> Link: {target}')
