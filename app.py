#/bin/python

# Required packages
import cherrypy, random, string, os, jinja2, sqlite3, hashlib

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
        data = {
            "page": "home"
        }
        if not cherrypy.session.get("username"):
            raise cherrypy.HTTPRedirect("/login/")
        else:
            return render('files/head.html', "") + render("files/navbar.html", data) + render("files/index.html", "") + render("files/footer.html", "")

    # Login
    @cherrypy.expose
    def login(self):
        data = {
            "page": "login"
        }
        return render('files/head.html', "") + render("files/navbar.html", data) + render("files/login.html", "") + render("files/footer.html", "")

    # Servers
    @cherrypy.expose
    def servers(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.execute("SELECT * FROM servers")
        result = cursor.fetchall()

        data = {
            "page": "servers",
            "servers": result
        }
        return render('files/head.html', "") + render("files/navbar.html", data) + render("files/servers.html", data) + render("files/footer.html", "")
    # New server
    @cherrypy.expose
    def new_server(self):
        data = {
            "page": "new-server",
        }
        return render('files/head.html', "") + render("files/navbar.html", data) + render("files/new-server.html", data) + render("files/footer.html", "")

class API(object):

    # Login backend
    @cherrypy.expose
    def login(self, email, password):
        hash_object = hashlib.sha256(password)
        hex_dig = hash_object.hexdigest()
        conn = sqlite3.connect('data.db')

        cursor = conn.execute("SELECT COUNT(*) from users WHERE email = '" + email + "' AND password = '" + hex_dig + "'")
        if(cursor.fetchone()[0] == 1):
            cherrypy.session['username'] = email
            raise cherrypy.HTTPRedirect("/")
        else:
            raise cherrypy.HTTPRedirect("/error/")
        conn.close()

    # Signout backend
    @cherrypy.expose
    def signout(self):
        cherrypy.session['username'] = ""
        raise cherrypy.HTTPRedirect("/login/")


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
            'tools.staticdir.index': 'index.html',
            'tools.sessions.on':  True,
            'tools.sessions.storage_type': 'File',
            'tools.sessions.storage_path': "sessions",
            'tools.sessions.timeout': 60
        }
    }
    # Start the server
    cherrypy.tree.mount(Webinterface(), '/', conf)
    cherrypy.tree.mount(API(), '/api', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()
