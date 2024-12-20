# 飲食店向けシフト管理ウェブアプリ

英語版のREADMEも利用可能です。  
[English version README](./README.md) is also available

## 目的

このプロジェクトは就職活動等に向けた、ポートフォリオ作成のためのプロジェクトです。自身の持っているスキル（MVC, Database, HTML/CSS/JS, Python, AWS）の一部を広く浅く示すために作成を開始しました。そのため実際のシフト管理を行うためのアプリとしては不十分な部分があります。   
このアプリはカナダの飲食店に向けて作られており、銀行口座の入力や住所の入力はカナダのフォーマットに基づいています。

## 概要

このアプリはユーザー管理、アクセス管理、ワークロケーション管理、シフト管理の機能を有しています。  
マネージャー/オーナーはユーザーや役職ごとにページのアクセス権限を設定することができ、ワークロケーション（複数の店舗を保持している場合や、同じで店舗内でもポジションを分けたい場合に役に立ちます）の管理と、シフトの作成をすることが可能です。  
ユーザーは自身に割り当てられたシフトの確認とシフトの希望を提出することが可能です。  
詳しい機能は[要件定義書(英語のみ)](./documents/RDD/Requirements%20definition%20document.md)をご確認ください。

## 環境

### 開発環境/ライブラリ

このアプリケーションはAWS上で、動作させることが可能です  
セットアップの方法は別ドキュメント[AWS Setup (English only)](./documents/AWS%20Setup/README.md)で確認できます

#### 開発環境

| | 名前 | バージョン |
| - | - | - |
| OS | Windows 11 Pro | 23H2 |
| エディタ | Visual Studio Code | 1.94.0 (user setup) |
| 言語 | Python3 | 3.12.3 |

#### ライブラリ

pip ライブラリ
| ライブラリ名 | バージョン |
| - | - |
| asgiref              | 3.8.1 |
| beautifulsoup4       | 4.12.3 |
| Django               | 5.1.1 |
| django-bootstrap5    | 24.2 |
| django-filter        | 24.3 |
| django-widget-tweaks | 1.5.0 |
| packaging            | 24.1 |
| pillow               | 10.4.0 |
| pip                  | 24.2 |
| python-environ       | 0.4.54 |
| soupsieve            | 2.6 |
| sqlparse             | 0.5.1 |
| tzdata               | 2024.1 |
| gunicorn             | 23.0.0 |
| psycopg2             | 2.9.9 |

その他ライブラリ
| ライブラリ名 | バージョン |
| - | - |
| jquery | 3.7.1.min |
| jquery-datetimepicker | 2.5.20 |
| Google fonts |  |

### ウェブブラウザ

Google Chrome Version 129.0.6668.90 (Official Build) (64-bit)

## 変更履歴

| 更新日時 | 更新者 | 更新内容 |
| - | - | - |
| 2024-10-04 | 内海 陽慈 | 初版作成 |
| 2024-10-15 | 内海 陽慈 | Pip ライブラリを追加 |
