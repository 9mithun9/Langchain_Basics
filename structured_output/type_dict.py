from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Optional
import json

load_dotenv()

model = ChatOpenAI()

class Review(TypedDict):
    summary: Annotated[str, "A brief summary of the review in 50 words or less"]
    sentiment: Annotated[str, "The sentiment of the review, either 'positive', 'negative', or 'neutral'"]
    positive: Annotated[Optional[list[str]], "A list of positive aspects of the review, if any"]
    negative: Annotated[Optional[list[str]], "A list of negative aspects of the review, if any"]
    reviewer: Annotated[Optional[str], "The name of the reviewer if written by a specific person. Don't include if not specified or anonymous."]


structured_model = model.with_structured_output(Review)


result = structured_model.invoke("""Do not be fooled by the coy charm of the promotional poster. The image of the girl shyly leaning over to kiss the cheek of a bare-backed boy on golden sands drenched in sunlight represents an ideal that many residents of the City of God strive for, but few achieve.

The rewards are all too tangible: The football, the music, the heady culture of samba and carnival joie de vivre is never far away, but escaping from the slums of Rio is a little more complicated than sloping off to the beach for the afternoon. The City of God is a raging maelstrom of violence, drugs and gang warfare, and its inhabitants are indoctrinated in the way of the gun from an early age.

Fernando Meirelles' film (based on a true story) is a breathtakingly convincing interpretation of life in the notorious Rio favela. Using hundreds of real-life slum children to supplement a superb central cast and shooting entirely around the dusty streets and abject poverty of the neighbourhood, Meirelles charts the history of the area through the narration of Rocket, a peaceable soul with journalistic aspirations who is entirely at odds with the mayhem around him.

Rocket explains how the slum was used as a dumping ground for all Rio's undesirables in the 1960s. Despite a population of criminals and ne'er-do-wells, the early part of the film is an homage to plucky underdog cheeriness and community spirit. Rocket's brother is a member of the 'Tender Trio', a dashing group of bandits who go about brandishing pistols and holding up gas trucks like latter day highwaymen.

Despite an elegant notoriety, the Trio's crimes tend to yield less than impressive fiscal reward, so they plan a heist on a motel-cum-knocking shop in an attempt to up the ante. It goes badly wrong. The gang's lily-livered tendencies mean they make a sharp exit at the first sniff of trouble but, unbeknownst to them, their lookout, unhappy with his passive role in proceedings (as bored nine-year-old little brothers are wont to be), strolls into the motel and fires at will, chortling psychotically as each hooker and john crumples to the floor.

The kid in question is L'il Dice, a chubby Arnold-out-of-Diff'rent-Strokes lookalike with an insatiable lust for mayhem. The motel incident marks a shift in emphasis for the City of God and the following years see the slum descend into chaos as L'il Dice (later renamed L'il Ze) builds a narcotics empire by ruthlessly eliminating the competition.

The streets become a recruiting ground for drug dealers and gang lieutenants. Small children (or 'runts' as they are affectionately known) come to see guns and criminal activity as the only viable rungs up the status ladder. 'I smoke, I snort, I've killed and robbed - I'm a man,' one prepubescent boy states defiantly.

The film culminates in all-out war between L'il Ze's bunch of hoodlums and an idealistic group of insubordinates who throng behind the handsome Knockout Ned after he stands up to Ze's cruel regime. Meirelles is careful not to lionise Ned. Turning him into a hero figure would, I suppose, have romanticised a bitter and essentially futile conflict. Rocket, caught in the middle of the hostility highlights the ultimate irony: 'By the end, after years of fighting, nobody could remember how it all started,' he says. The war becomes the way of life in the favela. Being affiliated to one of the gangs gives the street kids credibility and, more importantly, access to weapons. Before long, guns are being handed out like lollipops, and the runts are running about excitedly firing their new 'toys' indiscriminately. It is the ultimate in power without responsibility.

In their breathless exaltations, many reviewers have dubbed City of God 'Brazil's answer to Goodfellas'. It is a comparison that may be sound in terms of structure  Meirelles has certainly mastered Scorsese's canny editing and daring method of chronicling events over long periods of time  but overall this is a different beast. It is more of a Lord of the Flies with AK-47s. The most alarming aspect of all is the shocking lack of parental presence.

This is essential in conveying the choices these street children have (or rather don't have). L'il Ze and his barbaric ilk become all these poor, impressionable little tykes have to aspire to. In short: they don't stand a chance  a fact sharply illustrated in one particularly distressing and almost unwatchable initiation scene where a young gang recruit is required to murder a cornered infant in order to appease his older colleagues.

But Meireilles does not let this base, visceral tone swamp his movie. In Rocket he has an inspirational protagonist  the perfect foil to the madness and despair. His coming of age scenes where he bashfully attempts to flirt with girls and lose his virginity; and the sequence where he and his mate resort to petty crime only to bottle out when their intended victims turn out to be 'way too cool' to rob are the glue that holds the drama together. Without the light relief this would be intense and depressing fare.

As it is, City of God is a triumph of story-telling: Magnificent, gut-wrenching and utterly compelling, it is cinema of the very highest order.

Do not miss it.
-Mithun Marshal""")

# Save the result as JSON
with open("structured_output/review_result.json", "w") as f:
    json.dump(result, f, indent=2)

print(result['reviewer'])