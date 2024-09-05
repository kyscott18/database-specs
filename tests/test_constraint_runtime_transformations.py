from helpers import *


@pytest.fixture(scope='function', autouse=True)
def setup(connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract):
    dummy_code.insert(connection)
    dummy_contract.insert(
        connection, dummy_code.code_hash, dummy_code.code_hash)
    dummy_contract_deployment.insert(connection, dummy_contract.id)
    dummy_compiled_contract.insert(
        connection, dummy_code.code_hash, dummy_code.code_hash)


class TestCommon:
    def test_empty_array_is_allowed(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = []
        dummy_verified_contract.insert(
            connection, dummy_contract_deployment.id, dummy_compiled_contract.id)

    def test_expected_type_values(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "library", "type": "replace",
                "offset": 0, "id": "file1:lib1"},
            {"reason": "immutable", "type": "replace", "offset": 0, "id": "0"},
            {"reason": "cborAuxdata", "type": "replace", "offset": 0, "id": "0"},
            {"reason": "callProtection", "type": "replace", "offset": 0}
        ]
        dummy_verified_contract.insert(
            connection, dummy_contract_deployment.id, dummy_compiled_contract.id)

    @pytest.mark.parametrize("value", [None, "", dict()], ids=["null", "string", "object"])
    def test_invalid_json_type_fails(self, value, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = value
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    @pytest.mark.parametrize("value", [None, "", []], ids=["null", "string", "array"])
    def test_invalid_transformation_value_type_fails(self, value, connection, dummy_code, dummy_contract, dummy_contract_deployment,
                                                     dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [value]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    def test_no_reason_key_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"type": "insert", "offset": 0, "id": "0"}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    @pytest.mark.parametrize("value", [None, [], dict()], ids=["null", "array", "object"])
    def test_reason_with_invalid_type_fails(self, value, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": value, "type": "insert", "offset": 0, "id": "0"}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    def test_invalid_reason_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "unknownReason", "type": "insert", "offset": 0, "id": "0"}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    def test_constructor_arguments_reason_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "constructorArguments", "type": "insert", "offset": 0}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")


class TestLibrary:
    def test_valid_value(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "library", "type": "replace",
                "offset": 0, "id": "file1:lib1"}
        ]
        dummy_verified_contract.insert(
            connection, dummy_contract_deployment.id, dummy_compiled_contract.id)

    def test_missing_key_type_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "library", "offset": 0, "id": "file1:lib1"}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    @pytest.mark.parametrize("value", [None, 0, [], dict()], ids=["null", "number", "array", "object"])
    def test_invalid_key_type_type_fails(self, value, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "library", "type": value, "offset": 0, "id": "file1:lib1"}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    def test_invalid_key_type_value_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "library", "type": "insert",
                "offset": 0, "id": "file1:lib1"}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    def test_missing_key_offset_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "library", "type": "replace", "id": "file1:lib1"}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    @pytest.mark.parametrize("value", [None, "", [], dict()], ids=["null", "string", "array", "object"])
    def test_invalid_key_offset_type_fails(self, value, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "library", "type": "replace",
                "offset": value, "id": "file1:lib1"}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    def test_invalid_key_offset_value_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment,
                                            dummy_compiled_contract, dummy_verified_contract):
        # The offset must be >= 0
        dummy_verified_contract.runtime_transformations = [
            {"reason": "library", "type": "replace",
                "offset": -1, "id": "file1:lib1"}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    def test_missing_key_id_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "library", "type": "replace", "offset": 0}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    @pytest.mark.parametrize("value", [None, 0, [], dict()], ids=["null", "number", "array", "object"])
    def test_invalid_key_id_type_fails(self, value, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "library", "type": "replace", "offset": 0, "id": value}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    def test_invalid_key_id_value_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment,
                                        dummy_compiled_contract, dummy_verified_contract):
        # The length of `id` must be > 0
        dummy_verified_contract.runtime_transformations = [
            {"reason": "library", "type": "replace", "offset": 0, "id": ""}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")


class TestImmutable:
    def test_valid_value(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "immutable", "type": "replace", "offset": 0, "id": "0"},
        ]
        dummy_verified_contract.insert(
            connection, dummy_contract_deployment.id, dummy_compiled_contract.id)

    def test_missing_key_type_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "immutable", "offset": 0, "id": "0"},
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    @pytest.mark.parametrize("value", [None, 0, [], dict()], ids=["null", "number", "array", "object"])
    def test_invalid_key_type_type_fails(self, value, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "immutable", "type": value, "offset": 0, "id": "0"},
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    def test_invalid_key_type_value_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "immutable", "type": "insert", "offset": 0, "id": "0"},
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    def test_missing_key_offset_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "immutable", "type": "replace", "id": "0"},
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    @pytest.mark.parametrize("value", [None, "", [], dict()], ids=["null", "string", "array", "object"])
    def test_invalid_key_offset_type_fails(self, value, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "immutable", "type": "replace", "offset": value, "id": "0"},
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    def test_invalid_key_offset_value_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment,
                                            dummy_compiled_contract, dummy_verified_contract):
        # The offset must be >= 0
        dummy_verified_contract.runtime_transformations = [
            {"reason": "immutable", "type": "replace", "offset": -1, "id": "0"},
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    def test_missing_key_id_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "immutable", "type": "replace", "offset": 0},
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    @pytest.mark.parametrize("value", [None, 0, [], dict()], ids=["null", "number", "array", "object"])
    def test_invalid_key_id_type_fails(self, value, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "immutable", "type": "replace", "offset": 0, "id": value},
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    def test_invalid_key_id_value_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment,
                                        dummy_compiled_contract, dummy_verified_contract):
        # The length of `id` must be > 0
        dummy_verified_contract.runtime_transformations = [
            {"reason": "immutable", "type": "replace", "offset": 0, "id": ""},
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")


class TestCborAuxdata:
    def test_valid_value(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "cborAuxdata", "type": "replace", "offset": 0, "id": "0"}
        ]
        dummy_verified_contract.insert(
            connection, dummy_contract_deployment.id, dummy_compiled_contract.id)

    def test_missing_key_type_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "cborAuxdata", "offset": 0, "id": "0"}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    @pytest.mark.parametrize("value", [None, 0, [], dict()], ids=["null", "number", "array", "object"])
    def test_invalid_key_type_type_fails(self, value, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "cborAuxdata", "type": value, "offset": 0, "id": "0"}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    def test_invalid_key_type_value_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "cborAuxdata", "type": "insert", "offset": 0, "id": "0"}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    def test_missing_key_offset_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "cborAuxdata", "type": "replace", "id": "0"}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    @pytest.mark.parametrize("value", [None, "", [], dict()], ids=["null", "string", "array", "object"])
    def test_invalid_key_offset_type_fails(self, value, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "cborAuxdata", "type": "replace", "offset": value, "id": "0"}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    def test_invalid_key_offset_value_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment,
                                            dummy_compiled_contract, dummy_verified_contract):
        # The offset must be >= 0
        dummy_verified_contract.runtime_transformations = [
            {"reason": "cborAuxdata", "type": "replace", "offset": -1, "id": "0"}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    def test_missing_key_id_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "cborAuxdata", "type": "replace", "offset": 0}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    @pytest.mark.parametrize("value", [None, 0, [], dict()], ids=["null", "number", "array", "object"])
    def test_invalid_key_id_type_fails(self, value, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "cborAuxdata", "type": "replace", "offset": 0, "id": value}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    def test_invalid_key_id_value_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment,
                                        dummy_compiled_contract, dummy_verified_contract):
        # The length of `id` must be > 0
        dummy_verified_contract.runtime_transformations = [
            {"reason": "cborAuxdata", "type": "replace", "offset": 0, "id": ""}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")


class TestCallProtection:
    def test_valid_value(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "callProtection", "type": "replace", "offset": 0}
        ]
        dummy_verified_contract.insert(
            connection, dummy_contract_deployment.id, dummy_compiled_contract.id)

    def test_missing_key_type_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "callProtection", "offset": 0}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    @pytest.mark.parametrize("value", [None, 0, [], dict()], ids=["null", "number", "array", "object"])
    def test_invalid_key_type_type_fails(self, value, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "callProtection", "type": value, "offset": 0}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    def test_invalid_key_type_value_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "callProtection", "type": "insert", "offset": 0}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    def test_missing_key_offset_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "callProtection", "type": "replace"}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    @pytest.mark.parametrize("value", [None, "", [], dict()], ids=["null", "string", "array", "object"])
    def test_invalid_key_offset_type_fails(self, value, connection, dummy_code, dummy_contract, dummy_contract_deployment, dummy_compiled_contract, dummy_verified_contract):
        dummy_verified_contract.runtime_transformations = [
            {"reason": "callProtection", "type": "replace", "offset": value}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")

    def test_invalid_key_offset_value_fails(self, connection, dummy_code, dummy_contract, dummy_contract_deployment,
                                            dummy_compiled_contract, dummy_verified_contract):
        # The offset must be >= 0
        dummy_verified_contract.runtime_transformations = [
            {"reason": "callProtection", "type": "replace", "offset": -1}
        ]
        check_constraint_fails(
            lambda: dummy_verified_contract.insert(
                connection, dummy_contract_deployment.id, dummy_compiled_contract.id),
            "runtime_transformations_array")
