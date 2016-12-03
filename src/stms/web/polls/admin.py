from django.contrib import admin


# Register your models here.
class NewsAdmin(admin.ModelAdmin):
    class Media:
        js = ('/js/tinymce/tinymce.min.js', '/js/textareas.js')
