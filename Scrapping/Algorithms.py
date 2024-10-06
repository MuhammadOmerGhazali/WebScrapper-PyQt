def heap_sort(df, column_name):
    """ Perform heap sort on the specified column of the DataFrame. """
    # Build heap
    n = len(df)
    arr = df[column_name].tolist()  # Convert the column to a list
        
    def heapify(arr, n, i):
        largest = i  # Initialize largest as root
        left = 2 * i + 1  # left = 2*i + 1
        right = 2 * i + 2  # right = 2*i + 2
        
        # See if left child of root exists and is greater than root
        if left < n and arr[left] > arr[largest]:
            largest = left
        
        # See if right child of root exists and is greater than root
        if right < n and arr[right] > arr[largest]:
            largest = right
        
        # Change root if needed
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]  # Swap
            heapify(arr, n, largest)  # Recursively heapify the affected sub-tree

    # Build heap (rearrange array)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
        
    # One by one extract an element from heap
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # Swap
        heapify(arr, i, 0)
        
    # Create a new DataFrame to reflect the sorted order
    sorted_df = df.iloc[[df[column_name].tolist().index(x) for x in arr]].reset_index(drop=True)
    return sorted_df

def quick_sort(df, column_name):
        """ Quick sort implementation. """
        arr = df[column_name].tolist()  # Convert the column to a list
        quick_sort_helper(arr, 0, len(arr) - 1, df)
        return df

def quick_sort_helper( arr, low, high, df):
        if low < high:
            # pi is partitioning index
            pi = partition(arr, low, high, df)

            # Recursively sort elements before partition and after partition
            quick_sort_helper(arr, low, pi - 1, df)
            quick_sort_helper(arr, pi + 1, high, df)

def partition(arr, low, high, df):
        pivot = arr[high]  # pivot
        i = low - 1  # Index of smaller element
        for j in range(low, high):
            # If current element is smaller than or equal to pivot
            if arr[j] <= pivot:
                i += 1  # increment index of smaller element
                arr[i], arr[j] = arr[j], arr[i]  # swap
        arr[i + 1], arr[high] = arr[high], arr[i + 1]  # swap pivot with the element at i+1
        return i + 1

def bubble_sort(df, column_name):
        """ Bubble sort implementation. """
        arr = df[column_name].tolist()  # Convert the column to a list
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                # Traverse the array from 0 to n-i-1. Swap if the element found is greater than the next element
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]  # Swap
        
        # Create a new DataFrame to reflect the sorted order
        sorted_df = df.iloc[[df[column_name].tolist().index(x) for x in arr]].reset_index(drop=True)
        return sorted_df