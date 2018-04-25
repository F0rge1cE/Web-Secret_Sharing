import numpy as np
import math
import random

def generate_polynomial(segment, shares, required):
	# Generate random polynomial based on parameters
	# Param:
	#	segment: given byte
	#	shares: number of wanted shares
	#	required: number of required share to reconstruct polynomial
	# Return: List of shares, length = shares
	bound = math.pow(2,8)
	secret = ord(segment)
	coefficients = []
	for i in range(required-1):
		random_coeff = random.randint(1, bound-1)
		coefficients.append(random_coeff)
	coefficients.append(secret)
	# print(coefficients)
	return get_points(coefficients, shares)

def get_points(coefficients, shares):
	# Generate points based on polynomial
	# Param:
	#	coefficients: given byte
	#	shares: number of wanted shares
	# Return: List of shares, length = shares
	poly = np.poly1d(coefficients)
	pointsX = []
	pointsY = []
	for x in range(1,shares+1):
		y = poly(x)
		pointsX.append(x)
		pointsY.append(y)
	# print(pointsX)
	# print(pointsY)
	# print(zip(pointsX,pointsY))
	return zip(pointsX,pointsY)

def reconstruct(share_list, k):
	# Reconstruct the polynomial 
	# Param:
	#	share_list: shares uploaded by users
	#	k: number of shares needed to reconstruct the polynomial
	# Return: secret
	x, y = zip(*share_list)
	res = np.polyfit(x,y,k-1)
	return np.around(res).astype(int)[-1]
print(reconstruct(generate_polynomial('t', 5, 4),4))