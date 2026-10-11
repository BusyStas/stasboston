# Read automatically by gunicorn from the working directory.
# A job pitch waits on a Claude call and possibly a resuming database,
# which can run past gunicorn's default 30-second worker timeout.
timeout = 300
