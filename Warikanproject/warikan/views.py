from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import MemberModel, DetailModel ,PictureModel, TripModel
from django.urls import reverse_lazy
from django.urls import reverse
from django.db.models import Sum
from logging import getLogger

class AddMember(CreateView):
    template_name = 'addmember.html'
    model = MemberModel
    fields = ('membername','pictureID','tripID',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trip_pk'] = self.kwargs['pk']
        return context

    def get_success_url(self):
        return reverse('memberlist',kwargs={'pk': self.object.tripID.id})

class DeleteMember(DeleteView):
    template_name = 'memberdelete.html'
    model = MemberModel
    def get_success_url(self):
        return reverse('memberlist',kwargs={'pk': self.object.tripID.id})

class MemberList(ListView):
    template_name = 'memberlist.html'
    model = MemberModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_count = MemberModel.objects.filter(tripID=self.kwargs['pk']).count()
        data_sum = DetailModel.objects.filter(tripID=self.kwargs['pk']).aggregate(Sum('price'))
        data_list = MemberModel.objects.raw('SELECT \
                                                warikan.*,\
                                                ifnull(smr_detail.cnt,0 ) as cnt,\
                                                ifnull(smr_detail.sum_price,0 ) as sum_price\
                                             FROM warikan_membermodel as warikan\
                                             left join (select\
                                                            memberID_id,\
                                                            count(*) as cnt,\
                                                            sum(price) as sum_price\
                                                        from warikan_detailmodel\
                                                        group by memberID_id) as smr_detail\
                                                        on smr_detail.memberID_id = warikan.id\
                                             where tripID_id = %s' ,[self.kwargs['pk']]
                                            )
        trip_name = TripModel.objects.raw('SELECT * FROM warikan_tripmodel WHERE id = %s' ,[self.kwargs['pk']])
        context['trip_name'] = trip_name
        context['object_list'] = data_list
        if data_sum['price__sum'] is not None and 0 < data_sum['price__sum']:
            data_per = data_sum['price__sum'] // data_count
        else:
            data_per = 0
        context['data_count'] = data_count
        context['data_sum'] = data_sum
        context['data_per'] = data_per
        context['trip_pk'] = self.kwargs['pk']
        return context

class AddDetail(CreateView):
    template_name = 'adddetail.html'
    model = DetailModel
    fields = ('memberID','title','price','tripID',)

    def get_success_url(self):
        return reverse('memberlist',kwargs={'pk': self.object.tripID.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['memberID'] = self.kwargs['pk']
        data_list = MemberModel.objects.raw('select * from warikan_membermodel where id = %s',[self.kwargs['pk']])
        context['object_list'] = data_list
        return context

class DetailList(ListView):
    template_name = 'detaillist.html'
    model = DetailModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_list = DetailModel.objects.raw('select * from warikan_detailmodel where memberID_id = %s',[self.kwargs['pk']])
        context['object_list'] = data_list
        data_list = MemberModel.objects.raw('select * from warikan_membermodel where id = %s',[self.kwargs['pk']])
        context['object_member'] = data_list
        return context

class DetailUpdate(UpdateView):
    template_name = 'detailupdate.html'
    model = DetailModel
    fields = ('memberID','title','price','tripID',)
    def get_success_url(self):
        return reverse('detaillist',kwargs={'pk': self.object.memberID.id})

class DetailDelete(DeleteView):
    template_name = 'detaildelete.html'
    model = DetailModel
    def get_success_url(self):
        return reverse('detaillist',kwargs={'pk': self.object.memberID.id})

class AddPicture(CreateView):
    template_name = 'addpicture.html'
    model = PictureModel
    fields = ('picturename','url',)
    success_url = reverse_lazy('triplist')

class Division(ListView):
    template_name = 'division.html'
    model = MemberModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_count = MemberModel.objects.filter(tripID=self.kwargs['pk']).count()
        data_sum = DetailModel.objects.filter(tripID=self.kwargs['pk']).aggregate(Sum('price'))
        data_list = MemberModel.objects.raw('SELECT warikan.*,\
                                                ifnull(smr_detail.sum_price,0) as sum_price,\
                                                ifnull(smr_detail.sum_price,0)-(total_price/cnt_member) as pay_price\
                                                FROM warikan_membermodel as warikan\
                                            left join (select\
                                                tripID_id,\
                                                count(id) as cnt_member\
                                                from warikan_membermodel\
                                                group by tripID_id) as aaa\
                                                on aaa.tripID_id = warikan.tripID_id\
                                            left join (select\
                                                tripID_id,\
                                                sum(price) as total_price\
                                                from warikan_detailmodel\
                                                group by tripID_id) as bbb\
                                                on bbb.tripID_id = warikan.tripID_id\
                                            left join (select\
                                                memberID_id,\
                                                sum(price) as sum_price\
                                                from warikan_detailmodel\
                                                group by memberID_id) as smr_detail\
                                                on smr_detail.memberID_id = warikan.id\
                                                where warikan.tripID_id = %s' ,[self.kwargs['pk']]
                                            )
        context['object_list'] = data_list

        # 次は誰にはらうかのロジックを作成    

        detail_list = DetailModel.objects.filter(tripID=self.kwargs['pk'])
        context['detail_list'] = detail_list
        return context

class AddTrip(CreateView):
    template_name = 'addtrip.html'
    model = TripModel
    fields = ('tripname','startdate','enddate',)
    success_url = reverse_lazy('triplist')

class TripList(ListView):
    template_name = 'triplist.html'
    model = TripModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_list = TripModel.objects.raw('SELECT \
                                                trip.*,\
                                                ifnull(smr_member.membername,"") as membername\
                                             FROM warikan_tripmodel as trip\
                                             left join (select\
                                                            tripID_id as tripID_id,\
                                                            group_concat(membername) as membername\
                                                        from warikan_membermodel\
                                                        group by tripID_id) as smr_member\
                                                        on smr_member.tripID_id = trip.id'
                                            )
        context['object_list'] = data_list
        return context


class TripDelete(DeleteView):
    template_name = 'tripdelete.html'
    model = TripModel
    success_url = reverse_lazy('triplist')
