
#!/bin/bash

# 私のホームディレクトリを/tmpにバックアップする

# バックアップするディレクトリ
src_dir=$HOME

# バックアップ先のディレクトリ
dst_dir=/tmp/backup_$(date +%Y%m%d%H%M%S)

# バックアップを実行する
rsync -av --delete $src_dir $dst_dir

# バックアップが完了したことを知らせる
echo "バックアップが完了しました。"
