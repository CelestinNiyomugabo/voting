from django.shortcuts import render, get_object_or_404
from .models import Election, Candidate, Vote
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from .forms import VoteForm
from django.http import JsonResponse

def election_list(request):
    elections = Election.objects.all()
    now = timezone.now()
    return render(request, 'election/list.html', {'contests': elections, 'now': now})

def election_vote(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    candidates = Candidate.objects.filter(election=election)

    if request.method == 'POST':
        # Process voting form submission
        candidate_id = request.POST.get('candidate')
        candidate = get_object_or_404(Candidate, pk=candidate_id)
        voter_data = {
            'voter_name': request.POST.get('name'),
            'voter_email': request.POST.get('email'),
            'voter_gender': request.POST.get('gender'),
            'voter_province': request.POST.get('province'),
            'voter_phone': request.POST.get('phone')
        }

        # Save the vote
        vote = Vote.objects.create(candidate=candidate, **voter_data)
        
        # Send confirmation email
        send_mail(
            'Your Vote Confirmation',
            f'Thank you for voting in the election: {election.name}. You voted for {candidate.name}.',
            'admin@votingplatform.com',
            [voter_data['voter_email']],
        )

        messages.success(request, 'Your vote has been submitted successfully!')

    return render(request, 'election/vote.html', {'election': election, 'candidates': candidates})



def dashboard(request):
    votes_per_candidate = Vote.objects.values('candidate__name').annotate(vote_count=Count('id'))
    votes_per_gender = Vote.objects.values('voter_gender').annotate(vote_count=Count('id'))
    votes_per_province = Vote.objects.values('voter_province').annotate(vote_count=Count('id'))

    return render(request, 'election/dashboard.html', {
        'votes_per_candidate': votes_per_candidate,
        'votes_per_gender': votes_per_gender,
        'votes_per_province': votes_per_province
    })

def about(request):
    return render(request, 'election/about.html')

def voting_form(request, contest_id):
    contest = get_object_or_404(Election, id=contest_id)
    candidates = Candidate.objects.filter(election=contest)  # Filter based on contest
    form = VoteForm()

    return render(request, 'election/voting_form.html', {
        'contest': contest,
        'candidates': candidates,
        'form': form,
    })

def submit_vote(request):
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            # Save the vote and process the data
            return JsonResponse({'success': True})
        else:
            # If form is invalid, re-render the form with error messages
            return JsonResponse({'success': False, 'html': render_to_string('voting_form.html', {'form': form})})