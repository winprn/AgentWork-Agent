## Overview

This project provides a supervisor graph for managing agents. It helps in visualizing and controlling the interactions and states of various agents in a system.

## Features

- Visual representation of agent interactions
- Real-time updates on agent states
- Easy integration with existing systems

## Installation

To install the project, clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/supervisor-graph-agents.git
cd AgentWork-Agent
pip install -r requirements.txt
```

## Usage

To start the supervisor graph, run the following command:

```bash
uvicorn agent_server:app
```

It will run on localhost.

If you want to run Demo1, make POST with body like this:

```
requests.post("http://127.0.0.1:8000/invoke",body={"id":"1", "request":"Your request"})
```

```
{
"id":"1",
"request":"Your request",
"id_thread":"Specific ID for that job"
}
```

If you want to run Demo2:

```
{
"id":"2",
"request":"Your request",
"id_thread":"Specific ID for that job"
}
```

For the request, You can find them in Agent_team_1, Agen_team_2
