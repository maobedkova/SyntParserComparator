# SyntParserComparator
The algorithm was written for comparing the quality of different syntactic parsers (RuSyntax, SyntaxNet, UDPipe). Now it is rewritten for comparing the output of a syntactic parser and a golden standard and measuring the quality of the syntactic parser output.
## How to use
```
import compare_parsers
compare_parsers(<path to golden standard file>,
                <path to syntactic parser output>)
```

NB! Works only with conll(u) format.
