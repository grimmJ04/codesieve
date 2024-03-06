# CodeSieve

The package _codesieve_ is a pip installable package
to help developers and/or researchers in mining software repositories.

To install, run

> pip install <path/to/codesieve>

from any python virtual environment.

Anyone can freely customize the library, make copies, or modify the code, or simply use it as is.

<details>
<summary>Example usage</summary>

```python
from tree_sitter_languages import get_parser

from codesieve import data

src_java = """
import java.util.List;

class Greeter implements IGreeter {
    public void Hello() {
        System.out.println("Goodbye World!");
    }
    
    public void DumDum() {
        System.out.println("Some things never change ...");
    }
    
    public void BeProductive(List<double> values) {
        double prod = 0;
        foreach (var val in values) {
            prod *= val;
        }
    }
}
"""
tgt_java = """
import java.util.List;

class Greeter implements IGreeter {
    // Say hello instead
    public void Hello() {
        System.out.println("Hello World!");
    }
    
    public void DumDum() {
        System.out.println("Some things never change ...");
    }
    
    public double BeProductive(List<Double> values) {
        double prod = 1.0;
        for (var val : values) {
            prod *= val;
        }
        return prod;
    }
}
"""
parser = get_parser('java')
parts = data.datasieve(parser, parser, src_java, tgt_java, clazz='function', level=1, dist='s2s')
# example output
[
    (
        'public void Hello() {\n        System.out.println("Goodbye World!");\n    }',
        'public void Hello() {\n        System.out.println("Hello World!");\n    }'
    ),
    (
        'public void BeProductive(List<double> values) {\n        double prod = 0;\n        foreach (var val in values) {\n            prod *= val;\n        }\n    }',
        'public double BeProductive(List<Double> values) {\n        double prod = 1.0;\n        for (var val : values) {\n            prod *= val;\n        }\n        return prod;\n    }'
    )
]
```
</details>

# CodegrainHouse Dataset

CodegrainHouse is a multi-linguistic dataset consisting of 5 popular programming languages, mined from more than 7500 GitHub repositories from wich 5273 contained bug-fixes based on our criteria, containing 371483 methods extracted from code from 250090 bug-fixing commits. Most importantly, the dataset includes the buggy, and the fixed version of methods extracted from the bugfixing commit. It also contains some additional information like the commit message, or the commit diff information.

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
