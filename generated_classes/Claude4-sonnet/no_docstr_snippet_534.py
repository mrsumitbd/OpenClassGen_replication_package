class BaseNewsItemChooserMixin:
    
    def get_filter_form_class(self):
        from wagtail.admin.forms import WagtailAdminPageForm
        
        class NewsItemFilterForm(WagtailAdminPageForm):
            q = forms.CharField(
                label=_("Search"),
                widget=forms.TextInput(attrs={'placeholder': _("Search news items")}),
                required=False
            )
            
        return NewsItemFilterForm

    @property
    def columns(self):
        return [
            {
                'name': 'title',
                'label': _('Title'),
                'sort_key': 'title',
            },
            {
                'name': 'date',
                'label': _('Date'),
                'sort_key': 'date',
            },
            {
                'name': 'status',
                'label': _('Status'),
                'sort_key': 'live',
            },
        ]