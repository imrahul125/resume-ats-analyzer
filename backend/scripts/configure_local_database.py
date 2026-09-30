"""Write a local DATABASE_URL without echoing or committing the password."""

from getpass import getpass
from pathlib import Path

from sqlalchemy.engine import URL, make_url

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"


def default_port() -> int:
    """Reuse this project's configured port, or use PostgreSQL's standard port."""
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            key, separator, value = line.partition("=")
            if separator and key.strip() == "DATABASE_URL" and value.strip():
                try:
                    return make_url(value.strip()).port or 5432
                except Exception:
                    break
    return 5432


def update_env_file(key: str, value: str) -> None:
    """Set one key in the ignored .env file while preserving other settings."""
    lines = ENV_FILE.read_text(encoding="utf-8").splitlines() if ENV_FILE.exists() else []
    replacement = f"{key}={value}"
    for index, line in enumerate(lines):
        if line.partition("=")[0].strip() == key:
            lines[index] = replacement
            break
    else:
        lines.append(replacement)

    ENV_FILE.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    port_default = default_port()
    port_text = input(f"PostgreSQL port [{port_default}]: ").strip() or str(port_default)
    if not port_text.isdecimal():
        raise SystemExit("Port must be a number.")

    password = getpass("Password for PostgreSQL role resume_app: ")
    if not password:
        raise SystemExit("The database password cannot be empty.")

    confirmation = getpass("Confirm database password: ")
    if password != confirmation:
        raise SystemExit("The passwords did not match. No file was changed.")

    database_url = URL.create(
        drivername="postgresql+psycopg",
        username="resume_app",
        password=password,
        host="127.0.0.1",
        port=int(port_text),
        database="resume_ats",
    ).render_as_string(hide_password=False)

    update_env_file("DATABASE_URL", database_url)
    update_env_file("ENVIRONMENT", "development")
    print("Local database settings saved to the ignored root .env file.")


if __name__ == "__main__":
    main()
