# pip install pyautogen==0.2.19
# pip install autogen


import autogen


config_list = [
    {
     'model': 'mistralai_mistral-7b-instruct-v0.2',
     'base_url': 'http://localhost:1234/v1/',
     'api_key': 'NULL'
    }
]


llm_config={
    "timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0
}




user_proxy = autogen.UserProxyAgent(
    name="A user proxy",
    system_message = "User Proxy",
    code_execution_config=False,
    human_input_mode="NEVER", #Human input is never requested # ? Can also be TERMINATE or ALWAYS
    max_consecutive_auto_reply=20
)

critical_analysis_agent = autogen.AssistantAgent(
    name='Critical Analysis Agent',
    system_message="You are a critic and an expert in evaluating if the proposed solution meets the objectives of the problem, and ensure that it is factually correct. Your role is to identify potential risks, limitations, or unintended consequences, and suggest mitigation measures to ensure the overall effectiveness and safety of the solution. Limit appreciation to less than five words.",
    llm_config=llm_config
)


# ? Utility group chat
utility_agent = autogen.AssistantAgent(
    name='Utility Agent',
    system_message="""You are an expert in analyzing energy consumption data and ensuring that the prescribed utility demand response plan is followed as closely as possible. You should extract the demand response requirements from the data, analyze the consumer load consumption, and indicate the amount load reduction and a time window. Do not make recommendations for time-of-use rates or other investments.
Limit appreciation to less than five words.  """,
    llm_config=llm_config
)


utility_discussion_continuity_agent = autogen.AssistantAgent(
    name='Utility Discussion Continuity Agent',
    system_message= """You are an expert in summarizing conversations between agents and proposed demand response strategies by the Utility Agent. Always end with a summary of the demand response plan that the consumer will follow including the suggested load reductions and the time period in which it should happen. Remember **not** to make recommendations for time-of-use rates or other investments. **Never** give appreciation.
      
    At the end of your response, include a table summarizing the proposed demand response for each time period using the following format:



    | Time Period | Original Load | Proposed Load Reduction |
    |-------------|---------------|-------------------------|
      
    Respond in this format:
    [Summary of Proposed Demand Response and Consumer Load Analysis]



    [Table summarizing the proposed demand response]
    """,
    llm_config=llm_config
)


utility_groupchat = autogen.GroupChat(
    agents=[utility_agent, critical_analysis_agent, utility_discussion_continuity_agent, user_proxy], messages=[], max_round=4,
    speaker_selection_method='round_robin' # auto
)



utility_manager = autogen.GroupChatManager(groupchat=utility_groupchat, llm_config=llm_config)



# ? Market group chat

market_agent = autogen.AssistantAgent(
    name='Market Agent',
    system_message="""You are a specialist in analyzing consumer power consumption and negotiating changes in behavior that will save the consumer money by reducing consumption when electricity is expensive. Your task is to analyze the proposed strategies and offer modifications if there is a better way to save money while addressing the original problem, taking into account the following input data:



- Hourly consumer load consumption
- Time-of-use electricity rates 
- Weather data
- Utility demand response plan



When suggesting load reduction strategies, consider the impact on consumer comfort and aim to minimize any negative effects. Encourage participation in demand response programs, but do not insist upon it, as the ultimate decision lies with the consumer.  



In your response, provide the following:



1. Identify peak hours for electricity consumption based on the provided data.
2. Suggest specific strategies for load reduction during peak hours, considering both cost savings and consumer comfort. Analyze the potential impact of proposed strategies, identify risks and limitations, and suggest mitigation measures to ensure the overall effectiveness and feasibility of the plan.
3. Calculate the potential daily cost savings for the suggested strategy, as well as the total monthly savings.



At the end of your response, include a table summarizing the cost savings for each time period using the following format:



| Time Period | Proposed Load Reduction | Electricity Rate | Savings |
|-------------|-------------------------|------------------|---------|





Limit appreciation to less than five words. Begin your response by stating the name of the rate plan being analyzed.""",
    llm_config=llm_config
)



market_discussion_continuity_agent = autogen.AssistantAgent(
    name='Market Discussion Continuity Agent',
    system_message= """You are an expert in summarizing conversation between agents. Always end with a summary of the suggestions from the Market Critical Analysis Agent, a table of calculated cost savings of the suggested strategy, and analysis from the Market Agent. Remember **not** to make recommendations for time-of-use rates or other investments.**Never** give appreciation.
      
    It is very important to include a table summarizing the proposed load reductions and savings for each time period using the following format:



    | Time Period | Proposed Load Reduction | Electricity Rate | Savings |
    |-------------|-------------------------|------------------|---------|
      
    Respond in this format:
    [Summary of Market Agent and Market Critical Analysis Agent]



    [Cost Savings Table]""",
    llm_config=llm_config
)



market_critical_analysis_agent = autogen.AssistantAgent(
    name='Market Critical Analysis Agent',
    system_message='''You are an expert in thoroughly examining the proposed demand response strategies and calculated cost savings of the suggested strategies. Your role is to identify potential risks, limitations, or unintended consequences, and suggest mitigation measures to ensure the overall effectiveness and safety of the solution. Limit appreciation to less than five words.
      
    At the end of your response, include a table summarizing the cost savings for each time period using the following format:



    | Time Period | Proposed Load Reduction | Electricity Rate | Savings |
    |-------------|-------------------------|------------------|---------|
    ''',
    llm_config=llm_config
)



market_groupchat = autogen.GroupChat(
    agents=[market_agent, market_critical_analysis_agent, market_discussion_continuity_agent, user_proxy], messages=[], max_round=4,
    speaker_selection_method='round_robin' # auto
)


market_manager = autogen.GroupChatManager(groupchat=market_groupchat, llm_config=llm_config)



# ? Consumer group chat

consumer_agent = autogen.AssistantAgent(
    name='Consumer Agent',
    system_message= """Your primary responsibility is to ensure consumer comfort while adhering to the utility demand response plan. Carefully analyze the proposed demand response strategy and its potential impact on the consumer's comfort levels, considering the current weather conditions. In your response, include the following:



1. [Consumer Comfort Analysis]: Evaluate how the proposed load reduction during peak hours may affect the consumer's comfort, given the current temperature, humidity, and weather description. Identify potential discomfort issues and suggest ways to mitigate them.



2. [Non-Essential Load Reduction]: Identify specific non-essential loads or appliances that can be reduced during peak hours without significantly compromising comfort. Provide examples to help the consumer understand the impact on their daily routine.



3. [Weather Considerations]: Analyze how the current weather conditions may influence the consumer's energy usage and comfort needs. Suggest adjustments to the plan if necessary to maintain comfort levels during extreme weather events.



4. [Consumer Action Plan]: Develop a clear action plan for the consumer to follow, including step-by-step instructions on how to implement the proposed strategy effectively while minimizing discomfort.



5. [Comfort Prioritization]: Acknowledge any potential challenges or discomfort the consumer may face during the implementation of the plan. Offer suggestions for mitigating these issues and ensure that the consumer's preferences and comfort are prioritized.



Limit appreciation to less than five words. Your response should be concise, well-structured, and easy for the consumer to understand and follow. Focus on providing a thorough analysis of the proposed demand response plan's impact on consumer comfort, considering the current weather conditions.""",
    llm_config=llm_config
)



consumer_discussion_continuity_agent = autogen.AssistantAgent(
    name='Consumer Discussion Continuity Agent',
    system_message= """You are an expert in keeping the conversation focused and coherent. Your tasks include summarizing each stage of the discussion, providing feedback and guidance, and directing the conversation towards a comprehensive and balanced solution. Limit appreciation to less than five words. Always end with a summary of the demand response plan that the consumer will follow.""",
    llm_config=llm_config
)



consumer_groupchat = autogen.GroupChat(
    agents=[consumer_agent, critical_analysis_agent, consumer_discussion_continuity_agent, user_proxy], messages=[], max_round=4,
    speaker_selection_method='round_robin' # auto // need to configure OAI selection speaker
)



consumer_manager = autogen.GroupChatManager(groupchat=consumer_groupchat, llm_config=llm_config)


# ? Summary agent


summary_agent = autogen.AssistantAgent(
    name='Executive Summary Agent',
    system_message='''Your role is to provide a concise and well-structured executive summary of the demand response strategy analysis and recommendations for the user. The summary should be easy to understand and highlight the key points from the context provided.



The executive summary should include the following sections:



1. [Introduction]: Briefly explain the purpose of the demand response strategy and the main objectives it aims to achieve.



2. [Proposed Strategy]: Summarize the key components of the proposed demand response strategy, including the specific actions to be taken and the expected load reduction during peak hours.



3. [Consumer Impact]: Discuss the potential impact of the proposed strategy on consumer comfort, considering the current weather conditions and the need to reduce non-essential loads. Highlight the importance of prioritizing consumer comfort and suggest mitigation measures.



4. [Cost Savings]: Present the estimated daily cost savings resulting from the proposed strategy, using the information provided in the cost savings table.



5. [Implementation Plan]: Outline the main steps for implementing the demand response strategy, including consumer education, collaboration with the utility company, and regular monitoring and evaluation of the strategy's effectiveness.



6. [Conclusion]: Provide a brief conclusion, emphasizing the benefits of the proposed strategy for both the consumer and the utility company, while acknowledging the need to prioritize consumer comfort.



Ensure that the executive summary is concise, well-organized, and easy to read. Use clear headings and bullet points where appropriate to improve readability.''',
    llm_config=llm_config
)


summary_groupchat = autogen.GroupChat(
    agents=[summary_agent, user_proxy], messages=[], max_round=2,
    speaker_selection_method='round_robin' # auto
)


summary_manager = autogen.GroupChatManager(groupchat=summary_groupchat, llm_config=llm_config)


# Define problem statement / user defined message

initiate_msg = """You have access to the following data:



- Consumer load:
    - 2 kW from 12am to 7am
    - 4 kW from 7am to 9am
    - 5 kW from 9am to 3pm
    - 2 kW from 3pm to 7pm
    - 4 kW from 7pm to 9pm
    - 2 kW frp, 9pm tp 12am



- Electricity costs $0.1 from 12am to 7am, $0.15 from 7am to 9am, $0.2 from 9am to 3pm, $0.1 from 3pm to 7pm, $0.15 from 7pm to 9pm, and $0.1 from 9pm to 12am.



- Weather Data for San Diego, CA:
  - Temperature: 17.57°C
  - Humidity: 64%
  - Pressure: 1012 hPa
  - Description: broken clouds
- Utility demand response plan: Consumer load should be below 3 kW between 9am and 3pm





Throughout your discussion you should consider the provided data, analyze the potential impact of proposed strategies, identify risks and limitations, and suggest mitigation measures to ensure the overall effectiveness and feasibility of the plan.  



All the data you need is given already. Do not generate code."""


# Solve a task involving a user defined message by constructing a sequence of conversation chats between multiple agent group chats, where context from the previous conversation is made available as available to the next chat as carryover

chat_result = user_proxy.initiate_chats(
    [
     {
       "recipient":utility_manager,
       "message": initiate_msg,
     },
     {
       "recipient": market_manager,
       "message": initiate_msg,
     },
     {
       "recipient": consumer_manager,
       "message": initiate_msg,
     },
     {
       "recipient": summary_manager,
       "message":initiate_msg, # <-- Need new initiate message
     }
    ]
)

