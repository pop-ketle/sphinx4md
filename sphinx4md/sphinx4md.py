import os
import sys
import json
import datetime
from pathlib import Path
from distutils import extension

from . import extentions

from sphinx import __display_version__, package_dir
from sphinx.cmd import quickstart
from sphinx.cmd.quickstart import ask_user, generate, do_prompt, nonempty, boolean, is_path, allow_empty
from sphinx.util.console import bold, color_terminal, colorize, nocolor, red  # type: ignore
from sphinx.util.template import SphinxRenderer


DATE = datetime.date.today()
CURRENT_PATH = Path(os.getcwd())
SETTING_FILE = CURRENT_PATH / 'docs/sphinx4md_setting.json'
CONFIG_FILE  = CURRENT_PATH / 'docs/conf.py'

PRESET_EXTENTIONS = [
    extentions.sphinx_commonmark_extension,
    extentions.nbsphinx_extension,
    extentions.sphinx_blockdiag_extension,
    extentions.sphinx_fontawesome_extension,
    extentions.sphinx_sphinx_rtd_theme_extension,
    extentions.sphinx_autobuild_extension,
]


def wrap_ask_user(d):
    """Ask the user for quickstart values missing from *d*.
    
    Values are:
    * sep:       separate source and build dirs (bool)
    * path:      root path
    * project:   project name
    * author:    author names
    * version:   version of project
    * release:   release of project
    * extensions:  extensions to use (list)
    * makefile:  make Makefile
    * batchfile: make command file
    """
    print('Please enter values for the following settings.')
    print('(just press Enter to accept a default value, if one is given in brackets).')

    if 'sep' not in d:
        print()
        print(bold('You have two options for placing the build directory for Sphinx output.\n'
                'Either, you use a directory "_build" within the root path, or you separate\n'
                '"source" and "build" directories within the root path.'))
        d['sep'] = do_prompt('Separate source and build directories (y/n)', 'y', boolean)

    if 'path' not in d:
        print()
        print(bold('Enter the root path for documentation.'))
        d['path'] = do_prompt('Root path for the documentation', '.', is_path)

    if 'project' not in d:
        print()
        print(bold('The project name will occur in several places in the built documentation.'))
        d['project'] = do_prompt('Project name')
    if 'author' not in d:
        d['author'] = do_prompt('Author name(s)')

    if 'version' not in d:
        print()
        d['version'] = do_prompt('Project version', '', allow_empty)
    if 'release' not in d:
        d['release'] = do_prompt('Project release', d['version'], allow_empty)

    if 'extensions' not in d:
        extensions = {}
        print()
        print(bold('Select the extension you want to use'))
        for ext in PRESET_EXTENTIONS:
            extensions[ext.extension] = do_prompt(f'[{ext.extension}] {ext.usage} (y/n)', 'y', boolean)
        d['extensions'] = extensions

    if 'makefile' not in d:
        print()
        print(bold('A Makefile and a Windows command file can be generated for you so that you\n'
                'only have to run e.g. `make html\' instead of invoking sphinx-build\n'
                'directly.'))
        d['makefile'] = do_prompt('Create Makefile? (y/n)', 'y', boolean)

    if 'batchfile' not in d:
        d['batchfile'] = do_prompt('Create Windows command file? (y/n)', 'y', boolean)

    return d


class QuickstartRenderer(SphinxRenderer):
    def __init__(self, templatedir):
        self.templatedir = templatedir or ''
        super().__init__()

    def _has_custom_template(self, template_name):
        """Check if custom template file exists.
        Note: Please don't use this function from extensions.
            It will be removed in the future without deprecation period.
        """
        template = os.path.join(self.templatedir, os.path.basename(template_name))
        if self.templatedir and os.path.exists(template):
            return True
        else:
            return False

    def render(self, template_name, context):
        if self._has_custom_template(template_name):
            custom_template = os.path.join(self.templatedir, os.path.basename(template_name))
            return self.render_from_file(custom_template, context)
        else:
            return super().render(template_name, context)

def wrap_generate(d, conf_file, overwrite=True):
    """Generate project based on values in *d*."""
    template = QuickstartRenderer(templatedir=None)

    # d['master'] = 'index'
    d['suffix'] = ['.md']
    d['root_doc'] = 'index'
    d['mastertoctree'] = ''
    d['mastertocmaxdepth'] = 2
    d['copyright'] = f'{DATE}@{d["author"]}'

    os.makedirs(d['path'], exist_ok=True)

    src_dir = Path(d['path']) / 'source' if d['sep'] else d['path']
    os.makedirs(src_dir, exist_ok=True)

    if d['sep']:
        build_dir = Path(d['path']) / 'build'
        d['exclude_patterns'] = ''
    else:
        build_dir = Path(src_dir) / '_build'
        exclude_patterns = map(repr, [
            '_build',
            'Thumbs.db', '.DS_Store',
        ])
        d['exclude_patterns'] = ', '.join(exclude_patterns)
    os.makedirs(build_dir, exist_ok=True)
    os.makedirs(Path(src_dir) / '_templates', exist_ok=True)
    os.makedirs(Path(src_dir) / '_static', exist_ok=True)

    conf_path = os.path.join(package_dir, 'templates', 'quickstart', 'conf.py_t')
    with open(conf_path) as f:
        conf_text = f.read()

    with open(Path(src_dir) / 'conf.py', 'wt', encoding='utf-8') as f:
        f.write(template.render_string(conf_text, d))
    
    # masterfile = Path(src_dir) / d['master']
    # if template._has_custom_template('quickstart/master_doc.rst_t'):
    #     msg = ('A custom template `master_doc.rst_t` found. It has been renamed to '
    #         '`root_doc.rst_t`.  Please rename it on your project too.')
    #     print(colorize('red', msg))  # RemovedInSphinx60Warning
    #     with open(masterfile, 'wt', encoding='utf-8') as f:
    #         f.write(template.render('quickstart/master_doc.rst_t', d))
    # else:
    #     with open(masterfile, 'wt', encoding='utf-8') as f:
    #         f.write(template.render('quickstart/root_doc.rst_t', d))

    if d.get('make_mode') is True:
        makefile_template = 'quickstart/Makefile.new_t'
        batchfile_template = 'quickstart/make.bat.new_t'
    else:
        makefile_template = 'quickstart/Makefile_t'
        batchfile_template = 'quickstart/make.bat_t'

    if d['makefile']:
        d['rsrcdir'] = 'source' if d['sep'] else '.'
        d['rbuilddir'] = 'build' if d['sep'] else '_build'
        # use binary mode, to avoid writing \r\n on Windows
        with open(os.path.join(d['path'], 'Makefile'), 'wt', encoding='utf-8', newline='\n') as f:
            f.write(template.render_string(makefile_template, d))

    if d['batchfile']:
        d['rsrcdir'] = 'source' if d['sep'] else '.'
        d['rbuilddir'] = 'build' if d['sep'] else '_build'
        with open(os.path.join(d['path'], 'make.bat'), 'wt', encoding='utf-8', newline='\r\n') as f:
            f.write(template.render(batchfile_template, d))

    if d['makefile'] or d['batchfile']:
        print('Use the Makefile to build the docs, like so:   make builder')
    else:
        print(f'Use the sphinx-build command to build the docs, like so:\n'
                '   sphinx-build -b builder {src_dir} {build_dir}')
    print('where "builder" is one of the supported builders, e.g. html, latex or linkcheck.')
    print()




def main():
    print(bold(f'Welcome to the Sphinx4md. Sphinx version:{__display_version__}'))

    # make doc directory
    os.makedirs(CURRENT_PATH / 'docs', exist_ok=True)

    ####################
    # make dict
    ####################

    d = {} # all settings in this dict

    if os.path.isfile(SETTING_FILE):
        flag = do_prompt(bold('Do you want to use an existing setting file?'), 'y', boolean)
        if flag: # load setting file
            d.update(json.load(open(SETTING_FILE)))
        else:
            d = wrap_ask_user(d)
    else:
        d = wrap_ask_user(d)

    # save setting file
    with open(SETTING_FILE, 'w') as f:
        json.dump(d, f, indent=2)

    ####################
    # make conf.py
    ####################
    
    wrap_generate(d, CONFIG_FILE, overwrite=True)

    src_dir = Path(d['path']) / 'source' if d['sep'] else d['path']
    conf_path = Path(src_dir) / 'conf.py'

    ####################
    # install extension
    ####################

    with open(conf_path, 'a+') as f:
        f.write('\n')
        for ext in PRESET_EXTENTIONS:
            if d['extensions'][ext.extension]:
                f.write(ext.text)


    if d['makefile']:
        make_path = Path(d['path']) / 'Makefile'
        with open(make_path, 'a+') as f:
            for ext in PRESET_EXTENTIONS:
                if d['extensions'][ext.extension]:
                    f.write(ext.text)
                    

if __name__ == '__main__':
    main()