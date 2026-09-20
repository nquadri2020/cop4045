import ast
import io
import tokenize

def line_number(input_filename: str, output_filename: str) -> None:
    """Write a numbered copy of a text file to another file.
    Args:
        input_filename: Name of the input text file.
        output_filename: Name of the output text file.
    Raises:
        OSError: If the input or output file cannot be accessed.
    """
    try:
        with open(input_filename, "r", encoding="utf-8") as input_file:
            lines = input_file.readlines()
        with open(output_filename, "w", encoding="utf-8") as output_file:
            for number, line in enumerate(lines, start=1):
                output_file.write("{}.".format(number) + line)
    except OSError as error:
        print("Error processing files: {}".format(error))
        raise

def remove_comments_and_empty_lines(source: str) -> str:
    """Remove comments and empty lines from Python source code.
    Args:
        source: Python source code.
    Returns:
        Source code with comments and empty lines removed.
    """
    result = []
    tokens = tokenize.generate_tokens(io.StringIO(source).readline)

    for token in tokens:
        if token.type == tokenize.COMMENT:
            continue
        result.append(token)

    cleaned = tokenize.untokenize(result)

    lines = [
        line for line in cleaned.splitlines()
        if line.strip()
    ]
    return "\n".join(lines) + "\n"

def parse_functions(filename: str) -> tuple:
    """Parse a Python file and return information about its functions.
    Args:
        filename: Name of the Python source file.
    Returns:
        A tuple of tuples containing the line number, function name,
        formal arguments, and source code for each function.
    Raises:
        OSError: If the file cannot be read.
        SyntaxError: If the Python source cannot be parsed.
    """
    try:
        with open(filename, "r", encoding="utf-8") as input_file:
            source = input_file.read()
        tree = ast.parse(source)
        lines = source.splitlines(keepends=True)

        functions = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                function_source = "".join(
                    lines[node.lineno - 1:node.end_lineno]
                )
                function_source = remove_comments_and_empty_lines(
                    function_source
                )

                arguments = []
                for argument in node.args.posonlyargs:
                    arguments.append(argument.arg)
                for argument in node.args.args:
                    arguments.append(argument.arg)
                if node.args.vararg is not None:
                    arguments.append("*" + node.args.vararg.arg)
                for argument in node.args.kwonlyargs:
                    arguments.append(argument.arg)
                if node.args.kwarg is not None:
                    arguments.append("**" + node.args.kwarg.arg)
                argument_string = ", ".join(arguments)

                functions.append(
                    (
                        node.lineno,
                        node.name,
                        argument_string,
                        function_source,
                    )
                )
        functions.sort(key=lambda function: function[1])
        return tuple(functions)
    except (OSError, SyntaxError) as error:
        print("Error parsing Python file: {}".format(error))
        raise

def main() -> None:
    source_filename = "p1_Quadri_Naabeghah.py"
    numbered_filename = "p1_Quadri_Naabeghah.py.txt"
    line_number(source_filename, numbered_filename)
    functions = parse_functions(source_filename)
    print(functions)

if __name__ == "__main__":
    main()