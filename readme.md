# XPlainHub Dataset

XPlainHub is a multi-linguistic dataset consisting of 5 popular programming languages, mined from more than 7500 GitHub repositories containing 371483 methods extracted from code from 250090 bug-fixing commits. Most importantly, the dataset includes the buggy, and the fixed version of methods extracted from the bugfixing commit. It also contains some additional information like the commit message, or the commit diff information.

## Data Format

Data format and some basic information can be observed below.

- **project:** the project's name containing the bug
- **hexsha:** hex sha identification of bugfixing commit
- **parent_hexsha:** sha of the bugfixing commit's parent
- **message:** the commit message
- **summary:** the commit summary
- **file:** modified file by the commit (location in repo)
- **total:** metadata on changes - eg.: addition, or removal of lines
- **language:** main language of the repository
- **size:** size of the bugfix
- **diff:** commit diff information
- **repo_url:** the URL of the repository
- **part:** makes distincion between different bugfixing parts in case the bugfix affects multiple functions
- **parts:** the number of function affected by the bugfixing commit
- **a:** fixed code segment
- **b:** buggy code segment

Every line in the _.jsonl_ file follows this format, and is compatible with JSON format.
One can read every line, and parse them as JSON strings.

## Data Metrics

| Language    | #Samples   | #Chars (mean) | #Chars (med) | Size (MiB) |
|-------------|------------|---------------|--------------|------------|
| C           | 63928      | 1612.50       | 885.0        | 196.65     |
| C++         | 69905      | 1503.97       | 828.0        | 200.60     |
| Java        | 69917      | 1075.18       | 654.5        | 143.58     |
| JavaScript  | 66453      | 1196.82       | 541.5        | 151.86     |
| Python      | 101280     | 1168.78       | 693.5        | 225.94     |
|             |            |               |              |            |
| **Summary** | **371483** | **1311.45**   | **720.5**    | **918.63** |

_#Samples_ is the number of buggy-fixed pairs extracted from commits under a specific language.
_#Chars_ _mean_, and _median_ values provide some insight into the average source code length
of the mined programs, while _Size_ measures the UTF-8 encoded length of the source codes
in mebibytes. The summary of sample, and size information is a cumulative value of the
separate samples, while both _mean_ and _median_ character values are averaged over the buggy
and fixed codes.

## Dataset

To access the dataset visit: https://zenodo.org/records/10198721

## Citation

If you find useful methods in this package you can site us with:

### Paper

This work is submitted for the
[21st International Conference on Mining Software Repositories](https://2024.msrconf.org/).

**BibTeX:**
```
@misc{XPlainHub:hpaper2023,
  author       = {Horváth Dániel},
  title        = {Yet Another GitHub Mined Dataset: XPlainHub},
  year         = 2024,
  publisher    = {???},
  doi          = {???},
}
```

___

### Dataset

**BibTeX:**
```
@dataset{XPlainHub:hdata2023,
  author       = {Horváth Dániel},
  title        = {XPlainHub},
  month        = nov,
  year         = 2023,
  publisher    = {Zenodo},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.10198721},
  url          = {https://doi.org/10.5281/zenodo.10198721}
}
```

___


