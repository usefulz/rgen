Regular expression password list generator

## Features

* Regex-based password strings
* Forever mode
* Numbered mode
* STDOUT output
* File output
* ^C stops

## Requirements

* argparse
* signal
* sys
* os
* re
* rstr

## Usage

```
> usage: rgen.py <-r 'REGEX'> [-f|--forever] [--numpasses <n>] [-o|--output] <[filename|-]> [-h|--help]
>  -h, --help            show this help message and exit
>  -r REGEX, --regex REGEX              - Regular expression in single quotes
>  -f, --forever                        - Run until Control-C is pressed
>  -n NUMPASSES, --numpasses NUMPASSES  - Number of passwords to generate (>0 disables -f, 0 enables -f)
>  -o OUTPUT, --output OUTPUT           - Output file path. '-' prints to stdout
```

## Example

```
python3.7 rgen.py -r 'abc[def]123' -f -o -
```

Generates the following output:

```
abcd123
abce123
abcf123
...
```

# Tested on

* Python 2.7
* Python 3.8
