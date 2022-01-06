# DSA5-ProbeMaker

A little tool for The Dark Eye 5th Edition ([Das Schwarze Auge 5](https://ulisses-spiele.de/spielsysteme/dsa5/)) to load .json from [Optolith](https://github.com/elyukai/optolith-client) character generation and easily perform talent probes. For the Meister: It can handle more than one hero/NPC simultaneously!

## Usage

0. Get and install [Python 3](https://www.python.org/).
1. Download/clone repository.
2. Copy `settings_template.py` to `settings.py`.
3. Adjust paths/file names/settings in `settings.py`.
4. Run `python probemaker.py`.
5. Once asked, you can perform a probe by entering the name of a talent (do not use German Umlaute, but ae etc. and replace `&` by `u`). If you want to use a modifier just enter the numerical value separated by a comma, e.g. `Bekehren u Ueberzeugen, -1`. If there is more than one hero loaded, you are first asked to enter the name of the hero you want to probe. You can also probe on attributes by using their abbreviation (e.g. `KK,+1`). If you want to log a hit taken or given, enter `hit_taken`or `hit_given`and enter source and amount.
6. To exit the program, type `feddich`.


### Implemented features
- Talent probes with modifier
- Attribute probes with modifier
- Logging of probes and their results
- Logging of damage taken or given (LP are not handled correctly outside the log so far.)

### Missing features
 No magic.

### Licence
DSA5-Probemaker</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/arnohakk/DSA5-Probemaker" property="cc:attributionName" rel="cc:attributionURL"></a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Text" property="dct:title" rel="dct:type">

### Misc
Beta mode, no warranty!
