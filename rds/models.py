# rds/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class RDSInstance(models.Model):
    """Model to represent AWS RDS instances"""
    
    STATUS_CHOICES = [
        ('creating', 'Creating'),
        ('available', 'Available'),
        ('modifying', 'Modifying'),
        ('deleting', 'Deleting'),
        ('deleted', 'Deleted'),
        ('failed', 'Failed'),
    ]
    
    ENGINE_CHOICES = [
        ('mysql', 'MySQL'),
        ('postgres', 'PostgreSQL'),
        ('mariadb', 'MariaDB'),
        ('oracle', 'Oracle'),
        ('sqlserver', 'SQL Server'),
    ]
    
    # Basic Information
    database_name = models.CharField(max_length=100, unique=True)
    expected_size = models.CharField(max_length=50, help_text="Expected database size (e.g., 10GB, 100GB)")
    
    # AWS RDS Information
    aws_instance_identifier = models.CharField(max_length=200, blank=True, null=True)
    endpoint = models.CharField(max_length=500, blank=True, null=True)
    port = models.IntegerField(default=3306)
    engine = models.CharField(max_length=20, choices=ENGINE_CHOICES, default='mysql')
    
    # Database Credentials
    database_username = models.CharField(max_length=100, default='admin')
    database_password = models.CharField(max_length=255, blank=True, null=True)
    service_account_username = models.CharField(max_length=100, blank=True, null=True)
    app_username = models.CharField(max_length=100, blank=True, null=True)
    
    # Status and Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='creating')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rds_instances')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # AWS Resource Information
    instance_class = models.CharField(max_length=50, default='db.t3.micro')
    allocated_storage = models.IntegerField(default=20, help_text="Storage in GB")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'RDS Instance'
        verbose_name_plural = 'RDS Instances'
    
    def __str__(self):
        return f"{self.database_name} ({self.status})"
    
    def get_connection_string(self):
        """Generate connection string for the database"""
        if self.endpoint and self.database_username:
            return f"{self.engine}://{self.database_username}:[PASSWORD]@{self.endpoint}:{self.port}/{self.database_name}"
        return "Not available yet"
    
    def is_available(self):
        """Check if instance is available for use"""
        return self.status == 'available'