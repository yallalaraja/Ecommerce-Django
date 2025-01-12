from django.core.exceptions import ValidationError

def validate_file_size(file):
    max_size_kb = 5000

    if file.size > max_size_kb*1024:
        raise ValidationError(f"File should not exceed {max_size_kb} KB")
        
    