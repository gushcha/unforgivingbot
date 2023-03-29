CREATE ROLE submitter LOGIN PASSWORD :password_db_submitter;
CREATE ROLE notifier LOGIN PASSWORD :password_db_notifier;

CREATE TABLE disputes (
    id VARCHAR(7) NOT NULL,
    text TEXT NOT NULL,
    created_on TIMESTAMP default current_timestamp,
    ends_on TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
);

GRANT SELECT, INSERT ON disputes TO submitter;
GRANT SELECT, DELETE ON disputes TO notifier;

CREATE TABLE trackers (
    chat_id BIGSERIAL NOT NULL,
    dispute_id VARCHAR(7) NOT NULL,
    username VARCHAR(64),
    PRIMARY KEY (chat_id, dispute_id),
    FOREIGN KEY (dispute_id) REFERENCES disputes (id) ON DELETE CASCADE
);

GRANT SELECT, INSERT ON trackers TO submitter;
GRANT SELECT, DELETE ON trackers TO notifier;