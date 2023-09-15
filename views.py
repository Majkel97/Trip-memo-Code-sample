from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST


@login_required(login_url="/signin")
def add_member(request, pk):
    """
    A view for adding a member to a trip.

    Args:
        pk (int): The ID of the trip to add a member to.

    """
    if request.method == "POST":
        form = TripMemberInvitationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["member_email"] != request.user.email:
                invitation = form.save(commit=False)
                invitation.trip = Trip.objects.get(id=pk)
                invitation.invited_by = request.user.profile
                try:
                    member = User.objects.get(email=invitation.member_email).profile
                    if member in invitation.trip.members.all():
                        messages.error(request, "This user is already invited!")
                        return HttpResponse(status=204)
                    invitation.trip.members.add(member)
                    invitation.trip.save()

                    _send_notification_email(invitation)
                    messages.success(request, "Member invited!")
                    return HttpResponse(
                        status=204,
                        headers={"HX-Trigger": json.dumps({"memberListChanged": None})},
                    )
                except User.DoesNotExist:
                    _send_invite_email(invitation)
                    invitation.save()
                    messages.success(request, "Member invited!")
                    return HttpResponse(status=204)
            else:
                messages.error(request, "You can't invite yourself!")
                return HttpResponse(status=406)
        else:
            messages.error(request, "Invalid form")
    else:
        form = TripMemberInvitationForm()

    context = {"form": form}
    return render(request, "trips/add_member.html", context)


def create_note(request, pk):
    """
    A view for creating a note associated with a trip.

    Args:
        pk (int): The ID of the trip to create a note for.

    Template:
        trips/create_edit_note.html

    """
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.trip = Trip.objects.get(id=pk)
            note.save()
            messages.success(request, "Note created.")
            return HttpResponse(
                status=204,
                headers={"HX-Trigger": json.dumps({"noteListChanged": None})},
            )
    else:
        form = NoteForm()
    context = {"form": form}
    return render(request, "trips/create_edit_note.html", context)


@login_required(login_url="/signin")
@require_POST
def delete_note(request, pk):
    """
    A view for deleting a note associated with a trip.

    Args:
        pk (int): The ID of the note to delete.

    """
    note = get_object_or_404(Note, id=pk)
    note.delete()
    messages.success(request, "Note deleted.")
    return HttpResponse(
        status=204,
        headers={"HX-Trigger": json.dumps({"noteListChanged": None})},
    )