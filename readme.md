# Jubeat TSV updater

A brief program to populate [jubeat.tsv](https://github.com/DragonMinded/bemaniutils/blob/223c93874c33deac17d3ff35b3ff41bddeac8891/data/jubeat.tsv) with data from a game's music_info.xml. Potentially useful for adding support for additional versions. I used this for updating [my fork](https://github.com/swestastic/bemaniutils) to support Beyond the Avenue so hopefully someone else can make use of it as well.

Only compatible with Festo, Avenue, and Beyond the Avenue as versions below Festo do not contain the <name_string> tags in music_info.xml

Titles are all presented in katakana; English titles will need to be done manually.
Artist information is not contained in music_info.xml so that will need to be manually populated as well

## Usage

Help menu: ```./jubeat_tsv_updater --help```

Run like: ```./jubeat_tsv_updater --xml /path/to/music_info.xml --tsv /path/to/jubeat.tsv```

If run from a directory already containing music_info.xml and jubeat.tsv then you do not need to specify a path. When finished music_info.tsv and jubeat_new.tsv will be saved to the current directory
