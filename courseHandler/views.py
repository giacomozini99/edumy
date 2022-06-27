# Create your views here.index'
from audioop import avg

from dj_shop_cart.cart import get_cart_class
from django.db.models import Max, Count
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import DetailView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin

from courseHandler.forms import CreateVideo, SearchCourseForm, UpdateVideoForm
from courseHandler.models import Video, Course, FollowCourse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse, HttpRequest, HttpResponse

from django.shortcuts import redirect, render
from django.urls import reverse_lazy,reverse
from django.views.generic import CreateView, ListView
from courseHandler.forms import CourseForm

from userInteractions.forms import QuestionForm, ReviewForm
from userInteractions.models import Question, Answer, Review

"""
class VideoUploadView(CreateView):
    model = Video
    form_class = CreateVideo
    template_name = 'courseHandler/video/upload-video.html'

"""

Cart = get_cart_class()

def teacher_is_authorized(request, pk):
    if not request.user.is_authenticated:
        return False
    course_check = Course.objects.get(pk=pk)
    if course_check.author_id != request.user.id:
        return False

    return True

def VideoUploadDetail(request, course_id, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form_question = QuestionForm(request.POST, request.FILES)
            if form_question.is_valid():
                instance = form_question.save(commit=False)
                instance.student_id = request.user.id
                instance.video_id = int(pk)
                instance.save()
                return HttpResponse("You have created a question", content_type='text/plain')
        else:
            form_question = QuestionForm()
            questions = Question.objects.all().filter(video_id=pk)
            answers = Answer.objects.all().filter(video_id=pk)
            course = Course.objects.filter(pk=course_id)
            questions_answer_list = list(zip(questions, answers))
            video = Video.objects.get(pk=pk)
            context = {
                "form_question": form_question,
                "questions_answer_list": questions_answer_list,
                "video": video,
                "course": course,
                "pk": pk
            }
            return render(request, 'courseHandler/video/upload-video-detail.html', context)
    else:
        return HttpResponseRedirect('/')


def VideoUploadView(request, pk):
    if request.user.is_authenticated:
        course_check = Course.objects.get(pk=pk)
        if course_check.author_id != request.user.id:
            return HttpResponseRedirect('/')

        if request.method == 'POST':
            form = CreateVideo(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.course_id = int(pk)
                instance.save()
                return redirect('courseHandler:course-upload-video', pk)
        else:
            form = CreateVideo()
            videos = Video.objects.filter(course_id=pk)
            context = {
                "form": form,
                "videos": videos,
                "pk": pk
            }
            return render(request, 'courseHandler/video/upload-video.html', context)
    else:
        return HttpResponseRedirect('/')


class VideoUpdateView(LoginRequiredMixin, UpdateView):
    model = Video
    form_class = UpdateVideoForm
    template_name = 'courseHandler/video/update.html'

    def form_valid(self, form):
        form.instance.save()
        pk = str(form.instance.course_id)
        return redirect('courseHandler:course-upload-video', pk)


class CourseCreate(LoginRequiredMixin, CreateView):
    template_name = 'courseHandler/course/create.html'
    success_url = reverse_lazy('homepage')
    form_class = CourseForm

    def form_valid(self, form):
        # author = get_object_or_404(UserType, pk=form.instance.author_id)
        # if author.type == "Teacher":
        form.instance.author_id = self.request.user.id
        return super().form_valid(form)
        # else:
        # print("Tu non sei un teacher")


class CourseDetail(FormMixin, DetailView):
    model = Course
    template_name = "courseHandler/course/detail.html"
    form_class= ReviewForm

    def dispatch(self, request, *args, pk, **kwargs):
        course_check = Course.objects.get(pk=pk)
        if not course_check.is_active and course_check.author_id != request.user.id:
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('courseHandler:course-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(CourseDetail, self).get_context_data(**kwargs)
        #se userCourses è vuoto fare una ricerca totale dei corsi
        #userCourses = FollowCourse.objects.filter(student_id=self.request.user.id).select_related('course')
        #courses = [course.course for course in userCourses]
        #listPrice = [c.price for c in courses]
        #listcategory = [c.category for c in courses]
        #avg = sum(listPrice) / len(listcategory)
        #percentage = avg * 0.3
        #minAvg = avg - percentage
        #maxAvg = avg + percentage
        #popularCategory = list(Counter(listcategory))[0]
        #fare la ricerca su corso preso in dettaglio(utilizzare self)
        #all_courses = Course.objects.filter(category=popularCategory, price__range=(minAvg,maxAvg))
        percentage = self.object.price * 0.3
        min_price = self.object.price - percentage
        max_price = self.object.price + percentage
        all_courses = Course.objects.filter(category=self.object.category, price__range=(min_price,max_price))
        #ids = [course.pk for course in userCourses]
        course_no_follow = [course for course in all_courses if course.id != self.object.id]
        context['couseList'] = course_no_follow
        #context['couseList'] = all_courses
        context['reviews'] = Review.objects.filter(course_id=self.object.id)
        context['formReview'] = ReviewForm(initial={'post': self.object})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, formReview):
        course = self.get_object()
        instance = formReview.save(commit=False)
        instance.course_id = int(course.pk)
        instance.student_id = int(self.request.user.id)
        formReview.save()
        return super(CourseDetail, self).form_valid(formReview)


class CourseDelete(DeleteView):
    model = Course
    template_name = 'courseHandler/course/delete.html'
    success_url = reverse_lazy('courseHandler:course-list')

    def dispatch(self, request, *args, pk, **kwargs):
        if not teacher_is_authorized(request, pk):
            return redirect('homepage')

        return super().dispatch(request, *args, **kwargs)


class CourseUpdate(UpdateView):
    model = Course
    template_name = 'courseHandler/course/update.html'
    success_url = reverse_lazy('courseHandler:course-list')
    form_class = CourseForm

    def dispatch(self, request, *args, pk, **kwargs):
        if not teacher_is_authorized(request, pk):
            return redirect('homepage')

        return super().dispatch(request, *args, **kwargs)


class CourseList(ListView):
    model = Course
    template_name = 'courseHandler/course/list.html'

def CourseListView(request):
    if not request.user.is_authenticated:
        return redirect('homepage')

    if request.user.usertype.type == 'student':
       courses = FollowCourse.objects.filter(student_id=request.user.id).select_related('course')
       courses = [e.course for e in courses]
    else:
        courses = Course.objects.filter(author_id=request.user.id)

    context = {
        "courses": courses,
    }
    return render(request, 'courseHandler/course/list.html', context)

def CourseListStore(request):
    if request.method == 'POST':


        """
         form = CreateVideo(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.course_id = int(pk)
            instance.save()
            return redirect('courseHandler:course-upload-video', pk)
        """
    else:
        courses = Course.objects.all().filter(is_active=True)
        cart = Cart.new(request)
        context = {
            "courses": courses,
            "cartProd": cart.products
        }
        return render(request, 'courseHandler/course/store.html', context)

"""class CourseListStore(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'courseHandler/course/store.html'

"""

def search(request):
    if request.method == "POST":
        form = SearchCourseForm(request.POST)
        if form.is_valid():
            sstring = form.cleaned_data.get("search_string")
            where = form.cleaned_data.get("search_where")
            return redirect("courseHandler:course-search-result", sstring, where)
    else:
        form = SearchCourseForm()
    return render(request, template_name="courseHandler/course/search.html", context={"form": form})


class CourseSearchView(CourseList):
    titolo = "La tua ricerca ha dato come risultato"
    def get_queryset(self):
        sstring = self.request.resolver_match.kwargs["sstring"]
        where = self.request.resolver_match.kwargs["where"]
        if "Title" in where:
            qq = self.model.objects.filter(title__icontains=sstring)
        elif "Author" in where:
            qq = self.model.objects.filter(author__username__icontains=sstring)
        else:
            qq = self.model.objects.filter(category__icontains=sstring)
        return qq

        #return super().form_valid(form)


def CartView(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateVideo(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return redirect('homepage')
        else:
            cart = Cart.new(request)
            items_prices = [item.price for item in cart.products]
            tot_price = sum(items_prices)
            context = {
                "cart": cart,
                'totPrice': tot_price
            }
            return render(request, 'cart.html', context)
    else:
        return HttpResponseRedirect('/')


@require_GET
def add_product(request, pk):
    cart = Cart.new(request)
    course = Course.objects.get(pk=pk)
    cart.add(course, quantity=1)
    return JsonResponse({'msg': 'Course added'})

@require_GET
def remove_product(request, pk):
    course = Course.objects.get(pk=pk)
    cart = Cart.new(request)
    cart.remove(course, quantity=1)
    return redirect(reverse('courseHandler:cart-view'))


@require_POST
def empty_cart(request: HttpRequest):
    Cart.new(request).empty()

