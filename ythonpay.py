from tokenize import tokenize, untokenize, NAME
import sys
import code
from io import BytesIO


banner_text = """Elcomeway otay ethay Ythonpay EPLRAY (Welcome to the Ythonpay REPL)!

Ythonpay is literally just Python, but the keywords are in Pig Latin.
(e.g. "and", "class", "False" become "andway", "assclay", "Alsefay".)

Note that things like "print" and "range" are not keywords, so they must be
written in English.

The Pig Latin naming rules are as specified in the Pig Latin Wikipedia article:
https://en.wikipedia.org/wiki/Pig_Latin#Rules.
        
As with Python, type "exit()" to exit the REPL. """

to_python = {
    'Alsefay': 'False',
    'awaitway': 'await',
    'elseway': 'else',
    'importway': 'import',
    'asspay': 'pass',
    'Onenay': 'None',
    'eakbray': 'break',
    'exceptway': 'except',
    'inway': 'in',
    'aiseray': 'raise',
    'Uetray': 'True',
    'assclay': 'class',
    'inallyfay': 'finally',
    'isway': 'is',
    'eturnray': 'return',
    'andway': 'and',
    'ontinuecay': 'continue',
    'orfay': 'for',
    'ambdalay': 'lambda',
    'rytay': 'try',
    'asway': 'as',
    'efday': 'def',
    'omfray': 'from',
    'onlocalnay': 'nonlocal',
    'ilewhay': 'while',
    'assertway': 'assert',
    'elday': 'del',
    'obalglay': 'global',
    'otnay': 'not',
    'ithway': 'with',
    'asyncway': 'async',
    'elifway': 'elif',
    'ifway': 'if',
    'orway': 'or',
    'ieldyay': 'yield',
}

to_ythonpay = {v: k for k, v in to_python.items()}


def repl_read(prompt: str = ""):
    print("> ", end="", flush=True)
    line = sys.stdin.readline()
    return convert_to_python(line)


def repl():
    code.interact(
        banner=banner_text,
        readfunc=repl_read, exitmsg="Yebay!")


def tok_error(tok):
    _, tok_val, (row, col), _, _ = tok
    print(
        f"Invalidway Ythonpay eywordkay (atway owray {row}, olumcay {col}): '{tok_val}'",
        file=sys.stderr)
    exit(1)


def convert_to_ythonpay(s: str) -> str:
    """ Converts (assumed valid) Python code into Ythonpay. """
    result = []
    toks = tokenize(BytesIO(s.encode("utf-8")).readline)
    for tok_num, tok_val, _, _, _ in toks:
        if tok_val in to_ythonpay:
            result.append((NAME, to_ythonpay[tok_val]))
        else:
            result.append((tok_num, tok_val))
    return untokenize(result).decode("utf-8")


def convert_to_python(s: str) -> str:
    """ Converts Ythonpay into Python code suitable for being executed. """
    result = []
    toks = tokenize(BytesIO(s.encode("utf-8")).readline)
    for tok in toks:
        tok_val = tok[1]

        if tok_val in to_python:
            result.append((NAME, to_python[tok_val], *tok[2:]))
        elif tok_val in to_ythonpay:
            # ERROR: found python code. This is supposed to be ythonpay!!
            tok_error(tok)
        else:
            result.append(tok)

    return untokenize(result).decode("utf-8")


def exec_ythonpay(s: str) -> str:
    """ Executes the given Ythonpay code string. """
    exec(convert_to_python(s))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        repl()
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
        with open(filename, "r") as f:
            exec_ythonpay(f.read())
