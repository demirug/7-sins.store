from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from feedback.models import Feedback
from manager.forms import ProductModelForm, OrderModelForm, FeedbackModelForm
from orders.models import Order
from products.models import Product

__all__ = ('ProductListView', 'OrderListView', 'FeedbackListView', 'editProduct', 'createProduct', 'deleteProduct', 'changeOrder', 'answerFeedback',)


class ProductListView(LoginRequiredMixin, ListView):
    login_url = '/authorization/login/'
    model = Product
    template_name = 'manager/productsList.html'
    ordering = ['pk']
    paginate_by = 10


class OrderListView(LoginRequiredMixin, ListView):
    login_url = '/authorization/login/'
    model = Order
    template_name = 'manager/ordersList.html'
    ordering = ['-pk']
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.annotate(
            custom_order=models.Case(
                models.When(status="NEW", then=1),
                models.When(status="ACCEPTED", then=2),
                models.When(status="CANCELED", then=4),
                models.When(status="DONE", then=3),
                output_field=models.IntegerField())
        ).order_by('custom_order', '-timestamp')


class FeedbackListView(LoginRequiredMixin, ListView):
    login_url = '/authorization/login/'
    model = Feedback
    template_name = 'manager/feedbackList.html'
    paginate_by = 10

    def get_queryset(self):
        return Feedback.objects.annotate(
            custom_order=models.Case(
                models.When(answer="", then=0),
                output_field=models.IntegerField(),
                default=1,
            )
        ).order_by('custom_order', 'timestamp')


@login_required(login_url='/authorization/login/')
def changeOrder(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = OrderModelForm(data=request.POST or None, instance=order)
    if form.is_valid():
        if form.has_changed():
            form.save()
            messages.success(request, 'Состояния заказа было сохранено')
        return redirect('manager:orders')
    else:

        for tag in form.errors.as_data():
            for validationError in form.errors.as_data()[tag]:
                for error in validationError:
                    messages.error(request, error)

        return render(request, 'manager/orderForm.html', {'form': form, 'order': order})


@login_required(login_url='/authorization/login/')
def createProduct(request):
    form = ProductModelForm(data=request.POST or None, files=request.FILES or None)
    print(form.instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'Товар был успешно создан')
        return redirect('manager:products')
    else:
        for tag in form.errors.as_data():
            for validationError in form.errors.as_data()[tag]:
                for error in validationError:
                    messages.error(request, error)
        return render(request, 'manager/productForm.html', {'form': form, 'title': 'Создание товара'})


@login_required(login_url='/authorization/login/')
def editProduct(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductModelForm(data=request.POST or None, files=request.FILES or None, instance=product)
    if form.is_valid():
        if form.has_changed():
            form.save()
            messages.success(request, 'Товар был успешно изменен')
        return redirect('manager:products')
    else:
        for tag in form.errors.as_data():
            for validationError in form.errors.as_data()[tag]:
                for error in validationError:
                    messages.error(request, error)
        return render(request, 'manager/productForm.html', {'form': form, 'title': 'Редактирование товара'})


@login_required(login_url='/authorization/login/')
def deleteProduct(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'Товар был успешно удален')
    return redirect('manager:products')


@login_required(login_url='/authorization/login/')
def answerFeedback(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    form = FeedbackModelForm(request.POST or None, instance=feedback)
    if form.is_valid():
        form.save()
        messages.success(request, 'Ответ был размещен')
        return redirect('manager:feedback')
    else:
        return render(request, 'manager/feedbackForm.html', context={'form': form, 'object': feedback})