from core.config import get_config


def main():
    config = get_config()
    print(f"DeepSearch Agent starting ({config.environment}) with model '{config.model_name}'")


if __name__ == "__main__":
    main()
