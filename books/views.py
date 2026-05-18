from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Book, Offer
from django.contrib.auth.decorators import login_required
from .forms import BookForm, OfferForm
from django.contrib import messages
from django.db.models import Case, When, Value, IntegerField


def book_list_view(request):
    books = Book.objects.all()
    return render(request, 'books/list.html', {'books': books})

@login_required
def add_book_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()

    return render(request, 'books/add.html', {'form': form})


@login_required
def edit_book_view(request, pk):
    book = get_object_or_404(Book, id=pk)

    if book.owner != request.user:
        return redirect('book_list')

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)

    return render(request, 'books/edit.html', {'form': form, 'book': book})


@login_required
def delete_book_view(request, pk):
    book = get_object_or_404(Book, id=pk)

    if book.owner != request.user:
        return redirect('book_list')

    if request.method == 'POST':
        book.delete()
        return redirect('book_list')

    return render(request, 'books/delete.html', {'book': book})


@login_required
def create_offer_view(request):
    requested_id = request.GET.get('requested')
    initial = {}

    if requested_id:
        initial['requested_book'] = requested_id

    form = OfferForm(
        request.POST or None,
        user=request.user,
        initial=initial
    )

    if request.method == 'POST':
        if form.is_valid():
            offer = form.save(commit=False)

            offer.from_user = request.user
            offer.to_user = offer.requested_book.owner

            if offer.offered_book.owner != request.user:
                return redirect('book_list')

            if offer.requested_book.owner == request.user:
                messages.error(request, "Ви не можете запропонувати обмін на власну книгу!")
                return redirect('book_list')

            offer.save()

            messages.success(request, "Пропозицію успішно відправлено!")
            return redirect('offers_sent')

    return render(request, 'offers/create.html', {'form': form})



@login_required
def accept_offer_view(request, pk):
    offer = get_object_or_404(Offer, id=pk)

    if offer.to_user != request.user:
        return redirect('book_list')

    if offer.status != 'pending':
        return redirect('offers_received')

    offered_book = offer.offered_book
    requested_book = offer.requested_book

    offered_book.owner = offer.to_user
    requested_book.owner = offer.from_user

    offered_book.save()
    requested_book.save()

    offer.status = 'accepted'
    offer.save()

    Offer.objects.filter(
        requested_book=requested_book,
        status='pending'
    ).exclude(id=offer.id).update(status='rejected')

    messages.success(request, "Обмін успішно прийнято!")
    return redirect('offers_received')



@login_required
def reject_offer_view(request, pk):
    offer = get_object_or_404(Offer, id=pk)

    if offer.to_user != request.user:
        return redirect('book_list')

    offer.status = 'rejected'
    offer.save()

    messages.info(request, "Пропозицію відхилено")

    return redirect('offers_received')


@login_required
def received_offers_view(request):
    offers = Offer.objects.filter(to_user=request.user).annotate(
        status_order=Case(
            When(status='pending', then=Value(0)),
            When(status='accepted', then=Value(1)),
            When(status='rejected', then=Value(2)),
            output_field=IntegerField(),
        )
    ).order_by('status_order', '-created_at')

    return render(request, 'offers/received.html', {'offers': offers})


@login_required
def sent_offers_view(request):
    offers = Offer.objects.filter(from_user=request.user).annotate(
        status_order=Case(
            When(status='pending', then=Value(0)),
            When(status='accepted', then=Value(1)),
            When(status='rejected', then=Value(2)),
            output_field=IntegerField(),
        )
    ).order_by('status_order', '-created_at')

    return render(request, 'offers/sent.html', {'offers': offers})

def book_detail_view(request, pk):
    book = get_object_or_404(Book, id=pk)
    return render(request, 'books/detail.html', {'book': book})


def book_list_view(request):
    category_id = request.GET.get('category')

    books = Book.objects.all()

    if category_id:
        books = books.filter(category_id=category_id)

    categories = Category.objects.all()

    return render(request, 'books/list.html', {
        'books': books,
        'categories': categories
    })