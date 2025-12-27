"""Input handling utilities."""


class InputHandler:
    """Static methods for user input."""

    @staticmethod
    def prompt(message: str) -> str:
        """Get user input with prompt.

        Args:
            message: Prompt to display.

        Returns:
            User input stripped of whitespace.
        """
        return input(message).strip()

    @staticmethod
    def menu_choice() -> str:
        """Get menu choice from user.

        Returns:
            Lowercase, stripped choice string.
        """
        return input("Enter choice: ").strip().lower()

    @staticmethod
    def confirm(message: str) -> bool:
        """Get yes/no confirmation.

        Args:
            message: Confirmation prompt.

        Returns:
            True only if user enters 'y' or 'Y'.
        """
        response = input(message).strip().lower()
        return response == "y"
