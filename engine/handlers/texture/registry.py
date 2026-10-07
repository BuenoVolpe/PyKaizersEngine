from pathlib import Path
#-------------------------------------#
from engine.configs import configs
from engine.utils.log import printlog
#-------------------------------------#
from engine.handlers.texture.texture_data import TextureData
from engine.resource_string.resource_reference import ResourceReference
#=====================================#
class TextureRegistry:
    #=====================================#
    def __init__(self, atlas:object, resource_manager:object):
        #-------------------------------------#
        self.atlas = atlas
        self.resource_manager = resource_manager
    #=====================================#
    def register(self, resource: str) -> TextureData:
        #-------------------------------------#
        reference:ResourceReference = self.resource_manager.parse(resource)
        #-------------------------------------#
        if self.atlas.exists(reference.string):
            return self.atlas.get(reference.string)
        #-------------------------------------#
        path = self._get_path(reference)
        if path is None: return
        #=====================================#
        json_path = path.with_suffix(".json")
        if not json_path.exists():
            json_path = None
        #=====================================#
        texture = TextureData(
            resource=reference.string,
            path=path,
            json_path=json_path,
            image=None,
            initial_image=None,
            parameters=reference.parameters.copy()
        )
        #-------------------------------------#
        self.atlas.add(texture)
        #-------------------------------------#
        return texture
    #=====================================#
    def _get_path(self, reference):
        #-------------------------------------#
        path = (
            reference.path.replace(".", "/")
            + f".{configs.engine.extensions.texture}"
        )
        #-------------------------------------#
        if reference.namespace == configs.engine.acronym:
            #-------------------------------------#
            return Path(
                configs.paths.engine.texture + path
            )
        #-------------------------------------#
        if reference.namespace == configs.game.acronym:
            #-------------------------------------#
            return Path(
                configs.paths.game.texture + path
            )
        #-------------------------------------#
        printlog.error(f"Unknown texture namespace: {reference.namespace}")
        return None
