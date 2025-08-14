import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import analysis


class TestAnalysis(unittest.TestCase):

    def setUp(self):
        # Мокаем plt.show, чтобы тесты не открывали окна
        patcher = patch("matplotlib.pyplot.show")
        self.mock_show = patcher.start()
        self.addCleanup(patcher.stop)

    @patch("analysis._read_sql")
    def test_show_top_clients_with_data(self, mock_read_sql):
        # Подготовка данных
        df = pd.DataFrame({
            "name": ["Alice", "Bob"],
            "total_orders": [10, 5]
        })
        mock_read_sql.return_value = df

        analysis.show_top_clients()
        mock_read_sql.assert_called_once()
        self.mock_show.assert_called_once()

    @patch("analysis._read_sql")
    def test_show_top_clients_empty(self, mock_read_sql):
        mock_read_sql.return_value = pd.DataFrame()
        with patch("builtins.print") as mock_print:
            analysis.show_top_clients()
            mock_print.assert_called_with("Нет данных для анализа")
        self.mock_show.assert_not_called()

    @patch("analysis._read_sql")
    def test_show_orders_over_time_with_data(self, mock_read_sql):
        df = pd.DataFrame({
            "created_at": ["2025-01-01", "2025-01-01", "2025-01-02"]
        })
        mock_read_sql.return_value = df

        analysis.show_orders_over_time()
        mock_read_sql.assert_called_once()
        self.mock_show.assert_called_once()

    @patch("analysis._read_sql")
    def test_show_orders_over_time_empty(self, mock_read_sql):
        mock_read_sql.return_value = pd.DataFrame()
        with patch("builtins.print") as mock_print:
            analysis.show_orders_over_time()
            mock_print.assert_called_with("Нет данных для анализа")
        self.mock_show.assert_not_called()

    @patch("analysis._read_sql")
    def test_show_client_graph_with_data(self, mock_read_sql):
        df = pd.DataFrame({
            "client": ["Alice", "Bob"],
            "product": ["Laptop", "Phone"]
        })
        mock_read_sql.return_value = df

        analysis.show_client_graph()
        mock_read_sql.assert_called_once()
        self.mock_show.assert_called_once()

    @patch("analysis._read_sql")
    def test_show_client_graph_empty(self, mock_read_sql):
        mock_read_sql.return_value = pd.DataFrame()
        with patch("builtins.print") as mock_print:
            analysis.show_client_graph()
            mock_print.assert_called_with("Нет данных для анализа")
        self.mock_show.assert_not_called()


if __name__ == "__main__":
    unittest.main()
