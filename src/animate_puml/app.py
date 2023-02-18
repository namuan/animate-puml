#!/usr/bin/env python3
"""
A simple command line tool to generate animated gif from plantuml file
"""
from __future__ import annotations

import logging
import re
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from collections.abc import Generator
from pathlib import Path
from typing import Any

from PIL import Image  # type: ignore
from py_executable_checklist.workflow import WorkflowBase, run_command, run_workflow
from pygifsicle import optimize  # type: ignore

from animate_puml import setup_logging


# Workflow steps
class ReadPlantUmlFile(WorkflowBase):
    """
    Read the plantuml file into string
    """

    plantuml_file_path: Path

    def execute(self) -> dict:
        logging.info("Reading plantuml file %s", self.plantuml_file_path)
        plantuml_file_contents = self.plantuml_file_path.read_text()
        return {"plantuml_file_contents": plantuml_file_contents}


class GenerateFrames(WorkflowBase):
    """
    Generate a copy of file for each frame
    """

    plantuml_file_contents: str
    _start_tag: str = r"'\s*start"
    _end_tag: str = r"'\s*end"

    def replace_once(self, text: str, pattern: str, replacement: str) -> str:
        return re.sub(pattern, replacement, text, count=1)

    def each_line(self, extracted_text: str) -> Generator[str, None, None]:
        new_text = extracted_text
        for _ in extracted_text.splitlines():
            new_text = self.replace_once(new_text, r"\[#lightgray]->", "[thickness=2]->")
            new_text = self.replace_once(new_text, r"\$disabled ", "")
            yield new_text

    def execute(self) -> dict:
        pattern = re.compile(self._start_tag + "(.*?)" + self._end_tag, re.DOTALL)
        extracted_text = pattern.search(self.plantuml_file_contents).group(1)  # type: ignore

        modified_file_content = self.plantuml_file_contents

        frames = []

        modified_extracted_text = extracted_text

        for i in self.each_line(extracted_text):
            modified_file_content = modified_file_content.replace(
                modified_extracted_text,
                i,
            )
            modified_extracted_text = i
            frames.append(modified_file_content)
        # output
        return {"frames": frames}


class GenerateImageForFrames(WorkflowBase):
    """
    Use Plantuml to generate image file for each frame
    """

    frames: list[str]
    plantuml_file_path: Path
    debug: bool

    def execute(self) -> dict:
        output_dir = self.plantuml_file_path.parent
        output_file_prefix = self.plantuml_file_path.stem

        image_file_paths = []

        for idx, frame in enumerate(self.frames):
            target_file = output_dir.joinpath(f"{output_file_prefix}-{idx}.puml")
            target_file.write_text(frame)
            run_command(f"plantuml -tpng {target_file}")
            image_file_paths.append(target_file.with_suffix(".png"))
            if not self.debug:
                target_file.unlink()

        return {
            "output_dir": output_dir,
            "output_file_prefix": output_file_prefix,
            "image_file_paths": image_file_paths,
        }


class CombineFramesIntoVideo(WorkflowBase):
    """
    Combine images into animated video
    """

    output_dir: Path
    output_file_prefix: str
    image_file_paths: list[Path]
    output_file_path: Path

    def padded_image(self, original_image: Any) -> Any:
        width, height = original_image.size
        padding = 50
        new_width = width + padding
        new_height = height + padding
        new_image = Image.new(original_image.mode, (new_width, new_height), (255, 255, 255))
        new_image.paste(original_image, ((new_width - width) // 2, (new_height - height) // 2))
        return new_image

    def execute(self) -> dict:
        target_animated_gif = self.output_dir / f"{self.output_file_prefix}.gif"
        target_compressed_animated_gif = self.output_file_path
        img, *imgs = (self.padded_image(Image.open(f)) for f in self.image_file_paths)
        img.save(
            fp=target_animated_gif.as_posix(),
            format="GIF",
            append_images=imgs,
            save_all=True,
            duration=2000,
            loop=0,
        )
        optimize(target_animated_gif, target_compressed_animated_gif)
        return {
            "target_animated_gif": target_animated_gif,
            "animated_gif_file_path": target_compressed_animated_gif.as_posix(),
        }


class CleanUpTemporarilyFiles(WorkflowBase):
    """
    Clean up temporary files
    """

    target_animated_gif: Path
    animated_gif_file_path: str
    image_file_paths: list[Path]
    debug: bool

    def execute(self) -> dict:
        if not self.debug:
            self.target_animated_gif.unlink()
            for image_file_path in self.image_file_paths:
                image_file_path.unlink()

        return {"animated_gif_file_path": self.animated_gif_file_path}


def workflow() -> list[type[WorkflowBase]]:
    return [
        ReadPlantUmlFile,
        GenerateFrames,
        GenerateImageForFrames,
        CombineFramesIntoVideo,
        CleanUpTemporarilyFiles,
    ]


def parse_args() -> Any:
    parser = ArgumentParser(description=__doc__, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--plantuml-file-path", type=Path, required=True, help="Path to PlantUML file")
    parser.add_argument("-o", "--output-file-path", type=Path, required=True, help="Path to animated gif file")
    parser.add_argument("-d", "--debug", action="store_true", default=False, help="Leave temporary files for debugging")
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        dest="verbose",
        help="Increase verbosity of logging output. Display context variables between each step run",
    )
    return parser.parse_args()


def main() -> None:  # pragma: no cover
    args = parse_args()
    setup_logging(args.verbose)
    context = args.__dict__
    run_workflow(context, workflow())
    print("Generated animation: " + context["animated_gif_file_path"])


if __name__ == "__main__":  # pragma: no cover
    main()
