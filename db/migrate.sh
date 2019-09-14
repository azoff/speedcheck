#!/usr/bin/env sh

set -eo pipefail

db_path=${1:-$SQLITE3_DB_PATH}
alias sqlite="/usr/bin/sqlite3 $db_path"

check_migration() {
	if [ "$(sqlite '.table migration')" != '' ]; then
		sqlite "select applied from migration where name = '$1'"
	fi
}

apply_migration() {
	echo "applying $1..."
	cat $MIGRATIONS_PATH/$1 | sqlite
	sqlite "insert into migration (name) values ('$1')"
}

for migration in $(ls $MIGRATIONS_PATH | grep .sql); do
	[ "$(check_migration $migration)" == '' ] && apply_migration $migration
done

sqlite "select * from migration"