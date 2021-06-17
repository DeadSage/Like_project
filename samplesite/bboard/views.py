from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, FileResponse, JsonResponse
from django.views import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from django.views.generic.edit import FormView, UpdateView, DeleteView
from .serializers import RubricSerializer
from .models import Bb, Rubric, Img
from django.template.loader import get_template
from .forms import BbForm, ImgForm, LoginForm, RegistrationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin

# @api_view(['GET'])
# def api_rubrics(request):
#     if request.method == 'GET':
#         rubrics = Rubric.objects.all()
#         serializer = RubricSerializer(rubrics, many=True)
#         return Response(serializer.data)
#
#
# @api_view(['GET'])
# def api_rubrics_detail(request, pk):
#     if request.method == 'GET':
#         rubric = Rubric.objects.get(pk=pk)
#         serializer = RubricSerializer(rubric)
#         return Response(serializer.data)

"""высокоуровневый контроллеры"""
# class APIRubrics(generics.ListCreateAPIView):
#     queryset = Rubric.objects.all()
#     serializer_class = RubricSerializer
#
#
# class APIRubricDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Rubric.objects.all()
#     serializer_class = RubricSerializer
"""метаконтроллеры"""


class APIRubricViewSet(ModelViewSet):
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer
    permission_classes = (IsAuthenticated,)

# @login_required()
def index(request):
    if request.user.is_authenticated:
        bbs = Bb.objects.all()
        rubrics = Rubric.objects.all()
        paginator = Paginator(bbs, 2)
        if 'page' in request.GET:
            page_num = request.GET['page']
        else:
            page_num = 1
        page = paginator.get_page(page_num)
        context = {'rubrics': rubrics, 'page': page, 'bbs': page.object_list}
        template = get_template('bboard/index.html')
        # return render(request, 'bboard/index.html', context)
        return HttpResponse(template.render(context=context, request=request))
    else:
        return redirect('login')


def by_rubric(request, rubric_id):
    if request.user.is_authenticated:
        bbs = Bb.objects.filter(rubric=rubric_id)
        rubrics = Rubric.objects.all()
        current_rubric = Rubric.objects.get(pk=rubric_id)
        context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
        return render(request, 'bboard/by_rubric.html', context)
    else:
        return HttpResponse('Гость не имеет доступа к списку рубрик')


def add_and_save(request):
    if request.method == 'POST':
        bbf = BbForm(request.POST)
        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(reverse('by_rubric',
                                                kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request, 'bboard/create.html', context)
    else:
        bbf = BbForm()
        context = {'form': bbf}
        return render(request, 'bboard/create.html', context)


class BbCreateView(SuccessMessageMixin, CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')
    success_message = 'Объявление о продаже товара создано'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


# class BbRubricView(TemplateView):
#     template_name = 'bboard/by_rubric.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['bbs'] = Bb.objects.filter(rubric=context['rubric_id'])
#         context['rubrics'] = Rubric.objects.all()
#         context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
#         return context


class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbByRubricView(SingleObjectMixin, ListView):
    template_name = 'bboard/by_rubric.html'
    pk_url_kwarg = 'rubric_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Rubric.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.bb_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_rubric'] = self.object
        context['rubrics'] = Rubric.objects.all()
        context['bbs'] = context['object_list']
        return context


class BbAddView(FormView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    initial = {'price': 0.0}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse('bboard:by_rubric', kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})


class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbDeleteView(DeleteView):
    model = Bb
    success_url = success_url = reverse_lazy('index')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


def add(request):
    """controller of adding imgFiles"""
    if request.method == 'POST':
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # return redirect('testapp:index')
            return redirect('bboard:index')
    else:
        form = ImgForm()
    context = {'form': form}
    return render(request, 'bboard/add.html', context)


def delete(request, pk):
    img = Img.objects.get(pk=pk)
    img.img.delete()
    img.delete()
    return redirect('bboard:index')


class LoginView(FormView):
    template_name = "registration/login.html"

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {'form': form}
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                # return redirect('bboard:index')
                return redirect(index)
            context = {'form': form}
            return render(request, 'login.html', context)


class RegistrationView(View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {'form': form}
        return render(request, 'registration/registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return redirect('index')
        context = {'form': form}
        return render(request, 'registration/registration.html', context)
