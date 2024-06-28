import typing as t

from pydantic import Field

from composio.local_tools.local_workspace.commons.get_logger import get_logger
from composio.local_tools.local_workspace.commons.history_processor import (
    history_recorder,
)
from composio.workspace.base_workspace import BaseCmdResponse
from composio.local_tools.local_workspace.commons.utils import process_output

from .base_class import BaseAction, BaseRequest, BaseResponse


LONG_TIMEOUT = 200
logger = get_logger("workspace")


class GetPatchRequest(BaseRequest):
    new_file_path: t.List[str] = Field(
        default=[],
        description="Paths of the files newly created to be included in the patch.",
    )


class GetPatchResponse(BaseResponse):
    pass


class GetPatchCmd(BaseAction):
    """
    Get the patch from the current working directory. The patch is present in the output field of the response.
    The patch is in the format of a proper diff format.
    It incorporates any new files specified in the request, thereby excluding irrelevant installation files.
    It includes deleted files by default.
    You should run it after all the changes are made.
    Example:
    diff --git a/repo/example.py b/repo/example.py
    index 1234567..89abcde 100644
    --- a/repo/example.py
    +++ b/repo/example.py
    @@ -1 +1 @@
    -Hello, World!
    +Hello, Composio!
    """

    _history_maintains: bool = True
    _display_name = "Get Patch Action"
    _request_schema = GetPatchRequest
    _response_schema = GetPatchResponse

    @history_recorder()
    def execute(
        self, request_data: GetPatchRequest, authorisation_data: dict
    ) -> BaseResponse:
        print("Get patch command...")
        self._setup(request_data)
        print("Setup completed.")
        new_files = " ".join(request_data.new_file_path)
        cmd1 = "git add -u"
        if len(request_data.new_file_path) > 0:
            cmd1 = f"git add {new_files} && " + cmd1
        cmd_response: BaseCmdResponse = self.workspace.communicate(cmd1)
        output, return_code = process_output(cmd_response.output, cmd_response.return_code)
        print(f"Output of git add: {output}")
        cmd2 = "git diff --cached"
        cmd_response: BaseCmdResponse = self.workspace.communicate(cmd2)
        output, return_code = process_output(cmd_response.output, cmd_response.return_code)
        return BaseResponse(
            output=output,
            return_code=return_code,
        )
