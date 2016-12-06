from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.urls import reverse

import drafts.forms as f
from drafts.models import Dataset, Datafile
from drafts.util import convert_to_slug

from django.views.generic.edit import FormView, UpdateView


class DatasetCreate(FormView):
    model = Dataset
    form_class = f.DatasetForm
    template_name = 'drafts/edit_title.html'

    def form_valid(self, form):
        name = convert_to_slug(form.cleaned_data['title'])

        dataset = Dataset.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                name=name
        )
        self.object = dataset
        return super(DatasetCreate, self).form_valid(form)

    def get_initial(self):
        return {'new': True}

    def get_success_url(self):
        return reverse('edit_licence', args=[self.object.name])


class DatasetEditView(FormView):
    model = Dataset
    form_class = f.DatasetForm
    template_name = 'drafts/edit_title.html'
    slug_url_kwarg = 'dataset_name'
    slug_field = 'name'

    def form_valid(self, form):
        self.object = get_object_or_404(Dataset, name=self.get_initial()['name'])
        self.object.title = form.cleaned_data['title']
        self.object.description = form.cleaned_data['description']
        self.object.save()

        return super(DatasetEditView, self).form_valid(form)

    def get_initial(self):
        return get_object_or_404(Dataset, name=self.kwargs['dataset_name']).as_dict()

    def get_context_data(self):
        return {'dataset': self.get_initial(), 'new': False }

    def get_success_url(self):
        return reverse('edit_licence', args=[self.object.name])


class EditLicenceView(FormView):
    model = Dataset
    form_class = f.LicenceForm
    template_name = 'drafts/edit_licence.html'
    slug_url_kwarg = 'dataset_name'
    slug_field = 'name'

    def form_valid(self, form):
        self.object = get_object_or_404(Dataset, name=self.get_initial()['name'])
        self.object.licence = form.cleaned_data['licence']
        self.object.licence_other = form.cleaned_data['licence_other']
        self.object.save()

        return super(EditLicenceView, self).form_valid(form)

    def get_initial(self):
        return get_object_or_404(Dataset, name=self.kwargs['dataset_name']).as_dict()

    def get_context_data(self):
        return {'dataset': self.get_initial() }

    def get_success_url(self):
        return reverse('edit_country', args=[self.object.name])


class EditCountryView(FormView):
    model = Dataset
    form_class = f.CountryForm
    template_name = 'drafts/edit_country.html'
    slug_url_kwarg = 'dataset_name'
    slug_field = 'name'

    def form_valid(self, form):
        self.object = get_object_or_404(Dataset, name=self.get_initial()['name'])
        self.object.countries = form.cleaned_data['countries']
        self.object.save()

        return super(EditCountryView, self).form_valid(form)

    def get_initial(self):
        return get_object_or_404(Dataset, name=self.kwargs['dataset_name']).as_dict()

    def get_context_data(self):
        return {'dataset': self.get_initial() }

    def get_success_url(self):
        return reverse('edit_frequency', args=[self.object.name])


class EditFrequencyView(FormView):
    model = Dataset
    form_class = f.FrequencyForm
    template_name = 'drafts/edit_frequency.html'
    slug_url_kwarg = 'dataset_name'
    slug_field = 'name'

    def form_valid(self, form):
        self.object = get_object_or_404(Dataset, name=self.get_initial()['name'])
        self.object.frequency = form.cleaned_data['frequency']
        self.object.save()

        return super(EditFrequencyView, self).form_valid(form)

    def get_initial(self):
        return get_object_or_404(Dataset, name=self.kwargs['dataset_name']).as_dict()

    def get_context_data(self):
        return {'dataset': self.get_initial() }

    def get_success_url(self):
        return reverse('edit_addfile', args=[self.object.name])


class AddFileView(FormView):
    model = Datafile
    form_class = f.AddFileForm
    template_name = 'drafts/edit_addfile.html'
    slug_url_kwarg = 'dataset_name'
    slug_field = 'name'

    def form_valid(self, form):
        self.dataset = get_object_or_404(Dataset, name=self.get_initial()['name'])

        self.datafile = Datafile.objects.create(
            title=form.cleaned_data['title'],
            url=form.cleaned_data['url'],
            dataset=self.dataset
        )

        return super(AddFileView, self).form_valid(form)

    def get_initial(self):
        return get_object_or_404(Dataset, name=self.kwargs['dataset_name']).as_dict()

    def get_context_data(self):
        return {'dataset': self.get_initial() }

    def get_success_url(self):
        return reverse('show_files', args=[self.dataset.name])


class EditNotificationView(FormView):
    model = Dataset
    form_class = f.NotificationsForm
    template_name = 'drafts/edit_notifications.html'
    slug_url_kwarg = 'dataset_name'
    slug_field = 'name'

    def form_valid(self, form):
        self.object = get_object_or_404(Dataset, name=self.get_initial()['name'])
        self.object.notifications = form.cleaned_data['notifications']
        self.object.save()

        return super(EditNotificationView, self).form_valid(form)

    def get_initial(self):
        return get_object_or_404(Dataset, name=self.kwargs['dataset_name']).as_dict()

    def get_context_data(self):
        return {'dataset': self.get_initial() }

    def get_success_url(self):
        return reverse('check_dataset', args=[self.object.name])


@login_required()
def show_files(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    return render(request, "drafts/show_files.html", {
        "dataset": dataset,
    })

@login_required()
def check_dataset(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    return render(request, "drafts/check_dataset.html", {
        "dataset": dataset.as_dict(),
    })
