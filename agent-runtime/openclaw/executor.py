from openclaw.tool_registry import call_tool

class Executor:
    def run_step(self, agent: str, instruction: str):
        # Tool call detection
        if instruction.startswith("tool:"):
            name, args = self.parse_tool_call(instruction)
            return call_tool(name, **args)

        # Default LLM simulation
        if "analyze" in instruction.lower():
            return "Analysis complete"

        if "draft" in instruction.lower():
            return "Draft written successfully"

        if "critique" in instruction.lower():
            return "Critique complete"

        if "finalize" in instruction.lower():
            return "Final result complete"

        return "Step complete"

    def parse_tool_call(self, instruction: str):
        # Example: tool:web_fetch(url="https://example.com")
        inside = instruction[len("tool:"):]
        name, arg_str = inside.split("(", 1)
        arg_str = arg_str.rstrip(")")
        args = eval(f"dict({arg_str})")
        return name, args

executor = Executor()
