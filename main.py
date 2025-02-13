from datetime import datetime, date
import json
from typing import Dict, List, Optional
import pandas as pd
from dataclasses import dataclass
import matplotlib.pyplot as plt
from pathlib import Path
import random

@dataclass
class Transaction:
    date: datetime
    amount: float
    category: str
    description: str
    transaction_type: str  # 'income' or 'expense'

class BudgetManager:
    def __init__(self):
        self.categories = {
            'Housing': 0,
            'Transportation': 0,
            'Food': 0,
            'Utilities': 0,
            'Healthcare': 0,
            'Entertainment': 0,
            'Savings': 0,
            'Income': 0,
            'Other': 0,
            'mortgage_interest': 0,
            'charitable_contributions': 0,
            'medical_expenses': 0,
            'child_care': 0,
            'education': 0
        }
        self.transactions: List[Transaction] = []
        self.monthly_budget = {}
        self.monthly_spending = {}

    def set_budget(self, category: str, amount: float) -> None:
        if category in self.categories:
            self.monthly_budget[category] = amount
        else:
            raise ValueError(f"Invalid category: {category}")

    def get_budget(self, category: str) -> float:
        return self.monthly_budget.get(category, 0.0)

    def add_transaction(self, amount: float, category: str, description: str,
                        transaction_type: str = 'expense', transaction_date: Optional[datetime] = None) -> None:
        if category not in self.categories:
            raise ValueError(f"Invalid category: {category}")

        if transaction_date is None:
            transaction_date = datetime.now()

        transaction = Transaction(
            date=transaction_date,
            amount=amount,
            category=category,
            description=description,
            transaction_type=transaction_type
        )
        self.transactions.append(transaction)

        if transaction_type == 'expense':
            self.categories[category] += amount
        else:  # income
            self.categories['Income'] += amount

    def get_monthly_report(self, year: int, month: int) -> Dict:
        monthly_transactions = [
            t for t in self.transactions
            if t.date.year == year and t.date.month == month
        ]

        report = {
            'total_income': sum(t.amount for t in monthly_transactions if t.transaction_type == 'income'),
            'total_expenses': sum(t.amount for t in monthly_transactions if t.transaction_type == 'expense'),
            'transactions_by_category': {},
            'savings_rate': 0
        }

        for category in self.categories:
            cat_transactions = [t for t in monthly_transactions if t.category == category]
            if cat_transactions:
                report['transactions_by_category'][category] = {
                    'total': sum(t.amount for t in cat_transactions),
                    'count': len(cat_transactions),
                    'budget': self.get_budget(category),
                    'transactions': [
                        {
                            'date': t.date.strftime('%Y-%m-%d'),
                            'amount': t.amount,
                            'description': t.description
                        } for t in cat_transactions
                    ]
                }

        if report['total_income'] > 0:
            report['savings_rate'] = ((report['total_income'] - report['total_expenses']) / report['total_income']) * 100

        return report

    def get_budget_status(self) -> Dict:
        status = {}
        for category in self.categories:
            budget = self.get_budget(category)
            spent = self.categories[category]
            if budget > 0:
                status[category] = {
                    'budget': budget,
                    'spent': spent,
                    'remaining': budget - spent,
                    'percentage_used': (spent / budget * 100) if budget > 0 else 0
                }
        return status

class InvestmentAdvisor:
    def __init__(self):
        self.risk_tolerance = None
        self.investment_goals = None
        self.market_conditions = self.simulate_market_conditions()

    def simulate_market_conditions(self):
        return {
            'stock_market': random.choice(['bull', 'bear', 'neutral']),
            'interest_rates': random.uniform(0.5, 5.0),
            'economic_outlook': random.choice(['positive', 'negative', 'neutral'])
        }

    def set_user_profile(self, risk_tolerance, investment_goals):
        self.risk_tolerance = risk_tolerance
        self.investment_goals = investment_goals

    def provide_investment_advice(self, monthly_report: Dict) -> List[str]:
        advice = []
        income = monthly_report['total_income']
        expenses = monthly_report['total_expenses']
        savings_rate = monthly_report['savings_rate']

        if self.risk_tolerance is None or self.investment_goals is None:
            advice.append("Please set your risk tolerance and investment goals for personalized advice.")
            return advice

        if savings_rate < 10:
            advice.append("Focus on increasing your savings rate before making significant investments.")
            return advice

        if self.risk_tolerance == 'low':
            advice.append("Consider low-risk investments like high-yield savings accounts or government bonds.")
        elif self.risk_tolerance == 'medium':
            advice.append("A balanced portfolio of stocks and bonds could be suitable for your risk tolerance.")
        elif self.risk_tolerance == 'high':
            advice.append("You might consider a stock-heavy portfolio or exploring alternative investments.")

        if self.market_conditions['stock_market'] == 'bull':
            advice.append("The stock market is currently bullish. It might be a good time to invest in equities.")
        elif self.market_conditions['stock_market'] == 'bear':
            advice.append("The stock market is bearish. Consider defensive stocks or wait for better entry points.")

        if self.market_conditions['interest_rates'] > 3:
            advice.append(f"With high interest rates ({self.market_conditions['interest_rates']:.2f}%), consider bonds or high-yield savings accounts.")

        if self.investment_goals == 'retirement':
            advice.append("For retirement, consider tax-advantaged accounts like 401(k)s or IRAs.")
        elif self.investment_goals == 'short_term':
            advice.append("For short-term goals, focus on liquid and low-risk investments.")

        return advice

class TaxAssistant:
    def __init__(self):
        self.tax_brackets = {
            (0, 9950): 0.10,
            (9951, 40525): 0.12,
            (40526, 86375): 0.22,
            (86376, 164925): 0.24,
            (164926, 209425): 0.32,
            (209426, 523600): 0.35,
            (523601, float('inf')): 0.37
        }
        self.standard_deduction = 12550  # for single filers, 2021

    def calculate_tax_liability(self, income: float) -> float:
        taxable_income = max(income - self.standard_deduction, 0)
        tax = 0
        for (lower, upper), rate in self.tax_brackets.items():
            if taxable_income > lower:
                tax += (min(taxable_income, upper) - lower) * rate
        return tax

    def provide_tax_advice(self, income: float, expenses: Dict[str, float]) -> List[str]:
        advice = []
        tax_liability = self.calculate_tax_liability(income)

        advice.append(f"Based on your income of ${income:.2f}, your estimated tax liability is ${tax_liability:.2f}.")
        advice.append(f"Your effective tax rate is approximately {(tax_liability / income) * 100:.2f}%.")

        if expenses.get('mortgage_interest', 0) > 0:
            advice.append("You may be eligible for the mortgage interest deduction.")
        if expenses.get('charitable_contributions', 0) > 0:
            advice.append("Don't forget to claim your charitable contributions as deductions.")
        if expenses.get('medical_expenses', 0) > 0.075 * income:
            advice.append("You may be eligible to deduct medical expenses exceeding 7.5% of your income.")

        if expenses.get('child_care', 0) > 0:
            advice.append("Look into the Child and Dependent Care Credit.")
        if expenses.get('education', 0) > 0:
            advice.append("You might be eligible for education-related tax credits like the American Opportunity Credit or Lifetime Learning Credit.")

        advice.append("Keep all receipts and documentation for your deductions and credits.")
        advice.append("The deadline for filing your tax return is April 15th. Mark your calendar!")

        return advice

class FinancialAIAgent:
    def __init__(self):
        self.budget_manager = BudgetManager()
        self.investment_advisor = InvestmentAdvisor()
        self.tax_assistant = TaxAssistant()
        self._create_data_directory()

    def _create_data_directory(self):
        Path("financial_data").mkdir(exist_ok=True)

    def save_data(self, filename: str = "financial_data/financial_data.json") -> None:
        try:
            data = {
                'categories': self.budget_manager.categories,
                'monthly_budget': self.budget_manager.monthly_budget,
                'transactions': [
                    {
                        'date': t.date.isoformat(),
                        'amount': t.amount,
                        'category': t.category,
                        'description': t.description,
                        'transaction_type': t.transaction_type
                    }
                    for t in self.budget_manager.transactions
                ]
            }
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Data successfully saved to {filename}")
        except Exception as e:
            print(f"Error saving data: {str(e)}")

    def set_investment_profile(self, risk_tolerance: str, investment_goals: str):
        self.investment_advisor.set_user_profile(risk_tolerance, investment_goals)

    def generate_financial_report(self, year: int, month: int) -> Dict:
        monthly_report = self.budget_manager.get_monthly_report(year, month)

        report = {
            'period': f"{year}-{month:02d}",
            'income_summary': {
                'total_income': monthly_report['total_income'],
                'total_expenses': monthly_report['total_expenses'],
                'net_income': monthly_report['total_income'] - monthly_report['total_expenses'],
                'savings_rate': monthly_report['savings_rate']
            },
            'spending_by_category': monthly_report['transactions_by_category'],
            'recommendations': self._generate_recommendations(monthly_report)
        }

        return report

    def _generate_recommendations(self, monthly_report: Dict) -> List[str]:
        recommendations = []
        income = monthly_report['total_income']
        expenses = monthly_report['total_expenses']
        savings_rate = monthly_report['savings_rate']

        if savings_rate < 20:
            recommendations.append("Consider increasing your savings rate to at least 20% of income")

        if 'Housing' in monthly_report['transactions_by_category']:
            housing_cost = monthly_report['transactions_by_category']['Housing']['total']
            if housing_cost > income * 0.3:
                recommendations.append("Housing costs exceed 30% of income - consider ways to reduce housing expenses")

        investment_advice = self.investment_advisor.provide_investment_advice(monthly_report)
        recommendations.extend(investment_advice)

        expense_dict = {category: data['total'] for category, data in monthly_report['transactions_by_category'].items()}
        tax_advice = self.tax_assistant.provide_tax_advice(income, expense_dict)
        recommendations.extend(tax_advice)

        return recommendations

def create_sample_financial_agent():
    try:
        agent = FinancialAIAgent()

        agent.budget_manager.set_budget('Housing', 1600)
        agent.budget_manager.set_budget('Food', 500)
        agent.budget_manager.set_budget('Transportation', 300)

        agent.budget_manager.add_transaction(5000, 'Income', 'Monthly Salary', 'income')
        agent.budget_manager.add_transaction(1500, 'Housing', 'Rent', 'expense')
        agent.budget_manager.add_transaction(400, 'Food', 'Groceries', 'expense')
        agent.budget_manager.add_transaction(200, 'Transportation', 'Gas', 'expense')
        agent.budget_manager.add_transaction(100, 'charitable_contributions', 'Donation', 'expense')
        agent.budget_manager.add_transaction(300, 'medical_expenses', 'Doctor visit', 'expense')

        return agent
    except Exception as e:
        print(f"Error creating sample agent: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        agent = create_sample_financial_agent()

        agent.set_investment_profile(risk_tolerance='medium', investment_goals='retirement')

        current_year = datetime.now().year
        current_month = datetime.now().month
        report = agent.generate_financial_report(current_year, current_month)

        print("\nFinancial Report")
        print("-" * 50)
        print(f"Period: {report['period']}")
        print(f"\nIncome Summary:")
        print(f"Total Income: ${report['income_summary']['total_income']:,.2f}")
        print(f"Total Expenses: ${report['income_summary']['total_expenses']:,.2f}")
        print(f"Net Income: ${report['income_summary']['net_income']:,.2f}")
        print(f"Savings Rate: {report['income_summary']['savings_rate']:.1f}%")

        print("\nBudget Status:")
        budget_status = agent.budget_manager.get_budget_status()
        for category, status in budget_status.items():
            print(f"\n{category}:")
            print(f"  Budget: ${status['budget']:,.2f}")
            print(f"  Spent: ${status['spent']:,.2f}")
            print(f"  Remaining: ${status['remaining']:,.2f}")
            print(f"  Used: {status['percentage_used']:.1f}%")

        print("\nRecommendations:")
        for rec in report['recommendations']:
            print(f"- {rec}")

    except Exception as e:
        print(f"Error running the program: {str(e)}")