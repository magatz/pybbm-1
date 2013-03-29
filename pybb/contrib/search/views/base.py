from django.shortcuts import render_to_response
from django.http import Http404

from pure_pagination import Paginator, InvalidPage

from haystack.views import SearchView as BaseSearchView

from pybb.helpers import lookup_users, lookup_post_topics
from pybb.contrib.search.fields import TreeModelMultipleChoiceField
from pybb.models import Forum


class SearchView(BaseSearchView):
    def build_form(self, *args, **kwargs):
        '''
        Override to change the form and the searchqueryset according to the user.
        Be carefull this is not thread safe ! Use haystack.views.search_view_factory
        to build this view.
        '''
        form = super(SearchView, self).build_form(*args, **kwargs)

        user = self.request.user
        if not user.is_authenticated():
            form.searchqueryset = form.searchqueryset.exclude(hidden=True)
            form.fields['forums'] = TreeModelMultipleChoiceField(
                queryset=Forum.objects.filter(hidden=False),
                join_field='forum_id',
                required=False
            )
        elif not user.is_staff:
            form.searchqueryset = form.searchqueryset.exclude(staff=True)
            form.fields['forums'] = TreeModelMultipleChoiceField(
                queryset=Forum.objects.filter(staff=False),
                join_field='forum_id',
                required=False
            )
        return form

    def build_page(self):
        """
        override to use pure_pagination
        """
        try:
            page_no = int(self.request.GET.get('page', 1))
        except (TypeError, ValueError):
            raise Http404("Not a valid number for page.")

        if page_no < 1:
            raise Http404("Pages should be 1 or greater.")

        start_offset = (page_no - 1) * self.results_per_page
        self.results[start_offset:start_offset + self.results_per_page]

        paginator = Paginator(self.results, self.results_per_page)

        try:
            page = paginator.page(page_no)
        except InvalidPage:
            raise Http404("No such page!")

        return (paginator, page)

    def normalize_results(self, result_list):
        """
        Adapt results to Post interface in order to display them the same way
        in templates
        """
        lookup_post_topics(result_list)
        lookup_users(result_list)
        for result in result_list:
            result.id = result.pk
            result.get_body_html = False

    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        """
        (paginator, page) = self.build_page()
        # build query_string
        qs = '&'.join(['='.join([k, v]) for k, v in self.form.data.items() if k != 'page'])

        objects = [o for o in page.object_list if o is not None]

        self.normalize_results(objects)

        # Fake Page object to build posts redirect_url
        post_page = {
            'number': 1
        }

        context = {
            'qs': qs,
            'query': self.query,
            'form': self.form,
            'page_obj': page,
            'paginator': paginator,
            'suggestion': None,
            'is_paginated': paginator.num_pages > 1,
            'show_information': True,
            'post_page': post_page,
        }

        if (self.results and hasattr(self.results, 'query') and
                self.results.query.backend.include_spelling):
            context['suggestion'] = self.form.get_suggestion()

        context.update(self.extra_context())

        return render_to_response(self.template,
                                  context,
                                  context_instance=self.context_class(self.request))
