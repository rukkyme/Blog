from django import forms


#EmailPostForm inherits from base Form class which is in module forms.
#the class will use django's built-in form handling system to manage form fields
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25) #instance of CharField. name of the person sending the post
    email = forms.EmailField()   #instance of EmailField.email of the person sending the post recommendation
    to = forms.EmailField()  #instance of EmailField. email of the one recieving the mail.
    comments = forms.CharField( required=False, widget=forms.Textarea)  #its for optional comments that users can include in email.