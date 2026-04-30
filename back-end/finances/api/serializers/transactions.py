from rest_framework import serializers
from finances.models.transactions import Transaction
from finances.services.transaction import TransactionService

class TransactionSerializer(serializers.ModelSerializer):
    """
    
    Serializer for the Transaction model, used for creating and listing transactions.
    It includes fields for the transaction's type, amount, currency, category, date, and description.
    The create method is overridden to use the TransactionService for creating transactions, which handles
    the logic for associating transactions with monthly budgets, categories, and descriptions.

    """
    description = serializers.CharField(required=False, allow_blank=True)
    category = serializers.CharField(required=False, allow_blank=True)
    category_id = serializers.IntegerField(required=False, allow_null=True, read_only=True)

    class Meta:
        model = Transaction
        fields = ["id", "name", "type", "amount", "currency", "category_id", "category", "date", "description"]

    def create(self, validated_data):
        user = self.context["request"].user

        transaction_service = TransactionService(user)
        transaction = transaction_service.create_transaction(validated_data)

        return transaction
    
