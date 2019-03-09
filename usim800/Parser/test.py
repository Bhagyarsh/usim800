from  JsonParser import ATJSONObjectParser

data = """
kfjgifdjgiojidsjgiwdssge 23 32532 dgdg 123213 df df21e  
{ 
  "accounting"  : [   
                     { "firstName" : "John",  
                       "lastName"  : "Doe",
                       "age"       : 23 },

                     { "firstName" : "Mary",  
                       "lastName"  : "Smith",
                        "age"      : 32 }
                 ],                            
  "sales"      : [ 
                     { "firstName" : "Sally", 
                       "lastName"  : "Green",
                        "age"      : 27 },

                     { "firstName" : "Jim",   
                       "lastName"  : "Galley",
                       "age"       : 41 }
                 ] 
} kfjgifdjgiojidsjgiwdssge 23 32532 dgdg 123213 df df21e 
"""
data = "bhagyarsh"
jop = ATJSONObjectParser(data)
print(jop.JSONObjectPresent)
# print(type(jop.JSONObject[0]))