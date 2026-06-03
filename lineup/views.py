from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max, Count, Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from .models import Session, Participant, EventRegistration, EventRegistrationEntry


@login_required
def index(request):
    """Participant page"""
    sessions = Session.objects.all()
    if not sessions.exists():
        session = Session.objects.create(name="Main Room")
    else:
        session = sessions.first()

    queue = Participant.objects.filter(session=session, is_completed=False)
    user_in_queue = queue.filter(screen_name=request.user.username).first()

    context = {
        'session': session,
        'queue': queue,
        'user_in_queue': user_in_queue,
    }
    return render(request, 'participant.html', context)


def register_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('lineup:admin_panel')
        return redirect('lineup:index')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not password:
            messages.error(request, 'Username and password are required.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            if user.is_staff:
                return redirect('lineup:admin_panel')
            return redirect('lineup:index')

    return render(request, 'register.html')


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('lineup:admin_panel')
        return redirect('lineup:index')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('lineup:admin_panel')
            return redirect('lineup:index')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('lineup:login')


@login_required
def host(request):
    """Host/Admin control panel - merged single page"""
    if not request.user.is_staff:
        return redirect('lineup:index')

    sessions_qs = Session.objects.all()
    if not sessions_qs.exists():
        session = Session.objects.create(name="Main Room")
    else:
        session = sessions_qs.first()

    queue = Participant.objects.filter(session=session, is_completed=False)
    completed = Participant.objects.filter(session=session, is_completed=True)

    context = {
        'session': session,
        'queue': queue,
        'completed': completed,
    }

    if request.user.is_superuser:
        sessions_list = Session.objects.annotate(
            total_count=Count('participants'),
            active_count=Count('participants', filter=Q(participants__is_completed=False))
        ).order_by('-created_at')
        users = User.objects.all().order_by('-date_joined')
        active_participants = Participant.objects.filter(is_completed=False).select_related('session').order_by('session', 'position')
        completed_participants = Participant.objects.filter(is_completed=True).select_related('session').order_by('session', '-added_at')
        context.update({
            'sessions': sessions_list,
            'users': users,
            'active_participants': active_participants,
            'completed_participants': completed_participants,
        })

    return render(request, 'host_admin.html', context)


@login_required
def admin_panel(request):
    return redirect('lineup:host')


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def admin_create_session(request):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    data = json.loads(request.body)
    name = data.get('name', '').strip()
    if not name:
        return JsonResponse({'success': False, 'message': 'Session name is required.'})

    session = Session.objects.create(name=name)
    return JsonResponse({'success': True, 'session': {'id': session.id, 'name': session.name}})


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def admin_delete_session(request):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    data = json.loads(request.body)
    session_id = data.get('session_id')
    try:
        session = Session.objects.get(id=session_id)
        session.delete()
        return JsonResponse({'success': True})
    except Session.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Session not found.'})


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def admin_toggle_staff(request):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    data = json.loads(request.body)
    user_id = data.get('user_id')
    role = data.get('role')  # 'admin', 'host', or 'user'
    if role not in ('admin', 'host', 'user'):
        return JsonResponse({'success': False, 'message': 'Invalid role.'})
    try:
        user = User.objects.get(id=user_id)
        if user == request.user:
            return JsonResponse({'success': False, 'message': 'Cannot modify your own role.'})
        if role == 'admin':
            user.is_staff = True
            user.is_superuser = True
        elif role == 'host':
            user.is_staff = True
            user.is_superuser = False
        else:
            user.is_staff = False
            user.is_superuser = False
        user.save()
        return JsonResponse({'success': True, 'role': role})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'User not found.'})


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def admin_delete_user(request):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    data = json.loads(request.body)
    user_id = data.get('user_id')
    try:
        user = User.objects.get(id=user_id)
        if user == request.user:
            return JsonResponse({'success': False, 'message': 'Cannot delete your own account.'})
        user.delete()
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'User not found.'})


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def admin_clear_completed(request):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    data = json.loads(request.body)
    session_id = data.get('session_id')
    if session_id:
        Participant.objects.filter(session_id=session_id, is_completed=True).delete()
    else:
        Participant.objects.filter(is_completed=True).delete()
    return JsonResponse({'success': True})


@require_http_methods(["POST"])
@csrf_exempt
def raise_hand(request):
    """Add the logged-in user to the queue"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Please log in first'}, status=401)

    try:
        screen_name = request.user.username
        session = Session.objects.first() or Session.objects.create(name="Main Room")

        existing = Participant.objects.filter(session=session, screen_name=screen_name).first()
        if existing and not existing.is_completed:
            return JsonResponse({'success': False, 'message': 'Already in lineup!'})

        max_position = Participant.objects.filter(session=session).aggregate(Max('position'))['position__max'] or 0

        if existing:
            existing.is_completed = False
            existing.position = max_position + 1
            existing.save()
        else:
            Participant.objects.create(
                session=session,
                screen_name=screen_name,
                position=max_position + 1
            )

        queue = list(Participant.objects.filter(session=session, is_completed=False).values_list('screen_name', flat=True))
        return JsonResponse({'success': True, 'message': 'Added to lineup!', 'queue': queue})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def leave_queue(request):
    """Remove the logged-in user from the queue"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Please log in first'}, status=401)

    try:
        screen_name = request.user.username
        session = Session.objects.first() or Session.objects.create(name="Main Room")
        participant = Participant.objects.get(session=session, screen_name=screen_name, is_completed=False)
        participant.delete()

        queue = list(Participant.objects.filter(session=session, is_completed=False).values_list('screen_name', flat=True))
        return JsonResponse({'success': True, 'message': 'You left the queue', 'queue': queue})

    except Participant.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'You are not in the queue'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def next_participant(request):
    """Move to next participant (skips on-hold participants)"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)
    try:
        session = Session.objects.first() or Session.objects.create(name="Main Room")
        next_p = Participant.objects.filter(session=session, is_completed=False, is_on_hold=False).first()

        if not next_p:
            all_active = Participant.objects.filter(session=session, is_completed=False).exists()
            if all_active:
                return JsonResponse({'success': False, 'message': 'All remaining participants are on hold'})
            return JsonResponse({'success': False, 'message': 'Queue is empty'})

        current_name = next_p.screen_name
        next_p.is_completed = True
        next_p.save()

        queue = list(Participant.objects.filter(session=session, is_completed=False).values_list('screen_name', flat=True))

        return JsonResponse({'success': True, 'message': f'NEXT UP: {current_name}', 'current': current_name, 'queue': queue})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def admin_toggle_hold(request):
    """Toggle on-hold status for any participant (staff only)"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    try:
        data = json.loads(request.body)
        screen_name = data.get('screen_name', '').strip()
        if not screen_name:
            return JsonResponse({'success': False, 'message': 'screen_name is required'})

        session = Session.objects.first() or Session.objects.create(name="Main Room")
        participant = Participant.objects.get(session=session, screen_name=screen_name, is_completed=False)
        participant.is_on_hold = not participant.is_on_hold
        participant.save()

        return JsonResponse({'success': True, 'is_on_hold': participant.is_on_hold, 'screen_name': screen_name})

    except Participant.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Participant not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def toggle_hold(request):
    """Toggle the on-hold status of the logged-in user"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Please log in first'}, status=401)

    try:
        screen_name = request.user.username
        session = Session.objects.first() or Session.objects.create(name="Main Room")
        participant = Participant.objects.get(session=session, screen_name=screen_name, is_completed=False)
        participant.is_on_hold = not participant.is_on_hold
        participant.save()

        queue = list(
            Participant.objects.filter(session=session, is_completed=False)
            .order_by('position')
            .values('screen_name', 'is_on_hold')
        )
        return JsonResponse({
            'success': True,
            'is_on_hold': participant.is_on_hold,
            'queue': [{'name': p['screen_name'], 'on_hold': p['is_on_hold']} for p in queue],
        })

    except Participant.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'You are not in the queue'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def clear_queue(request):
    """Clear entire queue"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)
    try:
        session = Session.objects.first() or Session.objects.create(name="Main Room")
        Participant.objects.filter(session=session, is_completed=False).delete()
        
        return JsonResponse({'success': True, 'message': 'Queue cleared', 'queue': []})
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@require_http_methods(["GET"])
def get_queue(request):
    """Get current queue"""
    session = Session.objects.first() or Session.objects.create(name="Main Room")
    participants = list(
        Participant.objects.filter(session=session, is_completed=False)
        .order_by('position')
        .values('screen_name', 'is_on_hold')
    )
    queue = [p['screen_name'] for p in participants]
    on_hold = [p['screen_name'] for p in participants if p['is_on_hold']]
    return JsonResponse({'queue': queue, 'on_hold': on_hold})


@require_http_methods(["GET"])
def full_state(request):
    """Get full queue + completed state for the main session"""
    session = Session.objects.first() or Session.objects.create(name="Main Room")
    queue = list(
        Participant.objects.filter(session=session, is_completed=False)
        .order_by('position')
        .values('screen_name', 'position', 'added_at', 'is_on_hold')
    )
    completed = list(
        Participant.objects.filter(session=session, is_completed=True)
        .order_by('-added_at')
        .values('screen_name')
    )
    return JsonResponse({
        'queue': [{'name': p['screen_name'], 'position': p['position'],
                   'added_at': p['added_at'].strftime('%H:%M:%S'),
                   'on_hold': p['is_on_hold']} for p in queue],
        'completed': [p['screen_name'] for p in completed],
        'queue_count': len(queue),
        'completed_count': len(completed),
    })


@login_required
@require_http_methods(["GET"])
def admin_state(request):
    """Get all participants across all sessions for admin view"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    active = list(
        Participant.objects.filter(is_completed=False)
        .select_related('session')
        .order_by('session', 'position')
        .values('screen_name', 'position', 'session__name', 'added_at')
    )
    completed = list(
        Participant.objects.filter(is_completed=True)
        .select_related('session')
        .order_by('session', '-added_at')
        .values('screen_name', 'session__name')
    )
    return JsonResponse({
        'active': [{'name': p['screen_name'], 'position': p['position'],
                    'session': p['session__name'], 'added_at': p['added_at'].strftime('%H:%M')}
                   for p in active],
        'completed': [{'name': p['screen_name'], 'session': p['session__name']}
                      for p in completed],
    })


@require_http_methods(["POST"])
@csrf_exempt
def remove_participant(request):
    """Remove a participant from queue"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)
    try:
        data = json.loads(request.body)
        screen_name = data.get('screen_name', '').strip()
        
        session = Session.objects.first() or Session.objects.create(name="Main Room")
        participant = Participant.objects.get(session=session, screen_name=screen_name, is_completed=False)
        participant.delete()
        
        queue = list(Participant.objects.filter(session=session, is_completed=False).values_list('screen_name', flat=True))
        
        return JsonResponse({'success': True, 'message': f'{screen_name} removed', 'queue': queue})
    
    except Participant.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Participant not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


# ===== REGISTRATION VIEWS =====

@require_http_methods(["GET"])
def get_registrations(request):
    """Get all active registrations with counts and user registration status"""
    regs = EventRegistration.objects.filter(is_active=True).order_by('-created_at')

    user_registered_ids = set()
    if request.user.is_authenticated:
        user_registered_ids = set(
            EventRegistrationEntry.objects.filter(user=request.user)
            .values_list('registration_id', flat=True)
        )

    result = []
    for reg in regs:
        result.append({
            'id': reg.id,
            'title': reg.title,
            'description': reg.description,
            'count': reg.entries.count(),
            'registered': reg.id in user_registered_ids,
            'created_by': reg.created_by.username,
            'created_by_id': reg.created_by_id,
        })

    return JsonResponse({'registrations': result})


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def create_registrations(request):
    """Batch-create registrations (Admin or Host)"""
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    data = json.loads(request.body)
    items = data.get('items', [])

    if not items:
        return JsonResponse({'success': False, 'message': 'At least one registration is required.'})

    created = []
    for item in items:
        title = item.get('title', '').strip()
        description = item.get('description', '').strip()
        if not title:
            continue
        reg = EventRegistration.objects.create(
            title=title,
            description=description,
            created_by=request.user,
        )
        created.append({
            'id': reg.id,
            'title': reg.title,
            'description': reg.description,
            'count': 0,
            'registered': False,
            'created_by': request.user.username,
            'created_by_id': request.user.id,
        })

    if not created:
        return JsonResponse({'success': False, 'message': 'No valid registrations provided.'})

    return JsonResponse({'success': True, 'registrations': created})


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def edit_registration(request):
    """Edit a registration (Admin: any; Host: own only)"""
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    data = json.loads(request.body)
    reg_id = data.get('id')
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()

    if not title:
        return JsonResponse({'success': False, 'message': 'Title is required.'})

    try:
        reg = EventRegistration.objects.get(id=reg_id)
    except EventRegistration.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Registration not found.'})

    if not request.user.is_superuser and reg.created_by != request.user:
        return JsonResponse({'success': False, 'message': 'You can only edit your own registrations.'}, status=403)

    reg.title = title
    reg.description = description
    reg.save()

    return JsonResponse({'success': True, 'registration': {
        'id': reg.id,
        'title': reg.title,
        'description': reg.description,
    }})


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def delete_registration(request):
    """Delete a registration (Admin: any; Host: own only)"""
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    data = json.loads(request.body)
    reg_id = data.get('id')

    try:
        reg = EventRegistration.objects.get(id=reg_id)
    except EventRegistration.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Registration not found.'})

    if not request.user.is_superuser and reg.created_by != request.user:
        return JsonResponse({'success': False, 'message': 'You can only delete your own registrations.'}, status=403)

    reg.delete()
    return JsonResponse({'success': True})


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def register_for_event(request):
    """User registers for a specific event"""
    data = json.loads(request.body)
    reg_id = data.get('id')

    try:
        reg = EventRegistration.objects.get(id=reg_id, is_active=True)
    except EventRegistration.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Registration not found.'})

    if EventRegistrationEntry.objects.filter(registration=reg, user=request.user).exists():
        return JsonResponse({'success': False, 'message': 'Already registered!'})

    EventRegistrationEntry.objects.create(registration=reg, user=request.user)
    count = reg.entries.count()
    return JsonResponse({'success': True, 'count': count})


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def unregister_from_event(request):
    """User unregisters from a specific event"""
    data = json.loads(request.body)
    reg_id = data.get('id')

    try:
        entry = EventRegistrationEntry.objects.get(registration_id=reg_id, user=request.user)
        entry.delete()
        count = EventRegistration.objects.get(id=reg_id).entries.count()
        return JsonResponse({'success': True, 'count': count})
    except EventRegistrationEntry.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Not registered.'})
    except EventRegistration.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Registration not found.'})


@login_required
@require_http_methods(["GET"])
def get_registration_entries(request, reg_id):
    """Return the list of users registered for a specific event (staff only)"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    try:
        reg = EventRegistration.objects.get(id=reg_id)
    except EventRegistration.DoesNotExist:
        return JsonResponse({'error': 'Registration not found.'}, status=404)

    entries = (
        EventRegistrationEntry.objects
        .filter(registration=reg)
        .select_related('user')
        .order_by('registered_at')
    )

    return JsonResponse({
        'title': reg.title,
        'entries': [
            {
                'username': e.user.username,
                'registered_at': e.registered_at.strftime('%b %d, %Y %H:%M'),
            }
            for e in entries
        ],
    })
