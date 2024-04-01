from openai import OpenAI
import keys
client = OpenAI(
            api_key=keys.gbt_api_key)

def story_writer(desc):
    writer = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": '''
                                            You are given a list of descriptions, of a similar event. Using the small descriptions craft an unbiased news article at 150 words.
                                            '''},
            {"role": "user",
             "content": f'''
                                                DESCRIPTIONS:{desc}. 
                                                Create a news article using the descriptions in the tupple.'''}
        ]
    )
    return writer.choices[0].message.content

def opinnion_id(ref_art,op_art):
    writer = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": ''' You are given a objective and opinnionated article. Identify opinnions present in the opinnionated
             article, present these as short sentences.
                                            '''},
            {"role": "user",
             "content": f'''
                         unbiased articles: {ref_art}
                         opinionated article:{op_art}
                         Identify opinnions present in the opinnionated
                        article, present these as short sentences as follows:
                        !p1!: first opinnion
                        !p2!: second opinnion ... '''}
        ]
    )
    return writer.choices[0].message.content
