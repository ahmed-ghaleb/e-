# rds/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from .models import RDSInstance
from .forms import RDSInstanceForm
import secrets
import string


@login_required
def rds_list(request):
    """
    Display list of RDS instances for the current user
    """
    instances = RDSInstance.objects.filter(created_by=request.user)
    
    # Search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        instances = instances.filter(
            database_name__icontains=search_query
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        instances = instances.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(instances, 10)  # Show 10 instances per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_title': 'RDS Instances',
        'instances': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'total_instances': instances.count(),
        'status_choices': RDSInstance.STATUS_CHOICES,
    }
    
    return render(request, 'rds/list.html', context)


@login_required
def rds_create(request):
    """
    Create a new RDS instance
    """
    if request.method == 'POST':
        form = RDSInstanceForm(request.POST)
        if form.is_valid():
            # Create the instance
            instance = form.save(commit=False)
            instance.created_by = request.user
            
            # Generate secure password
            instance.database_password = generate_secure_password()
            
            # Generate AWS identifier (simulate)
            instance.aws_instance_identifier = f"rds-{instance.database_name.lower().replace(' ', '-')}-{secrets.token_hex(4)}"
            
            # Generate service account and app usernames
            instance.service_account_username = f"svc_{instance.database_name.lower().replace(' ', '_')}"
            instance.app_username = f"app_{instance.database_name.lower().replace(' ', '_')}"
            
            instance.save()
            
            # Simulate RDS creation (in real implementation, this would call AWS API)
            try:
                create_aws_rds_instance(instance)
                messages.success(
                    request, 
                    f'RDS instance "{instance.database_name}" has been created successfully! '
                    f'It may take a few minutes to become available.'
                )
                return redirect('rds:list')
            except Exception as e:
                instance.status = 'failed'
                instance.save()
                messages.error(
                    request,
                    f'Failed to create RDS instance: {str(e)}'
                )
    else:
        form = RDSInstanceForm()
    
    context = {
        'page_title': 'Create RDS Instance',
        'form': form,
    }
    
    return render(request, 'rds/create.html', context)


@login_required
def rds_detail(request, instance_id):
    """
    Display detailed information about an RDS instance
    """
    instance = get_object_or_404(
        RDSInstance, 
        id=instance_id, 
        created_by=request.user
    )
    
    context = {
        'page_title': f'RDS Instance: {instance.database_name}',
        'instance': instance,
    }
    
    return render(request, 'rds/detail.html', context)


@login_required
@require_http_methods(["POST"])
def rds_delete(request, instance_id):
    """
    Delete an RDS instance
    """
    instance = get_object_or_404(
        RDSInstance, 
        id=instance_id, 
        created_by=request.user
    )
    
    try:
        # In real implementation, this would call AWS API to delete the instance
        delete_aws_rds_instance(instance)
        
        instance_name = instance.database_name
        instance.delete()
        
        messages.success(
            request,
            f'RDS instance "{instance_name}" has been deleted successfully.'
        )
        
        if request.headers.get('Accept') == 'application/json':
            return JsonResponse({'success': True})
            
    except Exception as e:
        messages.error(
            request,
            f'Failed to delete RDS instance: {str(e)}'
        )
        
        if request.headers.get('Accept') == 'application/json':
            return JsonResponse({'success': False, 'error': str(e)})
    
    return redirect('rds:list')


def generate_secure_password(length=16):
    """Generate a secure random password"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password


def create_aws_rds_instance(instance):
    """
    Simulate AWS RDS instance creation
    In production, this would use boto3 to actually create the RDS instance
    """
    import time
    import random
    
    # Simulate processing time
    time.sleep(1)
    
    # Simulate success/failure (90% success rate)
    if random.random() > 0.1:
        # Success - update instance with "AWS" details
        instance.status = 'available'
        instance.endpoint = f"{instance.aws_instance_identifier}.c123456789.us-east-1.rds.amazonaws.com"
        instance.port = 3306 if instance.engine == 'mysql' else 5432
        instance.save()
        return True
    else:
        # Simulate failure
        raise Exception("AWS RDS service temporarily unavailable")


def delete_aws_rds_instance(instance):
    """
    Simulate AWS RDS instance deletion
    In production, this would use boto3 to actually delete the RDS instance
    """
    import time
    import random
    
    # Simulate processing time
    time.sleep(0.5)
    
    # Simulate success/failure (95% success rate)
    if random.random() > 0.05:
        return True
    else:
        raise Exception("Failed to delete AWS RDS instance")