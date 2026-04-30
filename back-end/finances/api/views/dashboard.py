from datetime import datetime
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from finances.models.budget import MonthlyBudget
from finances.selectors.dashboard import MonthlyBudgetSelector
from finances.api.serializers.dashboard import DashboardResponseSerializer


class DashboardView(viewsets.ViewSet):
    queryset = MonthlyBudget.objects.all()
    serializer_class = DashboardResponseSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def list(self, request):
        # Extract query parameters
        user = request.user
        transaction_type = request.query_params.get("type", "actual")
        year = request.query_params.get("year") or datetime.now().year
        month = request.query_params.get("month") or datetime.now().month

        # Validate and parse year and month
        if year and month:
            try:
                date = datetime(int(year), int(month), 1)
            except ValueError:
                return Response({"error": "Invalid year or month."}, status=400)
        else:
            date = datetime.now().replace(day=1)

        # Get dashboard data using the selector
        dashboard_selector = MonthlyBudgetSelector(user, date)
        dashboard_data = dashboard_selector.get_dashboard_data(transaction_type=transaction_type)

        # Serialize and return the response
        serializer = DashboardResponseSerializer(dashboard_data)

        return Response(serializer.data)