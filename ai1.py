from groq import Groq
import json
import requests



def fahrenheit_to_celsius(fahrenheit):
    celsius = (fahrenheit - 32) * 5 / 9
    return celsius

def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius."""
    celsius = kelvin - 273.15
    return int(celsius) 
def getWeatherdetails(city="Lucknow"):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=4576e660c722646e31010124a003636e"
    response = requests.get(url)
    data = response.json()["main"]["temp"]
    temp = kelvin_to_celsius(data)
    return temp


def llm():
    API_KEY = "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"
    tools = {"getWeatherdetails": getWeatherdetails}
    
    prompt = """
            You are an AI assistant with start,plan ,action , observation and output state
            wait from the user prompt and first plan using available tools.
            after planning , take the  action with appropriate tools and wit for observation based on action
            once you get the observation, return the AI response based on start prompt and observations

            Strictly follow the JSON output formate as in example

            Available Tools:
            def getWeatherdetails(city:string)->string
            getWeatherdetails accept the city name as string and return weather detail of that city

            Example
            START
            {"type":"user","user":"what is the weather in lucknow?"}
            {"type":"plan","plan":"i will call the getWeatherdetails for lucknow"}
            {"type":"action","function":"getWeatherdetails","input":"lucknow"}
            {"type":"observation","observation":"10°C"}
            {"type":"output","output":"the weather in lucknow is 10°C"}

            """
    prompt2="""
            You are an AI assistant when user greets you have to greet to user 

             Strictly follow the JSON output formate as in example
            Example
            START
            {"type":"user","user":"Hi"}
            {"type":"output","output":"Hello, how can I help you ..."}

            this is a example you can give output by yourself
            """
    try:
        clint = Groq(api_key=API_KEY)
        message = [
            {
                "role": "system",
                "content": prompt,
            },
             {
            "role": "system",
            "content": prompt2
        }
        ]
        while True:
            inp = input(">>-- ")
            q = {"type": "user", "user": inp}
            message.append(
                {
                    "role": "user",
                    "content": json.dumps(q, separators=(",", ":")),
                }
            )
            while True:
                response = clint.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=message,
                    response_format={"type": "json_object"},
                )
                result = response.choices[0].message.content
                message.append({"role": "assistant", "content": result})
                call = json.loads(result)
                if call["type"] == "output":
                    print(f"🤖 {call['output']}")
                    break
                elif call["type"] == "action":
                    fn = tools[call["function"]]
                    observation = fn(call["input"])
                    obs = {"type": "observation", "observation": observation}
                    message.append({"role": "assistant", "content": json.dumps(obs)})
    except Exception as e:
        print(e)


llm()


