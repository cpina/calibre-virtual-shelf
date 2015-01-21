import os
from calibre.customize import CatalogPlugin
from calibre.customize.conversion import DummyReporter

class VirtualShelfPlugin(CatalogPlugin):
    name                = 'VirtualShelfPlugin'
    description         = 'Generates an HTML like a traditional shelf'
    supported_platforms = ['windows', 'osx', 'linux']
    author              = 'Carles Pina i Estany'
    version             = (0, 0, 1)
    file_types          = set(['html'])
    cli_options         = []
    minimum_calibre_version = (0, 7, 53)

    actual_plugin = 'calibre_plugins.virtual_shelf.ui:virtual_shelf_plugin'

    def run(self, path_to_output, opts, db, notification=DummyReporter()):
        import pystache
        file = open(path_to_output, 'w')

        opts.sort_by="author"

        data = self.search_sort_db(db, opts)

        f = open("/home/carles/virtual.log", "a")

        index_moustache = "templates/index.moustache"
        templates = self.load_resources([index_moustache])
        f.write("here01")

        for entry in data:
            print pystache.render(templates[index_moustache], entry)
            f.write(pystache.render(templates[index_moustache], entry)+"\n")
            break

        self.notification = notification
        #return path_to_output
