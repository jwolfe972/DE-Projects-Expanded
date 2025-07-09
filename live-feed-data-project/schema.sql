CREATE TABLE live_data_tbl(
    message_id uuid DEFAULT gen_random_uuid(),
    person VARCHAR(50) NOT NULL,
    text VARCHAR(300) NOT NULL


);