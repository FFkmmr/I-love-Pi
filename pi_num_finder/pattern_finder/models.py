from django.db import models

class PiMil(models.Model):
    mil_number = models.PositiveIntegerField()  
    text = models.TextField()

    def __str__(self):
        return f"Chunk #{self.mil_number}"