import re

def remove_comments(content):
    # Remove HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    # Remove CSS/JS multi-line comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    # Remove JS single-line comments (but not inside strings, this is simplistic)
    # To avoid removing // in URLs or something, but for this file, it's fine
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        # Remove // comments, but keep if it's inside a string (simplistic)
        if '//' in line:
            # Find the first // not inside quotes
            in_string = False
            quote_char = None
            for i, char in enumerate(line):
                if char in ['"', "'"] and (i == 0 or line[i-1] != '\\'):
                    if not in_string:
                        in_string = True
                        quote_char = char
                    elif char == quote_char:
                        in_string = False
                        quote_char = None
                elif char == '/' and i < len(line) - 1 and line[i+1] == '/' and not in_string:
                    line = line[:i]
                    break
        new_lines.append(line)
    content = '\n'.join(new_lines)
    return content

with open('index.html', 'r') as f:
    content = f.read()

new_content = remove_comments(content)

with open('index.html', 'w') as f:
    f.write(new_content)

print("Comments removed.")