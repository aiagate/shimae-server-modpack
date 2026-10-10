# サーバー導入手順

Server Pack は Docker Compose と [itzg AUTO_CURSEFORGE](https://docker-minecraft-server.readthedocs.io/en/latest/types-and-platforms/mod-platforms/auto-curseforge/) で MOD と NeoForge を取得するための ZIP です。Docker、Docker Compose、MOD をダウンロードできるネットワークが必要です。初回導入には新しいデータ領域を使用してください。

## 新しいサーバーを導入する

1. 新しい空フォルダに 使用する版の `shimae-server-modpack-<version>-serverpack.zip` をコピーし、展開します。インストーラーが ZIP を読むため、元の ZIP は `compose.yaml` と同じ場所に残します。
2. 同じ場所に空の `downloads` ディレクトリを作ります。
3. [Minecraft EULA](https://www.minecraft.net/eula) を確認し、同意する場合は `.env` に `EULA=true` を記入します。必要に応じて `MEMORY=4G`、`MC_PORT=25565` を指定します。4G は既定値で、必要メモリの実測値ではありません。
4. 展開先で `docker compose up -d` を実行します。データは Compose の名前付き volume `server-data` に保存されます。
5. `docker compose logs -f minecraft` で導入と起動を確認します。自動取得できないファイルが表示されたら、正確な file ID のファイルを CurseForge からブラウザで取得し、`downloads` に置いて `docker compose restart minecraft` を実行します。
6. 起動を確認したら、同じ版のクライアントから接続します。

`docker compose down` で停止・コンテナー削除を行えます。データを保持する場合は volume を削除しないでください。バックアップ対象は `/data` 内の world と運用設定です。

TrueNAS では同等の Custom App を使い、pack と downloads を読み取り専用で mount します。初回確認には新しい `/data` dataset を用意してください。CurseForge App への ZIP インポートだけでは、このサーバーは起動しません。

## 認証とイメージ

同梱 Compose は `itzg/minecraft-server:java21` を使用します。既存の導入手順は、このイメージに含まれる Core API key を利用する前提です。自分のキーを指定する場合は、標準ツールの説明に従い `CF_API_KEY_FILE` と Docker secret 等を使用してください。作者用 Upload token は別の認証情報で、Minecraft サーバーへ渡しません。

イメージの更新で導入動作が変わる可能性があります。本番では起動を確認したイメージの digest を記録・固定してください。

## 既存 world を移行する

この ZIP は world や `server.properties` を移行しません。旧 `CURSEFORGE` は `CF_BASE_DIR`（既定 `/data/FeedTheBeast`）の下で起動する場合があり、`AUTO_CURSEFORGE` の導入先 `/data` と異なります。まず実際の起動場所と `level-name` を確認してください。

旧サーバーを停止し、整合性のあるコピーまたは snapshot を別のデータ領域へ作成して移行を検証します。world と私的な運用設定は保持し、MOD と loader は manifest から導入します。導入時に overrides が適用されるため、既存の設定変更も比較してください。`TYPE` の変更や ZIP の差し替えだけでは world は移りません。
