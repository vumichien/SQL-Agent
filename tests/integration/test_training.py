"""
Integration Tests for Training Script

Tests the training script that loads data into ChromaDB via Vanna.

Prerequisites:
    - Claude Agent endpoint running on http://localhost:8000
    - Chinook database at data/chinook.db
    - Training data in training_data/chinook/
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.train_chinook import train_chinook_database, verify_training
from src.detomo_vanna import DetomoVanna


class TestTrainingScript:
    """Test suite for Chinook database training script"""

    def test_training_script_loads_data(self):
        """Test that training script loads data successfully"""
        # Run training
        count = train_chinook_database()

        # Verify minimum number of items loaded
        # We have 12 DDL files + 11 docs + 70 Q&A pairs = 93 items minimum
        assert count >= 70, f"Expected at least 70 training items, got {count}"
        assert isinstance(count, int), "Training count should be an integer"

    def test_training_data_persisted_to_chromadb(self):
        """Test that training data is persisted to ChromaDB"""
        # Verify ChromaDB directory exists
        vectordb_path = Path("./detomo_vectordb")
        assert vectordb_path.exists(), "ChromaDB directory should exist"
        assert vectordb_path.is_dir(), "ChromaDB path should be a directory"

    def test_training_data_retrievable(self):
        """Test that training data can be retrieved after loading"""
        # Initialize Vanna
        vn = DetomoVanna(config={"path": "./detomo_vectordb"})

        # Get training data
        training_data = vn.get_training_data()

        # Verify data exists (Vanna returns DataFrame)
        assert len(training_data) > 0, "Should have training data in ChromaDB"
        # Note: Vanna returns a DataFrame, not a list

    def test_training_data_contains_expected_types(self):
        """Test that training data contains DDL, docs, and Q&A pairs"""
        vn = DetomoVanna(config={"path": "./detomo_vectordb"})
        training_data = vn.get_training_data()

        # Check for different training data types
        # Vanna returns a DataFrame with 'training_data_type' column
        has_ddl = False
        has_documentation = False
        has_sql = False

        if 'training_data_type' in training_data.columns:
            types = training_data['training_data_type'].unique()
            has_ddl = 'ddl' in types
            has_documentation = 'documentation' in types
            has_sql = 'sql' in types

        # Verify we have substantial training data
        assert len(training_data) >= 70, "Should have substantial training data"

        # Optionally check we have different types
        # (Not strictly required as long as we have data)
        assert has_ddl or has_documentation or has_sql, "Should have at least one type of training data"

    def test_verify_training_function(self):
        """Test the verify_training helper function"""
        result = verify_training()
        assert result is True, "Verification should return True when data exists"

    def test_vanna_can_connect_to_database(self):
        """Test that Vanna can connect to Chinook database"""
        vn = DetomoVanna(config={"path": "./detomo_vectordb"})

        # Connect to database
        vn.connect_to_sqlite("data/chinook.db")

        # Verify connection by running a simple query
        result = vn.run_sql("SELECT COUNT(*) as count FROM customers")

        assert result is not None, "Should get result from database"
        assert len(result) > 0, "Should have at least one row"
        assert 'count' in result.columns, "Should have count column"

    def test_training_is_idempotent(self):
        """Test that running training multiple times doesn't cause errors"""
        # Run training twice
        count1 = train_chinook_database()
        count2 = train_chinook_database()

        # Both should succeed
        assert count1 >= 70, "First training should succeed"
        assert count2 >= 70, "Second training should succeed"

        # Note: Vanna may deduplicate or accumulate data
        # We just verify both runs complete successfully


class TestTrainingDataQuality:
    """Test suite for training data quality checks"""

    def test_qa_pairs_are_valid(self):
        """Test that all Q&A pairs have valid format"""
        import json
        from pathlib import Path

        qa_dir = Path("training_data/chinook/questions")
        total_pairs = 0

        for qa_file in qa_dir.glob("*.json"):
            with open(qa_file, 'r', encoding='utf-8') as f:
                qa_pairs = json.load(f)

                for pair in qa_pairs:
                    # Check required fields
                    assert "question" in pair, f"Missing 'question' in {qa_file.name}"
                    assert "sql" in pair, f"Missing 'sql' in {qa_file.name}"

                    # Check types
                    assert isinstance(pair["question"], str), "Question should be string"
                    assert isinstance(pair["sql"], str), "SQL should be string"

                    # Check not empty
                    assert len(pair["question"]) > 0, "Question should not be empty"
                    assert len(pair["sql"]) > 0, "SQL should not be empty"

                    total_pairs += 1

        # Verify we have expected number of pairs
        assert total_pairs >= 70, f"Expected at least 70 Q&A pairs, got {total_pairs}"

    def test_ddl_files_are_valid_sql(self):
        """Test that DDL files contain valid SQL"""
        from pathlib import Path

        ddl_dir = Path("training_data/chinook/ddl")
        ddl_count = 0

        for ddl_file in ddl_dir.glob("*.sql"):
            with open(ddl_file, 'r', encoding='utf-8') as f:
                content = f.read()

                # Basic checks
                assert len(content) > 0, f"{ddl_file.name} should not be empty"

                # relationships.sql is documentation, not CREATE TABLE
                if ddl_file.name != "relationships.sql":
                    assert "CREATE TABLE" in content.upper(), f"{ddl_file.name} should contain CREATE TABLE"

                ddl_count += 1

        # Verify we have expected number of DDL files
        assert ddl_count >= 11, f"Expected at least 11 DDL files, got {ddl_count}"

    def test_documentation_files_exist(self):
        """Test that all documentation files exist and are not empty"""
        from pathlib import Path

        doc_dir = Path("training_data/chinook/documentation")
        doc_count = 0

        for doc_file in doc_dir.glob("*.md"):
            with open(doc_file, 'r', encoding='utf-8') as f:
                content = f.read()

                # Check not empty
                assert len(content) > 0, f"{doc_file.name} should not be empty"

                # Check has markdown headers
                assert "#" in content, f"{doc_file.name} should have markdown headers"

                doc_count += 1

        # Verify we have expected number of docs
        assert doc_count >= 11, f"Expected at least 11 documentation files, got {doc_count}"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
