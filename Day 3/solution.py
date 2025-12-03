def most_joltage(bank):
    n = len(bank)
    # Precompute best digit to the right of each index
    best_right = [0]*n
    best = 0
    for i in range(n-1, -1, -1):
        best_right[i] = best
        best = max(best, bank[i])
    
    ans = 0
    for i in range(n-1):
        tens = bank[i]
        ones = best_right[i]
        ans = max(ans, 10*tens + ones)
    return ans

        

def total_joltage_pt1(file):
    ans = 0
    with open(file, 'r') as f:
        for i in f.readlines():
            i = i.strip()
            i = [int(_) for _ in str(i)]
            ans+= most_joltage(i)
    return ans

test = """
987654321111111
811111111111119
234234234234278
818181911112111"""

def total_joltage_pt1_test():
    ans = 0
    for i in test.strip().split('\n'):
        i = i.strip()
        i = [int(_) for _ in str(i)]
        ans+= most_joltage(i)
        print(most_joltage(i))
    return ans

def most_joltage_pt2(bank, k):
    stack = []
    to_remove = len(bank) - k  # how many we are allowed to drop

    for digit in bank:
        # while we can remove AND the stack top is smaller than current digit
        while to_remove > 0 and stack and stack[-1] < digit:
            stack.pop()
            to_remove -= 1

        stack.append(digit)

    # if still too long (didn't remove enough), truncate from end
    return stack[:k]

def total_joltage_pt2_test():
    ans = 0
    for i in test.strip().split('\n'):
        i = i.strip()
        i = [int(_) for _ in str(i)]
        k = 12  # example length
        max_digits = int("".join(map(str, most_joltage_pt2(i, k))))
        ans+= max_digits
        print(max_digits)
    return ans

def total_joltage_pt2(file, k):
    ans = 0
    with open(file, 'r') as f:
        for i in f.readlines():
            i = i.strip()
            i = [int(_) for _ in str(i)]
            max_digits = int("".join(map(str, most_joltage_pt2(i, k))))
            ans+= max_digits
    return ans

if __name__ == "__main__":
    # print(total_joltage_pt1_test())
    # print(total_joltage_pt1("Day 3\\input.txt"))
    # print(total_joltage_pt2_test())
    print(total_joltage_pt2("Day 3\\input.txt", 12))