from django.contrib import admin
from .models import User, Challenges, BlogPost

@admin.register(User)
class adminUser(admin.ModelAdmin):
    list_display = ['name', 'email', 'password', 'mobile']
    
    
@admin.register(Challenges)
class adminChallenges(admin.ModelAdmin):
    list_display =  ["problemstatement","sample_input_1","sample_output_1","image","explanations","stack","level","rating"] 
    

@admin.register(BlogPost)
class adminChallenges(admin.ModelAdmin):
    list_display =  ["title","content","writer","created_at",]
    



