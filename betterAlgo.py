import numpy as np
import math
import random

_PRIME = 277

def ext_euclid(a, b):
	# Use Extended Euclidean algorithm s.t. ax + by = gcd(a,b)
	# Param:
	#	a: given a
	#	b: given b
	# Return: x , y, gcd(a,b)
	if b == 0:
		return 1, 0, a
	else:
		x, y, q = ext_euclid(b, a % b) # q = gcd(a, b) = gcd(b, a%b)
		x, y = y, (x - (a // b) * y)
		return x, y, q


def inv_mod(denominator, prime):
	# Calculate inverse mod s.t. inv_mod(denominator, prime) ^ -1 = denominator % denominator
	# Param:
	#	denominator: given denominator
	#	prime: selected prime number
	# Return: inverse mod 

	# k = k % prime
	# if k < 0:
	#     r = gcd(prime, -k)[2]
	# else:
	r = ext_euclid(denominator, prime)[0]
	# return (prime + r) % prime
	return r

def generate_polynomial(segment, shares, required, prime = _PRIME):
	# Generate random polynomial based on parameters
	# Param:
	#	segment: given byte
	#	shares: number of wanted shares
	#	required: number of required share to reconstruct polynomial
	# Return: List of shares, length = shares
	bound = math.pow(2,8) #bound can be change accordingly to prime number
	secret = ord(segment)
	coefficients = []
	for i in range(required-1):
		random_coeff = random.randint(1, bound-1)
		coefficients.append(random_coeff)
	coefficients.append(secret)
	# print(coefficients)
	return get_points(coefficients, shares, prime)

def get_points(coefficients, shares, prime):
	# Generate points based on polynomial
	# Param:
	#	coefficients: given byte
	#	shares: number of wanted shares
	# Return: List of shares, length = shares
	rev_coef = reversed(coefficients)
	points = []

	for x in range(0,shares+1):
		idx = 0
		y = 0
		for coef in rev_coef:
			variable = (x**idx) % prime
			idx += 1
			multiplication = coef * variable  % prime
			y = (y + multiplication) % prime 
		points.append((x,y))
	return points

def reconstruct(share_list, k, prime = _PRIME):
	# Reconstruct the polynomial 
	# Param:
	#	share_list: shares uploaded by users
	#	k: number of shares needed to reconstruct the polynomial
	# Return: secret
	x, y = zip(*share_list)
	secret = 0
	for i in range(len(share_list)):
		numerator = 1
		denominator = 1
		for j in range(len(share_list)):
			if i!=j:
				numerator = (numerator * x[j]) % prime
				denominator = (denominator * (x[j]-x[i])) % prime
		multiplication = numerator * inv_mod(denominator, prime)
		secret = (secret + prime + y[i] * multiplication) % prime
	return secret

print(reconstruct(generate_polynomial('t', 5, 4),4))