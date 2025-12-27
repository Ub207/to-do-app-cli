"""Input prompts and validation."""


class InputHandler:
    """Handles user input with prompts."""

    @staticmethod
    def prompt(message: str) -> str:
        """
        Prompt for input and return stripped result.

        Args:
            message: Prompt message

        Returns:
            Stripped user input
        """
        return input(message).strip()

    @staticmethod
    def confirm(message: str) -> bool:
        """
        Prompt for yes/no confirmation.

        Args:
            message: Confirmation message (should include "(y/N)")

        Returns:
            True if user entered 'y' or 'Y', False otherwise
        """
        response = input(message).strip().lower()
        return response == 'y'

    @staticmethod
    def menu_choice() -> str:
        """
        Prompt for menu choice.

        Returns:
            User's menu choice (lowercase, stripped)
        """
        return input("Enter choice: ").strip().lower()

    @staticmethod
    def wait_for_enter() -> None:
        """Wait for user to press Enter."""
        input("Press Enter to continue...")
