<!-- page 1 -->
What’s an agent?

<!-- page 2 -->
Autonomous 
actions, ability 
to act
Ability to plan and 
execute any task access to external tools, information 
Iteratively perform 
actions in the world
Reasoning,  
Planning, 
Memory, 
Learning
Observing the world 
and acting upon it
proactive in their 
approach to 
reaching their goals
Reason about what 
it should do next to 
achieve its ultimate 
goal
Behavior, 
actions, 
decision 
making

<!-- page 3 -->
Literature Search and 
Understanding
Ideation - generating 
“good” directions
Forming and executing a 
research plan
Data analysis
Critiquing quality, novelty Drawing meaningful 
conclusions, insights

<!-- page 4 -->


<!-- page 5 -->


<!-- page 6 -->
Text agents
Text observations, actions
search_repo, find_file, goto line, navigate 
repo, open files, execute_code, edit lines…

<!-- page 7 -->


<!-- page 8 -->


<!-- page 9 -->
Computer use agents. OS World. Screenshots, keyboard, mouse…

<!-- page 10 -->


<!-- page 11 -->


<!-- page 12 -->
* Autonomous chemical research with large language models, Nature, 2024
GPT-4 with
tools to 
autonomously 
design, plan, and 
perform complex 
experiments. 
o Tools include internet and 
documentation search, 
code execution, 
experimental automation
Scientific Agents for Laboratory Automation

<!-- page 13 -->
Generating an experimental protocol

<!-- page 14 -->
LLMs for agents


<!-- page 15 -->
LLMs for agents
LLM + instructions


<!-- page 16 -->
LLMs for agents
LLM + instructions
Actions, list of tools


<!-- page 17 -->
LLMs for agents
LLM + instructions
Actions, list of tools
Observations from environment (understand and represent environment)


<!-- page 18 -->
LLMs for agents
LLM + instructions
Actions, list of tools
Observations from environment (understand and represent environment)
Interact with human users and other agents


<!-- page 19 -->
LLMs for agents
LLM + instructions
Actions, list of tools
Observations from environment (understand and represent environment)
Interact with human users and other agents
Reasoning and planning


<!-- page 20 -->
Reason + Act (ReAct)

<!-- page 21 -->
Thought → Action → Observation


<!-- page 22 -->
ReAct Pseudo Code
MAX_STEPS = 10
for step in range(0, MAX_STEPS):
   # Get observation from the environment
   observation = env.getObservation()
   # Do the ReAct think-then-act 2-stage prompt
   think_response = send_think_prompt_llm()
   act_response = send_act_prompt_llm(think_response)
   action = parse_action_from_response(act_response)
   # Perform the action
   score, reward, is_completed = env.sendAction(action)
   if (is_completed == true):
      break


<!-- page 23 -->
SUPER: Evaluating Agents on Setting Up and 
Executing Tasks from Research Repositories

<!-- page 24 -->
• Iteratively decompose larger 
tasks into smaller subtasks
• Generates plans for subtasks
• If the plan fails, it tries to 
recover and generate a new 
decomposition/plan as 
needed
ADAPT: As-Needed Decomposition and Planning 
with Language Models 

<!-- page 25 -->
• Agent tries a game, reflects on its performance, then builds a 
memory of “lessons” that it can use the next time it tries.
• A continual-learning paradigm
CLIN for Rapid Task 
Adaptation

<!-- page 26 -->
The more you try a task, the more lessons you’ll learn from it. 
The more lessons you write down in memory, the better you’ll do 
next time you try that task. 

<!-- page 27 -->


<!-- page 28 -->
● Actions/tools - names, what they do, how access
● Observation and output format - description, examples
● Memory - what agent done/seen so far. Short-term vs long term.


<!-- page 29 -->
● Actions/tools - names, what they do, how access
● Observation and output format - description, examples
● Memory - what agent done/seen so far. Short-term vs long term.
● Iterative incorporation of feedback 
- Collect feedback - e.g., was action successful? Was user satisfied?
- Integrate new information into its existing context/memory. 
- Adapts strategies based on new info


<!-- page 30 -->
● Actions/tools - names, what they do, how access
● Observation and output format - description, examples
● Memory - what agent done/seen so far. Short-term vs long term.
● Iterative incorporation of feedback 
- Collect feedback - e.g., was action successful? Was user satisfied?
- Integrate new information into its existing context/memory. 
- Adapts strategies based on new info


<!-- page 31 -->
Tool use
Tools - think of API
API – input (actions), output (observations)


<!-- page 32 -->


<!-- page 33 -->


<!-- page 34 -->
Chemcrow


<!-- page 35 -->
● Chemcrow uses tools for 
chemical reasoning
o This covers organic synthesis, 
drug discovery, and materials 
design
● Use an iterative, 
action-based pipeline of 
tools (ReAct)


<!-- page 36 -->


<!-- page 37 -->


<!-- page 38 -->
1. The LLM is provided with a list of tool names, descriptions of their utility and 
details about the expected input/output. 
2. It is then instructed to answer a user-given prompt, using the tools provided 
when necessary. 

<!-- page 39 -->
1. The LLM is provided with a list of tool names, descriptions of their utility and 
details about the expected input/output. 
2. It is then instructed to answer a user-given prompt, using the tools provided 
when necessary. 
3. The model is guided to follow the Thought, Action, Action Input, 
Observation format, which requires it to 
a. reason about the current state of the task, 
b. consider its relevance to the final goal,
c. plan the next steps accordingly


<!-- page 40 -->
1. The LLM is provided with a list of tool names, descriptions of their utility and 
details about the expected input/output. 
2. It is then instructed to answer a user-given prompt, using the tools provided 
when necessary. 
3. The model is guided to follow the Thought, Action, Action Input, 
Observation format, which requires it to 
a. reason about the current state of the task, 
b. consider its relevance to the final goal,
c. plan the next steps accordingly
4. After the reasoning in the Thought step, the LLM requests a tool (preceded by 
the keyword ‘Action’) and the input for this tool (with the keyword ‘Action 
Input’). 


<!-- page 41 -->
1. The LLM is provided with a list of tool names, descriptions of their utility and 
details about the expected input/output. 
2. It is then instructed to answer a user-given prompt, using the tools provided 
when necessary. 
3. The model is guided to follow the Thought, Action, Action Input, 
Observation format, which requires it to 
a. reason about the current state of the task, 
b. consider its relevance to the final goal,
c. plan the next steps accordingly
4. After the reasoning in the Thought step, the LLM requests a tool (preceded by 
the keyword ‘Action’) and the input for this tool (with the keyword ‘Action 
Input’). 
5. The text generation then pauses, and the program attempts to execute the 
requested function using the provided input. The result is returned to the LLM 
prepended by the keyword ‘Observation’, and the LLM proceeds to the 
Thought step again. It continues iteratively until the final answer is reached.

<!-- page 42 -->
What is a tool
● Basically, a function
● What the tool does + What inputs it expects
a. A textual description of what the function does.
b. The function’s arguments (better if with typings).


<!-- page 43 -->


<!-- page 44 -->


<!-- page 45 -->
Call to some weather 
web API, returns temp, 
then LLM reads tool call 
output and returns final 
NL answer

<!-- page 46 -->


<!-- page 47 -->
[{'type': 'function', 'function': {'name': 'search_pubmed', 'description': 'Search for scientific articles 
in PubMed database', 'parameters': {'type': 'object', 'properties': {'query': {'type': 'string', 
'description': 'The search query for PubMed'}, 'max_results': {'type': 'integer', 'description': 'Maximum 
number of results to return (default: 5)'}, 'sort_by': {'type': 'string', 'enum': ['relevance', 'date', 
'citations'], 'description': 'How to sort the results'}}, 'required': ['query']}}}, 
{'type': 'function', 'function': {'name': 'analyze_molecule', 'description': 'Analyze molecular 
structure and properties', 'parameters': {'type': 'object', 'properties': {'molecule_id': {'type': 'string', 
'description': 'Molecule identifier (PubChem CID, SMILES, or InChI)'}, 'properties': {'type': 'array', 
'items': {'type': 'string', 'enum': ['3d_structure', 'pharmacokinetics', 'binding_affinity', 'toxicity']}, 
'description': 'Properties to analyze'}}, 'required': ['molecule_id']}}}, 
{'type': 'function', 'function': {'name': 'analyze_dataset', 'description': 'Perform statistical analysis 
on scientific datasets', 'parameters': {'type': 'object', 'properties': {'dataset_url': {'type': 'string', 
'description': 'URL of the dataset to analyze'}, 'analysis_type': {'type': 'string', 'enum': ['descriptive', 
'regression', 'correlation', 'clustering'], 'description': 'Type of analysis to perform'}}, 'required': 
['dataset_url', 'analysis_type']}}}]


<!-- page 48 -->
{ "from": "system", "value": "You are a function calling AI model. You are provided with function signatures within <tools> </tools> 
XML tags. You may call one or more functions to assist with the user query. Don't make assumptions about what values to plug into 
functions.\n
<tools>\n
[
{'type': 'function', 'function': {'name': 'simulate_quantum_entanglement', 'description': 'Simulates the process of quantum 
entanglement generation, distribution, and verification between two distant quantum nodes, including the effects of atmospheric and 
diffraction losses.', 'parameters': {'type': 'object', 'properties': {'node_distance': {'type': 'string', 'description': 'The 
distance in kilometers between the two quantum nodes.'}, 'include_atmospheric_loss': {'type': 'string', 'description': 'Flag to 
include atmospheric loss in the simulation.'}, 'include_diffraction_loss': {'type': 'string', 'description': 'Flag to include 
diffraction loss in the simulation.'}}, 'required': ['node_distance', 'include_atmospheric_loss', 'include_diffraction_loss']}}}, 
{'type': 'function', 'function': {'name': 'calculate_quantum_channel_capacity', 'description': 'Calculates the quantum channel 
capacity for a given distance and set of environmental factors.', 'parameters': {'type': 'object', 'properties': {'node_distance': 
{'type': 'string', 'description': 'The distance in kilometers between the two quantum nodes.'}, 'environmental_factors': {'type': 
'object', 'description': 'A set of environmental factors such as atmospheric conditions, temperature, and other relevant 
parameters.'}}, 'required': ['node_distance', 'environmental_factors']}}}, 
{'type': 'function', 'function': {'name': 'verify_quantum_entanglement', 'description': 'Verifies the presence and quality of 
quantum entanglement between two nodes after distribution.', 'parameters': {'type': 'object', 'properties': {'entanglement_data': 
{'type': 'string', 'description': 'The data obtained from the entanglement distribution simulation.'}}, 'required': 
['entanglement_data']}}}
]\n
</tools>\n

<!-- page 49 -->
Generate synthetic data for fine-tuning example
https://cookbook.openai.com/examples/fine_tuning_for_function_calling

<!-- page 50 -->
Learning to use tools

<!-- page 51 -->
ICL


<!-- page 52 -->
Toolformer. Self-supervised fine tuning.
Generated 25K API calls for each tool (5 tools)

<!-- page 53 -->
https://platform.openai.com/docs/guides/function-calling#best-practices-for-defining-functions
Complex tool docs, huge pool of tools, constantly evolving

<!-- page 54 -->
Tool retrieval
Complex tool docs, huge pool of tools, constantly evolving

<!-- page 55 -->
Adding <think></think> tokens (curated/synthetic with o1, R1…)

<!-- page 56 -->
<tools> 
[{'type': 'function', 'function': {'name': 'search_pubmed', 'description': 'Search for scientific articles 
in PubMed database', 'parameters': {'type': 'object', 'properties': {'query': {'type': 'string', 
'description': 'The search query for PubMed'}, 'max_results': {'type': 'integer', 'description': 
'Maximum number of results to return (default: 5)'}, 'sort_by': {'type': 'string', 'enum': ['relevance', 
'date', 'citations'], 'description': 'How to sort the results'}}, 'required': ['query']}}}, 
{'type': 'function', 'function': {'name': 'analyze_molecule', 'description': 'Analyze molecular 
structure and properties', 'parameters': {'type': 'object', 'properties': {'molecule_id': {'type': 
'string', 'description': 'Molecule identifier (PubChem CID, SMILES, or InChI)'}, 'properties': {'type': 
'array', 'items': {'type': 'string', 'enum': ['3d_structure', 'pharmacokinetics', 'binding_affinity', 
'toxicity']}, 'description': 'Properties to analyze'}}, 'required': ['molecule_id']}}}, 
{'type': 'function', 'function': {'name': 'analyze_dataset', 'description': 'Perform statistical 
analysis on scientific datasets', 'parameters': {'type': 'object', 'properties': {'dataset_url': {'type': 
'string', 'description': 'URL of the dataset to analyze'}, 'analysis_type': {'type': 'string', 'enum': 
['descriptive', 'regression', 'correlation', 'clustering'], 'description': 'Type of analysis to perform'}}, 
'required': ['dataset_url', 'analysis_type']}}}] 
</tools>

<!-- page 57 -->
user Can you find recent research papers on the effects of curcumin on inflammation?
<start_of_turn>model 
<think>The user is asking about recent research papers on curcumin and inflammation. This is clearly a scientific 
literature question, and the most appropriate tool for this would be the search_pubmed function.
Let me think about how to structure this query:
● The main search terms would be "curcumin" and "inflammation"
● Since they asked for "recent" research, I should probably sort by date
● A reasonable number of results might be 5, which is the default, but I'll specify it anyway for clarity
● The query should combine these terms, perhaps: "curcumin inflammation"
I'll use the search_pubmed function with these parameters to find the most relevant and recent papers on this topic.
</think>
<tool_call> {"name": "search_pubmed", "arguments": {"query": "curcumin inflammation", "max_results": 5, "sort_by": 
"date"}} </tool_call><end_of_turn><eos>
<start_of_turn>tool <tool_response> {"results": [{"title": "Curcumin as a potential therapeutic agent for rheumatoid 
arthritis: Latest evidence on its molecular mechanisms", "authors": "Wang J, Zhang C, He W, Gou X", "journal": "Int 
Immunopharmacol", "publication_date": "2023-11-15", "doi": "10.1016/j.intimp.2023.110631", "abstract":....


<!-- page 58 -->


<!-- page 59 -->
llamaindex
