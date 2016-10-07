#/bin/python

# Required packages
import cherrypy, random, string, os
import jinja2

def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context) + "\n"

# Class holding all URLs and functions
class Webinterface(object):

    # Home
    @cherrypy.expose
    def index(self):
        return render('files/head.html', "") + render("files/index.html", "") + render("files/footer.html", "")

    # Login
    @cherrypy.expose
    def login(self):
        return 'test'

if __name__ == '__main__':
    # Set the root directory dynamically
    root = os.path.dirname(os.path.abspath(__file__))
    # Listen on 0.0.0.0
    cherrypy.server.socket_host = '0.0.0.0'
    # Various configs to serve static files
    conf = {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': root,
            'tools.staticdir.index': 'index.html'
        }
    }
    # Start the server
    cherrypy.quickstart(Webinterface(), '/', conf)
