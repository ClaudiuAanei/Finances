from datetime import datetime
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from finances.api.serializers.transactions import TransactionSerializer
from finances.selectors.transactions import TransactionsSelector


class TransactionsView(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        year = self.request.query_params.get("year") or datetime.now().year
        month = self.request.query_params.get("month") or datetime.now().month
        category = self.request.query_params.getlist("category")
        name = self.request.query_params.get("name", None)

        date = datetime(int(year), int(month), 1)

        transactions = TransactionsSelector(user)
        
        return transactions.get_transactions(date, category, name)


    def list(self, request):
        transactions = self.get_queryset()
        serializer = self.serializer_class(transactions, many=True)
        return Response(serializer.data)