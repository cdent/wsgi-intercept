
from setuptools import setup, find_packages
import compiler, pydoc
from compiler import visitor

class ModuleVisitor(object):
    def __init__(self):
        self.mod_doc = None
        self.mod_version = None
    def default(self, node):
        for child in node.getChildNodes():
            self.visit(child)
    def visitModule(self, node):
        self.mod_doc = node.doc
        self.default(node)
    def visitAssign(self, node):
        if self.mod_version:
            return
        asn = node.nodes[0]
        assert asn.name == '__version__', (
            "expected __version__ node: %s" % asn)
        self.mod_version = node.expr.value
        self.default(node)
        
def get_module_meta(modfile):
    ast = compiler.parseFile(modfile)
    modnode = ModuleVisitor()
    visitor.walk(ast, modnode)
    if modnode.mod_doc is None:
        raise RuntimeError(
            "could not parse doc string from %s" % modfile)
    if modnode.mod_version is None:
        raise RuntimeError(
            "could not parse __version__ from %s" % modfile)
    return (modnode.mod_version,) + pydoc.splitdoc(modnode.mod_doc)

version, description, long_description = get_module_meta("./wsgi_intercept/__init__.py")

setup(
    name = 'wsgi_intercept',
    version = version,
    author = 'Titus Brown, Kumar McMillan, Chris Dent',
    author_email = 'cdent@peermore.com',
    description = description,
    url="http://pypi.python.org/pypi/wsgi_intercept",
    long_description = long_description,
    license = 'MIT License',
    packages = find_packages(),
    )
