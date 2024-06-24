# Random Settings Weighting File Documentation

All options that are randomized in random settings should be included in each of the `rs_weightings/*.yaml` files. The four main weightings are:

- Random (Equal chance for all options under a setting)
- Quick (Randomized settings will favor a quicker run)
- Balanced (Settings will randomize fairly for a middle-of-the-road seed)
- Insanity (Randomized settings will favor a longer, more complicated seed)

RSL weightings are used for Random Settings League races.

Within each file, the randomized options are listed by type (int, singlechoice, bool, multichoice*). **Weights are supplied as relative integers**. The total weighting does not have to add up to a certain number. Examples of existing weightings can be viewed in the weighting files.

## Int

Structure:

```
name: <SETTING NAME AS IN options.yaml>
command: <SETTING COMMAND AS IN options.yaml>
type: int
choices:
    0: <WEIGHT>
    1: <WEIGHT>
    2: <WEIGHT>
    ...
```

The number of choices should range from the min to the max, as defined in `options.yaml`.

## Singlechoice

Structure:

```
name: <SETTING NAME AS IN options.yaml>
command: <SETTING COMMAND AS IN options.yaml>
type: singlechoice
choices:
    <CHOICE 1>: <WEIGHT>
    <CHOICE 2>: <WEIGHT>
    <CHOICE 3>: <WEIGHT>
    ...
```

All choices listed in `options.yaml` should be included in the weighting.

## Bool

```
name: <SETTING NAME AS IN options.yaml>
command: <SETTING COMMAND AS IN options.yaml>
type: bool
checked: <WEIGHT OF TRUE>
unchecked: <WEIGHT OF FALSE>
```

Checked refers to if the box in the UI would be checked, therefore making the value of the option `true`. Unchecked refers to a value of `false`.

## Multichoice*

```
name: <SETTING NAME AS IN options.yaml>
command: <SETTING COMMAND AS IN options.yaml>
type: multichoice
maxpicks: <MAXIMUM NUMBER OF SELECTIONS>
choices:
    - [<CHOICE 1>, <WEIGHT OUT OF 100>]
    - [<CHOICE 2>, <WEIGHT OUT OF 100>]
    - [<CHOICE 3>, <WEIGHT OUT OF 100>]
    ...
```

All choices listed in `options.yaml` should be included. Choices are shuffled and each choice is selected individually by its weighting out of 100, which should be an integer between 0-100. The randomizer will go through each choice until it successfully picks the `maxpicks` defined above or it runs out of options.

# Adding New Options

If you are a developer and you are adding one or more options, you should add the option(s) to all of the weighting files, or add it to `NON_RANDOMIZED_SETTINGS` in `logic/constants.py` if it is an option that is not to be randomized in random settings. If you do not do either, the randomizer will default to using random weighting on the setting (i.e. weighting value of `1` for all choices).

**Cosmetic options are not added to weighting files**. All cosmetic options use random weighting if the `randomize-cosmetics` option is enabled. If you are creating a cosmetic option that should be not randomized, add it to `NON_RANDOMIZED_COSMETICS` in `logic/constants.py`.

A python program that developers can run to automatically add the new option(s) to all weighting files is in development.
