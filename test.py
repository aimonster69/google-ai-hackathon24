def fun():
  data_dict, d = {}, {}
  s = '''data_dict={
        'tbl_description': 'This table contains data on fatal police shootings in the United States.', 
        'columns': {
                    'id': {'col_description':'Unique identifier for each row', 'data_type':'int64'},
                    'name': {'col_description':'Name of the person who was shot', 'data_type':'object'},
                    'date': {'col_description':'Date of the shooting', 'data_type':'object'},
                    'manner_of_death': {'col_description':'Manner of death', 'data_type':'object'},
                    'armed': {'col_description':'Whether or not the person who was shot was armed', 'data_type':'object'},
                    'age': {'col_description':'Age of the person who was shot', 'data_type':'float64'},
                    'gender': {'col_description':'Gender of the person who was shot', 'data_type':'object'},
                    'race': {'col_description':'Race of the person who was shot', 'data_type':'object'},
                    'city': {'col_description':'City where the shooting occurred', 'data_type':'object'},
                    'state': {'col_description':'State where the shooting occurred', 'data_type':'object'},
                    'signs_of_mental_illness': {'col_description':'Whether or not the person who was shot showed signs of mental illness', 'data_type':'bool'},
                    'threat_level': {'col_description':'Level of threat posed by the person who was shot', 'data_type':'object'},
                    'flee': {'col_description':'Whether or not the person who was shot was fleeing from the police', 'data_type':'object'},
                    'body_camera': {'col_description':'Whether or not the shooting was captured on body camera', 'data_type':'bool'},
                    'age_categories': {'col_description':'Age category of the person who was shot', 'data_type':'object'}
                }
        }'''
  d['data_dict'] = data_dict
  exec(s,d)
  print(d['data_dict'])

fun()