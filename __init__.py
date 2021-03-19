bl_info = {
    "name": "BlenderLib",
    "author": "Lorenzo Argentieri",
    "version": (1, 0, 0),
    "blender": (2, 92, 0),
    "support": "COMMUNITY",
    "location": "TopBar > BlenderLib",
    "description": "Tools",
    "warning": "",
    "doc_url": "",
    "category": "BlenderLib"#"Development"#
}

mainModulesNames = ['pipelineLib', 'menuLib', 'shaderLib']

import sys
import importlib
import pkgutil


modulesNames = []
for mod in mainModulesNames:
    modulesNames.extend([mod + '.' + name for _, name, _ in pkgutil.iter_modules([mod])])

modulesFullNames = {}
for currentModuleName in modulesNames:
    if 'DEBUG_MODE' in sys.argv:
        modulesFullNames[currentModuleName] = ('{}'.format(currentModuleName))
    else:
        modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))

for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)


def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()

def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()


if __name__ == "__main__":
    register()
