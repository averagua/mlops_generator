from {{project_name}}.base import BaseArtifact


class TemporalArtifact(BaseArtifact):
    def __init__(self, metadata: dict, tmp_dir: str, filename: str = "tmp_data.json"):
        """Artifact for build artifact to pass throw components or use it like ouputs.

        Args:
            metadata (dict): [description]
            tmp_dir (str): [description]
            filename (str, optional): Filename for temporal json. Defaults to "tmp_data.json".
        """
        super(TemporalArtifact, self).__init__(
            metadata=metadata, filename=filename, tmp_dir=tmp_dir
        )

    def foo(self):
        """Implement you own transformation in temporal artifact, like new paths or
        concatenated string to next components."""
        raise NotImplementedError("Method not implemented")