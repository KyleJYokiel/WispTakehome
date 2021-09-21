from flask import Flask
from flask import request
from flask import abort
import shelve

# function specialMath(int n) {
# 	if(n==0) return 0
# 	else if(n==1) return 1
# 	else return n + specialMath(n-1) + specialMath(n-2)
# }

# Calculate and return the resulting number from the 'specialmath' algorithm
# above, translated into an iterative process for improved time complexity
# if a list of previously calculated values is provided, 
# the value is either taken from the existing calculated value, 
# or further values are calculated from the existing values
# for additional time saved for large values
def do_specialmath(num:int, list_calculated):
    if len(list_calculated) == 0:
        list_calculated.append(0)
        list_calculated.append(1)

    try:
        return list_calculated[num], list_calculated
    except IndexError:
        list_len = len(list_calculated)

        while list_len <= num:
            list_calculated.append(list_len + list_calculated[-1] + list_calculated[-2])
            list_len += 1

        return list_calculated[num], list_calculated


app = Flask(__name__)

@app.route("/specialmath/<int:number>", methods = ['GET'])
def specialmath(number):
    with shelve.open('special_numbers') as special_numbers:    
        method = request.method

        if not 'numbers_list' in special_numbers:
            special_numbers['numbers_list'] = []

        if method == 'GET':
            return_val, return_list = do_specialmath(number, special_numbers['numbers_list'])
            special_numbers['numbers_list'] = return_list

            return str(return_val)
        else:
            return abort(501)