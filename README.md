nslocapysation
============

Replacing the good ol' genstrings-command with an actually useful python-module.

This module checks for usages of 'NSLocalizedString(@"key", @"comment")' (and possible custom macros, I use NSL(@"key"), for example) in your project's code, reads your Localizable.strings files and checks for missing translations.

Per default, it runs in dry-mode and only logs warnings for missing translations.
If you set the update-flag (-u), it writes the keys ('"key" = ', without translation and the semicolon) of missing translations to the strings-files,
so you get a compile-error when trying to build in Xcode. This will prevent you from releasing an App with missing translations.

It does not overwrite your existing translations. Instead, it orders them by word-count and by alphabet, so it merges
cleanly. You can run it multiple times without running into problems (apart from a backup-file of each .strings file generated in each -u run :)). As said, it creates a backup of each .strings-file that it rewrites (which should be obsolete, since everyone is using version-control for their Xcode-projects, right? :D)

Usage
---
```sh
$ python run.py [-ud] [-p project_source_root_path] [-i language_codes_to_ignore] [-c custom_macros]  
```
- -u Update-flag. If set, the keys of the missing translations will be written to all .strings-files that are not ignored
- -d Debug-flag. Enables debug logging. Beware, this will be quite verbose.
- -p The path to your project's source-root-folder.
- -i Language-codes that should be ignored. For example, if you use the original english strings as keys,
you might want to ignore 'en'.
- -c Custom macros that you are using in your source-code. They must contain the word 'key' as a placeholder for where the actual key that will be translated is positioned. (No worries, if there's no 'key' in there, it will raise a ValueError)

Known Issues / Improvement Ideas
---
- A line comment is always associated with the next following translation, not with a whole group.
  Since the translations are sorted by number of words and by alphabet, this can lead to a comment that was
  meant for a whole group being ripped away from the group. Instead, it is then glued to the first translation of the   group. 
- It's not yet possible to ignore folders or files, so one has to be sure to select the correct root.
