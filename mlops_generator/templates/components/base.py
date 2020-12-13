from pathlib import Path
import json
from collections import OrderedDict
from typing import List, Dict, Tuple, NoReturn


import logging

logger = logging.getLogger(__name__)


class BaseArtifact(object):
    def __init__(self, metadata: dict, filename: str, tmp_dir: str):
        """Implement basic operations for metadata artifact's.
        Args:
            metadata (dict): [description]
            filename (str): [description]
            tmp_dir (str): [description]
        """
        self.__metadata = OrderedDict(metadata)
        self.__filename = filename
        self.__tmp_dir = Path(tmp_dir)
        self.tmp_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Initialized artifact {}".format(str(self.fpath)))

    def __repr__(self):
        return json.dumps(self.metadata, indent=2)

    @property
    def filename(self) -> str:
        return self.__filename

    @property
    def tmp_dir(self) -> Path:
        """Get temporal directory."""
        return self.__tmp_dir

    @property
    def fpath(self) -> Path:
        """Resolve filename path."""
        return self.tmp_dir / self.filename

    @property
    def metadata(self) -> Dict:
        """Get metadata.

        Returns:
            dict: Metadata
        """
        return self.__metadata

    def make_dir(self, path: Path) -> Path:
        """Util for create parents and avois raise if exists.

        Args:
            path (pathlib.Path): Resolved path
        """
        path.mkdir(parents=True, exist_ok=True)
        return path

    def save_metadata(self, fpath: str = None):
        """Save metadata filename in temporal path.

        Args:
            fpath (str, optional): Filepath to save metadata. Defaults to None, and use built filename.

        Returns:
            [type]: self
        """
        try:
            # If the fpath is not given, use the defined filename
            if fpath is None:
                fpath = self.filename
            # Save json file
            logger.info("Saving metadata in {}".format(fpath))
            with open(fpath, "w") as f:
                json.dump(self.metadata, f, indent=2)
            return self
        except PermissionError as e:
            logger.error(e)

    def update(self, key: dict) -> NoReturn:
        """Update metadata dictionary

        Args:
            key (str): New dict to update
        """
        self.metadata.update(key)

    def pop(self, index: int) -> Dict:
        """Pop item from metadata given an index.

        Args:
            index (int): Index position to remove in ordered metadata dict.

        Returns:
            Dict: Metadata
        """
        return self.metadata["outputs"].pop(index)

    def get(self, index: int) -> Dict:
        """Get item from metadata given an index.

        Args:
            index (int): Index position to get

        Returns:
            [type]: Metadata
        """
        return self.metadata["outputs"][index]

    @classmethod
    def from_filename(cls, fpath: Path, *args, **kwargs):
        """Class method for create an artifact given json filepath.

        Args:
            fpath (str): Filepath to user for load artifact

        Returns:
            BaseArtifact: Built artifact
        """
        fpath.parent.mkdir(parents=True, exist_ok=True)
        with open(str(fpath), "r") as fh:
            metadata = json.load(fh)
            return cls(
                metadata=metadata,
                filename=fpath.name,
                tmp_dir=fpath.parent,
                *args,
                **kwargs
            )

    def __str__(self) -> str:
        """Simple string for log it."""
        return "\nArtifact: {}\nMetadata {}".format(
            str(self.fpath), json.dumps(self.metadata, indent=2)
        )
