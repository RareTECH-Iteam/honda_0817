DROP DATABASE chatapp;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp;
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE users (
    uid varchar(255) PRIMARY KEY,
    username varchar(255) UNIQUE NOT NULL,
    email varchar(255) UNIQUE NOT NULL,
    password varchar(255) NOT NULL,
    address varchar(255) NOT NULL,
    greeting varchar(255) NOT NULL
);

CREATE TABLE chat (
    id serial PRIMARY KEY,
    uid varchar(255) REFERENCES users(uid),
    name varchar(255) UNIQUE NOT NULL,
    abstract varchar(255),
    user_ids text  -- 参加ユーザーのIDをカンマ区切りで保存
);

CREATE TABLE messages (
    id serial PRIMARY KEY,
    uid varchar(255) REFERENCES users(uid),
    cid integer REFERENCES chat(id) ON DELETE CASCADE,
    message text,
    created_at timestamp not null default current_timestamp
);

INSERT INTO users (uid, username, email, password, address, greeting) VALUES
('1', 'alice', 'alice@example.com', 'password1', '北海道', 'こんにちは、アリスです。'),
('2', 'bob', 'bob@example.com', 'password2', '北海道', 'こんにちは、ボブです。'),
('3', 'charlie', 'charlie@example.com', 'password3', '北海道', 'こんにちは、チャーリーです。'),
('4', 'david', 'david@example.com', 'password4', '北海道', 'こんにちは、デイビッドです。'),
('5', 'eve', 'eve@example.com', 'password5', '北海道', 'こんにちは、イヴです。'),
('6', 'frank', 'frank@example.com', 'password6', '東京都', 'こんにちは、フランクです。'),
('7', 'grace', 'grace@example.com', 'password7', '東京都', 'こんにちは、グレースです。'),
('8', 'heidi', 'heidi@example.com', 'password8', '東京都', 'こんにちは、ハイジです。'),
('9', 'ivan', 'ivan@example.com', 'password9', '東京都', 'こんにちは、イヴァンです。'),
('10', 'judy', 'judy@example.com', 'password10', '東京都', 'こんにちは、ジュディです。');

-- チャットルームの挿入
INSERT INTO chat (uid, name, abstract, user_ids) VALUES
('1', 'Alice and Bob Chat Room', 'AliceさんとBobさんのチャットルームです', '1,2');

-- ('1', '北海道住民1とのメッセージ', 'Aliceさんの最初のチャットルームです', '1'),
-- ('1', '北海道住民2とのメッセージ', 'Aliceさんのセカンドチャットルームです', '1'),
-- ('1', '東京都民1とのメッセージ', 'Aliceさんのサードチャットルームです', '1'),
-- ('1', '東京都民2とのメッセージ', 'Aliceさんのフォースチャットルームです', '1'),
-- ('1', '東京都民3とのメッセージ', 'Aliceさんのフィフスチャットルームです', '1');

-- メッセージの挿入
INSERT INTO messages (uid, cid, message) VALUES
('1', 1, 'こんにちは、アリスです。');
-- ('2', 1, 'こんにちは、ボブです。お元気ですか？'),
-- ('1', 1, 'はい、元気です。ボブさんはどうですか？'),
-- ('2', 1, '私も元気です。');

-- -- その他のメッセージ
-- INSERT INTO messages (uid, cid, message) VALUES
-- ('1', 2, 'こんにちは、アリスです。'),
-- ('3', 2, 'こんにちは、チャーリーです。最近どうですか？'),
-- ('1', 2, '元気です、チャーリーさん。'),
-- ('3', 2, 'それは良かったです。'),
-- ('1', 3, 'こんにちは、アリスです。'),
-- ('6', 3, 'こんにちは、フランクです。最近の天気はどうですか？'),
-- ('1', 3, '北海道は寒いですが、晴れています。'),
-- ('6', 3, 'それは良いですね。東京は暖かいです。'),
-- ('1', 4, 'こんにちは、アリスです。'),
-- ('7', 4, 'こんにちは、グレースです。新しいプロジェクトについて話したいです。'),
-- ('1', 4, 'はい、もちろんです。どうぞ。'),
-- ('7', 4, '新しいアプリケーションのデザインについてですが...'),
-- ('1', 5, 'こんにちは、アリスです。'),
-- ('8', 5, 'こんにちは、ハイジです。最近の映画について話しましょう。'),
-- ('1', 5, '良いですね。どの映画ですか？'),
-- ('8', 5, '最近見た映画は「インセプション」です。'),
-- ('1', 5, 'それは素晴らしい映画ですね！');