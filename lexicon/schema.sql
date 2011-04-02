CREATE TABLE db_version (
    version integer
    );
CREATE TABLE lexicon_date (
    date date
    );
CREATE TABLE lexicon_file (
    file varchar(256)
    );
CREATE TABLE "words" (
    word varchar(16),
    length integer,
    playability integer,
    playability_order integer,
    min_playability_order integer,
    max_playability_order integer,
    combinations0 integer,
    probability_order0 integer,
    min_probability_order0 integer,
    max_probability_order0 integer,
    combinations1 integer,
    probability_order1 integer,
    min_probability_order1 integer,
    max_probability_order1 integer,
    combinations2 integer,
    probability_order2 integer,
    min_probability_order2 integer,
    max_probability_order2 integer,
    alphagram varchar(16),
    num_anagrams integer,
    num_unique_letters integer,
    num_vowels integer,
    point_value integer,
    front_hooks varchar(32),
    back_hooks varchar(32),
    is_front_hook integer,
    is_back_hook integer,
    lexicon_symbols varchar(16),
    definition varchar(256),
    consogram varchar(17)
    );
CREATE UNIQUE INDEX play_index on words (length, playability_order);
CREATE INDEX play_min_max_index on words (length, min_playability_order, max_playability_order);
CREATE UNIQUE INDEX prob0_index on words (length, probability_order0);
CREATE UNIQUE INDEX prob1_index on words (length, probability_order1);
CREATE UNIQUE INDEX prob2_index on words (length, probability_order2);
CREATE INDEX prob0_min_max_index on words (length, min_probability_order0, max_probability_order0);
CREATE INDEX prob1_min_max_index on words (length, min_probability_order1, max_probability_order1);
CREATE INDEX prob2_min_max_index on words (length, min_probability_order2, max_probability_order2);
CREATE INDEX word_alphagram_index ON words (alphagram);
CREATE INDEX word_back_hook_index ON words (is_back_hook);
CREATE INDEX word_front_hook_index ON words (is_front_hook);
CREATE INDEX word_length_index ON words (length);
CREATE INDEX word_consogram_index ON words (consogram);
CREATE UNIQUE INDEX word_index ON words (word);
