case "$1" in
"fix")
    uv run ruff check --select I --fix
    uv run ruff format
    ;;
"check")
    uv run ruff check --select I
    uv run ruff format --check
    ;;
*)
    echo "Usage"
    echo "To fix the format, use ./format.sh fix"
    echo "To check the format, use ./format.sh check"
    ;;
esac
