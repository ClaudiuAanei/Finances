from rest_framework import serializers
from finances.models.transactions import Transaction


class DashboardSummarySerializer(serializers.Serializer):
    income = serializers.DecimalField(max_digits=12, decimal_places=2)
    expense = serializers.DecimalField(max_digits=12, decimal_places=2)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)


class DashboardMonthlyTargetSerializer(serializers.Serializer):
    saving_target = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    current_saved = serializers.DecimalField(max_digits=12, decimal_places=2)
    remaining_to_target = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    progress_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True)


class DashboardCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    type = serializers.ChoiceField(choices=["income", "expense"])
    spent = serializers.DecimalField(max_digits=12, decimal_places=2)
    limit = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    remaining = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    percentage_used = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True)


class DashboardResponseSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=[choice[0] for choice in Transaction.TYPE_CHOICES])
    budget = serializers.CharField()
    selected_date = serializers.CharField()
    available_years = serializers.ListField(child=serializers.IntegerField())
    available_months = serializers.ListField(child=serializers.IntegerField())
    summary = DashboardSummarySerializer()
    monthly_target = DashboardMonthlyTargetSerializer(allow_null=True)
    categories = DashboardCategorySerializer(many=True)
