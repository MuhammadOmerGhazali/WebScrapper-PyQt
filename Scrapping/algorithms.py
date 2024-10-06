import re
def counting_sort_for_radix(data, column_index, exp):
    n = len(data)
    output = [0] * n
    count = [0] * 10
    
    for i in range(n):
        index = int(data[i][column_index]) // exp
        count[index % 10] += 1
    
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    for i in range(n - 1, -1, -1):
        index = int(data[i][column_index]) // exp
        output[count[index % 10] - 1] = data[i]
        count[index % 10] -= 1
    
    for i in range(n):
        data[i] = output[i]
    
    return data

def string_to_integer(s):
    # Use regular expression to find all digits in the string
    # The regular expression \d+ finds sequences of digits
    clean_string = re.sub(r'[^0-9]', '', s)
    # Convert the cleaned string to an integer
    return int(clean_string) if clean_string else 0  # Return 0 if no digits found

print(type(string_to_integer("$44,219")))