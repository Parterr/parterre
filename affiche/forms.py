from dal import autocomplete
from django import forms
from .models import PerformancePerformers, Performers, PerformanceConductor, Conductor, PerformanceCreatives, Creatives


class PerformancePerformersForm(forms.ModelForm):
    performer = forms.ModelMultipleChoiceField(
        queryset=Performers.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='performer-autocomplete'),
        required=False
    )

    class Meta:
        model = PerformancePerformers
        fields = ['performer', 'role']


class PerformanceCreativesForm(forms.ModelForm):
    name = forms.ModelChoiceField(
        queryset=Creatives.objects.all().order_by('name'),
        widget=autocomplete.ModelSelect2(url='creative-autocomplete'),
        required=False
    )

    class Meta:
        model = PerformanceCreatives
        fields = '__all__'


class PerformanceConductorForm(forms.ModelForm):
    name = forms.ModelChoiceField(
        queryset=Conductor.objects.all().order_by('name'),
        widget=autocomplete.ModelSelect2(url='conductor-autocomplete'),
        required=False
    )

    class Meta:
        model = PerformanceConductor
        fields = '__all__'
