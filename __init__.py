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

        books = self.prepare_books(books)

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

        covers_directory = output_directory + "/covers"
        if not os.path.exists(output_directory + "/covers"):
            os.makedirs(covers_directory)

        # Templates
        list_of_files = self.load_resources(["list_of_files.txt"])['list_of_files.txt']

        resources = self.load_resources(list_of_files.split("\n"))

        for file_name in resources.keys():
            file_name_output = os.path.basename(file_name)
            file = open(output_directory + "/" + file_name_output, "wb")
            
            if not file_name_output.endswith(".png"):
                output = pystache.render(resources[file_name], {'books': books})
            else:
                output = resources[file_name]

            file.write(output)
            file.close()

        # Generate covers
        for book in books:
            cover_path = book['cover']

            if cover_path is not None:
                file_name_output = book['uuid'] + "." + self.file_extension(cover_path)
                shutil.copyfile(cover_path, covers_directory + "/" + file_name_output)

        self.notification = notification

    def file_extension(self, file_path):
        filename, file_extension = os.path.splitext(file_path)
        return file_extension.lstrip(".")

    def prepare_books(self, books):
        index = 0
        for book in books:
            book['author_display'] = " ".join(book['authors'])

            # this uuid is to as a css selector and should not start with
            # a number
            book['uuid-no-dashes'] = 'a'+book['uuid'].replace("-", "")

            if book['cover'] is not None:
                book['cover-file'] = book['uuid'] + "." + self.file_extension(book['cover'])
            else:
                book['cover-file'] = ""

            book['z-index'] = index
            book['left'] = index*80
            index += 1

        return books[0:5]
