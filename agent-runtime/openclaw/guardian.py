class Guardian:
    def validate_input(self, agent: str, message: str):
        # Simple placeholder safety check
        if "kill" in message.lower():
            return False, "Unsafe content detected."
        return True, None

    def validate_output(self, agent: str, output: str):
        # Placeholder output safety
        return True, None

guardian = Guardian()
