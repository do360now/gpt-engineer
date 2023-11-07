from gpt_engineer.core.code import Code
from gpt_engineer.core.version_manager_interface import VersionManagerInterface
from gpt_engineer.core.step_bundle_interface import StepBundleInterface
from gpt_engineer.core.ai import AI
from gpt_engineer.core.default.lean_step_bundle import LeanStepBundle
from gpt_engineer.core.default.version_manager import VersionManager

class Agent:
    """
    The `Agent` class is responsible for managing the lifecycle of code generation and improvement.

    Attributes:
        path (str): The file path where the `Agent` will operate, used for version management and
                    file operations.
        version_manager (VersionManagerInterface): An object that adheres to the VersionManagerInterface,
                        responsible for version control of the generated code. Defaults to `VersionManager`
                        if not provided. PROBABLY GIT SHOULD BE USED IN THE DEFAULT
        step_bundle (StepBundleInterface): Workflows of code generation steps that define the behavior of gen_code and
        improve.
        ai (AI): Manages calls to the LLM.

    Methods:
        __init__(self, path: str, version_manager: VersionManagerInterface = None,
                 step_bundle: StepBundleInterface = None, ai: AI = None):
            Initializes a new instance of the Agent class with the provided path, version manager,
            step bundle, and AI. It falls back to default instances if specific components are not provided.

        init(self, prompt: str) -> Code:
            Generates a new piece of code using the AI and step bundle based on the provided prompt.
            It also snapshots the generated code using the version manager.

            Parameters:
                prompt (str): A string prompt that guides the code generation process.

            Returns:
                Code: An instance of the `Code` class containing the generated code.

        improve(self, prompt: str) -> Code:
            Improves an existing piece of code using the AI and step bundle based on the provided prompt.
            It also snapshots the improved code using the version manager.

            Parameters:
                prompt (str): A string prompt that guides the code improvement process.

            Returns:
                Code: An instance of the `Code` class containing the improved code.
    """

    def __init__(self, path: str, version_manager: VersionManagerInterface = None, step_bundle: StepBundleInterface = None, ai: AI = None):
        self.path = path
        self.version_manager = version_manager or VersionManager(self.path)
        self.step_bundle = step_bundle or LeanStepBundle(self.path)
        self.ai = ai or AI()

    def init(self, prompt: str) -> Code:
        code = self.step_bundle.gen_code(self.ai, prompt)
        version_hash = self.version_manager.snapshot(code)
        return code

    def improve(self, prompt: str) -> Code:
        code = self.step_bundle.improve_code(self.ai, prompt)
        version_hash = self.version_manager.snapshot(code)
        return code

