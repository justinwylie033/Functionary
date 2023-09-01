# test_DescribeFunction.py

from DescribeFunction import DescribeFunction

if __name__ == "__main__":
    # Test 1: Generate description for a simple function
    simple_function = """
def add(a, b):
    return a + b
    """
    print("Generating description for a simple function...")
    description = DescribeFunction.generate_description_from_code(simple_function)
    print(description)

    # Test 2: Generate description for a more complex function
    complex_function = """
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    left_idx, right_idx = 0, 0
    while left_idx < len(left) and right_idx < len(right):
        if left[left_idx] < right[right_idx]:
            result.append(left[left_idx])
            left_idx += 1
        else:
            result.append(right[right_idx])
            right_idx += 1
    result.extend(left[left_idx:])
    result.extend(right[right_idx:])
    return result
    """
    print("\nGenerating description for a more complex function...")
    description = DescribeFunction.generate_description_from_code(complex_function)
    print(description)

    # You can add more test cases as needed...
