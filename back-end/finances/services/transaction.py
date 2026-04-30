from finances.models.transactions import Transaction
from finances.models.categories import Category
from finances.services.monthly import MonthlyBudgetService
from django.db import IntegrityError

class TransactionService:
    def __init__(self, user):
        self.user = user

    def _get_or_create_monthly_budget(self, date):
        """Get or create the monthly budget for the given user and date."""
        monthly_budget, _ = MonthlyBudgetService.get_or_create_monthly_budget(user=self.user, date=date)
        return monthly_budget
    
    def _get_or_create_category(self, category_name):
        """Get or create the category for the transaction."""
        category, _ = Category.objects.get_or_create(name=category_name.strip().lower())

        if category:
            category.users.add(self.user)  # Associate the category with the user

        category.type = "expense" if category_name.strip().lower() != "income" else "income"
        category.save()

        return category
    

    def create_transaction(self, validated_data):

        monthly_budget = self._get_or_create_monthly_budget(validated_data["date"])
        category = self._get_or_create_category(validated_data.get("category"))
        description = validated_data.get("description", "").strip() if validated_data.get("description") else ""

        transaction = Transaction.objects.create(
            user=self.user,
            name =validated_data["name"].strip() if validated_data.get("name") else "No name",
            amount=abs(validated_data["amount"]),
            date=validated_data["date"],
            category=category,
            type=validated_data.get("type", "actual"),
            monthly_budget=monthly_budget,
            description = description
        )
        
        return transaction


    def create_many_transactions(self, transactions_data):
        """Create multiple transactions for the user."""
        created_transactions = []
        duplicates_data = []
        for data in transactions_data:
            try:
                transaction = self.create_transaction(data)
                created_transactions.append(transaction)
            except IntegrityError:
                duplicates_data.append(data)

        if len(duplicates_data) > 0:
            return {
                "processed_count": len(created_transactions),
                "duplicates_count": len(duplicates_data),
                "duplicates_data": duplicates_data
            }
        
        return created_transactions

    
    def get_transactions(self, date):
        """Get all transactions for the user and the specified month."""
        transactions = Transaction.objects.filter(
            user=self.user,
            date__year=date.year,
            date__month=date.month
        ).select_related("category")

        return transactions
    
