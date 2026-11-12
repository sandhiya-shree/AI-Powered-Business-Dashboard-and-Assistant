import requests

print("AI BUSINESS AGENT")
print("--------------")

Business_name = "Sunshine shop"
monthly_sales = 10000
monthly_cost = 6000
def calculate_profit (sales, cost):
    profit = sales - cost
    return profit

profit = calculate_profit (monthly_sales, monthly_cost)
tools = [
    {
        "type": "function",
    "function": 
    {
    "name": "calculate_profit",
    "description": "Calculate the shop's profit by finding the difference between sales and cost",
    "parameters": {
    "type": "object",
    "properties": {
        "sales":{
            "type":"number",
            "description":"total sales"
        },
        "cost":{
            "type":"number",
            "description":"total business cost"
        }
    },
        "required": ["sales","cost"]
    }
    }   
}]

print("Business name is ",Business_name)
print("Monthly sales is $",monthly_sales)
print("monthly profit is $", profit)
question = f"""
You are a business assistant.
The business is {Business_name}.
Its monthly sales are ${monthly_sales}.

Use the calculate_profit tool with sales = 10000 and cost = 6000. Do not invent or change these values.
"""

print("\nAsking the AI model for advice........\n")
response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "qwen2.5:3b",
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ],
        "stream": False,
        "tools": tools
    },
    timeout=180
)

response.raise_for_status()
result = response.json()["message"]
tool_call = result["tool_calls"][0]
print(tool_call)
arguments = tool_call["function"]["arguments"]
profit = calculate_profit(arguments["sales"],arguments["cost"])
print("AI tool calculated profit : $",profit)

print("\nMONTHLY BUSINESS REPORT")
print("------------")

monthly_data = [
    {"month": "January", "sales": 10000, "cost": 6000},
    {"month":"February", "sales": 12000, "cost": 10000},
    {"month": "March", "sales": 15000, "cost": 3000},
    {"month":"April", "sales": 19000, "cost": 7000},
]

for data in monthly_data:
    profit = data["sales"] - data["cost"]
    print(data["month"], "profit: $", profit)

print("\nBEST PERFORMING MONTH")
print("--------------------")

Best_month = max(monthly_data, key=lambda data: data["sales"])

print("month:", Best_month["month"])
print("Sales: $", Best_month["sales"])

Business_summary = "Sunshine shop monthly report\n"

for data in monthly_data:
    profit = data["sales"] - data["cost"]
    
    line = (
        f"{data['month']}:"
        f"sales $ {data['sales']}:"
        f"cost $ {data['cost']}:"
        f"profit $ {profit}\n"
    )

    Business_summary += line

Business_summary += (
    f"\nHighest sales month: {Best_month['month']}"
    f" (${Best_month['sales']})"
)

print("\nSUMMARY FOR AI")
print(Business_summary)

print("\nASKING QWEN FOR BUSINESS INSIGHTS")

response = requests.post(
    "http://localhost:11434/api/chat",
    json ={
        "model": "qwen2.5:3b",
        "messages":[
            {
                "role": "user",
                "content":(
                    "You are a business analyst for this shop. "
                    "Analyse the monthly sales, costs and profits. "
                    "Identify the strongest and weakest months by profit. "
                    "Suggest two practical ways to improve performance. "
                    "Use only the data provided and do not invent reasons.\n\n"
                    "Clearly distinguish data-based findings from general suggestions. "
                    "Do not claim that any particular factor caused a change in sales or profit. "
                    "State when the available data is insufficient to explain a result.\n\n"
                     +Business_summary
                )
            }
        ],
        "stream": False
    },
    timeout = 180
)

response.raise_for_status()
ai_insight = response.json()["message"]["content"]

print("\nAI BUSINESS INSIGHTS")
print("----------------")
print(ai_insight)

print("\nINTERACTIVE BUSINESS ASSISTANT")
print("--------------")
print("Ask questions about sunshine shop.")
print("Type'exit'to stop.\n")

Total_sales = sum(data["sales"]for data in monthly_data)
Total_cost = sum(data["cost"]for data in monthly_data)
Total_profit = Total_sales - Total_cost
Average_sales = Total_sales/len(monthly_data)
Average_profit = Total_profit/len(monthly_data)
Highest_profit = max(data["sales"]-data["cost"]for data in monthly_data)
Highest_profit_month = [
    data["month"]for data in monthly_data
    if data["sales"]-data["cost"] == Highest_profit
]
Lowest_profit_month = min(monthly_data, key=lambda data:data["sales"]-data["cost"])

business_facts=f"""
Business: {Business_name}
Reporting period:January to April (4 months only)
Total sales:${Total_sales}
Total cost:${Total_cost}
Total profit:${Total_profit}
Average monthly sales:${Average_sales:.2f}
Average monthly profit:${Average_profit:.2f}
Highest profit month(s):{','.join(Highest_profit_month)}(${Highest_profit})
Lowest profit month:{Lowest_profit_month['month']}

Monthly Report:
{Business_summary}
"""
if __name__=="__main__":
    while True:
        user_question = input("\nYou:")
        if user_question.lower().strip() == "exit":
            print("Business assisstant closed.Goodbye!")
            break
        if not user_question.strip():
            print("Please enter a question.")
            continue
        if "annual" in user_question.lower():
            print("\nAI ASSISTANT: Annual figures cannot be determined from the four months of data available.")
            continue
        response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model":"qwen2.5:3b",
            "messages":[
            {
                "role":"system",
                "content":(
                    "You are a business data assistant. "
                    "Answer using only the supplied business facts. "
                    "Do not invent figures or reasons. "
                    "If information is unavailable, say so. "
                    "Keep answers clear and concise. "
                    "Do not describe four months of data as annual figures. "
                    "Do not guess the reasons behind sales or profit changes. "
                    "If the data does not explain why, say that the reason is unavailable. "
                )
            },
            {
              "role":"user",
              "content":(
                business_facts
                +"\n\nBusiness question:"
                + user_question
              )  
            }
        ],
        "stream":False
    },
    timeout=180
    )

        response.raise_for_status()
        Answer = response.json()["message"]["content"]
        print("\nAI ASSISTANT:",Answer)

def get_business_answer(user_question):
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model":"qwen2.5:3b",
            "messages":[
                {"role": "system", "content": "Answer using only the supplied business facts. Be concise."},
                {"role": "user", "content": business_facts + "\n\n" + user_question}
            ],
            "stream":False
        },
        timeout=180
    )
    response.raise_for_status()
    return response.json()["message"]["content"]