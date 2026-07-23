import tokenize
import io
import sys

def strip_comments(filepath):
    with open(filepath, "r") as f:
        source = f.read()

    tokens = tokenize.generate_tokens(io.StringIO(source).readline)
    result = []
    last_lineno = -1
    last_col = 0

    for tok_type, tok_string, start, end, line in tokens:
        if tok_type == tokenize.COMMENT:
            continue  # skip comments entirely
        if start[0] > last_lineno:
            last_col = 0
        if start[1] > last_col:
            result.append(" " * (start[1] - last_col))
        result.append(tok_string)
        last_lineno, last_col = end

    new_source = "".join(result)

    with open(filepath, "w") as f:
        f.write(new_source)

    print(f"Stripped comments from: {filepath}")


if __name__ == "__main__":
    for path in sys.argv[1:]:
        strip_comments(path)
