'''RDF reader and writer for OAI-PMH harvester and server interface
'''
from lxml.etree import SubElement
from oaipmh.metadata import MetadataReader
from oaipmh.server import NS_XSI, nsdc, NS_DC

NSRDF = 'http://www.openarchives.org/OAI/2.0/rdf/'
NSOW = 'http://www.ontoweb.org/ontology/1#'
RDF_SCHEMA = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'

rdf_reader = MetadataReader(
    fields={
    'title':       ('textList', 'rdf:RDF/ow:Publication/dc:title/text()'),
    'creator':     ('textList', 'rdf:RDF/ow:Publication/dc:creator/text()'),
    'subject':     ('textList', 'rdf:RDF/ow:Publication/dc:subject/text()'),
    'description': ('textList', 'rdf:RDF/ow:Publication/dc:description/text()'),
    'publisher':   ('textList', 'rdf:RDF/ow:Publication/dc:publisher/text()'),
    'contributor': ('textList', 'rdf:RDF/ow:Publication/dc:contributor/text()'),
    'date':        ('textList', 'rdf:RDF/ow:Publication/dc:date/text()'),
    'type':        ('textList', 'rdf:RDF/ow:Publication/dc:type/text()'),
    'format':      ('textList', 'rdf:RDF/ow:Publication/dc:format/text()'),
    'identifier':  ('textList', 'rdf:RDF/ow:Publication/dc:identifier/text()'),
    'source':      ('textList', 'rdf:RDF/ow:Publication/dc:source/text()'),
    'language':    ('textList', 'rdf:RDF/ow:Publication/dc:language/text()'),
    'relation':    ('textList', 'rdf:RDF/ow:Publication/dc:relation/text()'),
    'coverage':    ('textList', 'rdf:RDF/ow:Publication/dc:coverage/text()'),
    'rights':      ('textList', 'rdf:RDF/ow:Publication/dc:rights/text()')
    },namespaces={
                  'rdf': NSRDF,
                  'ow': NSOW,
                  'dc': NS_DC
    }
    )
def rdf_writer(element, metadata):
    e_rdf = SubElement(element, nsrdf('RDF'),
                       nsmap={'rdf':NSRDF, 'ow':NSOW, 'xsi':NS_XSI})
    e_rdf.set('{%s}schemaLocation' % NS_XSI,
             '%s http://www.openarchives.org/OAI/2.0/rdf.xsd' % RDF_SCHEMA)
    rdf_pub = SubElement(e_rdf, nsow('Publication'))
    map = metadata.getMap()
    for ident in map.get('identifier', []):
        if ident.startswith('http://'):
            rdf_pub.set('{%s}about' % NSRDF, '%s' % (ident))
    for name in [
        'title', 'creator', 'subject', 'description', 'publisher',
        'contributor', 'date', 'type', 'format', 'identifier',
        'source', 'language', 'relation', 'coverage', 'rights']:
        for value in map.get(name, []):
            e = SubElement(rdf_pub, nsdc(name))
            e.text = value

def nsrdf(name):
    return '{%s}%s' % (NSRDF, name)

def nsow(name):
    return '{%s}%s' % (NSOW, name)
