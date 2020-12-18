# Changelog

Every noteable change is logged here.

## v3.2.0

### Feature

* add `run` method to reduce amount of code (3fb3ebfd3111)
* introduce message type (4640b2970c1c)
* shorten dissertation to diss (afe574bd4237)

### Documentation

* clarify documentation (8a665625b0e9)
* remove pages hierarchy level (13f7dab912f5)

## v3.1.6

## v3.1.5

## v3.1.4

## v3.1.3

## v3.1.2

## v3.1.1

## v3.1.0

### Feature

* add method to select findings by page number (e1ea11f299c9)

### Fix

* do not load invalid file names (e55663ca7c2d)
* remove useless default value (ffae7be677d8)

## v3.0.0

### Feature

* change to jinja2 template engine (6b844e70d227)
* add method to dump and load findings by page number (7e82c6ca4a05)

## v2.1.4

## v2.1.3

## v2.1.2

## v2.1.1

### Feature

* add assertion to ensure correct data type (4f88444f8bdb)

## v2.1.0

### Feature

* add method to create linter from multiple modules (fc3a5d760afb)

### Fix

* ensure to group zero pages correctly (0018015223b2)

## v2.0.0

## v1.3.1

## v1.3.0

### Feature

* add debug information about changing finding status (8f41376ba798)
* add method to hash finding to public interface (8f7888299f3e)
* add method to filter ranged findings (8083a8a7e408)

### Fix

* rename internal variable (02c9fdee27be)

## v1.2.1

## v1.2.0

### Feature

* extend ranged location with chars as minimal unit (218af1b17628)

## v1.1.0

### Feature

* add method to run registered checkers (d7a965e9e7fb)
* load checkers with loading linter (bcde4e8b2df0)
* add filter_solutions to skip non selected linter by doc type (e3df4d4d350e)
* add decorators to control which checker is selected (9d55f27fb629)
* add data structure to describe document type (3050da50569f)
* add method to replace editor dependent strings (e2ca188e0bc1)

### Documentation

* add general module documentation (414a5bc3742d)

## v1.0.5

## v1.0.4

## v1.0.3

## v1.0.2

## v1.0.1

## v1.0.0

### Feature

* add method to answer list of questions (8892f8e1ddf8)
* add option to disable user filter (36ea8ebc2644)
* write to yaml, not .lin files (6f9557d85576)
* add method to group finding by message id (dbe201e67ba1)
* add question enabler pattern (bc99b64c1a1d)
* add question parser (a79b2fa3de81)
* introduce short solution pattern (9d597a824162)

### Fix

* handle loading no files correctly (daa32bfd23a9)

### Documentation

* fix web solution doc pattern (c9b0071d4aae)

## v0.10.5

## v0.10.4

## v0.10.3

### Feature

* use multiprocessing to improve loading speed (482c27c193a9)
* add level to define importance of an finding (b391e3743a0f)
* extend interface to define msgid as int (b80fa932aded)

## v0.10.2

## v0.10.1

### Feature

* ensure that template is replaced before dumping finding (f9cc35bef71c)

## v0.10.0

### Feature

* add option to skip checker by id (dd33e47f8494)
* add parameter to load selective findings (0a9aad041116)
* extend finding selector with multiple ids (52831fd7eae9)
* add parameter to skip or select evaluation (fbf790efbf80)
* add method to select findings (d25dd9030191)

## v0.9.3

### Feature

* add shortcut to RangedLocation (f1df0074a1f0)

### Fix

* ensure to handle findings without shortcut correctly (02a3ce9af0cd)

## v0.9.2

### Feature

* clarify documentation of RangedLocation syntax (5ff1bd02357d)
* enable use location before start as summary page (46dbfc42f7c2)

## v0.9.1

### Feature

* create unique hash number on finding creation (de2bbab84ac0)
* add method filter sentences findings (d1bd159debff)

## v0.9.0

### Feature

* add method to update solution status (d1b7b437ffbb)
* add method to update finding status (df11f8440f89)
* add method to make finding number unique (f2623ec14b05)
* add method to collect findings from path (2a7df32eb523)
* add parameter to write_result to control linter result writing (90fb67176f69)
* add method to create sentence location (82b5b8c75ccd)

## v0.8.17

## v0.8.15

### Feature

* add groupby-page method (163bcac5dd6e)

## v0.8.0

### Feature

* add methods to parse linter and solution automatically (0a94d1873a25)
* add BoundingLocation to describe rectangle bounding (5a95f9af171f)
* ease using interface (111a114cda2e)

### Fix

* define error message on assertion error (e557dcde89c0)

### Documentation

* extend module documentation (82259e23369a)

## v0.7.2

## v0.7.1

### Feature

* add methods to filter Findings (6d74ed97d06f)

## v0.7.0

### Feature

* use default value confident instead of new method (6072a29c4267)
* add method to create linter from solution (888dd7009879)
* add method to create linter from_file (bea7fe7e98fe)
* extend public API (50bca3b16a6b)
* set message active as default state (7fb46902043b)
* specify dump and write of linter result (c246ebd21683)

### Documentation

* extend interface documentation (bce05effd646)

## v0.6.1

## v0.6.0

### Feature

* add RangedLocation to describe ranged locations (d36e1962f199)
* add internal documentation link (70b5859467e2)
* add template mechanism to create different linter solution (7d71ea7d96cc)

### Documentation

* fix and extend interface documentation (4d061669eaec)
* use general documentation structure (09cd53cac03a)
* fix documentation (9e24c1b65f0f)

## v0.5.4

## v0.5.1

### Documentation

* Happy New Year! (412dec0eb867)

## v0.5.0

### Feature

* add method to group findings by page location (45f55a1af656)
* add `Findings` to replace list of Finding (f8b92f69677f)

## v0.4.8

### Feature

* add method to determine oneline location (65b3ce9b577c)

## v0.4.7

## v0.4.0

### Feature

* add method to create solver from dict (e873a3fa8b25)
* add method to dump and load linter results (d0f8a388cb94)

### Documentation

* extend todo list (326dec513bee)

## v0.3.0

### Feature

* add method to create `Solver` from list of `Solution` (d006e4694226)
* add method to create Location from via given parameter (ea5ca06bd656)
* make Location hash able (0688840f810f)

### Documentation

* add todo list to archive further library improvements (f63dc65cc3b2)

## v0.2.5

## v0.2.2

### Fix

* overwrite linter result files instead of returning error (06aa9b4b0515)

## v0.2.1

### Feature

* add method to extract linter result without writing to file space (335a76315889)
* add option to write multiple findings only once (3835ba11279e)

## v0.2.0

### Feature

* add public API (4036da07413a)

## v0.1.1

## v0.1.0

### Feature

* make linter thread safe (1514ab64730e)
* add checker, finding and linter (c5fb8ef3a7c7)
* add active and confidence flag to control presentation mode (5c376f6f5454)
* add Location to define error location in document (2cc528e841da)
* add message definition and method to parse msgid's (ec75f61e5a97)
* add method to load and save MessageStatus (c70ffb99240b)

## v0.0.0 Initial release
