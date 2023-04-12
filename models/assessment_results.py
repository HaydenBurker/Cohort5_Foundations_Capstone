from date_operations import to_datetime

class AssessmentResult:
    table_name = "Assessment_Results"
    result_id = "result_id"
    user_id = "user_id"
    assessment_id = "assessment_id"
    manager_id = "manager_id"
    score = "score"
    date_taken = "date_taken"
    fields = (result_id, user_id, assessment_id, manager_id, score, date_taken)

    def __init__(self,result_id, user_id, assessment_id, manager_id, score, date_taken):
        self.result_id = result_id
        self.user_id = user_id
        self.assessment_id = assessment_id
        self.manager_id = manager_id
        self.score = score
        if type(date_taken) == str:
            self.date_taken = to_datetime(date_taken)
        else:
            self.date_taken = date_taken
    
    def __str__(self):
        return f'''Result ID:     {self.result_id}
User ID:       {self.user_id}
Assessment ID: {self.assessment_id}
Manager ID:    {self.manager_id}
Score:         {self.score}
Date Taken:    {self.date_taken}'''