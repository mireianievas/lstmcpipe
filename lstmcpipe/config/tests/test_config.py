from lstmcpipe.config import export_env, load_config
from lstmcpipe.config.pipeline_config import config_valid, parse_config_and_handle_global_vars
import tempfile
import os
import yaml
from datetime import datetime

yaml_keys = [
    "prod_id",
    "stages_to_be_run",
    "base_path_dl0",
    "pointing",
    "zenith",
    "particles",
    "offset_gammas",
    "obs_date",
    "prod_type",
    "workflow_kind",
]
dummy_config = {k: None for k in yaml_keys}
dummy_config["merging_options"] = {"no_image": False}
dummy_config["source_environment"] = {
    "source_file": "src_file",
    "conda_env": "env",
}


def test_export_env():
    tmp_dir = tempfile.mkdtemp()
    export_env(tmp_dir)
    if not os.path.exists(os.path.join(tmp_dir, 'requirements.txt')):
        assert os.path.exists(os.path.join(tmp_dir, 'conda_env.yml'))


def test_config_valid():
    """
    Test invalid values for all relevant fields individually.
    This tests values, that are supposed to fail.
    This does not test if no valid configuration is marked
    as invalid!
    """
    assert config_valid(dummy_config)[0] is False

    valid = dummy_config.copy()
    valid["prod_type"] = "prod5"
    valid["workflow_kind"] = "lstchain"
    valid["obs_date"] = "20200629_prod5_trans_80"
    assert config_valid(valid)[0] is True

    invalid_workflow = valid.copy()
    invalid_workflow["workflow_kind"] = "MARS"
    assert config_valid(invalid_workflow)[0] is False

    invalid_date = valid.copy()
    invalid_date["obs_date"] = "1970-01-01"
    assert config_valid(invalid_date)[0] is False

    invalid_prod = valid.copy()
    invalid_prod["prod_type"] = "prod42"
    assert config_valid(invalid_prod)[0] is False

    invalid_date_prod = valid.copy()
    # this should only be allowed with prod3, which is not chosen here
    invalid_date_prod["obs_date"] = "20190415"
    assert config_valid(invalid_date_prod)[0] is False


def test_parse_config_and_handle_global_vars():
    """
    Test that the file paths are properly set.
    This only tests a subset of the variables, that are set in
    the function.
    """
    config = dummy_config.copy()
    config["workflow_kind"] = "lstchain"
    config["prod_type"] = "prod5"
    config["obs_date"] = "20200629_prod5_trans_80"
    config["pointing"] = "90"
    config["zenith"] = "45"
    config["base_path_dl0"] = "/dummy/path/to/files"

    parsed_config = parse_config_and_handle_global_vars(config)
    date = datetime.today().strftime("%Y%m%d")
    assert (
        parsed_config["DL1_data_dir"] ==
        "/dummy/path/to/files/DL1/20200629_prod5_trans_80/{}/45/90/"+date+"_v0.7.3_prod5_trans_80_None"
    )
    assert (
        parsed_config["model_dir"] ==
        "/dummy/path/to/files/models/20200629_prod5_trans_80/45/90/"+date+"_v0.7.3_prod5_trans_80_None"
    )
    assert (
        parsed_config["source_environment"] ==
        "source src_file; conda activate env; "
    )
    assert parsed_config["stages_to_run"] is None
    assert parsed_config["workflow_kind"] == "lstchain"
