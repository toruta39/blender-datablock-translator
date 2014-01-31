# Blender Datablock Translator

A blender addon/plugin that helps to translate datablock names to English.

It can be useful for cases like:

* Export blender data into some format that don't support asian characters.
* Make datablock names visible even when **International Fonts** setting is switched off.

## Installation

1. Download <a href="https://raw.github.com/toruta39/blender-datablock-translator/master/translate_datablock_names.py" target="_blank" download="translate_datablock_names.py">translate_datablock_names.py</a>
2. Open preference window by **File Menu -> User Preferences**
3. Go to **Addons** tab
4. Click **Install from File...** at the buttom
5. Select the `translate_datablock_names.py` file you've just downloaded
6. Activate **Object: Translate Datablock Names** by checking the checkbox
7. **Save User Settings** to make sure the addon is loaded automatically next time you start Blender

## How to use it

You can find **Translate Dateblock Names** command in **Spacebar Menu**.
And you can also be found it **Outliner Window -> Search Menu**.

![Search Menu Screenshot](http://i.imgur.com/u5ZzW0Z.png)

In the dialog, choose datablock types that need translation, and click OK.

![Dialog Screenshot](http://i.imgur.com/kTVHaob.png)

The time it takes to translate may differ according to the number of objects and your network condition. (Normally less than 1min)

## How does it work?

Blender Datablock Translator will go through your blender data, looking for any name that contains special character, and translate them into English.
You can choose which datablock type should be translated (Object/Material/Animation/Armature), and keep the other datablocks untouched.

[Microsoft Translator API](http://msdn.microsoft.com/en-us/library/dd576287.aspx) is used for translations.

## Can I choose source/target language?

It's not supported right now. But this feature will be added very soon.

## Supported Blender Version

Blender Datablock Translator is tested on Blender 2.69.

## Need More Fancy Features?

Feel free to create feature issue :)
