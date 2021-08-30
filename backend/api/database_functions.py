from django.db.models import Subquery, IntegerField


class SubquerySum(Subquery):
    def __or__(self, other):
        super(SubquerySum, self).__or__(other)

    def __rand__(self, other):
        super(SubquerySum, self).__rand__(other)

    def __ror__(self, other):
        super(SubquerySum, self).__ror__(other)

    def __and__(self, other):
        super(SubquerySum, self).__and__(other)

    template = "(SELECT SUM({}) FROM (%(subquery)s) _sum)"

    def __init__(self, queryset, output_field=IntegerField(), field_name=None, **extra):
        if field_name is None:
            raise AssertionError('You need to provide field to sum on')
        if '__' in field_name:
            raise AssertionError('Cannot use relations yet')

        super(SubquerySum, self).__init__(queryset=queryset, output_field=output_field, **extra)
        self.template = self.template.format(field_name)
