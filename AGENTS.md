# 💩検出機器

## 概要

LightningTalk（LT会）用の💩検出機器を作成する。
Phase1ではRaspberry Piを用いた💩検出、Phase2でAWS+AI環境で💩から健康状態の推定等を行う

## 技術スタック

- **Phase1**:
  - Python: Raspberry Pi GPIO操作、メインプログラム
- **Phase2**:
  - AWS (CloudFormation)
  - Python(Lambda)

## ディレクトリ構成

| パス | 概要 |
| -- | -- |
| docs/phase1/ | phase1の設計書 |
| docs/phase2/ | phase2の設計書 |
| src/rpi/ | Raspberry Piに格納するプログラム |
| src/infra/ | AWSのインフラ。CFnで定義 |
| src/lambda/ | Lambda関数 |

## 応答原則

- 日本語で応答

