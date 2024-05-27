Добавить новый рулон: Добавление нового рулона на склад с обязательными параметрами длины и веса.
Удалить рулон: Удаление рулона со склада по его ID.
Получить рулоны: Получение списка рулонов с возможностью фильтрации по длине, весу, дате добавления и дате удаления.
Получить статистику: Получение различных статистических данных о рулонах за указанный период.
Обновить дату удаления: Обновление даты удаления для конкретного рулона по его ID.

## API Endpoints

### Add a new roll

- **Endpoint:** `POST /rolls/`
- **Request body:**
    ```json
    {
      "length": 120.5,
      "weight": 350.0
    }
    ```
- **Response:**
    ```json
    {
      "id": 1,
      "length": 120.5,
      "weight": 350.0,
      "date_added": "2024-05-22T12:00:00",
      "date_removed": null
    }
    ```

### Remove a roll

- **Endpoint:** `DELETE /rolls/{roll_id}`
- **Response:**
    ```json
    {
      "id": 1,
      "length": 120.5,
      "weight": 350.0,
      "date_added": "2024-05-22T12:00:00",
      "date_removed": null
    }
    ```

### Get rolls

- **Endpoint:** `GET /rolls/`
- **Query parameters (optional):**
    - `length`: Filter by length
    - `weight`: Filter by weight
    - `date_added`: Filter by date added
    - `date_removed`: Filter by date removed
- **Response:**
    ```json
    [
      {
        "id": 1,
        "length": 120.5,
        "weight": 350.0,
        "date_added": "2024-05-22T12:00:00",
        "date_removed": null
      }
    ]
    ```

### Get statistics

- **Endpoint:** `GET /stats/`
- **Query parameters:**
    - `start_date`: Start date for the statistics period
    - `end_date`: End date for the statistics period
- **Response:**
    ```json
    {
      "added_rolls": 10,
      "removed_rolls": 5,
      "average_length": 100.5,
      "average_weight": 300.5,
      "max_length": 150.0,
      "min_length": 50.0,
      "max_weight": 400.0,
      "min_weight": 200.0,
      "total_weight": 3005.0,
      "max_storage_duration": 30,
      "min_storage_duration": 5
    }
    ```

### Update date removed

- **Endpoint:** `PUT /rolls/{roll_id}/remove_date`
- **Request body:**
    ```json
    {
      "date_removed": "2024-05-22T12:00:00"
    }
    ```
- **Response:**
    ```json
    {
      "id": 1,
      "length": 120.5,
      "weight": 350.0,
      "date_added": "2024-05-22T12:00:00",
      "date_removed": "2024-05-22T12:00:00"
    }
