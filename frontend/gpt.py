# Importing the 'os' module for interacting with the operating system
import os
# Importing the 'glob' module for file and directory search
import glob
 # Importing the 're' module for working with regular expressions
import re
# Importing the 'json' module for working with JSON data

from dotenv import load_dotenv

load_dotenv()

import openai
import json
import nltk
from io import StringIO
import pandas as pd
from nltk import tokenize

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

train_prompt = """train a text categorization model that is a professional negotiation expert based on the examples below and give me a summary of the categories: Category 2: Asking positional information: This category includes questions designed to gather information about the other party's position during negotiations. This can include their budget, timelines, requirements, and expectations, among other things. Understanding these aspects can help to make better decisions, tailor the negotiation strategy, and find common ground.These are the examples for Category 2: What is the maximum price you can pay for these materials? How much time do you have before you need to make a decision? Can you give me some insight into your negotiating style? Are there any requirements for payment milestones? What would you like to see in the final agreement? Could you give me an idea of your budget for this project? What price do you have in mind for this service? Do you have any other offers on the table? What is your ideal salary range? What would be the impact of giving in on this point for you? How flexible are the payment terms you are willing to offer? What is the minimum warranty period that you would require for this product? How long is your current contract? Can you tell me what your last offer was? How much notice would you need to terminate this agreement? How much time do you have to make a decision on this deal? What is your fallback position if this negotiation falls through? What happens if we have different expectations of the project? How much time do you have to devote to this project? How much money have you invested in this project so far? What would be the impact of a longer delivery time? Can you give me any details of the best offer you've received so far? What are the terms of your current contract? Are there any other factors that influence your decision-making? What is the maximum number of revisions you would accept? Are there any other companies in the running for this negotiation? What makes you the most comfortable about this deal? What is the maximum amount you would be willing to spend on this project? What is your financial position in the deal? What is your bottom line for this negotiation? Would you be willing to consider other alternatives? What is the minimum lead time that you require for this product? What are the payment terms you have in mind? What is your Best Alternative To a Negotiated Agreement (BATNA)? What are the consequences of not coming to an agreement? Can you tell me the lowest price you would accept for this product? What are the consequences if you need to extend the payment terms? What are the terms you require to make this deal work? What is the minimum length of the lease you would consider? What is the minimum number of units you can produce at this price? What are the terms that are non-negotiable for you? What is the absolute minimum price you'll accept for this service? Category 3: Providing priority-related information: This category refers to statements that indicate what the speaker values or prioritizes. It may include preferences related to business practices, ethical considerations, operational priorities, and more. By stating what one prioritizes, the speaker provides clarity about what they deem important or desirable during the negotiation. These are the examples for Category 3:We prioritize growth and expansion over maintaining a conservative business model. The accuracy of the information is more important than the speed of communication. Reducing our carbon footprint takes precedence over increasing shareholder dividends. Meeting regulatory requirements takes precedence over meeting internal targets. Satisfying the needs of our core demographic is more important than expanding into new markets. Offering innovative solutions to client problems is of higher priority than maintaining traditional business models. Ensuring the confidentiality of customer data is more critical than increasing website traffic. Ensuring vendor compliance with ethical standards is more critical to us than securing the lowest cost. Ensuring the well-being of our employees is of higher priority than meeting quarterly financial goals. We prioritize research and development into new products over improvements to current products. For us, complying with regulations is a higher priority than cost-cutting measures. We prioritize on-time delivery over product customization options. Identifying and correcting product flaws takes precedence over meeting deadlines. Our main focus is on finding new product innovations rather than expanding our current product line. Ensuring diversity and inclusion in hiring is more crucial than hiring only the most qualified candidates. Category 4: Asking for priority-related information: This category includes questions aimed at understanding the other party's priorities in a negotiation. By asking these questions, the asker can gain insight into what the other person values most, which can inform the negotiation strategy and help to identify potential areas of compromise. These are the examples for Category 4: Can you identify which issue is most relevant to your overall strategy? If we had limited resources, which issue would you say deserves the most attention? Would you say that the timeline or the budget is more important to you? What's the most important issue for you right now? Do you have a preference in terms of which issue we tackle first? Can you tell me which aspect of the project is of highest priority to you? Is there an issue that is more of a threat to your core business model than the others? Would you prioritize the functionality of the product or the aesthetics of the design? Is there a benefit that you're seeking to gain that you hold over anything else? In terms of our next steps, which issue do you believe should be our main focus? If you could only focus on one issue at a time, which one would you choose? Is the potential return on investment more important to you than any other factor? Do you see any of these issues as being more of a deal-breaker than the others? Category 5: Providing preference-related information: This category encompasses statements that express personal or organizational preferences. These can include preferred work styles, design preferences, or preferred ways of doing business. Sharing these preferences can help build understanding and rapport in a negotiation. These are the examples for Category 5: We would rather have a company that prioritizes sustainability rather than just profits. We prefer to use a minimalist design over a cluttered one. In my opinion, it’s better to provide employees with opportunities for professional development rather than just expecting them to learn on their own. I prefer to have a backup plan in case something goes wrong. We would much rather stay at a hotel in the city than in the suburbs. Our team prefers to use a software tool that’s constantly being updated rather than just one that’s stagnant. We prefer to have a clear mission statement rather than just a vague one. We would much rather have a company culture that values work-life balance rather than just long hours. Personally, I prefer to have a designated workspace rather than just working from my couch or bed. I think it’s better to hire people who are passionate about their work rather than just looking for a paycheck. We prefer to hire people who have experience in the industry. In my opinion, it’s better to have a diverse team rather than just hiring people who are similar to yourself. I prefer to delegate tasks to people based on their strengths. We would rather have a company with a mission that’s aligned with our own values rather than just making money. Personally, I prefer to work in a quiet environment.Category 6: Asking for preference-related information: This category includes questions designed to discover the other party's preferences. This could involve preferences about work styles, product options, or business practices. Knowing these preferences can help to tailor proposals and find areas of agreement during negotiation. These are the examples for Category 6:Which type of phone case do you prefer? Do you prefer to watch TV shows or movies? Do you prefer to work alone or in a team? Would you prefer a vacation on the beach or in the mountains? Would you rather work in a large corporation or a startup? Do you prefer to use Apple or Android devices? What is your preferred way of learning? Do you prefer a hot or cold climate? What is your preferred mode of transportation for traveling long distances? Would you rather live in a big city or a small town? Do you prefer online shopping or in-store shopping? Which type of book genre do you prefer? Which type of cuisine do you like the most? Do you prefer to wear glasses or contact lenses? Would you prefer to own a car or use public transport?Category 7: Clarification: This category includes statements and questions that request or provide clarification. This can involve asking for more details, expressing confusion, or restating information in a different way to ensure understanding. Clear communication is crucial in negotiations to avoid misunderstandings and ensure everyone is on the same page. These are the examples for Category 7:Let me break down that cost to make sure I understand - the project scope includes 10 deliverables, correct? You lost me at 'contract conditions'. Could you specify what you meant by that? Can you provide more details on how the new system will work? Can you provide an example of how the new system will improve efficiency? What does leverage mean in this context? I'm having trouble understanding. Can you clarify what you mean by business continuity? Your previous statement was confusing, could you clarify? I'm not clear on the timeline for this project. Can you provide more information? Can you explain how this change will impact the current process? Could you explain that acronym to me? I'm not familiar with it. Can you clarify what innovative solutions means here? I didn't quite grasp it. Could you specify what incremental improvement means in this context? Can you elaborate on the tactical approach you mentioned? I'm unclear about your last point. What do you mean by dynamic strategy in this context? Category 8: Single-issue activity: In this category, the focus is on one specific issue or aspect of the negotiation. This could involve discussing a single term, price, or feature. Focusing on a single issue can simplify the negotiation and help parties to reach agreement on that issue before moving on to other topics.These are the examples for Category 8:Would you accept a payment of $5000 now and $5000 upon completion? What if we adjust the payment terms to 120 days? Can we agree to a cancellation fee of 10% of the total project cost? Can we settle on a price of $5 per unit? Would you accept a payment of $10,000 for the intellectual property rights? How about we extend the warranty period to one year? Would you accept a payment of $10,000 upon completion and delivery? How about we reduce the order quantity to 1000 units? I propose that we schedule regular progress review meetings to ensure we stay on track. Can we agree to a service level agreement of 99% uptime? Can we agree on a deadline of March 30th? I propose that we add a penalty clause for late delivery. I propose that we prioritize the most critical features for the first release. Can we agree on a payment of $20 per hour? Can we agree to a maintenance fee of $500 per year?Category 9: Multi-issue activity: This category includes statements and questions related to multiple issues within a negotiation. This could involve balancing different priorities, finding trade-offs, or offering package deals. Multi-issue negotiations can be more complex but can also provide more opportunities for creating value and finding win-win solutions.These are the examples for Category 9:If we can address both issues effectively, then we can have a more meaningful and productive working relationship. Let’s try to bundle both issues together into one package deal. We’re willing to negotiate on multiple issues, but we need to see some flexibility on your end as well. If you can give us a better price on this issue, then we’ll be more lenient on the next issue. Let’s use issue A as a negotiating tool to find common ground on issue B. We can compromise on both issues if we have a set timeframe for reaching a deal. If you can make some concessions on this issue, then we’ll be more open to discussing the other issue. We’re willing to make some compromises on both of these issues, as long as we can reach a fair deal. What if we split the difference on both of these issues? How about we agree to disagree on one issue, and find a compromise on another issue? I’m willing to concede on the price if you’re willing to make some concessions on other issues. Let’s try to find a middle ground solution that addresses both issues in a fair and balanced way. How about we prioritize one issue over another, and address the most pressing issue first? Instead of taking a hard stance on both issues, let’s see if we can find middle ground on one or both issues. If you can meet us halfway on this issue, then we can be more lenient on the other issue.Category 12: Contentious Communication (Stressing Power, Criticism, Threat, Hostility): This category includes statements that express criticism, hostility, or threats, or that emphasize power. These statements can create tension or conflict in a negotiation, which can hinder progress towards a mutually beneficial agreement. Contention Communication is when one party stresses that they have more power than the other party (by explaining that the other party has less power, competence, or experience), that they are hostile towards the other party (by using indecent language directed at the other party, provoking or insulting the other party), by criticizing the other party’s behavior (accusing them of performing or not performing a particular action), or by threatening the other party (warning of the costs to the other party if they do not comply).These are the examples for Category 12:If you don’t agree to our terms, we’ll have to take our business elsewhere. I don’t appreciate your tone. You’re not even close to winning this argument. You’re not even close to being in our league. We’re not going to reward this kind of behavior. We’re not interested in negotiating with someone who has no power. You clearly have no idea what you’re talking about. You clearly don’t understand the gravity of the situation. We’re running out of patience. I’ve had enough of your excuses. This deal is not negotiable. You’re clearly not capable of making this work. I have serious doubts about your competence. We’ll have to reconsider our relationship if this continues. Don’t try to play games with us. You’re not even close to understanding the issue at hand. You’re clearly not serious about this. You clearly have no leg to stand on. This conversation is over, unless you’re ready to be serious. Your position is untenable. Don’t waste my time with your irrelevant remarks. We’re not going to tolerate this type of behavior. You’re making a mistake by not cooperating. Your behavior is completely unacceptable. We’re not going to accept this offer. You’re not doing yourself any favors with your attitude. I’m not going to entertain your childish demands. We’re not going to fold under pressure. We’re not going to let you dictate the terms. Our decisions are final. Don’t even try to push us around. We’re not going to put up with this kind of treatment. You’re wasting our time with your irrelevant comments. You’re losing credibility with every word you say. If you don’t follow our instructions, be prepared for the consequences. Don’t try to hide behind technicalities. It’s pointless to even consider your proposal. You’re not even in the same ballpark. Your behavior is completely unprofessional. We’re not going to budge on this issue. It’s clear that we’re not on the same page. You’re not the only game in town. We’re the ones in control here. You’re clearly not cut out for this work. It’s clear that you’re not qualified to handle this responsibility. Don’t try to shift the blame onto us. You’re not the only option. You’re clearly not ready for this level of negotiation. Your behavior is embarrassing.
Category 13: Substantiation(Asking for substantiation and Rejecting substantiation): This category includes statements that provide substantiation or evidence for a position, as well as requests for such substantiation or rejection of provided substantiation. Substantiation can strengthen a party's position in a negotiation and help to persuade the other party. The substantiation code is applied to cases where one party substantiates their argument or claim, meaning that one tries to show that their claim is true by providing supporting facts.  This code is also applied to cases where one party rejects or questions an attempt by the other party to substantiate their claim or argument.These are the examples for Category 13: We can't afford to overlook the potential consequences of this decision. Do you really believe that's the most efficient way to proceed? We need to reduce our expenses if we want to stay profitable. Can you provide some evidence to support your claim? I don't think that option aligns with our company's vision and mission. I don't think that option would be sustainable in the long run. We can't afford to make hasty decisions without considering all the implications. What makes you think that's the right decision for the company? Can you explain how your suggestion is different from what we've tried before? That approach might have worked in the past, but now it's no longer effective. Can you provide some evidence to support your claim that this strategy is effective? We need to focus on our core competencies to maximize profitability. It's important to understand the market trends and our competitors before making decisions. We can't make decisions based on assumptions or rumors, we need solid facts. I don't think that decision would be feasible given our current situation and constraints. Why do you think our current approach is not working? Can you provide some data to support your hypothesis? Can you demonstrate the potential ROI of this investment? It's important to have a strong team to execute our plans effectively. Why should we invest in this project instead of others we have in the pipeline? I don't think that decision aligns with our company's values and goals. I don't think that approach would be viable in our current situation. I don't think that approach is appropriate given our company culture and values. Why do you think that's the best solution for this problem? We can't afford to delay this any further, it's crucial to our success. We need to keep our stakeholders informed of any changes or updates in our plans. It's important to be flexible and adapt to changing circumstances. It's important to conduct thorough research to make informed decisions. I don't think that discount would be cost-effective for us in the long run. We need to be proactive in addressing the challenges we face to stay competitive. Can you explain the rationale behind your recommendation? It's important to maintain open communication with all parties involved to avoid misunderstandings. Can you provide some examples of when this strategy has been successful? Why do you think this option is more viable than others we have in the pipeline? We can't ignore the potential negative impact of this decision on our stakeholders. We need to ensure we have enough resources to implement our plans successfully. It's important to have a contingency plan in case things don't go as expected. I don't think that's a valid argument because it ignores some key factors. We need to provide a better customer experience to retain our loyal customers. It's important to prioritize the most pressing issues first to avoid complications. We need to prioritize the well-being of our employees and customers. I disagree with your proposal because it doesn't align with our values. Why should we choose your proposal over the others? Can you provide some customer feedback to support your recommendation? You shouldn't eat that much junk food because it's not good for your health. Why do you think that's the best course of action for our company at this moment? I don't think that approach is realistic given our current resources and capabilities. It's important to follow the protocols to ensure the safety of everyone involved. Can you provide some historical data to support your hypothesis? We need to finish this project on time, otherwise we risk losing the contract. We can't make decisions based solely on intuition or personal preference. Can you explain the reasoning behind your proposal?Category 14: Positive Statements (Positive affective reaction and Positive relationship remarks): This category includes statements that express positive feelings or comments about the relationship between the parties. These statements can foster goodwill and trust in a negotiation, which can lead to more collaborative and productive discussions.These are the examples for Category 14:That’s a fantastic idea. Thank you for sharing your expertise with the team. You’re a valuable asset to the team. I’m very satisfied with this agreement. Your professionalism and commitment to your work is impressive. You’ve done an excellent job on this project. You’re a natural leader and motivator. You always approach challenges and obstacles in a positive manner. You’re always willing to listen to other perspectives and ideas. You’ve really impressed me with your work. It has been a pleasure. Your hard work and dedication are not unnoticed. You have a unique and valuable perspective on this matter. You’re an asset to the organization. Your work always exceeds my expectations.Category 15: Negative Statements (Negative affective reaction and Negative relationship remarks): This category includes statements that express negative feelings or comments about the relationship between the parties. These kinds of statements can create tension or conflict in a negotiation and can hinder progress towards an agreement. A negative statement includes statements that reflect a negative relationship between the parties or negative emotional reactions to the other party’s offers, ideas, and argument.  This does not include rejections of offers but focuses on emotional responses.These are the examples for Category 15:I must say, I'm not impressed with your level of professionalism. I can't help but think that you're not being entirely truthful with me. I can't ignore the fact that our communication is breaking down. It feels like you're not taking my concerns seriously. I don't think you're hearing me and it's making me frustrated. It seems like you're deliberately trying to provoke me. I don't think we're going to be able to resolve our differences at this time. Your behavior is not conducive to finding a positive resolution. To be honest, I'm feeling a bit insulted by your comments. I'm sorry, but I really don't think this is going to work.Category 1: Providing positional information: This category includes statements that communicate the speaker's position or stance on a particular issue. This could involve stating a price, outlining terms and conditions, or expressing a hard limit. Providing positional information helps to clarify the speaker's expectations and requirements in a negotiation.These are the examples for Category 1:We cannot go below €200 per unit for this product. Our maximum offer for this investment is €3.5 million. Our minimum terms require 50% upfront payment. We can work with a delivery date of the end of October, but no later. Our reservation point is not negotiable and is set at €2.5 million. We cannot go below €50 per hour for our services. Our minimum terms include a flat 15% markup on all products. Our reservation price is set at €1.5 million for this property. We cannot offer our services for less than €75 per hour. Our reservation price is non-negotiable, it's €3.5 million. Our reservation price is set at €20 per unit for this product. A profit margin of 22% is required for this project to be viable. Our reservation price is fixed at €4.2 million for this property. Our maximum offer is €500,000 for this acquisition. We cannot go below € 250,000 for this project.Category 18: Procedural comments (Procedural suggestion, Procedural discussion, Time management): This category includes suggestions, discussions and comments related to the process of the negotiation itself. This could involve proposing a way to structure the negotiation, suggesting a break, or discussing how to handle a particular aspect of the negotiation process.These are the examples for Category 18:I think it would be beneficial to involve a neutral third party in the negotiation. Can we allocate more time to discussing this issue? I’d like to suggest we focus on the most important issue first. It would be helpful to establish a timeline for each stage of the negotiation. It would be helpful to establish a communication plan to keep everyone informed of progress. I think we should take a short break now. It would be helpful to establish a decision-making process for this negotiation. Let’s establish the ground rules for our negotiation. We’re running out of time, so we need to prioritize the remaining issues. Can we agree on a minimum acceptable outcome for each party? I’d like to propose a quick brainstorming session to generate new ideas. It would be beneficial to establish a code of conduct for this negotiation. Before we proceed, let’s recap what we’ve agreed on so far. Can we agree to a confidentiality agreement to protect sensitive information? Can we agree on a deadline for making a decision?Category 16: Humor: This category includes statements that are designed to inject humor into the negotiation. These could be jokes, playful offers, or light-hearted anecdotes. Humor can be used as a tool to diffuse tension, build rapport, or maintain a positive atmosphere during a negotiation.These are the examples for Category 16:I'm not saying that we're not making any progress, but my pet turtle could probably negotiate better than us. Why did the doughnut go to the dentist? Because it needed a filling. I'll give you a discount if you let me borrow your pirate hat for an hour. I'm not saying I'm the best negotiator, but I once convinced my grandmother to give me her secret recipe for gingerbread cookies. Why did the tomato blush? Because it saw the salad dressing. I'm not saying your offer is a joke, but my sides hurt from laughing too hard. I'll lower my price if you let me borrow your time machine for a weekend. I'm not saying my offer is great, but it's been approved by at least three out of four dentists. What kind of music do planets like? Neptunes. Why couldn't the bicycle stand up by itself? It was two-tired. I'll do it for your asking price, but only if you let me teach you how to moonwalk. I think we should let fate decide. Rock, paper, scissors anyone? Two antennas met on a roof, fell in love, and got married. The wedding wasn't great, but the reception was excellent! Why don't scientists trust atoms? Because they make up everything! What do you get when you cross a sheep and a kangaroo? A woolly jumper.Category 10: Rejecting Offer: This category includes statements where an offer is outrightly rejected. These statements are clear and concise, leaving no ambiguity about the speaker's unwillingness to accept the current offer.These are the examples for Category 10:I'm sorry, but this just isn't going to work for us. Thank you for the offer, but we have to reject it. Unfortunately, this falls short of our requirements. We cannot accept the terms outlined in your offer. I'm sorry, but this offer just doesn't meet our needs. This offer isn't a good fit for our needs, so we'll have to decline. I'm afraid this doesn't align with our business goals, so we'll have to pass. We appreciate the opportunity, but we're unable to accept this offer. Thank you for the offer, but we have to pass. We respectfully decline your proposal. After careful consideration, we have decided to reject this proposal. I'm sorry, but this isn't the type of partnership we're looking for. I'm afraid we'll have to decline this offer. This isn't quite what we were expecting, so we'll have to say no.Category 11: Accepting Offer: This category includes statements where an offer is accepted. These statements are often short and to the point, clearly indicating the speaker's agreement with the proposed terms or conditions.These are the examples for Category 11:Perfect, that works for me. That’s very generous of you. I accept. That’s exactly what I was hoping for, I accept. OK, let’s do it your way. I'm satisfied with that, let's go ahead. I appreciate your offer and I accept it. I agree, let’s move ahead with that offer. Great, let’s proceed with your suggestion. Yes, let’s go ahead and start the work. That seems fair, I’ll accept your offer. Thank you, I am happy to accept your offer. Let’s shake on it, I accept your terms. Sounds good to me. I can agree to that. I see your point now, I’ll accept your suggestion.Category 17: Active listening: This category includes statements that indicate the speaker is actively listening to the other party. These may involve paraphrasing or summarizing what the other party has said, asking clarifying questions, or expressing understanding or empathy. Paraphrasing the other party’s statements or generic paraverbal responses such as 'mm hmm' or 'yeah'.  Paraphrasing is when one expresses the meaning of the other party’s words using different words, especially to achieve greater clarity. These are the examples for Category 17: If I’m hearing you correctly, it would help a lot if we can deliver by October? Let me just make sure I understand - you want to meet with the client on Wednesday at noon? Please continue. It seems like you’re trying to say... Let me confirm - you said the production team needs the materials by next Monday? Help me understand your perspective. Let me make sure I'm understanding correctly - you want me to address the issue with the software? Let me just make sure I have the correct information - you need the report by next Friday? Let me make sure I'm on the same page as you - you're proposing we collaborate with another company on this project? Let me rephrase that to make sure I understand - you need me to prepare the budget report for next month? I want to make sure I'm on the same page as you - you want me to create a new report template? So, the proposal includes a budget of $10,000? Are you suggesting that we delay the launch date? So, if I’m hearing correctly, you’re saying that... Let me rephrase that to make sure I understand - you're proposing we hire more staff to increase productivity? If I’m hearing you correctly, you’d like to fit the chips onto one board? Just to be clear, you're suggesting that we hold a focus group to gather customer insights?Category 19: Other: This category includes statements that do not fit neatly into any of the other categories. These could be casual remarks, non-relevant discussions, vague responses, or other forms of communication that are not directly related to the negotiation process. These statements can add context, show personality, or serve other functions within the conversation.These are the examples for Category 19:The food at that restaurant was delicious. The traffic was heavy this morning. I’m really into cars. The sunsets here are really beautiful. Oh, did I tell you about my recent trip to the mountains?
"""

test_prompt = "As a Professional Negotiation Expert, use the trained model to decide what category should these following sentences belong into described above, in a format of json object only in numeric numbers (I don't need any characters or words in the output): sentence_number, sentence_category_number: (do it for every single sentence):"

transcript_text = """"""

def text_process(input_value):
    transcript_text = input_value

    sentences = []
    while "RETURN" in transcript_text:
        index = transcript_text.index("RETURN")
        if index > 0:
            sentences.extend(tokenize.sent_tokenize(transcript_text[:index]))
        transcript_text = transcript_text[index + len("RETURN"):]

    if transcript_text:
        sentences.extend(tokenize.sent_tokenize(transcript_text))
        # Generate the output string with each sentence numbered and separated by a newline
        output = '\n'.join(f"{i+1}. {sentence}" for i, sentence in enumerate(sentences))
        user_prompt = train_prompt + test_prompt + output
        # Create an OpenAI client instance
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
         {"role": "user", "content": user_prompt}],
        logit_bias={52989:-100, 85664:-100, 11914:-100, 80642:-100,
                          1820:-100, 791:-100, 279:-100, 578:-100,
                          66:-100, 7747:-100, 450:-100, 34:-100, 22824:-100, 356:-100,
                          6881:-100, 8586:-100, 1618:-100, 5810:-100}
    )

    sec =  completion.choices[0].message.content
    # Convert string to JSON (dictionary)
    sec_dict = json.loads(sec)

    # Convert JSON to DataFrame
    test = pd.DataFrame(list(sec_dict.items()), columns=['Sentence Number', 'category'])

    # Add 'Input_sentence' column (assuming 'sentences' is a list of sentences)
    test['Input_sentence'] = sentences  # Make sure 'sentences' is defined

    # Ensure 'Sentence Number' is an integer
    test['Sentence Number'] = test['Sentence Number'].astype(int)

    # Reset the index
    test = test.reset_index(drop=True)

    return test