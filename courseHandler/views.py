# Create your views here.index'

from dj_shop_cart.cart import get_cart_class
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import DetailView, DeleteView, UpdateView
from courseHandler.forms import CreateVideo, SearchCourseForm, UpdateVideoForm
from courseHandler.models import Video, Course
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpRequest, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy,reverse
from django.views.generic import CreateView, ListView
from courseHandler.forms import CourseForm

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

class VideoUploadDetail(DetailView):
    model = Video
    template_name = 'courseHandler/video/upload-video-detail.html'


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
            videos = Video.objects.all().filter(course_id=pk)
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


class CourseDetail(DetailView):
    model = Course
    template_name = "courseHandler/course/detail.html"
    def dispatch(self, request, *args, pk, **kwargs):
        course_check = Course.objects.get(pk=pk)
        print(course_check.is_active)
        if not course_check.is_active and course_check.author_id != request.user.id:
            return redirect('homepage')

        return super().dispatch(request, *args, **kwargs)


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
    if not request.user.is_authenticated or request.user.usertype.type == 'student':
        return redirect('homepage')
    courses = Course.objects.all().filter(author_id=request.user.id)
    print(courses)
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

        return super().form_valid(form)


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

    """   def createCourse(request):
            if request.user.is_authenticated and request.user.type == "teacher":
                if request.method == 'POST':
                    form = CourseForm(request.POST, request.FILES)
                    if form.is_valid():
                        instance = form.save(commit=False)
                        instance.author_id = request.user.id
                        instance.save()
                        return redirect('courseHandler:course-create')
                else:
                    form = CourseForm()
                    context = {
                        "form": form,
                    }
                    return render(request, 'courseHandler/course/create.html', context)
            else:
                return HttpResponseRedirect('/') """
