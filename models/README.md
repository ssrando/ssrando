# Model pack guide
This is a complete guide on how to use and create custom model packs.
If anything is unclear or missing, please contact me on discord (Muzu#8192).

## How to use model packs
- In the root randomizer folder, there should be a folder called `models`, if not, you can create it, but make sure you name it correctly as it is caps-sensitive.
- To install a premade model pack, put the unzipped folder into the `models` folder. Make sure that the folder you put in the `models` folder contains a `Player`, `Loftwing`, etc. folder(s) and not another folder of the same name from the extraction process or it will not work. If you end up with multiple model packs with the same name for any reason, feel free to rename the folder, it'll only affect how it shows up on the UI.
- Once the model pack is installed, open the randomizer program and navigate to the `Cosmetics` tab. In here you will find a dropdown box for the `Type` and the `Pack`. Each type represents a model(s) that can be replaced by a model(s) from a model pack and each pack listed represents a model pack that contains a model of the type currently selected- select a type and a model pack you want to use for that type. This will patch the model from that pack into the generated seed. You can mix and match model packs for the different types available (e.g. a player model from model pack 1 and a loftwing model from model pack 2 etc).
- If the model pack supports masking, selecting a pack will display a list of color groups below. Changing these colors will change the textures in game to match. If the model pack provides preview files, you will be able to see a preview of the model on the right and it'll update as you select colors. If the color displays as `Default`, the color from the original texture will be used for that part- clicking the `Reset` or `Reset All Colors` buttons will restore colors to `Default`. The `Random` and `Randomize All Colors` buttons will randomize individual color groups or all color groups at once respectively.
- The `Tunic Swap` option will use the secondary player model if provided. On the default Link pack, it'll use Link's pyjama model from the beginning of the vanilla game. Some model packs may not support tunic swap, in these cases, the option will be grayed out.

## How to create model packs
In order to create a model pack, there are a few files that must be provided in a set file structure. The file structure is as follows:

- Root model pack folder
    - Model type folders
        - The model arc (for the `Player` type, `Alink.arc` is required and for the `Loftwing` type, `Bird_Link.arc` is required)
        - The metadata file
        - `Masks` folder
            - All the masks for this model named as `[original texture name]__[color group name]` as a png
        - `Preview` folder
            - `Preview` as a png that has the image that will show up as the preview 
            - All the preview masks named as `Preview__[color group name]` as a png
        - `AdditionalArcs` folder (in the `Player` folder only)

### Root model pack folder
This will contain everything in the model pack and the name of this folder will be the name of the model pack as it shows up on the UI. This can be anything except for `Default` as this will conflict with the default Link model pack- if the name `Default` is used, it will be ignored. Please try to avoid using the same name as other released model packs to minimise conflicts as any players that want to install both will have to rename one of them.

### Model type folders
These folders will contain all the files for specific model types. Currently, the only model types that are supported are `Player` for the player model and `Loftwing` for the loftwing model. More types may be added in the future, but for now, at least one of these folders must be present in a model pack. A model pack can contain one or both, if it only contains one, it'll only show up in the `Pack` dropdown when the supported type is selected (i.e. a model pack that only contains `Player` data will only show up in the `Pack` dropdown when `Player` is selected in the `Type` dropdown).

### The model arc
The required model arcs are as follows:
- In a `Player` folder, `Alink.arc`
- In a `Loftwing` folder, `Bird_Link.arc`

If the required arc is not supplied, the pack won't show up in the program. The supplied arc should contain any custom models and/or textures. For more info on how to create these, check out the channels in the Modding category in the SSR discord (https://discord.gg/evpNKkaaw6).

### The metadata file
Must be a JSON file named `metadata`. A bare minimum model pack will function without a metadata file, however one is required if you want to support texture masking or any of the other features detailed below.

The following is a sample metadata file:
```json
{
    "Colors":
    {
        "Hair": "Default",
        "Skin": "Default",
        "Shirt": "Default",
        "Pants": "Default"
    },
    "AllowTunicSwap": "False",
    "ModelAuthorName": "Muzu",
    "ModelAuthorComment": "Sample metadata file"
}
```
- In the `Colors` section, the color groups should be listed in the order you want them to show up on the UI. It is recommended to set the color to `Default` as resetting the color will do this anyway. NOTE: The color group names MUST match the color group names you use to name the texture mask images (more on that later). Omitting this section will cause the color groups to not show up on the UI and will therefore not allow any color groups to be edited.
- Setting `AllowTunicSwap` to `False` will gray out the `Tunic Swap` option on the UI. It is recommended to set `AllowTunicSwap` to `False` if your model pack doesn't have a different model replacing the pyjama Link models. This option is true by default and omitting this section will allow leave the option un-grayed out on the UI.
- If either or both of the `ModelAuthorName` or `ModelAuthorComment` sections are filled out, there will be a section on the rando UI above the color groups that displays any text set here. Put your name in the `ModelAuthorName` section. The `ModelAuthorComment` section is primarily intended to detail what is in the pack or anything else users should know. If either or both of these are omitted, the respective sections won't show up on the UI.

### Masks folder
This folder must be called `Masks`. This folder will contain all the texture masks needed for texture recoloring. Important notes for masks:

- The name of each mask must be as follows: `[original texture name]__[color group name]`.
    - It must be a double underscore between the original texture name and the color group name (as the original texture name may contain a variable number of single underscores).
    - The original texture name is the name of the texture in the arc that the mask is for, for example `pl_upbody` or `BirdLink_Feather`.
    - The color group name is the name of the color group as it is defined in the metadata folder and shows up in the UI.
- The mask must be a PNG.
- The mask must have the same dimensions as the original texture that it is a mask for.
- The mask must contain only black and white pixels.
    - The parts of the texture that should be recolored by this mask should be represented by black pixels (`0x000000`).
    - Every other pixel in the image must be white (`0xFFFFFF`).
- A color group may span over multiple textures (for example, Link's skin is on `al_hand` and `al_face`), in these cases, multiple masks will be required with the same color group name after the double underscore (e.g. `al_hand__Skin` and `al_face__Skin`). When the color for that group is set, all textures with masks in tht group will be modified.
    - No two color groups intended to be edited separately can have the same name.
- It is recommended to have a bit of overlap in masks for groups that fade into each other on a texture to prevent artifacting on the edges of the groups on the final texture.

### Preview folder
This folder must be called `Preview`. This folder must contain a PNG named `Preview` which will be the image that shows up as the preview on the UI. This folder will also contain any masks for the preview image that will recolor the preview image to give a representation of how the model will look in game with that color group applied. Important notes for the preview image and masks:

- The larger the preview image, the longer it'll take to update the preview on the UI- as a result, it is recommended to stay within a range of around 700-1000px by 400-500px. The smaller the image the quicker it'll update, but make sure the preview is still of good quality.
    - It is recommended to follow the standard format for previews that the Default model pack does, i.e. a front and back preview for the player model (and tunic swapped Link if your pack includes it) lined up side by side, and a side on and top down view of the loftwing side by side. Tutorials for how to best create these preview images can be found in `#modding-general` in the SSR discord (https://discord.gg/evpNKkaaw6).
- The name of each mask must be as follows: `Preview__[color group name]`.
    - It must be a double underscore between the original texture name and the color group name (for consistency with texture masks).
    - The color group name is the name of the color group as it is defined in the metadata folder and shows up in the UI.
- The mask must be a PNG.
- The mask must have the same dimensions as the preview image.
- The mask must contain only black and white pixels.
    - The parts of the texture that should be recolored by this mask should be represented by black pixels (`0x000000`).
    - Every other pixel in the image must be white (`0xFFFFFF`).
- It is recommended to have a bit of overlap in masks for groups that fade into each other on a texture to prevent artifacting on the edges of the groups on the final texture.

### Additional arcs folder
This folder must be called `AdditionalArcs`. For now, this folder will only be recognised if it is in a `Player` folder. Any additional arcs that should be patched in alongside the player model can be placed in here. This is primarily intended for item models but any arc (aside from `Alink.arc` and `Bird_Link.arc`) will work in here, meaning it essentially acts as `arc-replacements` but for specific model packs. The reason item models are currently tied to the player type is because bombs and arrows are part of `Alink.arc` and cannot currently be seperated out (this will hopefully come in future updates).

## Important notes
- Any arcs placed in the `AdditionalArcs` folder, as well as `Alink.arc` from the player model pack and `Bird_Link.arc` from the loftwing model pack, will overwrite anything placed in the `arc-replacements` folder. This feature is meant to start replacing `arc-replacements` and as a result, you will **no longer be able to use `arc-repacements` for custom player or loftwing models and/or textures**. Instead these will have to be in model packs.
- It is possible to skip a lot of the steps in making a model pack if you just want to make something quick for yourself. You can just put a folder in the `models` folder with a name, within that add a `Player` and/or `Loftwing` folder as needed, and within those put your `Alink.arc` or `Bird_Link.arc` file. Any other arcs can still be put in `arc-replacements` so long as there aren't arcs with the same name in the `AdditionalArcs` folder of the currently used `Player` model pack.
