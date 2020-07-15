from rest_framework.views import APIView
from rest_framework.response import Response
import datetime


class InsuranceFinder(APIView):
    def post(self, request):
        data = _data = request.data.copy()

        # Age factor for calculations
        AGE_FACTOR_DATA = {
            (18, 35): "25",
            (36, 45): "20",
            (46, 50): "15",
            (51, 55): "15",
        }

        if 'dob' in data:
            # checking the date format ..It should be in YYYY-mm-dd format
            try:
                date_of_birth = datetime.datetime.strptime(data['dob'], '%Y-%m-%d')
                date_of_birth = data['dob']
            except:
                return Response({"status": 400, 'message': 'Incorrect Date', "statusType": "failed"})
        else:
            return Response({"status": 400, 'message': 'Please Provide Date', "statusType": "failed"})

        # check if the age is provided else return response with error code
        if 'age' in data:
            age = int(data['age'])
        else:
            return Response({"status": 400, 'message': 'Please Provide Age', "statusType": "failed"})

        if age < 18 or age > 55:
            return Response({"status": 400, 'message': 'No Scheme Found', "statusType": "failed"})

        # check if the cover age is provided else return response with error code
        if 'cover_age' in data:
            try:
                cover_age = int(data['cover_age'])
            except Exception as e:
                return Response({"status": 400, 'message': 'Wrong Value for age', "statusType": "failed"})
        else:
            return Response({"status": 400, 'message': 'Please Provide Cover Age', "statusType": "failed"})

        if 'annual_income' in data:
            # user can type any kind of value in income field...so we need to catch the exception if he/she provide non integer type value
            try:
                cover_age = int(data['annual_income'])
            except Exception as e:
                return Response({"status": 400, 'message': 'Wrong Value for Annual Income', "statusType": "failed"})
        else:
            return Response({"status": 400, 'message': 'Please Provide Annual Income', "statusType": "failed"})

        # check if the smoking habit is provided else return response with error code
        if 'smoking' in data:
            if data['smoking'].lower() != 'n' and  data['smoking'].lower() != 'y':
                return Response({"status": 400, 'message': 'Wrong Input', "statusType": "failed"})
        else:
            return Response({"status": 400, 'message': 'Please Provide Smoking Habit', "statusType": "failed"})

        # finding the cover age as per the criteria
        if age > 18 and age < 55:
            smoking = data['smoking'].lower()
            if cover_age <= 65 and smoking == 'y':
                cover_age = int(data['cover_age'])
            elif cover_age > 65 and smoking == 'y':
                cover_age = 65

            if cover_age <= 75 and smoking == 'n':
                cover_age = int(data['cover_age'])
            elif cover_age > 75 and smoking == 'n':
                cover_age = 75

        # finding the maturity age
        if data['smoking'].lower() == 'n':
            maturity_age = 75
        else:
            maturity_age = 65

        # looping through age factor to find sum assured
        for key, value in AGE_FACTOR_DATA.items():
            if age >= key[0] and age <= key[1]:
                sum_assured = int(data['annual_income']) * int(value)

        # policy term is cover_age - age
        policy_term = cover_age - age

        # preparing json data to send in the response
        result = {
            'first_name' : data['firstname'],
            'lastname' : data['lastname'],
            'middlename' : data['middlename'],
            'dob' : date_of_birth,
            'gender' : data['gender'],
            'policy_term' : policy_term,
            'sum_assured' :sum_assured,
            'maturity_age':maturity_age
        }

        # sending the response
        return Response({"status": 200,'result':result, "statusType": "success"})
