import json
from openai import OpenAI
client=OpenAI(base_url="http://localhost:11434/v1",api_key="ollama")

addition_tool={
    "type":"function",
    "function":{
        "name":"addition",
        "description":"adds two number and returns sum",
        "parameters":{
            "type":"object",
            "properties":{
                "a":{"type":"number","description":"first number"},
                "b":{"type":"number","description":"second number"}
            },
        "required":["a","b"]
        }
    }
}
multiplication_tool={
    "type":"function",
    "function":{
        "name":"multiplication",
        "description":"takes two numbers and returns the product",
        "parameters":{
            "type":"object",
            "properties":{
                "a":{"type":"number","description":"the first number"},
                "b":{"type":"number","description":"the second number"}
            },
        "required":["a","b"]
        }
    }
}
subtraction_tool={
    "type":"function",
    "function":{
        "name":"subtraction",
        "description":"takes two numbers and outputs the difference",
        "parameters":{
            "type":"object",
            "properties":{
                "a":{"type":"number","description":"first number"},
                "b":{"type":"number","description":"second number"}
            },
        "required":["a","b"]
        }
    }
}
division_tool={
    "type":"function",
    "function":{
        "name":"division",
        "description":"takes two numbers and divides one with other and returns the result",
        "parameters":{
            "type":"object",
            "properties":{
                "a":{"type":"number","decription":"first number"},
                "b":{"type":"number","description":"second number"}
            },
        "required":["a","b"]
        }
    }
}

def addition(a,b):
    return a+b
def multiplication(a,b):
    return a*b
def subtraction(a,b):
    return a-b
def division(a,b):
    try:
        return a/b
    except Exception as e:
        return f"error in division {str(e)}"


tool_list=[addition_tool,multiplication_tool,subtraction_tool,division_tool]
tool_dispatch={"addition":addition,"multiplication":multiplication,"division":division,"subtraction":subtraction}

def run_agent(user_input,messages):
    messages.append({"role":"user","content":user_input})
    max_count=10
    current_count=0
    while current_count< max_count:
        current_count+=1
        response=client.chat.completions.create(model="llama3.1",messages=messages,tools=tool_list)
        assistant_msg=response.choices[0].message
        if not assistant_msg.tool_calls:
            messages.append({"role":"assistant","content":assistant_msg.content})
            return assistant_msg.content
        messages.append(assistant_msg)
        tool_call=assistant_msg.tool_calls[0]
        name=tool_call.function.name
        args_str=tool_call.function.arguments
        print(f"[tool] {name} ({args_str})")
        try:
            args=json.loads(args_str)
            func_to_call=tool_dispatch[name]
            result=func_to_call(**args)
        except  Exception as e:
            result= f"Error executing tool {str(e)}"
        messages.append({"role":"tool","tool_call_id":tool_call.id,"name":name,"content":str(result)})
    return "Agent terminated : exceeded the limit"

if __name__=="__main__":
    message_history=[{"role":"system","content":"act as an expert in solvung mathematical problems and solve it step by step"}]
    print("agent is active press 'q' to exit" )
    while True:
        user_input=input("You:  ")
        if user_input.strip().lower()=='q':
            print("Good bye")
            break
        if not user_input.strip():
            continue
        final_answer=run_agent(user_input,message_history)
        print(f"Agent: {final_answer}\n")