"""
module with the stuff needed to run a jobs sequence.

You can find:\n
the Pipeline class responsible to execute the jobs, see `.pipe.Pipeline`\n
and the context used to pass all the information accross all the jobs see `.context.Context`
"""

from .context import Context
from .pipe import Pipeline
