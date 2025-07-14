# Процесс

- ставите star
- делаете форк
- после выполнения задания - отправляете ссылку на свой форк в отклике вместе с бордами

# Тестовое задание: ресёрч сигнала на Bybit (Testnet)

Цель — исследовать возможность построения стратегии на основе всплесков дельты ордербука.

## Что нужно сделать

1. Собрать данные по ордербуку (Level 2) с Bybit Testnet.
2. Вычислить метрику дельты.
3. Построить простую стратегию на основе этой метрики.
4. Провести симуляцию / бэктест стратегии.
5. Подготовить отчёт

## Язык

- `python/` — реализация на Python
- `rust/` — реализация на Rust

Выбери одну директорию и реализуй всё в ней.

## Что сдавать

- Исходный код (датаингест, сигнал, стратегия, симуляция)

## Usage: Python Implementation
1. Frome console: `uv run main.py` OR `python main.py`
2. The `Report / Signal / Trades` will be saves in to `python/report/` folder

Report example:

- Start                    : 2025-07-13 14:41:08.493000
- End                      : 2025-07-13 14:46:06.992000
- Duration                 : 0 days 00:04:58.499000
- Exposure Time [%]        : 82.64463
- Equity Final [$]         : 102087.3431
- Equity Peak [$]          : 102215.6548
- Commissions [$]          : 665.2069
- Return [%]               : 2.08734
- Buy & Hold Return [%]    : -4.03269
- Return (Ann.) [%]        : 0.0
- Volatility (Ann.) [%]    : nan
- CAGR [%]                 : inf
- Sharpe Ratio             : nan
- Sortino Ratio            : nan
- Calmar Ratio             : 0.0
- Alpha [%]                : -0.45077
- Beta                     : -0.62939
- Max. Drawdown [%]        : -0.30351
- Avg. Drawdown [%]        : -0.07513
- Max. Drawdown Duration   : 0 days 00:01:12
- Avg. Drawdown Duration   : 0 days 00:00:13.611000
- `# Trades`                 : 2
- Win Rate [%]             : 100.0
- Best Trade [%]           : 1.97135
- Worst Trade [%]          : 1.30277
- Avg. Trade [%]           : 1.63651
- Max. Trade Duration      : 0 days 00:02:21.499000
- Avg. Trade Duration      : 0 days 00:02:02.999000
- Profit Factor            : nan
- Expectancy [%]           : 1.63706
- SQN                      : 4.60639
- Kelly Criterion          : nan
 