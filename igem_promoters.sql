CREATE TABLE promoters
    (
        numeric_id      SMALLINT(10)        NOT NULL,
        bba_id          CHAR(20)            NOT NULL,
        name            CHAR(255)           NULL        DEFAULT " ",
        designer        CHAR(255)           NULL        DEFAULT " ",
        design_group    CHAR(255)           NULL        DEFAULT " ",
        times_used      CHAR(5)             NULL        DEFAULT " ",
        rating          CHAR(5)             NULL        DEFAULT " ",
        URL             CHAR(255)           NULL        DEFAULT " ",
        PRIMARY KEY (numeric_id)
    );

CREATE TABLE promoter_features
    (
        numeric_id          SMALLINT(10)    NOT NULL,
        polymerase          CHAR(100)       NULL        DEFAULT " ",
        direction           CHAR(255)       NULL        DEFAULT " ",
        chassis             CHAR(255)       NULL        DEFAULT " ",
        regulation_type     CHAR(255)       NULL        DEFAULT " ",
        sequence            VARCHAR(8000)   NULL        DEFAULT " ",
        PRIMARY KEY (numeric_id)
    );
