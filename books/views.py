from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404,redirect
from django.urls import reverse_lazy
from . import models
from .forms import BookForm,ReviewForm
from . import forms
from .models import BorrowedBook,Category,Book,Review
from django. contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_list_or_404 
from django.views import View
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.
def send_transaction_email(user, subject, template):
    message = render_to_string(template, {
        'user': user,
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


@login_required
def book_view(request, category_slug=None):
    categories = Category.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        data = Book.objects.filter(category=category)
    else:
        data = Book.objects.all()
    return render(request, 'book_list.html', {'data': data, 'categories': categories})
@method_decorator(login_required, name='dispatch')
class DetailsPost(DetailView):
    model = models.Book
    pk_url_kwarg = 'pk'
    template_name = 'book_details.html'

        
    def post(self, request, *args, **kwargs):
        comment_form = forms.ReviewForm(data=self.request.POST)
        post = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object 
        comments = post.comments.all()
        comment_form = forms.ReviewForm()
        
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context


class BorrowBookView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        return render(request, 'borrow_book.html', {'book': book})

    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        if request.user.account.balance >= book.borrowing_price:
            request.user.account.balance -= book.borrowing_price
            BorrowedBook.objects.create(user=request.user, book=book)

            messages.success(request, f"You have successfully borrowed {book.title}.")
        else:
            messages.error(request, "Insufficient funds to borrow the book.")
        send_transaction_email(request.user, "borrowed Message", "borrow_email.html")
        return redirect('book_list')

@login_required
def return_book(request, book_id):
    borrowed_books = get_list_or_404(BorrowedBook, user=request.user, book__pk=book_id)
    if borrowed_books:
        borrowed_book = borrowed_books[0]
        request.user.account.balance += borrowed_book.book.borrowing_price
        request.user.account.save()
        borrowed_book.delete()
        messages.success(request, f"You have successfully returned {borrowed_book.book.title}.")
        return redirect('book_list')
    messages.error(request, "No borrowed book found.")
    return redirect('book_list')

