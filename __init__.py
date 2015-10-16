import os
import shutil
from calibre.customize import CatalogPlugin
from calibre.customize.conversion import DummyReporter

class VirtualShelfPlugin(CatalogPlugin):
    name                = 'VirtualShelfPlugin'
    description         = 'Generates an HTML like a traditional shelf'
    supported_platforms = ['windows', 'osx', 'linux']
    author              = 'Carles Pina i Estany'
    version             = (0, 0, 2)
    file_types          = set(['html'])
    cli_options         = []
    minimum_calibre_version = (0, 7, 53)

    actual_plugin = 'calibre_plugins.virtual_shelf.ui:virtual_shelf_plugin'

    def run(self, path_to_output, opts, db, notification=DummyReporter()):
        import pystache

        opts.sort_by="author"

        books = self.search_sort_db(db, opts)

        log = open("/home/carles/virtual-shelf.log","w")
        log.write(str(books) + "\n")

        opts_dir = vars(opts)
        if 'output_directory' in opts_dir:
            print "here here 01"
            output_directory = opts_dir['output_directory']
        else:
            print "here here 02"
            output_directory = path_to_output
            output_directory = output_directory.replace(".html", "")

        path_to_output = output_directory + "/index.html"

        print "path_to_output:",path_to_output

        file = open(path_to_output, 'w')
        file.write("See the output in " + output_directory)
        file.write("Calibre natively only supports one catalogue output file")
        file.write("but this plugin needs a few.")
        file.close()

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)


        # Main template
        index_moustache = "templates/index.moustache"
        list_of_files = "list_of_files.txt"

        templates = self.load_resources([index_moustache, list_of_files])

        file = open(output_directory + "/index.html", 'w')
        file.write(pystache.render(templates[index_moustache], {'books': books}))
        file.close()

        # Copy over other files
        list_of_files = templates[list_of_files].split("\n")

        all_files = self.load_resources(list_of_files)

        for file_name in list_of_files:
            if file_name == 'templates/index.moustache' or file_name == "":
                continue

            file_name_output = os.path.basename(file_name)
            file = open(output_directory + "/" + file_name_output, "wb")
            file.write(all_files[file_name])
            file.close()

        self.notification = notification
