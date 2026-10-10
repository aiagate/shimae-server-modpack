# ドキュメント精査記録

対象は、このリポジトリの案内・変更履歴・ライセンス通知・履歴資料、および Server Pack に生成される `README-SERVER.md` です。ファイル名と内容の役割、公開読者に必要な情報、実装との一致を確認しました。外部サイトの現在の状態と Minecraft の実機動作は今回の検証対象に含めていません。

## 案内文書を用途別に整理

| ファイル | 精査結果と対応 |
| --- | --- |
| `README.md` | 利用案内、提出手順、認証設定、過去の作業記録が混在。配布概要・導入の入口・文書案内へ書き換え。 |
| `CHANGELOG.md` | 冒頭が特定版の表題で、日本語と英語が混在。文書表題を Changelog、各版を同じ階層に統一し、変更内容を日本語で記載。 |
| `docs/server-setup.md` | README と生成文書の導入情報から新規作成。ZIP の保持、EULA、downloads、データ保存先、world 移行を説明。 |
| `docs/development.md` | README から編集対象・生成方式・検証を移動。固定版と ZIP ハッシュの再現性の限界を保持。 |
| `docs/publishing.md` | README から提出・認証・公開確認を移動。実装にある提出有効化変数の説明を追加し、過去の認証成功と現在の確認を区別。 |
| `CHANGELOG.md` の `0.0.2 submission evidence` | 提出 ID、SHA、回復経緯を記録しており、ファイル名と一致。根拠資料として保持。 |
| `CHANGELOG.md` の `0.0.1 App migration evidence` | 保存資料と歴史的パス、現行入力との区別を説明しており、役割と一致。保持。 |

## ライセンスと配布物内の文書

`LICENSE` と `pack/overrides/LICENSE-Shimae.txt` は同一の MIT 条文です。旧 `LICENSE-SCOPE.txt` の適用範囲説明は、現在の配布物内の通知に保持されています。法的な条文は編集していません。

`pack/overrides/THIRD-PARTY-NOTICES.txt` は旧 `LICENSE-SCOPE.txt` と同じ本文で、個別の第三者名・ライセンスを列挙する通知一覧ではありません。modlist と原プロジェクトのライセンスを参照する一般通知として機能しますが、見出しは「License scope」です。次版でこの見出しを第三者通知に合わせることが改善点です。各 MOD のライセンスを未確認のまま一覧へ補完してはいません。

`pack/overrides/config/better*/` の README 8 件は、各 MOD の設定ディレクトリや JSON の説明で、配置と役割は一致しています。その他の設定用 `.txt` は文書ではなく設定・状態ファイルとして扱いました。

生成される `README-SERVER.md` は導入手順、world 移行、認証を説明しています。一部に作者向けの提出・審査説明もありますが、導入方式の制約は明記されています。現在の本文は `scripts/serverpack.py` にあります。

配布物内の通知・設定 README は `pack/migration.json` の SHA 検証対象です。生成文書の変更も Server Pack のバイト列を変えます。公開済み 0.0.2 と同版の別バイトを作らないため、今回はこれらを保持し、改善は次版の配布内容として扱います。

## 最新 main の履歴統合を反映

PR #10 で `history/` とルートの `LICENSE-SCOPE.txt` が削除され、履歴資料は CHANGELOG に統合されました。今回の PR はその変更を保持し、参照を CHANGELOG の該当節と配布物の通知へ更新しています。公開履歴の英文・原 JSON の引用は根拠資料として保持しています。
