from django.db import models

class Tool(models.Model):
    user_id = models.CharField(max_length=50)
    tool_name = models.CharField(max_length=100)
    tool_code = models.CharField(max_length=50, unique=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_type = models.CharField(max_length=10,choices=([
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
    ]))
    image = models.ImageField(upload_to='tool_images/', null=True, blank=True)
    borrowed_quantity = models.PositiveIntegerField(default=0)  
    is_deleted = models.BooleanField(default=False)
    
    
    
    class Meta:
        db_table = 'Tool'
    

    def __str__(self):
        return f"{self.tool_name} ({self.tool_code})"
    


