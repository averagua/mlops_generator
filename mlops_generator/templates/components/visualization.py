from {{project_name}}.base import BaseArtifact
from typing import NoReturn, List, Dict, Tuple
from pathlib import Path
import matplotlib.pyplot as plt, mpld3

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class VisualizationArtifacts(BaseArtifact):
    def __init__(self):
        """Metadata visualizer.
        See https://www.kubeflow.org/docs/pipelines/sdk/output-viewer/

        Args:
            tmp_dir (str): Temporal directory.
            filename (str, optional): [description]. Defaults to 'mlpipeline-ui-metadata.json'.
        """
        super(VisualizationArtifacts, self).__init__(
            metadata={"outputs": []}, filename="mlpipeline-ui-metadata.json", tmp_dir=""
        )

    def extend_outputs(self, output: dict):
        """Magic output extends for metadata.

        Args:
            output (list): The output dicto to extend.
        """
        if not isinstance(output, list):
            output = [output]
        self.metadata["outputs"].extend(output)
        return self

    def add_tablemetadata(self, source: str, headers: List[str], storage:str=None):
        """Add table to metadata for use in pipelines ui.

        DISCUSSION: Kubeflow provide a volume operation for persist files. But doesnt work, and it has little documentation. So,
        the implementation are limited to work with google cloud storage.
        In future work prefer use minio, and try to debug the persistent volumes.
        See https://www.kubeflow.org/docs/pipelines/sdk/manipulate-resources/#volumeop
        Args:
            source (str): Blob path with the csv table.
            headers (List[str]): Headers to include in the visualization
            bucket_name (str): Working bucket name, not known for artifact.
            prefix (str, optional): [description]. Defaults to 'gs://'.

        Returns:
            [type]: [description]
        """
        logger.info("Settig Metadata Table {}".format(source))
        if isinstance(source, Path):
            source = str(source)
        output = {"type": "table", "source": source, "header": headers, "format": "csv"}
        if storage == "gs":
            output["storage"] = "gs"
            output["source"] = "gs://" + output["source"]
        return self.extend_outputs(output)

    def add_metadata_markdown(self, markdown: str = "# Hello markdown!"):
        """Add metadata markdown

        Args:
            markdown (str, optional): Markdown string. Defaults to "# Hello markdown!".
        """
        logger.info("Setting Metadata Markdown")
        output = {
            "type": "markdown",
            "source": markdown,
            "storage": "inline",
        }
        self.extend_outputs(output)

    def append_div(self, static_html:str) -> str:
        """Append static html between div tags"""
        return "<div>" + static_html + "</div>"

    def add_static_html(self, static_html: str, storage: str = "inline"):
        """Add static html to artifact"""
        logger.info("setting static html")
        output = {
            "type": "web-app",
            "storage": storage,
            "source": self.append_div(static_html=static_html),
        }
        self.extend_outputs(output)

    def figure_to_html(self, figure) -> str:
        """Transform matplotlib.figure to html

        Args:
            figure (Figure): Matplotlib figure to transform

        Returns:
            str: Transformed figured in string type
        """
        return mpld3.fig_to_html(figure)

    def add_html_from_figure(self, figure) -> NoReturn:
        self.add_static_html(static_html=self.figure_to_html(figure), storage="inline")

    def add_figures_html(self, figures: List) -> NoReturn:
        """Join matplotlib figures list to single html between div's tags"""
        figures = [self.append_div(self.figure_to_html(figure)) for figure in figures]
        figures = "".join(figures)
        self.add_static_html(figures)

    def filter(self, out_type: str) -> List[Dict]:
        """Apply filter to metadata for get some element"""
        return list(filter(lambda x: x["type"] == out_type, self.metadata["outputs"]))

    def plot_simple(
        self,
        serie,
        title:str,
        figsize: Tuple = (14, 5),
        label: str = "Label",
    ):
        fig, ax = plt.subplots(1, 1, sharex=False, figsize=figsize)
        ax = serie.plot(style='--',fontsize=12, figsize=figsize, ax=ax, c='g', label=label)
        ax.set_title(title, fontsize=18)
        ax.legend(fontsize=14)
        return fig