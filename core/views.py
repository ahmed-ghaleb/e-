# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from datetime import datetime, timedelta


@login_required
def dashboard(request):
    """
    Dashboard view for authenticated users
    Shows overview of RDS instances and system status
    """
    context = {
        'page_title': 'Dashboard',
        'user': request.user,
        'current_time': timezone.now(),
    }
    
    try:
        # Import RDS model dynamically to avoid circular imports
        from rds.models import RDSInstance
        
        # Get RDS statistics
        total_instances = RDSInstance.objects.filter(created_by=request.user).count()
        running_instances = RDSInstance.objects.filter(
            created_by=request.user, 
            status='available'
        ).count()
        
        # Recent instances (last 7 days)
        week_ago = timezone.now() - timedelta(days=7)
        recent_instances = RDSInstance.objects.filter(
            created_by=request.user,
            created_at__gte=week_ago
        ).order_by('-created_at')[:5]
        
        context.update({
            'total_instances': total_instances,
            'running_instances': running_instances,
            'recent_instances': recent_instances,
            'has_rds_data': True,
        })
        
    except Exception as e:
        # Handle case where RDS app/models don't exist yet
        context.update({
            'total_instances': 0,
            'running_instances': 0,
            'recent_instances': [],
            'has_rds_data': False,
        })
    
    # Add welcome message for first login
    if not request.session.get('welcomed', False):
        messages.success(
            request, 
            f'Welcome to e& Egypt Self-Service Portal, {request.user.first_name or request.user.username}!'
        )
        request.session['welcomed'] = True
    
    return render(request, 'core/dashboard.html', context)