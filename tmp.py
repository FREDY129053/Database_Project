import re

word, b = input(), input()

left, right = [], []

for i in re.finditer('<delete>|<left>|<right>|<bspace>|[a-z]', b):
	match i.group():
		case '<delete>':
			if right:
				right.pop()
		case '<bspace>':
			if left:
				left.pop()
		case '<right>':
			if right:
				left.append(right.pop())
		case '<left>':
			if left:
				right.append(left.pop())
		case letter:
			left.append(letter)

if word == ''.join(left + right[::-1]):
	print('Yes')
else:
	print('No')