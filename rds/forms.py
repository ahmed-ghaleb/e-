# rds/forms.py
from django import forms
from .models import RDSInstance


class RDSInstanceForm(forms.ModelForm):
    """Form for creating RDS instances"""
    
    class Meta:
        model = RDSInstance
        fields = ['database_name', 'expected_size', 'engine', 'instance_class', 'allocated_storage']
        
        widgets = {
            'database_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter database name (e.g., myapp-db)',
                'required': True,
            }),
            'expected_size': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter expected size (e.g., 50GB, 1TB)',
                'required': True,
            }),
            'engine': forms.Select(attrs={
                'class': 'form-control',
            }),
            'instance_class': forms.Select(attrs={
                'class': 'form-control',
            }),
            'allocated_storage': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '20',
                'max': '1000',
                'placeholder': '20',
            }),
        }
        
        labels = {
            'database_name': 'Database Name',
            'expected_size': 'Expected Database Size',
            'engine': 'Database Engine',
            'instance_class': 'Instance Type',
            'allocated_storage': 'Storage (GB)',
        }
        
        help_texts = {
            'database_name': 'Choose a unique name for your database instance',
            'expected_size': 'Estimate the size your database will grow to',
            'engine': 'Select the database engine you want to use',
            'instance_class': 'Choose the instance size based on your performance needs',
            'allocated_storage': 'Initial storage allocation in GB (minimum 20GB)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add instance class choices
        self.fields['instance_class'] = forms.ChoiceField(
            choices=[
                ('db.t3.micro', 'db.t3.micro (1 vCPU, 1GB RAM) - Free Tier'),
                ('db.t3.small', 'db.t3.small (1 vCPU, 2GB RAM)'),
                ('db.t3.medium', 'db.t3.medium (2 vCPU, 4GB RAM)'),
                ('db.t3.large', 'db.t3.large (2 vCPU, 8GB RAM)'),
                ('db.m5.large', 'db.m5.large (2 vCPU, 8GB RAM)'),
                ('db.m5.xlarge', 'db.m5.xlarge (4 vCPU, 16GB RAM)'),
                ('db.r5.large', 'db.r5.large (2 vCPU, 16GB RAM)'),
            ],
            widget=forms.Select(attrs={'class': 'form-control'}),
            initial='db.t3.micro'
        )
    
    def clean_database_name(self):
        """Validate database name"""
        database_name = self.cleaned_data.get('database_name')
        
        if not database_name:
            raise forms.ValidationError("Database name is required.")
        
        # Check for valid characters
        if not database_name.replace('-', '').replace('_', '').isalnum():
            raise forms.ValidationError(
                "Database name can only contain letters, numbers, hyphens, and underscores."
            )
        
        # Check length
        if len(database_name) < 3:
            raise forms.ValidationError("Database name must be at least 3 characters long.")
        
        if len(database_name) > 50:
            raise forms.ValidationError("Database name cannot be more than 50 characters long.")
        
        # Check for uniqueness
        if RDSInstance.objects.filter(database_name__iexact=database_name).exists():
            raise forms.ValidationError("A database with this name already exists.")
        
        return database_name
    
    def clean_expected_size(self):
        """Validate expected size format"""
        expected_size = self.cleaned_data.get('expected_size')
        
        if not expected_size:
            raise forms.ValidationError("Expected size is required.")
        
        # Basic validation - should contain numbers and units
        expected_size = expected_size.upper().strip()
        valid_units = ['GB', 'TB', 'MB']
        
        if not any(unit in expected_size for unit in valid_units):
            raise forms.ValidationError(
                "Expected size should include units (GB, TB, or MB). Example: 50GB"
            )
        
        return expected_size
    
    def clean_allocated_storage(self):
        """Validate allocated storage"""
        allocated_storage = self.cleaned_data.get('allocated_storage')
        
        if allocated_storage < 20:
            raise forms.ValidationError("Minimum storage allocation is 20GB.")
        
        if allocated_storage > 1000:
            raise forms.ValidationError("Maximum storage allocation is 1000GB for this form.")
        
        return allocated_storage