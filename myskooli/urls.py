
from django.contrib import admin
from django.urls import path, include  # add this
from rest_framework import routers  # add this

from .system import views
from .users.views import StudentSignUpView, LoginView, StudenView, TeacherSignUp, TeacherView, ReviewView, \
    CommunityView, ReplyView, FavoriteView, LessonsView, PackageLessonsView, AvailableTimeView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()                      # add this
router.register(r'students/signup', StudentSignUpView, 'Signup'),
router.register(r'teachers/signup', TeacherSignUp, 'Teacher'),
router.register(r'login', LoginView, 'Login'),
router.register(r'students', StudenView, 'Students'),
router.register(r'teachers', TeacherView, 'Teachers')
router.register(r'categories', views.CategoryViews , 'Categories'),
router.register(r'subcategories', views.SubCategoryViews , 'SubCategories'),
router.register(r'countries', views.CountryViews , 'Countries'),
router.register(r'reviews', ReviewView , 'Reviews'),
router.register(r'post', CommunityView , 'Post'),
router.register(r'reply', ReplyView , 'Reply'),
router.register(r'favorite', FavoriteView , 'Favorite'),
router.register(r'lessons', LessonsView , 'lessons'),
router.register(r'packagelessons', PackageLessonsView, 'PackageLessons'),
router.register(r'availabletimeView', AvailableTimeView, 'AvailableTimeView'),


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

   ]