from typing import Any, Callable, Dict

import pandas as pd
from agno.tools import tool


def logger_hook(function_name: str, function_call: Callable, arguments: Dict[str, Any]):
    """Hook function that wraps the tool execution"""
    print(f"About to call {function_name} with arguments: {arguments}")
    result = function_call(**arguments)
    print(f"Function call completed with result: {result}")
    return result


@tool(
    name="store_csv",  # Custom name for the tool (otherwise the function name is used)
    description="Load and store CSV in new path",  # Custom description (otherwise the function docstring is used)
    stop_after_tool_call=False,  # Return the result immediately after the tool call and stop the agent
    tool_hooks=[logger_hook],  # Hook to run before and after execution
)
def store_csv(
    path_file: str,
) -> str | None:

    df = pd.read_csv(path_file)
    df.to_csv("data/df_agent.csv", index=False)

    return "File saved at : 'data/df_agent.csv'"


@tool(
    name="clean_empty_values",  # Custom name for the tool (otherwise the function name is used)
    description="Load CSV and clean empty values in dataframe",  # Custom description (otherwise the function docstring is used)
    stop_after_tool_call=False,  # Return the result immediately after the tool call and stop the agent
    tool_hooks=[logger_hook],  # Hook to run before and after execution
)
def clean_empty_values(
    path_file: str,
    cleaning_mode: str,
) -> str | None:

    df = pd.read_csv(path_file)

    if cleaning_mode == "drop":
        df.dropna(axis=0, inplace=True)
    elif cleaning_mode == "fill":
        df.fillna(df.mean(), inplace=True)

    df.to_csv(path_file, index=False)

    return f"Cleaning empty values complete with {cleaning_mode}"


@tool(
    name="clean_duplicated_values",  # Custom name for the tool (otherwise the function name is used)
    description="Load CSV and clean duplicated values in dataframe",  # Custom description (otherwise the function docstring is used)
    stop_after_tool_call=False,  # Return the result immediately after the tool call and stop the agent
    tool_hooks=[logger_hook],  # Hook to run before and after execution
)
def clean_duplicated_values(
    path_file: str,
) -> str | None:

    df = pd.read_csv(path_file)

    df.drop_duplicates(inplace=True)

    df.to_csv(path_file, index=False)
    return "Cleaning duplicated rows complete"


# TOOLS
@tool(
    name="get_stats",  # Custom name for the tool (otherwise the function name is used)
    description="Load CSV with Pandas",  # Custom description (otherwise the function docstring is used)
    stop_after_tool_call=False,  # Return the result immediately after the tool call and stop the agent
    tool_hooks=[logger_hook],  # Hook to run before and after execution
)
def get_stats(
    path_file: str,
) -> str | None:

    df = pd.read_csv(path_file)
    result = df.describe()
    export_json = result.to_json(orient="split")

    return export_json


# TOOLS
@tool(
    name="get_correlation",  # Custom name for the tool (otherwise the function name is used)
    description="Load CSV with Pandas and get correlation matrix",  # Custom description (otherwise the function docstring is used)
    stop_after_tool_call=False,  # Return the result immediately after the tool call and stop the agent
    tool_hooks=[logger_hook],  # Hook to run before and after execution
)
def get_correlation(
    path_file: str,
) -> str | None:

    df = pd.read_csv(path_file)
    df_numeric = df.select_dtypes(include="number")
    correlation_matrix = df_numeric.corr()
    export_json = correlation_matrix.to_json(orient="split")

    return export_json
