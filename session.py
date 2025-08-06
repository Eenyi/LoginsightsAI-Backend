class LocalSession:
    session_data1 = {}
    session_history = []
    
    @classmethod
    def set(cls, key, value):
        cls.session_data1[key] = value
    
    @classmethod
    def get(cls, key):
         return cls.session_data1.get(key, None)
     
    @classmethod
    def set_history(cls, role, parts):
        session = {
            "role": role,
            "parts": [parts]
        }
        cls.session_history.append(session)
