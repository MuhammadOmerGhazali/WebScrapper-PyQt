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

def counting_sort(df, column_name):
    """ Perform counting sort on the specified column of the DataFrame, supporting strings and numbers. """
    
    # Create a list of tuples (value, index) to keep track of the original index
    arr = list(zip(df[column_name].tolist(), df.index.tolist()))
    
    # Initialize max_value and min_value for numeric types
    max_value = None
    min_value = None
    
    # Determine if we are dealing with numbers or strings
    if all(isinstance(value, (int, float)) for value, _ in arr):
        # Handle numeric values
        max_value = max(value for value, _ in arr)
        min_value = min(value for value, _ in arr)

        # Initialize count array
        range_of_elements = int(max_value - min_value + 1)
        count = [0] * range_of_elements
        output = [None] * len(arr)
        
        # Store the count of each unique numeric value
        for value, index in arr:
            count[int(value) - int(min_value)] += 1

        # Change count[i] so that it contains the actual position of this value in output[]
        for i in range(1, len(count)):
            count[i] += count[i - 1]
        
        # Build the output array using the count array
        for value, index in reversed(arr):  # Reverse to maintain stability
            output[count[int(value) - int(min_value)] - 1] = (value, index)
            count[int(value) - int(min_value)] -= 1

    else:
        # Handle strings (and potentially mixed types)
        # Get max and min based on string comparison
        max_value = max(value for value, _ in arr)
        min_value = min(value for value, _ in arr)

        # Initialize count array based on the ASCII values of characters
        range_of_elements = ord(max_value) - ord(min_value) + 1
        count = [0] * range_of_elements
        output = [None] * len(arr)

        # Store the count of each unique string value
        for value, index in arr:
            count[ord(value) - ord(min_value)] += 1

        # Change count[i] so that it contains the actual position of this value in output[]
        for i in range(1, len(count)):
            count[i] += count[i - 1]

        # Build the output array using the count array
        for value, index in reversed(arr):  # Reverse to maintain stability
            output[count[ord(value) - ord(min_value)] - 1] = (value, index)
            count[ord(value) - ord(min_value)] -= 1
    
    return create_sorted_dataframe(df, output)

def bucket_sort(df, column_name, num_buckets=10):
    """ Perform bucket sort on the specified column of the DataFrame. """
    # Create a list of tuples (value, index) to keep track of the original index
    arr = list(zip(df[column_name].tolist(), df.index.tolist()))
    
    if not arr:
        return create_sorted_dataframe(df, arr)

    # Determine the minimum and maximum values for range
    min_value = min(arr, key=lambda x: x[0])[0]
    max_value = max(arr, key=lambda x: x[0])[0]
    
    # Create buckets
    bucket_range = (max_value - min_value) / num_buckets
    buckets = [[] for _ in range(num_buckets)]
    
    # Distribute input array values into buckets
    for value, index in arr:
        bucket_index = int((value - min_value) / bucket_range)
        if bucket_index == num_buckets:  # Edge case for max_value
            bucket_index -= 1
        buckets[bucket_index].append((value, index))
    
    # Sort individual buckets and gather results
    sorted_array = []
    for bucket in buckets:
        sorted_bucket = insertion_sort(bucket, 0)  # Using insertion sort for individual buckets
        sorted_array.extend(sorted_bucket)
    
    return create_sorted_dataframe(df, sorted_array)

def radix_sort(df, column_name):
    """ Radix sort implementation for numeric and string columns. """
    # Create a list of tuples (value, index) to keep track of the original index
    arr = list(zip(df[column_name].tolist(), df.index.tolist()))
    
    # Determine the type of the column (numeric or string)
    if all(isinstance(value, (int, float)) for value, _ in arr):
        column_type = 'numeric'
        # Get the maximum number to know the number of digits
        max_value = max(value for value, _ in arr)
        exp = 1  # Start with the least significant digit
        while max_value // exp > 0:
            arr = counting_sort_for_radix(arr, exp, column_type)
            exp *= 10
    else:
        column_type = 'string'
        # Get the maximum string length for comparison
        max_length = max(len(value) for value, _ in arr)
        # Sort by each character starting from the least significant one (right to left)
        for exp in range(max_length - 1, -1, -1):
            arr = counting_sort_for_radix(arr, exp, column_type)

    return create_sorted_dataframe(df, arr)

def counting_sort_for_radix(arr, exp, column_type):
    """ Counting sort helper function for Radix Sort, utilizing the existing counting_sort logic. """
    # For numeric values, sort by digit at the given exponent (exp)
    if column_type == 'numeric':
        # Extract the current digit based on the exponent
        modified_df = pd.DataFrame({0: [int(value // exp) % 10 for value, _ in arr], 1: [index for _, index in arr]})
        sorted_df = counting_sort(modified_df, 0)
        return list(zip(sorted_df[0].tolist(), sorted_df[1].tolist()))

    # For string values, sort by the character at the given position (exp)
    else:
        max_length = max(len(value) for value, _ in arr)
        # Fill shorter strings with empty characters at the exp position
        modified_df = pd.DataFrame({
            0: [ord(value[exp]) if exp < len(value) else 0 for value, _ in arr], 
            1: [index for _, index in arr]
        })
        sorted_df = counting_sort(modified_df, 0)
        return list(zip([chr(val) if val != 0 else "" for val in sorted_df[0].tolist()], sorted_df[1].tolist()))

def create_sorted_dataframe(df, arr):
    """ Create a sorted DataFrame from the sorted array of tuples (value, index). """
    sorted_indices = [index for _, index in arr]
    sorted_df = df.loc[sorted_indices].reset_index(drop=True)
    return sorted_df
