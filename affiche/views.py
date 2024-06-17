import json

from dal import autocomplete
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from .forms import PerformancePerformersForm
from .models import MainImages, Performance, Creatives, Performers, Backstage, Ticket, Seat, Row, \
    PerformancePerformers, PerformanceConductor, PerformanceCreatives, Conductor
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index_page_view(request):
    if request.method == 'GET':
        images = MainImages.objects.all()
        now = timezone.now()
        performances = Performance.objects.filter(
            (Q(datetime1__gte=now) & Q(datetime1__lte=now + timedelta(days=31))) |
            (Q(datetime2__gte=now) & Q(datetime2__lte=now + timedelta(days=31))),
            hidden=False
        ).order_by('datetime1')
        return render(request, 'affiche/main.html', {'images': images, 'performances': performances})


def performance_detail_page_view(request, pk):
    if request.method == 'GET':
        performance = Performance.objects.get(id=pk)
        performance_creatives = PerformanceCreatives.objects.filter(performance=performance)
        performance_performers = PerformancePerformers.objects.filter(performance=performance)
        performance_conductor = PerformanceConductor.objects.filter(performance=performance)
        creatives_exist = performance_creatives.exists()
        performers_exist = performance_performers.exists()
        short_roles = [performer for performer in performance_performers if performer.short_roles]
        long_roles = [performer for performer in performance_performers if performer.long_roles]
        return render(request, 'affiche/per_detail.html', {'performance': performance,
                                                           'performance_creatives': performance_creatives,
                                                           'creatives_exist': creatives_exist,
                                                           'performers_exist': performers_exist,
                                                           'performance_performers': performance_performers,
                                                           'short_roles': short_roles,
                                                           'long_roles': long_roles,
                                                           'performance_conductor': performance_conductor,
                                                           })


def backstage_page_view(request):
    if request.method == 'GET':
        backstages_list = Backstage.objects.all()
        paginator = Paginator(backstages_list, 24)
        page_number = request.GET.get('page')
        try:
            backstages = paginator.page(page_number)
        except PageNotAnInteger:
            backstages = paginator.page(1)
        except EmptyPage:
            backstages = paginator.page(paginator.num_pages)

        page_range = range(max(1, backstages.number - 3),
                           min(backstages.paginator.num_pages, backstages.number + 3) + 1)
        return render(request, 'affiche/backstage.html', {'backstages': backstages, 'page_range': page_range})


def backstage_detail_page_view(request, backstage_pk):
    if request.method == 'GET':
        backstage = get_object_or_404(Backstage, id=backstage_pk)
        return render(request, 'affiche/backstage_info.html', {'backstage': backstage})


def repertory_page_view(request):
    if request.method == 'GET':
        performances = Performance.objects.all()
        performance_type = request.GET.get('type')
        if performance_type:
            performances = performances.filter(type=performance_type)
        return render(request, 'affiche/repertory.html', {'performances': performances})


def repertory_detail_page_view(request, performance_pk):
    performance = get_object_or_404(Performance, id=performance_pk)
    image_urls = performance.image_carousel.all()
    performers = PerformancePerformers.objects.filter(performance=performance)
    creatives = PerformanceCreatives.objects.filter(performance=performance)
    return render(request, 'affiche/repertory_detail.html',
                  {'performance': performance, 'image_urls': image_urls, 'performers': performers,
                   'creatives': creatives})


def hall_view(request, pk):
    rows = Row.objects.all()
    performance = get_object_or_404(Performance, id=pk)

    context = {
        'rows': rows,
        'performance': performance
    }
    return render(request, 'affiche/hall.html', context)


def buy_ticket(request):
    seat_id = request.POST.get('seat_id')

    seat = Seat.objects.get(id=seat_id)
    seat.is_reserved = True
    seat.save()

    ticket = Ticket.objects.create(seat=seat)

    response_data = {
        'row': seat.row.number,
        'seat_number': seat.number,
        'ticket_price': 10000  # Цена билета
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')


class CreativeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Creatives.objects.none()

        qs = Creatives.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class PerformerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Performers.objects.none()

        qs = Performers.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class ConductorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Conductor.objects.none()

        qs = Conductor.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs
