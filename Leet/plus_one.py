class Solution(object):
    def plusOne(self, digits):
        for i in range(len(digits) - 1, -1, -1):
            if 0 <= digits[i] <= 8:
                digits[i] += 1
                return digits
            else:
                digits[i] = 0
        digits.insert(0, 1)
        return digits
    
numbers = [9, 9, 9]
print(Solution().plusOne(numbers))