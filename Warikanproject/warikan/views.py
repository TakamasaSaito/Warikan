from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import WarikanModel, MemberModel, DetailModel ,PictureModel
from django.urls import reverse_lazy
from django.db.models import Sum

class AddMember(CreateView):
    template_name = 'addmember.html'
    model = MemberModel
    fields = ('membername','pictureID',)
    success_url = reverse_lazy('memberlist')

class MemberList(ListView):
    template_name = 'memberlist.html'
    model = MemberModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_count = DetailModel.objects.count()
        data_sum = DetailModel.objects.all().aggregate(Sum('price'))
        data_list = MemberModel.objects.raw('SELECT warikan.*, ifnull(smr_detail.cnt,0 ) as cnt,ifnull(smr_detail.sum_price,0 ) as sum_price FROM warikan_membermodel as warikan left join (select memberID_id,count(*) as cnt,sum(price) as sum_price from warikan_detailmodel group by memberID_id) as smr_detail  on smr_detail.memberID_id = warikan.id')
        context['object_list'] = data_list
        if data_sum['price__sum'] is not None and 0 < data_sum['price__sum']:
            data_per = data_sum['price__sum'] // data_count
        else:
            data_per = 0
        context['data_count'] = data_count
        context['data_sum'] = data_sum
        context['data_per'] = data_per
        return context

class AddDetail(CreateView):
    template_name = 'adddetail.html'
    model = DetailModel
    fields = ('memberID','title','price')
    success_url = reverse_lazy('memberlist')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['memberID'] = self.kwargs['pk']
        return context

class DetailList(ListView):
    template_name = 'detaillist.html'
    model = DetailModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_list = DetailModel.objects.filter(memberID=self.kwargs['pk'])
        context['object_list'] = data_list
        return context

class DetailUpdate(UpdateView):
    template_name = 'detailupdate.html'
    model = DetailModel
    fields = ('memberID','title','price')
    def get_url_success(self):
        return reverse_lazy('detaillist',kwargs=self.kwargs['pk'])

class DetailDelete(DeleteView):
    template_name = 'detaildelete.html'
    model = DetailModel
    def get_url_success(self):
        return reverse_lazy('detaillist',kwargs=self.kwargs['pk'])

class AddPicture(CreateView):
    template_name = 'addpicture.html'
    model = PictureModel
    fields = ('picturename','url',)
    success_url = reverse_lazy('memberlist')
