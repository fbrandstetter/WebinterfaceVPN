# WebinterfaceVPN
This is a webinterface built using Python / Flask which allows you to invoke OpenVPN certificates and change a proxy file on all servers. This webinterface utilizes SSH connections in order to communicate with the servers in question and to run commands on them.

## Requirements

WebinterfaceVPN is built using Python and thus requires a few additional packages which aren't served by Python directly. In this case, we assume that you have `pip` installed on your system, as we'll use it for the installation of the packages.

    pip install cherrypy
