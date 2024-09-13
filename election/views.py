from django.shortcuts import render, get_object_or_404, redirect
from .models import Election, Candidate, Vote, Auca_User
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from .forms import VoteForm
from django.http import JsonResponse
import random
from django.views.decorators.csrf import csrf_exempt
from .whatsapp import send_whatsapp_message
import requests
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Count, Q



OTP_STORAGE = {}


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
            'Your vote confirmation',
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

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from .models import Blog
from django import forms


# class ArticleListView(ListView):
#     model = Blog
#     ordering = ['-timestamp'] 
#     template_name = 'blog/home.html'


class ContestView(DetailView):
    model = Election
    template_name = 'election/contest.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ConntestCreate(CreateView):
    model = Election
    fields = ['name', 'description', 'start_date', 'end_date']
    template_name = 'election/add_contest.html'
    success_url = reverse_lazy('home') 
    def get_form(self, form_class=None):
        form = super(ConntestCreate, self).get_form(form_class)
        form.fields['name'].widget = forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter the contest name (eg: Miss Rwanda)'
        })
        form.fields['description'].widget = forms.Textarea(attrs={
            'class': 'form-control ckeditor',
            'placeholder': 'Enter the contest description'
        })
        form.fields['start_date'].widget = forms.DateTimeInput(attrs={
            'class': 'form-control',
            'placeholder': 'Date',
            'type': 'datetime-local'
        })
        form.fields['end_date'].widget = forms.DateTimeInput(attrs={
            'class': 'form-control',
            'placeholder': 'Date',
            'type': 'datetime-local'
        })
        return form


class ContestUpdate(UpdateView):
    model = Election
    fields = ['name', 'description', 'start_date', 'end_date']
    template_name = 'election/add_contest.html'
    success_url = reverse_lazy('home') 
    
    def get_form(self, form_class=None):
        form = super(ContestUpdate, self).get_form(form_class)
        form.fields['name'].widget = forms.TextInput(attrs={
            'class': 'form-control'
        })
        form.fields['description'].widget = forms.Textarea(attrs={
            'class': 'form-control ckeditor'
        })
        form.fields['start_date'].widget = forms.DateTimeInput(attrs={
            'class': 'form-control',
            'placeholder': 'Date',
            'type': 'datetime-local'
        })
        form.fields['end_date'].widget = forms.DateTimeInput(attrs={
            'class': 'form-control',
            'placeholder': 'Date',
            'type': 'datetime-local'
        })
        return form


class ContestDelete(DeleteView):
    model = Election
    success_url = reverse_lazy('home')



class ConntestantCreate(CreateView):
    model = Candidate
    fields = ['name', 'email', 'election', 'image']
    template_name = 'election/add_contestant.html'
    success_url = reverse_lazy('home') 
    def get_form(self, form_class=None):
        form = super(ConntestantCreate, self).get_form(form_class)
        form.fields['name'].widget = forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter the contestant name'
        })
        form.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter contestant email'
        })
        
       
        return form

def voting_form(request, contest_id):
    contest = get_object_or_404(Election, id=contest_id)
    candidates = Candidate.objects.filter(election=contest)  
    form = VoteForm()
    return render(request, 'election/voting_form.html', { 'contest': contest,'candidates': candidates,})

    

def generate_otp():
    return random.randint(100000, 999999)



@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        election_id = request.POST.get('election_id')

        # if Vote.objects.filter(voter_email=email, election_id=election_id).exists():
        #     return JsonResponse({'status': 'voted', 'message': 'You have already voted in this election'})
        #     return render(request, 'election/voting_confirmation.html', {'success': False, 'message': 'You have already voted in this election.'})


        if email and phone:
            otp = generate_otp()
            request.session['email'] = email
            request.session['phone'] = phone
            request.session['otp'] = otp
            request.session['election_id'] = election_id

           
            send_mail(
                'Your OTP Code',
                f'Your AUCA platform voting OTP code is {otp}',
                settings.DEFAULT_FROM_EMAIL, 
                [email],
                fail_silently=False,
            )
            
       
            send_whatsapp_message(phone, otp)
            
            # return response

            # print(f'SMS OTP sent to {phone}: {otp}')

            return JsonResponse({'status': 'success'})
        
        return JsonResponse({'status': 'error', 'message': 'Invalid email or phone'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def send_email(email, subject, message):
    try:
        # Send the email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL, 
            email,
            fail_silently=False,  
        )
        return JsonResponse({'status': 'success', 'message': 'Email sent successfully!'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    

def test_otp(request):
    phone = "250788604106"
    code = "1234"
    response = send_telegram_message('5551929479', code)
    return response


def send_telegram_message(chat_id, message):
    telegram_token = "7503721863:AAFWPm6sPltDFmuLeF7bQaSSmfPx60U_Tsw"
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,   
        "text": message,     
        "parse_mode": "HTML"  
    }
    
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error sending message: {response.text}")
    

@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        stored_otp = request.session.get('otp')
        if int(otp_code) == int(stored_otp):
            return JsonResponse({'status': 'verified'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid OTP'})




def submit_vote(request):
    if request.method == 'POST':
        voter_email = request.session.get('email')
        election_id = request.session.get('election_id')

        if Vote.objects.filter(voter_email=voter_email, election_id=election_id).exists():
            return render(request, 'election/voting_confirmation.html', {'success': False, 'message': 'You have already voted in this election.'})
            return JsonResponse({'success': False, 'message': 'You have already voted in this election.'})

        vote = Vote.objects.create(
            candidate=Candidate.objects.get(id=request.POST.get('candidate_id')),
            election=Election.objects.get(id=election_id),
            voter_gender=request.POST.get('gender'),
            voter_name=request.POST.get('name'),
            voter_province=request.POST.get('province'),
            voter_email=voter_email,
            voter_phone=request.session.get('phone')
        )
        return render(request, 'election/voting_confirmation.html', {'success': True, 'message': 'Vote submitted successfully.'})
        return JsonResponse({'success': True, 'message': 'Vote submitted successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


class AucaRegistrationForm(forms.ModelForm):
    class Meta:
        model = Auca_User
        fields = ['name', 'email', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'This will be your account username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name' : 'Name',
            'password': 'Password'
        }

    def save(self, commit=True):
        aucauser = super().save(commit=False)
        aucauser.set_password(self.cleaned_data['password'])
        if commit:
            aucauser.save()
        return aucauser
    

def register(request):
    if request.method == 'POST':
        form = AucaRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            subject = 'Your account registration is successful'
            message = f'Dear {request.POST.get('name')}! Thank you for registering with us. We are glad to have you on board!. Use { request.POST.get('email')} as your account username and { request.POST.get('password')} as your password to login to your user account'
            email_from = settings.EMAIL_HOST_USER
            EMAIL_USE_LOCALHOST = True
            recipient_list = ['celestin@vonsung.co.rw']
            
            send_mail(subject, message, email_from, recipient_list)
            return redirect('home')
        
    else:
        form = AucaRegistrationForm()
    return render(request, 'election/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            aucauser = Auca_User.objects.get(email=email)
            if check_password(password, aucauser.password):
                request.session['aucauser_id'] = aucauser.id  
                request.session['aucauser_name'] = aucauser.name
                request.session['aucauser_email'] = aucauser.email
                return redirect('home') 
            else:
                messages.error(request, 'Invalid email or password')
        except Auca_User.DoesNotExist:
            messages.error(request, 'User with such email does not exist')
    return render(request, 'election/login.html')

def logout(request):
    request.session.flush()
    return redirect('home') 

class UserLoginClass(LoginView):
    template_name = 'election/login.html' 
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True  

    def get_success_url(self):
        return reverse_lazy('home') 


def dashboard(request):
    # 1. Number of voters per election by gender
    election_data = (
        Vote.objects
        .values('election__name', 'voter_gender')
        .annotate(voter_count=Count('id'))
    )

    # 2. Total male and female voters (Pie Chart)
    gender_data = (
        Vote.objects
        .values('voter_gender')
        .annotate(voter_count=Count('id'))
    )

    # 3. Number of voters per province
    province_data = (
        Vote.objects
        .values('voter_province')
        .annotate(voter_count=Count('id'))
    )

    # 4. Number of votes per candidate
    candidate_data = (
        Vote.objects
        .values('candidate__name')
        .annotate(voter_count=Count('id'))
    )

    election_candidate_data = (
        Vote.objects
        .values('election__name', 'candidate__name')
        .annotate(vote_count=Count('id'))
        .order_by('election__name', 'candidate__name')
    )

    # Convert querysets to JSON-safe format
    context = {
        'election_data': list(election_data),
        'gender_data': list(gender_data),
        'province_data': list(province_data),
        'candidate_data': list(candidate_data),
        'election_candidate_data': list(election_candidate_data),
    }

    return render(request, 'election/dashboard.html', context)