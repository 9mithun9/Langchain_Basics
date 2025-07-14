from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import json
from typing import Annotated, Optional, Literal
from pydantic import BaseModel, Field

load_dotenv()

model = ChatOpenAI()


review_schema = {
  "title": "Review",
  "type": "object",
  "properties": {
    "summary": {
      "title": "Summary",
      "type": "string",
      "description": "A brief summary of the review."
    },
    "sentiment": {
      "title": "Sentiment",
      "type": "string",
      "description": "The sentiment of the review, either 'positive', 'negative', or 'neutral'.",
      "enum": ["positive", "negative"]
    },
    "positive": {
      "title": "Positive",
      "type": ["array", "null"],
      "items": {
        "type": "string"
      },
      "description": "A list of positive aspects of the review, if any."
    },
    "negative": {
      "title": "Negative",
      "type": ["array", "null"],
      "items": {
        "type": "string"
      },
      "description": "A list of negative aspects of the review, if any."
    },
    "reviewer": {
      "title": "Reviewer",
      "type": ["string", "null"],
      "description": "The name of the reviewer if written by a specific person. Don't include if not specified or anonymous."
    }
  },
  "required": ["summary", "sentiment"]
}


structured_model = model.with_structured_output(review_schema)


result = structured_model.invoke("""There is very little that I can add to the reviews on here, that have explained what is so wonderful about The Godfather so well. I have seen many amazing movies, as well as some clunkers, but The Godfather was beyond amazing. There are so many images, details and scenes that I seriously cannot get out of my head since watching it for the first time just nine hours ago. The Godfather is so incredibly well-made and acted that it stands out among the rest of those other amazing films I've seen, so much so I couldn't think of a single flaw, and I am struggling to think of a good enough reason to why I didn't see this film before now.

True, The Godfather is a little slow-moving and the plot takes a while to unfold, but neither of these are flaws as such. The slow pacing added to the elegiac quality The Godfather has, and as for the plot what is special about this plot is that it is very unpredictable because you have next to no idea where it is next going to take you. Being 18, I was worried whether I was old enough to appreciate this film or even understand it, but luckily I understood it perfectly, and I can well and truly appreciate it for the masterpiece it is considered to be.

The Godfather for one thing looks stunning. I strongly disagree with the previous reviewer who said the cinematography was horrid, for me the cinematography was one of the best assets of the film. In some scenes you have cinematography and lighting that is quite dark and mysterious, and then in scenes such as the wedding it is evergreen, autumnal and very picturesque. It is not just the cinematography that makes The Godfather look stunning, the costumes are beautifully tailored, the houses are gorgeous and majestic to look at and even the cars were immaculate.

Then there is the score by Nina Rota. One word, outstanding! I have heard many wonderful scores in my lifetime, but after hearing this score few stick in the memory as much as the score for The Godfather. This score is both beautiful as seen with the main theme, and haunting in the way it sticks in your head after watching the film itself. Other outstanding assets are the masterly direction from Francis Ford Coppola, and the brilliantly written screenplay that is intelligent, thought-provoking and darkly humorous. As for the violence, some of it is shocking and intense especially in the climax which was enough to almost make your heart either beat twice as fast or stop, and I almost covered my eyes when the producer found the horse's head in his bed, but underneath that this family is somewhat loyal and honourable come to think of it.

The acting is absolutely fantastic, bringing to life characters that are rich and complex, perhaps unlikeable at first but as you get to know them you warm to them. And I have to say, The Godfather is one of those rarities where no actor gives a weak performance. In particular, Marlon Brando is brilliant as Don Vito, very heavily disguised yet stately. Every word of dialogue, every subtle hand gesture and every facial expression was brilliantly judged. Al Pacino's casting was admittedly risky, but he still did a truly wonderful job carrying the film, while James Caan is dignified and loyal, Diane Keaton beautiful and alluring and Robert Duvall nicely understated.

In conclusion, absolutely amazing, and I can see completely why it is considered one of the 10 greatest movies ever made, it is that good. In fact my 15-year old brother loved it so much, he wants to see it again. 10/10, though this film is too good for that rating. Bethany Cox""")



print(result)

# Save the result_dict as JSON
with open("structured_output/review_result_json.json", "w") as f:
    json.dump(result, f, indent=2)

