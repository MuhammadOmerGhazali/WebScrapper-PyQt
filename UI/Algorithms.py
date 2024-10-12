import pandas as pd

def heap_sort(df, column_name):
    """ Perform heap sort on the specified column of the DataFrame. """
    # Create a list of tuples (value, index) to keep track of the original index
    arr = list(zip(df[column_name].tolist(), df.index.tolist()))

    def heapify(arr, n, i):
        largest = i  # Initialize largest as root
        left = 2 * i + 1  # left = 2*i + 1
        right = 2 * i + 2  # right = 2*i + 2

        # See if left child of root exists and is greater than root
        if left < n and arr[left][0] > arr[largest][0]:
            largest = left

        # See if right child of root exists and is greater than root
        if right < n and arr[right][0] > arr[largest][0]:
            largest = right

        # Change root if needed
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]  # Swap
            heapify(arr, n, largest)  # Recursively heapify the affected sub-tree

    # Build heap (rearrange array)
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # One by one extract an element from heap
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # Swap
        heapify(arr, i, 0)

    return create_sorted_dataframe(df, arr)

def quick_sort(df, column_name):
    """ Quick sort implementation. """
    arr = list(zip(df[column_name].tolist(), df.index.tolist()))
    quick_sort_helper(arr, 0, len(arr) - 1)
    return create_sorted_dataframe(df, arr)

def quick_sort_helper(arr, low, high):
    if low < high:
        # pi is partitioning index
        pi = partition(arr, low, high)

        # Recursively sort elements before partition and after partition
        quick_sort_helper(arr, low, pi - 1)
        quick_sort_helper(arr, pi + 1, high)

def partition(arr, low, high):
    pivot = arr[high][0]  # pivot value
    i = low - 1  # Index of smaller element
    for j in range(low, high):
        # If current element is smaller than or equal to pivot
        if arr[j][0] <= pivot:
            i += 1  # increment index of smaller element
            arr[i], arr[j] = arr[j], arr[i]  # swap
    arr[i + 1], arr[high] = arr[high], arr[i + 1]  # swap pivot with the element at i+1
    return i + 1

def bubble_sort(df, column_name):
    """ Bubble sort implementation. """
    arr = list(zip(df[column_name].tolist(), df.index.tolist()))
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            # Traverse the array from 0 to n-i-1. Swap if the element found is greater than the next element
            if arr[j][0] > arr[j+1][0]:
                arr[j], arr[j+1] = arr[j+1], arr[j]  # Swap

    return create_sorted_dataframe(df, arr)

def selection_sort(df, column_name):
    """ Selection sort implementation. """
    # Create a list of tuples (value, index) to keep track of the original index
    arr = list(zip(df[column_name].tolist(), df.index.tolist()))
    n = len(arr)

    for i in range(n):
        # Find the minimum element in the remaining unsorted array
        min_index = i
        for j in range(i + 1, n):
            if arr[j][0] < arr[min_index][0]:
                min_index = j

        # Swap the found minimum element with the first element
        arr[i], arr[min_index] = arr[min_index], arr[i]

    return create_sorted_dataframe(df, arr)

def merge_sort(df, column_name):
    """ Merge sort implementation. """
    # Create a list of tuples (value, index) to keep track of the original index
    arr = list(zip(df[column_name].tolist(), df.index.tolist()))
    merge_sort_helper(arr)
    
    return create_sorted_dataframe(df, arr)

def merge_sort_helper(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # Find the middle point
        left_half = arr[:mid]  # Dividing the elements into 2 halves
        right_half = arr[mid:]

        # Recursively sort the halves
        merge_sort_helper(left_half)
        merge_sort_helper(right_half)

        # Merging the sorted halves
        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i][0] <= right_half[j][0]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        # Copy the remaining elements of left_half, if any
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        # Copy the remaining elements of right_half, if any
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

def insertion_sort(df, column_name):
    """ Insertion sort implementation. """
    # Create a list of tuples (value, index) to keep track of the original index
    arr = list(zip(df[column_name].tolist(), df.index.tolist()))
    n = len(arr)

    for i in range(1, n):
        key = arr[i]  # The current element to be inserted
        j = i - 1

        # Move elements of arr[0..i-1], that are greater than key, to one position ahead of their current position
        while j >= 0 and arr[j][0] > key[0]:
            arr[j + 1] = arr[j]  # Shift element to the right
            j -= 1
        
        arr[j + 1] = key  # Insert the key in the correct position

    return create_sorted_dataframe(df, arr)

def counting_sort(df, column_name, position=0):
    """ Counting sort for strings at a specific character position. """
    # Create a list of tuples (string_value, index) to keep track of the original index
    arr = list(zip(df[column_name].tolist(), df.index.tolist()))
    
    # Determine the maximum length of strings in the column
    max_length = max(len(str(s[0])) for s in arr)
    
    # Initialize counting array with a size of 256 for ASCII characters
    count = [0] * 256
    output = [''] * len(arr)
    
    # Populate the counting array based on the character at the given position
    for string, index in arr:
        string = str(string)
        char_index = ord(string[position]) if position < len(string) else 0  # Handle shorter strings
        count[char_index] += 1

    # Update the counting array to reflect positions
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    # Build the output array based on the counting array and original indices
    for i in range(len(arr) - 1, -1, -1):
        string, index = arr[i]
        string = str(string)
        char_index = ord(string[position]) if position < len(string) else 0
        output[count[char_index] - 1] = (string, index)  # Store the (string, original_index) tuple
        count[char_index] -= 1

    # Return a sorted DataFrame using the helper function
    return create_sorted_dataframe(df, output)

def radix_sort(df, column_name):
    """ Radix sort implementation for DataFrame columns with string values. """
    # Determine the maximum length of any string (convert int to string if needed)
    arr = list(zip(df[column_name].tolist(), df.index.tolist()))
    max_length = max(len(str(s[0])) for s in arr)

    # Sort by each character position starting from the last character (least significant)
    for position in range(max_length - 1, -1, -1):
        df = counting_sort(df, column_name, position)

    return df  # Return the fully sorted DataFrame



def bucket_sort(df, column_name):
    """ Bucket sort for DataFrame column (numeric or string values). """
    # Create a list of tuples (value, index) to keep track of the original index
    arr = list(zip(df[column_name].tolist(), df.index.tolist()))
    
    if not arr:
        return df

    # Check if the column data is numeric
    is_numeric = all(isinstance(x[0], (int, float)) for x in arr)

    if is_numeric:
        max_value = max(s[0] for s in arr)
        bucket_count = len(arr) // 5  
        buckets = [[] for _ in range(bucket_count)]

        # Distribute the elements into buckets
        for value, index in arr:
            bucket_idx = value * bucket_count // (max_value + 1)  # Determine the bucket index
            buckets[bucket_idx].append((value, index))

        # Sort each bucket and concatenate the results
        sorted_array = []
        for bucket in buckets:
            sorted_array.extend(sorted(bucket, key=lambda x: x[0]))  # Sort the bucket by the value

    else:
        # For strings, determine the maximum length for the buckets
        max_length = max(len(str(s[0])) for s in arr)
        buckets = [[] for _ in range(max_length + 1)]  # Create a bucket for each string length

        # Distribute strings into buckets based on their length
        for string, index in arr:
            buckets[len(str(string))].append((string, index))

        # Sort each bucket and concatenate the results
        sorted_array = []
        for bucket in buckets:
            sorted_array.extend(sorted(bucket, key=lambda x: x[0]))  # Sort the bucket by the string value

    # Create a sorted DataFrame from the sorted array of tuples (value, index)
    return create_sorted_dataframe(df, sorted_array)




def shell_sort(df, column_name):
    """ Shell sort implementation. """
    arr = list(zip(df[column_name].tolist(), df.index.tolist()))
    n = len(arr)
    gap = n // 2

    # Reduce the gap until it becomes 0
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap][0] > temp[0]:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2

    return create_sorted_dataframe(df, arr)

def tim_sort(df, column_name):
    """ Tim sort implementation using Python's sorted function. """
    arr = list(zip(df[column_name].tolist(), df.index.tolist()))
    sorted_arr = sorted(arr, key=lambda x: x[0])
    
    return create_sorted_dataframe(df, sorted_arr)

def create_sorted_dataframe(df, arr):
    """ Create a sorted DataFrame from the sorted array of tuples (value, index). """
    sorted_indices = [index for _, index in arr]
    sorted_df = df.loc[sorted_indices].reset_index(drop=True)
    return sorted_df

def merge_columns(df, column_names):
    # Ensure column names exist in the DataFrame
    for col in column_names:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' does not exist in the DataFrame.")
    
    # Merge the specified columns into a new column without a separator
    df['merged_column'] = df[column_names].astype(str).agg(''.join, axis=1)
    
    # Convert numeric strings to integers in the merged column
    df['merged_column'] = df['merged_column'].apply(convert_if_numeric)
    
    return df

def convert_if_numeric(value):
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return value

