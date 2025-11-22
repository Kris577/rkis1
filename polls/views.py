from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from .forms import RegisterForm, UpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Question, Choice, CustomUser
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth import logout
from django.utils import timezone
from django.views import View
from .forms import QuestionForm, ChoiceFormSet

class Register(generic.CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('polls:login')

class Profile(generic.DetailView):
    model = CustomUser
    template_name = 'polls/profile.html'

class DeleteUser(generic.DeleteView):
    model = CustomUser
    success_url = reverse_lazy('polls:index')

def logout_user(request):
    logout(request)
    return redirect('polls:index')

class UpdateUser(generic.UpdateView):
    model = CustomUser
    form_class = UpdateForm
    template_name = 'polls/user_form.html'
    success_url = reverse_lazy('polls:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        other_user = CustomUser.objects.get(pk=self.kwargs['pk'])
        if self.request.user.pk != other_user.pk:
            raise Http404

        return context

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        return Question.objects.order_by('-pub_date')

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quest = Question.objects.get(pk=self.kwargs['pk'])
        if not quest.published_recently() and not self.request.user.is_superuser:
            raise Http404

        return context

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if not request.user.is_authenticated:
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'Вы не авторизированные',
        })
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'Вы не сделали выбор',
        })

    if question.voted_by.filter(id=request.user.id).exists():
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'Вы уже приняли участие в голосовании',
        })

    question.voted_by.add(request.user)
    selected_choice.votes += 1
    selected_choice.save()
    question.votes += 1
    question.save()

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

class QuestionCreateView(LoginRequiredMixin, View):
    template_name = 'polls/question_form.html'

    def get(self, request):
        question_form = QuestionForm()
        choice_formset = ChoiceFormSet()
        return render(request, self.template_name, {
            'question_form': question_form,
            'choice_formset': choice_formset,
        })

    def post(self, request):
        question_form = QuestionForm(request.POST, request.FILES)
        choice_formset = ChoiceFormSet(request.POST)

        if question_form.is_valid() and choice_formset.is_valid():
            question = question_form.save(commit=False)
            question.pub_date = timezone.now()
            question.save()

            choices = choice_formset.save(commit=False)
            for choice in choices:
                choice.question = question
                choice.save()

            for obj in choice_formset.deleted_objects:
                obj.delete()

            return redirect('polls:index')
        else:
            return render(request, self.template_name, {
                'question_form': question_form,
                'choice_formset': choice_formset,
            })