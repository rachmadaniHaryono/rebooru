import os

from yapsy.PluginManager import PluginManager


def parse_url(url):
    plugins_folder = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'plugins')
    manager = PluginManager()
    manager.setPluginPlaces([plugins_folder])
    manager.collectPlugins()
    plugins =  [
        x for x in manager.getAllPlugins()
        if hasattr(x.plugin_object, 'parse_url')
    ]
    for plugin in plugins:
        for item in plugin.plugin_object.parse_url(url):
            yield item
