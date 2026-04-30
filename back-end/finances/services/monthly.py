from finances.models.budget import MonthlyBudget

class MonthlyBudgetService:

    @staticmethod
    def get_or_create_monthly_budget(user, date):
        return MonthlyBudget.objects.get_or_create(
            user=user, 
            date__month=date.month, 
            date__year=date.year,
            date=date.replace(day=1),  # Store the date as the first of the month for consistency
            defaults={"saving_goal": 0}
        )
    
    @staticmethod
    def update_saving_goal(monthly_budget, saving_goal):
        monthly_budget.saving_goal = saving_goal
        monthly_budget.save()
        return monthly_budget
    
    @staticmethod
    def get_monthly_budget(user, date):
        return MonthlyBudget.objects.filter(
            user=user, 
            date__month=date.month, 
            date__year=date.year
        ).first()
