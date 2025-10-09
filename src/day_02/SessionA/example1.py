def calculate_profit_margin(revenue, cost):
    """
    Calculate profit margin.
    revenue (float): Total revenue
    cost (float): Total cost
    return (float): Profit margin percentage
    """
    profit = revenue - cost
    return round((profit / revenue) * 100, 2)


def compound_interest(principal, rate, times_compounded, years=5):
    """
    Calculate compound interest.

    principal (float): Initial amount of money
    rate (float): Annual interest rate in decimal (e.g., 0.05 for 5%)
    times_compounded (int): Number of times interest is compounded per year
    years (int): Number of years money is invested/borrowed

    Returns:
        final_amount (float): Value after interest
        interest (float): Compound interest earned
    """
    final_amount = principal * (1 + rate / times_compounded) ** (times_compounded * years)
    interest = final_amount - principal
    return round(final_amount, 2), round(interest, 2)



if __name__ == "__main__":
    # Example use in BI
    revenue = 100000
    cost = 65000
    margin = calculate_profit_margin(revenue, cost)
    print(f"Profit Margin: {margin}%")

    # Example usage
    amount, interest = compound_interest(
         times_compounded=5 , rate=0.05, principal=3000) 
     # $10,000 at 5% compounded quarterly for 5 years
    print("Final Amount:", amount)
    print("Compound Interest:", interest)
