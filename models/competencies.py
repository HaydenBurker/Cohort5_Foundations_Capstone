from date_operations import to_date

class Competency:
    table_name = "Competencies"
    competency_id = "competency_id"
    name = "name"
    date_created = "date_created"
    fields = (competency_id, name, date_created)
    
    def __init__(self, competency_id, name, date_created):
        self.competency_id = competency_id
        self.name = name
        self.date_created = date_created
        if type(date_created) == str:
            self.date_created = to_date(date_created)
    
    def __str__(self):
        return f'''Competency ID: {self.competency_id}
Name:          {self.name}
Date Created:  {self.date_created}'''