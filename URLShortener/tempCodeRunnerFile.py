def setup_logging(
    log_file="url_shortener.log", max_log_size=1024 * 1024, backup_count=2
):
    # Certifique-se de que o diretório do log existe
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Configurar o formato do log
    log_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Configurar o handler de arquivo rotacional
    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_log_size, backupCount=backup_count
    )
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)

    # Configurar o handler de console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)

    # Configurar o logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logging.info("Logging configurado com sucesso.")