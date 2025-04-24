import math

def round_number(num, minimum_power=1):
	if num < 10 ** minimum_power:
		return 10 ** minimum_power
	else:
		order = math.floor(math.log10(num))
		round_base = 10 ** max(minimum_power, order)
		return int(round(num / round_base) * round_base)