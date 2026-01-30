import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Set

import polars as pl
import kagglehub
from kagglehub import KaggleDatasetAdapter

# --- Configuração de Logging ---
LOG_DIR = Path("./logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ETL_Pipeline")


class ETL:
    """Interface base para processos de extração, transformação e carga."""

    VALID_EXTENSIONS: Set[str] = {".csv", ".json", ".parquet"}

    def __init__(self, name: str, source: str) -> None:
        self.name = name
        self._source = source
        logger.info("Instanciando pipeline '%s' via %s", self.name, self._source)

    def __repr__(self) -> str:
        return f"ETL(name='{self.name}', source='{self._source}')"

    def data_extract_kaggle(self, dataset: str, file_name: Optional[str] = None) -> pl.LazyFrame:
        """Extrai dados diretamente da API do Kaggle."""
        logger.info("[%s] Iniciando extração do dataset: %s", self.name, dataset)

        try:
            path_str = kagglehub.dataset_download(dataset)
            path = Path(path_str)
        except Exception as e:
            logger.error("Falha no download do Kaggle: %s", e)
            raise

        # Filtragem de arquivos válidos
        available_files = [f for f in path.iterdir() if f.suffix in self.VALID_EXTENSIONS]
        
        if not available_files:
            raise FileNotFoundError(f"Nenhum arquivo compatível {self.VALID_EXTENSIONS} encontrado em {path}")

        # Seleção do arquivo
        if file_name:
            target_file = path / file_name
            if not target_file.exists():
                raise FileNotFoundError(f"Arquivo '{file_name}' não encontrado. Disponíveis: {[f.name for f in available_files]}")
        else:
            target_file = available_files[0]
            logger.warning("file_name não especificado. Utilizando padrão: %s", target_file.name)

        try:
            return kagglehub.load_dataset(
                KaggleDatasetAdapter.POLARS,
                dataset,
                target_file.name
            )
        except Exception as e:
            logger.error("Erro ao carregar LazyFrame: %s", e)
            raise

    def data_transform(self, data: pl.LazyFrame) -> pl.LazyFrame:
        """Aplica limpeza básica e enriquecimento de metadados."""
        logger.info("[%s] Aplicando transformações de limpeza", self.name)

        return (
            data.drop_nulls()
            .unique()
            .with_columns([
                pl.lit(self._source).alias("_source"),
                pl.lit(self.name).alias("_etl_name"),
                pl.lit(datetime.now()).alias("_processed_at"),
            ])
        )

    def data_load(self, data: pl.LazyFrame, ext: str = '.csv') -> None:
        """Persiste o LazyFrame em disco (Sink)."""
        output_dir = Path("./loaded_data")
        output_dir.mkdir(exist_ok=True)

        file_path = output_dir / f"{self.name}_{self._source}{ext}"

        try:
            if ext == '.csv':
                data.sink_csv(file_path)
            elif ext == '.parquet':
                data.sink_parquet(file_path)
            else:
                raise ValueError(f"Extensão {ext} não suportada. Use .csv ou .parquet")
            
            logger.info("[%s] Carga finalizada com sucesso: %s", self.name, file_path)
        except Exception as e:
            logger.error("Erro durante o carregamento dos dados: %s", e)
            raise


class KagglePipeline(ETL):
    """Implementação específica para fluxos Kaggle."""

    def run(self, dataset: str, file_name: Optional[str] = None, output_ext: str = ".csv") -> None:
        """Executa o ciclo completo de ETL."""
        try:
            raw_data = self.data_extract_kaggle(dataset, file_name)
            transformed_data = self.data_transform(raw_data)
            self.data_load(transformed_data, output_ext)
        except Exception as e:
            logger.critical("[%s] Pipeline abortado: %s", self.name, e)


if __name__ == "__main__":
    # Exemplo de uso
    pipeline = KagglePipeline(name="Vendas_Anual", source="kaggle")
    pipeline.run(dataset="user/dataset-exemplo", output_ext=".parquet")