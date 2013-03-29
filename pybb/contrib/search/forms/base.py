from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from haystack.forms import SearchForm as HaystackSearchForm

from pybb.contrib.search.fields import TreeModelMultipleChoiceField
from pybb.models import Forum


class SearchForm(HaystackSearchForm):
    user_id = forms.ModelChoiceField(queryset=User.objects.all(),
                                     required=False,
                                     label=_('Username'))

    replies = forms.IntegerField(label=_('Number of answers'),
                                 min_value=0, required=False)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        self.fields['forums'] = TreeModelMultipleChoiceField(queryset=Forum.objects.all(),
                                                             join_field='forum_id',
                                                             required=False)

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        sqs = super(SearchForm, self).search()

        if self.cleaned_data.get('forums', None):
            sqs = sqs.filter(topic_breadcrumbs__in=[f.id for f in self.cleaned_data['forums']])
        if self.cleaned_data.get('user_id', None):
            sqs = sqs.filter(user_id=self.cleaned_data['user_id'].pk)
        if self.cleaned_data.get('replies', None):
            sqs = sqs.filter(replies__gte=self.cleaned_data['replies'])
        if self.cleaned_data.get('topic_id', None):
            sqs = sqs.filter(topic_id=self.cleaned_data['topic_id'])

        return sqs
