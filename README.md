# 🧠 EEG Dataset for ADHD — Análise Espectral

Projeto de análise de sinais EEG a partir do dataset [EEG Dataset for ADHD](https://www.kaggle.com/datasets/danizo/eeg-dataset-for-adhd) (Kaggle), com pipeline ETL, pré-processamento (CAR), análise espectral (FFT) e extração de potência por bandas de frequência e regiões cerebrais.

---

## Objetivos

- **ETL:** Carregar e preparar o dataset via pipeline reutilizável (Kaggle → Parquet).
- **Pré-processamento:** Aplicar referência comum média (CAR) nos 19 canais do sistema 10-20.
- **Análise espectral:** FFT e magnitude por canal; potência nas bandas delta, theta, alpha, beta e gamma.
- **Regiões cerebrais:** Mapear frontal, central, parietal, temporal e occipital e identificar bandas predominantes.

---

## Sobre o dataset (Kaggle)

- **Participantes:** 61 crianças com TDAH e 60 controles (7–12 anos); TDAH diagnosticado por psiquiatra (DSM-IV), uso de Ritalina até 6 meses.
- **EEG:** 19 canais (10-20), 128 Hz; referência A1/A2 (lóbulos das orelhas).
- **Tarefa:** Atenção visual — as crianças contavam personagens em imagens (5–16 por figura); cada nova imagem era exibida logo após a resposta, de forma contínua. A duração do registro dependia da velocidade de resposta.

---

## Estrutura do repositório

```
.
├── main.ipynb          # Notebook principal (carga, pré-processamento, FFT, bandas, regiões)
├── models/
│   └── pipeline.py     # Pipeline ETL (extract, transform, load)
├── loaded_data/        # Dados carregados (ex.: EEG - kaggle.parquet)
├── logs/               # Logs do pipeline
├── requirements.txt
└── README.md
```

---

## Como executar

1. **Ambiente:** crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   pip install -r requirements.txt
   ```

2. **Kaggle:** configure credenciais do Kaggle (ex.: `~/.kaggle/kaggle.json`) para o download do dataset.

3. **Notebook:** abra e execute o `main.ipynb` (Jupyter ou VS Code). O pipeline fará o download, transformação e carga; em seguida a análise espectral e os gráficos serão gerados.

---

## Conteúdo do notebook

| Seção | Descrição |
|-------|-----------|
| 1 | Configuração e dependências |
| 2 | Carga dos dados (ETL) |
| 3 | Pré-processamento (canais + CAR) |
| 4 | Análise espectral (FFT) e espectro |
| 5 | Bandas de frequência e potência (gráfico de barras) |
| 6 | Regiões cerebrais e predominância (heatmap) |
| 7 | Resumo e conclusões (TDAH × regiões cerebrais × ondas predominantes) |

---

## Tecnologias

- **Python** (pandas, numpy, matplotlib, seaborn)
- **Polars** e **kagglehub** no pipeline ETL
- **Parquet** para armazenamento dos dados carregados

---

## Licença e referências

- Dataset: [EEG Dataset for ADHD](https://www.kaggle.com/datasets/danizo/eeg-dataset-for-adhd) (Kaggle).
- Este repositório é de caráter educacional/portfólio.
