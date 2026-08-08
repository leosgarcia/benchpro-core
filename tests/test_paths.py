from benchpro_core.paths import app_data_dir, logs_dir, settings_dir


def test_core_paths_are_product_scoped() -> None:
    app_path = str(app_data_dir())

    assert "WL Tech" in app_path
    assert "Bench Pro Core" in app_path
    assert logs_dir().parent == app_data_dir()
    assert settings_dir().parent == app_data_dir()
