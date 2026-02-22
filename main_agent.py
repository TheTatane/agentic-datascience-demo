from agent.agent import agent_ollama

if __name__ == "__main__":
    agent_ollama.print_response(
        """ Show me the statistics and correlation matrix of this CSV file: "data/example_hums_data.csv".
        Don’t forget to clean the file by removing empty values and duplicates.""",
        stream=True,
    )
