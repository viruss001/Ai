"""
        clint=Groq(api_key=API_KEY)
        response = clint.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role":"system","content": prompt,}]
            

        )
        # print(response)
        result = response.choices[0].message.content
        print(result)"""