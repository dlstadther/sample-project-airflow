def test_dagbag_imports(dag_bag):
    # Arrange
    expected_dags = {"placeholder_dag"}

    # Act (fixtures)
    # Assert
    # Import errors aren't raised but captured to ensure all DAGs are parsed
    assert not dag_bag.import_errors

    assert set(dag_bag.dag_ids) == expected_dags
