# Blender Datablock Translator

A blender addon/plugin that helps to translate datablock names to English.

It can be useful for cases like:

* Export blender data into some format that don't support asian characters.
* Make datablock names visible even when **International Fonts** setting is switched off.

## Installation

1. Download `translate_datablock_names.py`
2. File Menu -> User Preferences
3. Go to Addons tab
4. Click Install from File... Button at the buttom
5. Select the `translate_datablock_names.py` script you've just download
6. Activate `Object: Translate Datablock Names` by checking the checkbox

## How does it work?

It will go through your blender data, looking for any name that contains special character, and translate them into English.
You can choose which datablock type should be translated (Object/Material/Animation/Armature), and keep the other datablocks untouched.

[Microsoft Translator API](http://msdn.microsoft.com/en-us/library/dd576287.aspx) is used for translations.

## Can I choose source/target language?

You cannot do it right now. But this feature will be added very soon.

## Supported Blender Version

It is written and tested on Blender 2.69.

## Need More Fancy Features?

Feel free to create feature-labeled issues :)
