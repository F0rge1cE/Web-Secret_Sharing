import numpy as np
import math
import random

def generate_polynomial(segment, shares, required):
	bound = math.pow(2,8)
	secret = ord(segment)
	coefficients = []
	for i in range(required-1):
		random_coeff = random.randint(1, bound-1)
		coefficients.append(random_coeff)
	coefficients.append(secret)
	print(coefficients)
	return get_points(coefficients, shares)

def get_points(coefficients, shares):
	poly = np.poly1d(coefficients)
	pointsX = []
	pointsY = []
	for x in range(1,shares+1):
		y = poly(x)
		pointsX.append(x)
		pointsY.append(y)
	# print(pointsX)
	# print(pointsY)
	print(zip(pointsX,pointsY))
	return zip(pointsX,pointsY)

def reconstruct(share_list, k):
	x = []
	y = []
	for s in share_list:
		x.append(s[0])
		y.append(s[1])
	res = np.polyfit(x,y,k-1)
	return np.around(res).astype(int)[-1]
print(reconstruct(generate_polynomial('t', 5, 5),5))