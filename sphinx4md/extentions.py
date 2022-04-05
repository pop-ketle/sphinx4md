class Extension(object):
    def __init__(self, extension, usage, text, package):
        self.extension = extension
        self.usage = usage
        self.text = text
        self.package = package


sphinx_fontawesome_extension = Extension(
    extension='ext_fontawesome',
    usage='use font awesome',
    text="""
# ----- sphinx-fontawesome
import sphinx_fontawesome
extensions.append('sphinx_fontawesome')
""",
    package=['sphinx-fontawesome'],
)

sphinx_commonmark_extension = Extension(
    extension='ext_commonmark',
    usage='use CommonMark and AutoStructify',
    text="""
# ----- CommonMark
source_suffix = [source_suffix, '.md']
from recommonmark.parser import CommonMarkParser
source_parsers = {
    '.md': CommonMarkParser,
}
from recommonmark.transform import AutoStructify
github_doc_root = 'https://github.com/rtfd/recommonmark/tree/master/doc/'
def setup(app):
    app.add_config_value('recommonmark_config', {
            'url_resolver': lambda url: github_doc_root + url,
            'auto_toc_tree_section': 'Contents',
            }, True)
    app.add_transform(AutoStructify)
""",
    package=['CommonMark', 'recommonmark'],
)

sphinx_sphinx_rtd_theme_extension = Extension(
    extension='ext_rtd_theme',
    usage='use Read the Doc theme',
    text="""
# ----- Read the Docs Theme
html_theme = "sphinx_rtd_theme"
""",
    package=['sphinx-rtd-theme'],
)

nbsphinx_extension = Extension(
    extension='ext_nbshpinx',
    usage='provides a source parser for *.ipynb files',
    text="""
# ----- Jupyter Notebook nbsphinx
extensions.append('nbsphinx')
exclude_patterns.append('**.ipynb_checkpoints')
""",
    package=['nbsphinx'],
)

sphinx_blockdiag_extension = Extension(
    extension='ext_blockdiag',
    usage='Sphinx extension for embedding blockdiag diagrams',
    text="""
# ----- blockdiag settings
extensions.extend([
    'sphinxcontrib.blockdiag',
    'sphinxcontrib.seqdiag',
    'sphinxcontrib.actdiag',
    'sphinxcontrib.nwdiag',
    'sphinxcontrib.rackdiag',
    'sphinxcontrib.packetdiag',
])
blockdiag_html_image_format = 'SVG'
seqdiag_html_image_format = 'SVG'
actdiag_html_image_format = 'SVG'
nwdiag_html_image_format = 'SVG'
rackiag_html_image_format = 'SVG'
packetdiag_html_image_format = 'SVG'
""",
    package=[
        'sphinxcontrib-actdiag', 'sphinxcontrib-blockdiag',
        'sphinxcontrib-nwdiag', 'sphinxcontrib-seqdiag'
    ]
)

sphinx_autobuild_extension = Extension(
    extension='ext_autobuild',
    usage='Watch a directory and rebuild the documentation',
    text="""
livehtml:
\tsphinx-autobuild -b html {0} $(ALLSPHINXOPTS) $(BUILDDIR)/html
""",
    package=['sphinx-autobuild'],
)