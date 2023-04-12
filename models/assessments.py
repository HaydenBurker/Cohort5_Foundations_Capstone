from date_operations import to_date

class Assessment:
    table_name = "Assessments"
    assessment_id = "assessment_id"
    competency_id = "competency_id"
    name = "name"
    date_created = "date_created"
    fields = (assessment_id, competency_id, name, date_created)
    
    def __init__(self, assessment_id, competency_id, name, date_created):
        self.assessment_id = assessment_id
        self.competency_id = competency_id
        self.name = name
        if type(date_created) == str:
            self.date_created = to_date(date_created)
        else:
            self.date_created = date_created
    
    def __str__(self):
        return f'''Assessment ID: {self.assessment_id}
Competency ID: {self.competency_id}
Name:          {self.name}
Date Created:  {self.date_created}'''