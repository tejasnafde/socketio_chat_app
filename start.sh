   #!/bin/bash
   TABLE_EXISTS=$(psql $DATABASE_URL -t -c "SELECT to_regclass('gra_action_hub');")

    if [ "$TABLE_EXISTS" = "" ]; then
        echo "Table 'gra_action_hub' does not exist. Running migrations..."
        flask db upgrade  # Run migrations to create the necessary tables
    else
        echo "Table 'gra_action_hub' already exists. Skipping migrations."
    fi
    
   gunicorn app:app --bind 0.0.0.0:$PORT