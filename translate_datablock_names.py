bl_info = {
    "name": "Translate Datablock Names",
    "author": "Joshua Zhang",
    "version": (1, 0),
    "blender": (2, 69, 0),
    "location": "Search > (rename)",
    "description": "A blender addon/plugin that helps to translate datablock \
        names to English.",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

import urllib.request
import urllib.parse
import json
import time
import re
import xml.etree.ElementTree as ET
import bpy


class MSTranslator():
    """A Class to communicate with Microsoft Translator API"""

    def __init__(self):
        self.access_token = ""
        self.access_token_expires_at = time.time()

        self.get_access_token()

    def get_access_token(self):
        """Get access token from Azure Marketplace.
        If there's no existed access token, it'll try request a new one.

        Returns: string
        """

        if (
            not bool(self.access_token) or
            time.time() > self.access_token_expires_at
        ):
            self.access_token = self.req_access_token()

        return self.access_token

    def req_access_token(self):
        """Request a new access token from Azure Marketplace

        Returns: string
        """

        url = "https://datamarket.accesscontrol.windows.net/v2/OAuth2-13"
        data = {
            "client_id": "blender-assets-translator",
            "client_secret": "5TITh8SzOtQIefUJ/vKW10yk4/oNbGbgI+GquUdtgHo=",
            "scope": "http://api.microsofttranslator.com",
            "grant_type": "client_credentials"
        }

        data = urllib.parse.urlencode(data)
        data = bytes(data, "utf-8")

        req = urllib.request.Request(url=url, data=data)

        result = urllib.request.urlopen(req).read()
        result = str(result, "utf-8")
        result = json.loads(result)

        self.access_token_expires_at = time.time() + int(result["expires_in"])

        return result["access_token"]

    def translate(self, text, to_lang="en", from_lang=""):
        """Translate text to the target language

        Keyword arguments:
        text -- text to translate
        to_lang -- optional, the target language code
        from_lang -- optional, the source language code

        Returns: string
        """

        url = "http://api.microsofttranslator.com/v2/Http.svc/Translate"

        data = {
            "text": text,
            "to": to_lang,
            "from": from_lang
        }

        data = urllib.parse.urlencode(data)
        url += "?" + data

        req = urllib.request.Request(url=url, method="GET")
        req.add_header("Authorization", "Bearer " + self.get_access_token())

        result = urllib.request.urlopen(req).read()
        result = str(result, "utf-8")
        result = ET.fromstring(result)
        result = result.text

        return result


class TranslateDatablockNames(bpy.types.Operator):
    """Translate Datablock Names"""

    bl_idname = "object.translate_datablock_names"
    bl_label = "Translate Datablock Names"
    bl_options = {'REGISTER', 'UNDO'}

    is_object_to_translate = bpy.props.BoolProperty(
        name='Object',
        default=True,
        description='Translate Object Names')

    is_material_to_translate = bpy.props.BoolProperty(
        name='Material',
        default=True,
        description='Translate Material Names')

    is_animation_to_translate = bpy.props.BoolProperty(
        name='Animation',
        default=True,
        description='Translate Animation Names')

    is_armature_to_translate = bpy.props.BoolProperty(
        name='Armature',
        default=True,
        description='Translate Armature Names')

    is_shapekey_to_translate = bpy.props.BoolProperty(
        name='Shape Key',
        default=True,
        description='Translate Shape Key Names')

    dialog_width = 200

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop(self.properties, 'is_object_to_translate')
        row.prop(self.properties, 'is_material_to_translate')
        row = layout.row()
        row.prop(self.properties, 'is_animation_to_translate')
        row.prop(self.properties, 'is_armature_to_translate')
        row = layout.row()
        row.prop(self.properties, 'is_shapekey_to_translate')

    def execute(self, context):
        translate_datablock_name(
            is_object_to_translate=self.is_object_to_translate,
            is_material_to_translate=self.is_material_to_translate,
            is_animation_to_translate=self.is_animation_to_translate,
            is_armature_to_translate=self.is_armature_to_translate,
            is_shapekey_to_translate=self.is_shapekey_to_translate
        )
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.invoke_props_dialog(self, self.dialog_width)
        return {'RUNNING_MODAL'}


def menu_func(self, context):
    self.layout.operator(TranslateDatablockNames.bl_idname)


def translate_datablock_name(
    is_object_to_translate=False,
    is_material_to_translate=False,
    is_animation_to_translate=False,
    is_armature_to_translate=False,
    is_shapekey_to_translate=False
):
    if is_object_to_translate:
        for obj in bpy.data.objects:
            if has_irregular_char(obj.name):
                obj.name = hyphenize(ms_translator.translate(obj.name))

        for mesh in bpy.data.meshes:
            if has_irregular_char(mesh.name):
                mesh.name = hyphenize(ms_translator.translate(mesh.name))

        for group in bpy.data.groups:
            if has_irregular_char(group.name):
                group.name = hyphenize(ms_translator.translate(group.name))

    if is_material_to_translate:
        for material in bpy.data.materials:
            if has_irregular_char(material.name):
                material.name = hyphenize(
                    ms_translator.translate(material.name)
                )

    if is_animation_to_translate:
        for action in bpy.data.actions:
            if has_irregular_char(action.name):
                action.name = hyphenize(ms_translator.translate(action.name))

    if is_armature_to_translate:
        for armature in bpy.data.armatures:
            if has_irregular_char(armature.name):
                armature.name = hyphenize(
                    ms_translator.translate(armature.name)
                )

            for bone in armature.bones:
                bone.name = hyphenize(
                    ms_translator.translate(bone.name)
                )
				
    if is_shapekey_to_translate:
        for shapekey in bpy.data.shape_keys:
            if has_irregular_char(shapekey.name):
                shapekey.name = hyphenize(
                    ms_translator.translate(shapekey.name)
                )
            for keyblock in shapekey.key_blocks:
                if has_irregular_char(keyblock.name):
                    keyblock.name = hyphenize(
                        ms_translator.translate(keyblock.name)
                    )

def hyphenize(string):
    return '-'.join(string.split())


def has_irregular_char(string):
    match = re.search(r"[^\x00-\x7F]", string)
    if match:
        return True
    else:
        return False


def register():
    global ms_translator
    ms_translator = MSTranslator()
    bpy.utils.register_class(TranslateDatablockNames)
    bpy.types.OUTLINER_MT_search.append(menu_func)


def unregister():
    global ms_translator
    ms_translator = None
    bpy.utils.unregister_class(TranslateDatablockNames)
    bpy.types.OUTLINER_MT_search.remove(menu_func)

if __name__ == "__main__":
    ms_translator = None
    register()
