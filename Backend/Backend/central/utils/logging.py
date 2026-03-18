import logging

class SafeFormatter(logging.Formatter):
    def format(self, record):
        
        if not hasattr(record, "user"):
            record.user = "anonymous"
            
        if not hasattr(record, "id"):
            record.id = "-"
            
        return super().format(record)