from animate_puml.app import (
    CleanUpTemporarilyFiles,
    CombineFramesIntoVideo,
    GenerateFrames,
    GenerateImageForFrames,
    ReadPlantUmlFile,
    workflow,
)


def test_return_expected_workflow() -> None:
    expected_workflow_steps = workflow()

    assert expected_workflow_steps == [
        ReadPlantUmlFile,
        GenerateFrames,
        GenerateImageForFrames,
        CombineFramesIntoVideo,
        CleanUpTemporarilyFiles,
    ]
