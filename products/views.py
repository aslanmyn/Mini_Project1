from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework import viewsets
from .serializers import ProductSerializer, CategorySerializer
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Product, Category
from django.contrib import messages
from .forms import ProductForm
from users.permissions import IsAdmin


class ProductListView(ListView):
    model = Product
    template_name = "products/products.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = Product.objects.all()

        # Filter by category if provided in query params
        category_id = self.request.GET.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Exclude products owned by the logged-in user
        if self.request.user.is_authenticated:
            queryset = queryset.exclude(representative=self.request.user)

        # Search filter
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()  # Include categories for the filter
        context["search_query"] = self.request.GET.get("search", "")  # Preserve search query
        return context

    
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm  # Use the form
    template_name = "products/product_create.html"  # Keep your existing template
    success_url = reverse_lazy("product_list")  # Redirect after success

    def form_valid(self, form):
        product = form.save(commit=False)  # Don't save yet
        product.representative = self.request.user  # Assign the logged-in user
        product.save()  # Now save the product
        messages.success(self.request, "Product created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        """Pass additional context like categories to the template."""
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()  # Pass categories for dropdown
        return context
    
    
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_update.html"  # Keep your existing template
    
    def get_success_url(self):
        return reverse_lazy("profile", kwargs={"username": self.request.user.username})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()  # Fetch categories
        return context

    def test_func(self):
        """Ensure only the product representative can update the product."""
        product = self.get_object()
        return self.request.user == product.representative
    
    
class ProductDeleteView(DeleteView):
    model = Product
    template_name = "products/product_delete.html"
    success_url = reverse_lazy('product-list')


class ProductViewAPI(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAdmin]
    
    
class CategoryViewAPI(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdmin]
    
    
